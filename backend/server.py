"""
FaizZab ISO & DPDPA Toolkit Generator — FastAPI backend.

Multi-tenant compliance toolkit platform: catalogue → purchase → onboarding →
admin verification → deterministic document generation → downloads.
"""
import os
import io
import base64
import logging
import uuid
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import jwt
from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, UploadFile, File
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from pydantic import BaseModel, Field

import content_packs as cp
import onboarding_schema as ob
from toolkit_engine import (
    render_docx_document, render_pdf_document, render_xlsx_register,
    build_zip, validate_document, resolve_variables, flatten_context,
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("faizzab")

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret")
JWT_ALG = "HS256"
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

BASE_PRICE = 4999
GST_RATE = 0.18

app = FastAPI(title="FaizZab Toolkit Generator")
api = APIRouter(prefix="/api")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return str(uuid.uuid4())


def clean(doc: Optional[dict]) -> Optional[dict]:
    if doc is None:
        return None
    doc = dict(doc)
    doc.pop("_id", None)
    return doc


def make_token(user: dict) -> str:
    payload = {
        "sub": user["id"],
        "role": user["role"],
        "org_id": user.get("org_id"),
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


async def audit(action: str, actor: Optional[dict] = None, org_id: Optional[str] = None, meta: Optional[dict] = None):
    await db.audit_logs.insert_one({
        "id": new_id(), "action": action,
        "actor_id": (actor or {}).get("id"), "actor_role": (actor or {}).get("role"),
        "org_id": org_id or (actor or {}).get("org_id"),
        "meta": meta or {}, "at": now_iso(),
    })


async def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Not authenticated")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Session expired")
    except Exception:
        raise HTTPException(401, "Invalid token")
    user = await db.users.find_one({"id": payload["sub"]})
    if not user:
        raise HTTPException(401, "User not found")
    return clean(user)


async def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "admin":
        raise HTTPException(403, "Admin access required")
    return user


async def require_client(user: dict = Depends(get_current_user)) -> dict:
    if user["role"] != "client":
        raise HTTPException(403, "Client access required")
    return user


# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #
class AdminLogin(BaseModel):
    email: str
    password: str
    mfa_code: Optional[str] = None


class OtpRequest(BaseModel):
    mobile: str
    name: Optional[str] = None


class OtpVerify(BaseModel):
    mobile: str
    code: str
    name: Optional[str] = None


class OrgIn(BaseModel):
    legal_name: str
    trade_name: str
    website: Optional[str] = ""
    industry: Optional[str] = ""
    employee_count: Optional[str] = ""
    registered_address: Optional[str] = ""
    locations: Optional[str] = ""
    primary_contact: Optional[str] = ""
    contact_email: Optional[str] = ""
    contact_mobile: Optional[str] = ""
    gstin: Optional[str] = ""
    registration_number: Optional[str] = ""
    products_services: Optional[str] = ""
    logo_base64: Optional[str] = ""


class OrderIn(BaseModel):
    standard_slug: str
    coupon: Optional[str] = None


class DraftIn(BaseModel):
    standard_slug: str
    answers: Dict[str, Any]


class SubmitIn(BaseModel):
    standard_slug: str
    answers: Dict[str, Any]
    declaration: bool


class ReviewAction(BaseModel):
    comment: Optional[str] = ""
    section_id: Optional[str] = None


class AdditionalReqIn(BaseModel):
    title: str
    description: str
    category: str


class QuotationIn(BaseModel):
    amount: float
    description: str


class CouponIn(BaseModel):
    code: str
    percent_off: int
    active: bool = True


# --------------------------------------------------------------------------- #
# Startup seed
# --------------------------------------------------------------------------- #
@app.on_event("startup")
async def seed():
    # seed admin (idempotent)
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@faizzab.com")
    existing = await db.users.find_one({"email": admin_email, "role": "admin"})
    if not existing:
        await db.users.insert_one({
            "id": new_id(), "role": "admin", "email": admin_email,
            "name": "FaizZab Admin",
            "password_hash": pwd_ctx.hash(os.environ.get("ADMIN_PASSWORD", "Admin@12345")),
            "mfa_enabled": True, "created_at": now_iso(),
        })
        logger.info("Seeded admin user")
    # seed default coupon
    if not await db.coupons.find_one({"code": "LAUNCH20"}):
        await db.coupons.insert_one({
            "id": new_id(), "code": "LAUNCH20", "percent_off": 20, "active": True, "created_at": now_iso(),
        })
    # seed pricing config
    if not await db.config.find_one({"key": "pricing"}):
        await db.config.insert_one({
            "key": "pricing", "base_price": BASE_PRICE, "gst_rate": GST_RATE,
            "additional_default": 2999,
        })


# --------------------------------------------------------------------------- #
# Auth routes
# --------------------------------------------------------------------------- #
@api.post("/auth/admin/login")
async def admin_login(body: AdminLogin):
    user = await db.users.find_one({"email": body.email, "role": "admin"})
    if not user or not pwd_ctx.verify(body.password, user["password_hash"]):
        raise HTTPException(401, "Invalid credentials")
    # MFA: for v1 a simple deterministic code 123456 is accepted (SIMULATED / testable).
    if user.get("mfa_enabled"):
        if body.mfa_code is None:
            return {"mfa_required": True}
        if body.mfa_code != "123456":
            await audit("admin_login_mfa_failed", clean(user))
            raise HTTPException(401, "Invalid MFA code")
    await audit("admin_login", clean(user))
    return {"token": make_token(clean(user)), "user": {
        "id": user["id"], "role": "admin", "name": user["name"], "email": user["email"]}}


@api.post("/auth/otp/request")
async def otp_request(body: OtpRequest):
    code = "654321"  # SIMULATED OTP (fixed for testability). Real SMS provider pluggable.
    await db.otps.update_one(
        {"mobile": body.mobile},
        {"$set": {"mobile": body.mobile, "code": code,
                  "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
                  "attempts": 0, "created_at": now_iso()}},
        upsert=True,
    )
    # OTP surfaced in response ONLY because SMS is simulated in v1 (MOCKED).
    return {"sent": True, "dev_otp": code, "message": "OTP sent (simulated). Use the code shown."}


@api.post("/auth/otp/verify")
async def otp_verify(body: OtpVerify):
    rec = await db.otps.find_one({"mobile": body.mobile})
    if not rec:
        raise HTTPException(400, "Request an OTP first")
    if datetime.fromisoformat(rec["expires_at"]) < datetime.now(timezone.utc):
        raise HTTPException(400, "OTP expired")
    if rec.get("attempts", 0) >= 5:
        raise HTTPException(429, "Too many attempts")
    if body.code != rec["code"]:
        await db.otps.update_one({"mobile": body.mobile}, {"$inc": {"attempts": 1}})
        raise HTTPException(401, "Invalid OTP")
    user = await db.users.find_one({"mobile": body.mobile, "role": "client"})
    if not user:
        user = {
            "id": new_id(), "role": "client", "mobile": body.mobile,
            "name": body.name or "Client Admin", "org_id": None, "created_at": now_iso(),
        }
        await db.users.insert_one(user)
    await db.otps.delete_one({"mobile": body.mobile})
    await audit("client_login", clean(user))
    return {"token": make_token(clean(user)), "user": {
        "id": user["id"], "role": "client", "name": user["name"],
        "mobile": user["mobile"], "org_id": user.get("org_id")}}


import httpx

EMERGENT_SESSION_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"


class GoogleSession(BaseModel):
    session_id: str


@api.post("/auth/google/session")
async def google_session(body: GoogleSession):
    """Exchange an Emergent Google Auth session_id for our app JWT.
    Google-authenticated users are mapped to role=client by email."""
    try:
        async with httpx.AsyncClient(timeout=15) as hc:
            resp = await hc.get(EMERGENT_SESSION_URL, headers={"X-Session-ID": body.session_id})
        if resp.status_code != 200:
            raise HTTPException(401, "Invalid or expired Google session")
        data = resp.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(502, "Could not verify Google session")

    email = (data.get("email") or "").lower()
    name = data.get("name") or "Client Admin"
    picture = data.get("picture") or ""
    if not email:
        raise HTTPException(400, "Google account has no email")

    user = await db.users.find_one({"email": email, "role": "client"})
    if not user:
        user = {
            "id": new_id(), "role": "client", "email": email, "name": name,
            "picture": picture, "auth_provider": "google", "mobile": None,
            "org_id": None, "created_at": now_iso(),
        }
        await db.users.insert_one(user)
    else:
        await db.users.update_one({"id": user["id"]}, {"$set": {"name": name, "picture": picture}})
    await audit("client_login_google", clean(user))
    return {"token": make_token(clean(user)), "user": {
        "id": user["id"], "role": "client", "name": name, "email": email,
        "org_id": user.get("org_id"), "picture": picture}}


@api.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    org = None
    if user.get("org_id"):
        org = clean(await db.organizations.find_one({"id": user["org_id"]}))
    return {"user": {k: user.get(k) for k in ("id", "role", "name", "email", "mobile", "org_id", "picture")}, "org": org}


# --------------------------------------------------------------------------- #
# Public catalogue
# --------------------------------------------------------------------------- #
@api.get("/catalogue")
async def catalogue():
    pricing = await db.config.find_one({"key": "pricing"}) or {}
    out = []
    for s in cp.STANDARDS:
        manifest = cp.manifest_summary(s)
        out.append({
            "slug": s["slug"], "code": s["code"], "version": s["version"], "name": s["name"],
            "short": s["short"], "purpose": s["purpose"], "intended_for": s["intended_for"],
            "industries": s["industries"], "accent": s["accent"],
            "document_count": len(manifest),
            "legal_disclaimer": s["legal_disclaimer"],
            "price": pricing.get("base_price", BASE_PRICE),
        })
    return {"toolkits": out, "price": pricing.get("base_price", BASE_PRICE), "gst_rate": pricing.get("gst_rate", GST_RATE)}


@api.get("/catalogue/{slug}")
async def catalogue_detail(slug: str):
    s = cp.get_standard(slug)
    if not s:
        raise HTTPException(404, "Toolkit not found")
    pricing = await db.config.find_one({"key": "pricing"}) or {}
    manifest = cp.manifest_summary(s)
    categories: Dict[str, int] = {}
    for d in manifest:
        categories[d["category"]] = categories.get(d["category"], 0) + 1
    return {
        "slug": s["slug"], "code": s["code"], "version": s["version"], "name": s["name"],
        "short": s["short"], "purpose": s["purpose"], "intended_for": s["intended_for"],
        "industries": s["industries"], "accent": s["accent"],
        "legal_disclaimer": s["legal_disclaimer"],
        "manifest": manifest, "document_count": len(manifest),
        "categories": categories,
        "formats": ["DOCX", "XLSX", "PDF", "ZIP"],
        "price": pricing.get("base_price", BASE_PRICE),
        "gst_rate": pricing.get("gst_rate", GST_RATE),
        "onboarding_sections": [{"id": sec["id"], "title": sec["title"]} for sec in ob.build_schema(slug)["sections"]],
    }


# --------------------------------------------------------------------------- #
# Organization
# --------------------------------------------------------------------------- #
@api.post("/org")
async def create_org(body: OrgIn, user: dict = Depends(require_client)):
    if user.get("org_id"):
        raise HTTPException(400, "Organization already exists for this account")
    org = body.dict()
    org["id"] = new_id()
    org["created_at"] = now_iso()
    await db.organizations.insert_one(dict(org))
    await db.users.update_one({"id": user["id"]}, {"$set": {"org_id": org["id"]}})
    await audit("org_created", user, org["id"])
    return clean(await db.organizations.find_one({"id": org["id"]}))


@api.get("/org")
async def get_org(user: dict = Depends(require_client)):
    if not user.get("org_id"):
        return None
    return clean(await db.organizations.find_one({"id": user["org_id"]}))


@api.put("/org")
async def update_org(body: OrgIn, user: dict = Depends(require_client)):
    if not user.get("org_id"):
        raise HTTPException(400, "Create an organization first")
    await db.organizations.update_one({"id": user["org_id"]}, {"$set": body.dict()})
    await audit("org_updated", user)
    return clean(await db.organizations.find_one({"id": user["org_id"]}))


# --------------------------------------------------------------------------- #
# Commerce
# --------------------------------------------------------------------------- #
async def _price_for(coupon_code: Optional[str]):
    pricing = await db.config.find_one({"key": "pricing"}) or {}
    base = pricing.get("base_price", BASE_PRICE)
    gst_rate = pricing.get("gst_rate", GST_RATE)
    discount = 0
    coupon = None
    if coupon_code:
        coupon = await db.coupons.find_one({"code": coupon_code.upper(), "active": True})
        if coupon:
            discount = round(base * coupon["percent_off"] / 100)
    subtotal = base - discount
    gst = round(subtotal * gst_rate)
    total = subtotal + gst
    return {"base": base, "discount": discount, "subtotal": subtotal, "gst": gst,
            "total": total, "gst_rate": gst_rate, "coupon_applied": bool(coupon),
            "coupon_code": coupon_code.upper() if (coupon and coupon_code) else None}


@api.post("/coupons/validate")
async def validate_coupon(body: dict):
    code = (body.get("code") or "").upper()
    coupon = await db.coupons.find_one({"code": code, "active": True})
    if not coupon:
        raise HTTPException(404, "Invalid or inactive coupon")
    return {"code": code, "percent_off": coupon["percent_off"]}


@api.post("/orders")
async def create_order(body: OrderIn, user: dict = Depends(require_client)):
    if not user.get("org_id"):
        raise HTTPException(400, "Create your organization profile first")
    s = cp.get_standard(body.standard_slug)
    if not s:
        raise HTTPException(404, "Toolkit not found")
    price = await _price_for(body.coupon)
    order = {
        "id": new_id(), "org_id": user["org_id"], "user_id": user["id"],
        "standard_slug": body.standard_slug, "standard_name": s["name"],
        "amount": price["total"], "price_breakdown": price,
        "status": "created",  # created -> paid / failed / refunded
        "created_at": now_iso(),
        # A real Razorpay order id would be created here; simulated in v1.
        "gateway": "simulated", "gateway_order_id": "sim_" + new_id()[:12],
    }
    await db.orders.insert_one(dict(order))
    await audit("order_created", user, meta={"order_id": order["id"]})
    return clean(order)


@api.post("/orders/{order_id}/verify-payment")
async def verify_payment(order_id: str, body: dict, user: dict = Depends(require_client)):
    """Server-side payment verification. In v1 this simulates a verified
    Razorpay signature check; entitlement is granted ONLY here (server-side)."""
    order = await db.orders.find_one({"id": order_id, "org_id": user["org_id"]})
    if not order:
        raise HTTPException(404, "Order not found")
    if order["status"] == "paid":
        return {"status": "paid", "already": True}
    # SIMULATED verification. Real impl: verify razorpay_payment_id + signature.
    payment_id = body.get("razorpay_payment_id", "sim_pay_" + new_id()[:12])
    verified = True
    if not verified:
        await db.orders.update_one({"id": order_id}, {"$set": {"status": "failed"}})
        raise HTTPException(400, "Payment verification failed")
    await db.orders.update_one({"id": order_id}, {"$set": {
        "status": "paid", "paid_at": now_iso(), "payment_id": payment_id}})
    # Entitlement — immutable snapshot of the purchased toolkit version
    entitlement = {
        "id": new_id(), "org_id": user["org_id"], "order_id": order_id,
        "standard_slug": order["standard_slug"], "standard_name": order["standard_name"],
        "toolkit_version": cp.get_standard(order["standard_slug"])["version"],
        "active": True, "created_at": now_iso(),
        "access_until": (datetime.now(timezone.utc) + timedelta(days=365)).isoformat(),
    }
    await db.entitlements.insert_one(dict(entitlement))
    # Invoice
    invoice = {
        "id": new_id(), "number": "INV-" + datetime.now().strftime("%Y%m%d") + "-" + new_id()[:6].upper(),
        "org_id": user["org_id"], "order_id": order_id, "amount": order["amount"],
        "breakdown": order["price_breakdown"], "created_at": now_iso(),
    }
    await db.invoices.insert_one(dict(invoice))
    await audit("payment_verified", user, meta={"order_id": order_id, "payment_id": payment_id})
    return {"status": "paid", "entitlement": clean(entitlement), "invoice": clean(invoice)}


@api.get("/orders")
async def list_orders(user: dict = Depends(require_client)):
    if not user.get("org_id"):
        return []
    docs = await db.orders.find({"org_id": user["org_id"]}).sort("created_at", -1).to_list(200)
    return [clean(d) for d in docs]


@api.get("/entitlements")
async def list_entitlements(user: dict = Depends(require_client)):
    if not user.get("org_id"):
        return []
    docs = await db.entitlements.find({"org_id": user["org_id"], "active": True}).to_list(100)
    return [clean(d) for d in docs]


@api.get("/invoices")
async def list_invoices(user: dict = Depends(require_client)):
    if not user.get("org_id"):
        return []
    docs = await db.invoices.find({"org_id": user["org_id"]}).sort("created_at", -1).to_list(100)
    return [clean(d) for d in docs]


# --------------------------------------------------------------------------- #
# Onboarding
# --------------------------------------------------------------------------- #
@api.get("/onboarding/schema/{slug}")
async def onboarding_schema(slug: str):
    if not cp.get_standard(slug):
        raise HTTPException(404, "Unknown standard")
    return ob.build_schema(slug)


async def _require_entitlement(org_id: str, slug: str):
    ent = await db.entitlements.find_one({"org_id": org_id, "standard_slug": slug, "active": True})
    if not ent:
        raise HTTPException(403, "No active entitlement — purchase this toolkit first")
    return ent


@api.post("/onboarding/draft")
async def save_draft(body: DraftIn, user: dict = Depends(require_client)):
    await _require_entitlement(user["org_id"], body.standard_slug)
    pct = ob.completion_percent(body.standard_slug, body.answers)
    existing = await db.submissions.find_one({"org_id": user["org_id"], "standard_slug": body.standard_slug})
    doc = {
        "org_id": user["org_id"], "user_id": user["id"], "standard_slug": body.standard_slug,
        "answers": body.answers, "completion": pct, "updated_at": now_iso(),
    }
    if existing and existing.get("status") in ("approved",):
        raise HTTPException(400, "Submission already approved")
    if existing:
        await db.submissions.update_one({"id": existing["id"]}, {"$set": doc})
        sub_id = existing["id"]
        status = existing.get("status", "draft")
        if status in ("submitted", "changes_requested"):
            status = "draft"
        await db.submissions.update_one({"id": sub_id}, {"$set": {"status": status}})
    else:
        doc.update({"id": new_id(), "status": "draft", "created_at": now_iso(),
                    "comments": [], "declaration": False})
        await db.submissions.insert_one(dict(doc))
        sub_id = doc["id"]
    return clean(await db.submissions.find_one({"id": sub_id}))


@api.get("/onboarding/submission/{slug}")
async def get_submission(slug: str, user: dict = Depends(require_client)):
    sub = await db.submissions.find_one({"org_id": user["org_id"], "standard_slug": slug})
    return clean(sub)


@api.post("/onboarding/submit")
async def submit_onboarding(body: SubmitIn, user: dict = Depends(require_client)):
    await _require_entitlement(user["org_id"], body.standard_slug)
    if not body.declaration:
        raise HTTPException(400, "You must accept the declaration")
    missing = [q for q in ob.required_question_ids(body.standard_slug, body.answers)
               if str(body.answers.get(q, "")).strip() in ("", "None", "[]")]
    if missing:
        raise HTTPException(400, f"Please complete required fields: {missing}")
    pct = ob.completion_percent(body.standard_slug, body.answers)
    existing = await db.submissions.find_one({"org_id": user["org_id"], "standard_slug": body.standard_slug})
    payload = {
        "org_id": user["org_id"], "user_id": user["id"], "standard_slug": body.standard_slug,
        "answers": body.answers, "completion": pct, "declaration": True,
        "status": "submitted", "submitted_at": now_iso(), "updated_at": now_iso(),
    }
    if existing:
        await db.submissions.update_one({"id": existing["id"]}, {"$set": payload})
        sub_id = existing["id"]
    else:
        payload.update({"id": new_id(), "created_at": now_iso(), "comments": []})
        await db.submissions.insert_one(dict(payload))
        sub_id = payload["id"]
    await audit("onboarding_submitted", user, meta={"submission_id": sub_id})
    return clean(await db.submissions.find_one({"id": sub_id}))


# --------------------------------------------------------------------------- #
# Admin — verification workflow
# --------------------------------------------------------------------------- #
@api.get("/admin/reviews")
async def admin_reviews(admin: dict = Depends(require_admin)):
    subs = await db.submissions.find({"status": {"$in": ["submitted", "changes_requested", "approved", "rejected"]}}
                                     ).sort("submitted_at", -1).to_list(500)
    out = []
    for s in subs:
        org = await db.organizations.find_one({"id": s["org_id"]})
        out.append({**clean(s), "org_name": (org or {}).get("legal_name", "—"),
                    "org_trade": (org or {}).get("trade_name", "")})
    return out


@api.get("/admin/reviews/{sub_id}")
async def admin_review_detail(sub_id: str, admin: dict = Depends(require_admin)):
    sub = await db.submissions.find_one({"id": sub_id})
    if not sub:
        raise HTTPException(404, "Not found")
    org = await db.organizations.find_one({"id": sub["org_id"]})
    schema = ob.build_schema(sub["standard_slug"])
    return {"submission": clean(sub), "org": clean(org), "schema": schema}


@api.post("/admin/reviews/{sub_id}/comment")
async def add_comment(sub_id: str, body: ReviewAction, admin: dict = Depends(require_admin)):
    comment = {"id": new_id(), "text": body.comment, "section_id": body.section_id,
               "by": admin["name"], "at": now_iso()}
    await db.submissions.update_one({"id": sub_id}, {"$push": {"comments": comment}})
    return {"ok": True, "comment": comment}


@api.post("/admin/reviews/{sub_id}/request-correction")
async def request_correction(sub_id: str, body: ReviewAction, admin: dict = Depends(require_admin)):
    sub = await db.submissions.find_one({"id": sub_id})
    if not sub:
        raise HTTPException(404, "Not found")
    comment = {"id": new_id(), "text": body.comment or "Please review flagged sections.",
               "section_id": body.section_id, "by": admin["name"], "at": now_iso(), "type": "correction"}
    await db.submissions.update_one({"id": sub_id}, {
        "$set": {"status": "changes_requested", "updated_at": now_iso()},
        "$push": {"comments": comment}})
    await audit("correction_requested", admin, sub["org_id"], {"submission_id": sub_id})
    return clean(await db.submissions.find_one({"id": sub_id}))


@api.post("/admin/reviews/{sub_id}/approve")
async def approve_submission(sub_id: str, admin: dict = Depends(require_admin)):
    sub = await db.submissions.find_one({"id": sub_id})
    if not sub:
        raise HTTPException(404, "Not found")
    await db.submissions.update_one({"id": sub_id}, {"$set": {
        "status": "approved", "approved_at": now_iso(), "approved_by": admin["name"], "updated_at": now_iso()}})
    await audit("onboarding_approved", admin, sub["org_id"], {"submission_id": sub_id})
    return clean(await db.submissions.find_one({"id": sub_id}))


@api.post("/admin/reviews/{sub_id}/reject")
async def reject_submission(sub_id: str, body: ReviewAction, admin: dict = Depends(require_admin)):
    sub = await db.submissions.find_one({"id": sub_id})
    if not sub:
        raise HTTPException(404, "Not found")
    await db.submissions.update_one({"id": sub_id}, {"$set": {
        "status": "rejected", "rejected_at": now_iso(), "reject_reason": body.comment, "updated_at": now_iso()}})
    await audit("onboarding_rejected", admin, sub["org_id"], {"submission_id": sub_id})
    return clean(await db.submissions.find_one({"id": sub_id}))


# --------------------------------------------------------------------------- #
# Generation pipeline
# --------------------------------------------------------------------------- #
def _build_context(org: dict, answers: dict) -> dict:
    a = answers or {}

    def pick(*keys, default=""):
        for k in keys:
            v = a.get(k)
            if v not in (None, "", []):
                return v
        return default

    locations = pick("locations", "included_locations", default=org.get("locations", ""))
    if isinstance(locations, str):
        locations_list = [x.strip() for x in locations.split(",") if x.strip()] or [locations]
    else:
        locations_list = locations

    logo_path = None
    logo_b64 = org.get("logo_base64") or ""
    if logo_b64:
        try:
            raw = logo_b64.split(",", 1)[-1]
            data = base64.b64decode(raw)
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            tmp.write(data)
            tmp.flush()
            logo_path = tmp.name
        except Exception:
            logo_path = None

    return {
        "org": {
            "legal_name": pick("legal_name", default=org.get("legal_name", "")),
            "trade_name": pick("trade_name", default=org.get("trade_name", "")),
            "website": pick("website", default=org.get("website", "")),
            "industry": pick("industry", default=org.get("industry", "")),
            "employee_count": pick("employee_count", default=org.get("employee_count", "")),
            "products_services": pick("products_services", default=org.get("products_services", "")),
            "brand_color": pick("brand_color", default="#1F3A5F"),
            "locations": locations_list,
            "logo_path": logo_path,
        },
        "roles": {
            "top_management": pick("top_management", default="Top Management"),
            "ms_coordinator": pick("ms_coordinator", default="Management System Coordinator"),
            "internal_auditor": pick("internal_auditor", default="Internal Auditor"),
            "privacy_contact": pick("privacy_contact", "ms_coordinator", default="Privacy Contact"),
            "security_contact": pick("security_contact", "ms_coordinator", default="Security Contact"),
        },
        "doc_control": {
            "version": pick("version", default="1.0"),
            "effective_date": pick("effective_date", default=datetime.now().strftime("%d %b %Y")),
            "review_date": pick("review_date", default=""),
            "classification": pick("classification", default="Internal"),
            "prepared_by": pick("prepared_by", default=""),
            "reviewed_by": pick("reviewed_by", default=""),
            "approved_by": pick("approved_by", default=""),
        },
    }


async def _run_generation(sub: dict, admin: dict) -> dict:
    org = await db.organizations.find_one({"id": sub["org_id"]})
    std = cp.get_standard(sub["standard_slug"])
    context = _build_context(org, sub["answers"])
    specs = cp.build_manifest(std)
    _flat_ctx = flatten_context(context)

    def _resolved_class(spec):
        return resolve_variables(spec.get("classification", "Internal"), _flat_ctx)

    job = {
        "id": new_id(), "org_id": sub["org_id"], "submission_id": sub["id"],
        "standard_slug": sub["standard_slug"], "status": "validating",
        "created_at": now_iso(), "logs": [], "validation": [],
    }
    await db.generation_jobs.insert_one(dict(job))

    # Validate
    validation = [validate_document(spec, context) for spec in specs]
    val_errors = [v for v in validation if not v["ok"]]
    await db.generation_jobs.update_one({"id": job["id"]}, {"$set": {
        "status": "generating", "validation": validation}})

    if val_errors:
        await db.generation_jobs.update_one({"id": job["id"]}, {"$set": {"status": "generation_failed"}})
        return {"job_id": job["id"], "status": "generation_failed", "errors": val_errors}

    # Generate + store
    artifacts = []
    zip_files: Dict[str, bytes] = {}
    # remove any previous generated docs for this submission (regeneration)
    await db.generated_documents.delete_many({"submission_id": sub["id"]})

    for spec in specs:
        fmt = spec["format"]
        safe_title = spec["title"].replace("/", "-").replace(" ", "_")
        if fmt == "docx":
            data = render_docx_document(spec, context)
            fname = f"{spec['doc_id']}_{safe_title}.docx"
            zip_files[f"documents/{fname}"] = data
            pdf = render_pdf_document(spec, context)
            pname = f"{spec['doc_id']}_{safe_title}.pdf"
            zip_files[f"reference_pdf/{pname}"] = pdf
            # store docx + pdf
            for f, d, mime in [(fname, data, "docx"), (pname, pdf, "pdf")]:
                aid = new_id()
                await db.generated_documents.insert_one({
                    "id": aid, "org_id": sub["org_id"], "submission_id": sub["id"],
                    "doc_id": spec["doc_id"], "title": spec["title"], "filename": f,
                    "format": mime, "category": spec["category"],
                    "template_class": spec["template_class"],
                    "classification": _resolved_class(spec),
                    "clause_refs": spec.get("clause_refs", []),
                    "data_b64": base64.b64encode(d).decode(), "version": context["doc_control"]["version"],
                    "created_at": now_iso(),
                })
                if mime == "docx":
                    artifacts.append({"id": aid, "doc_id": spec["doc_id"], "title": spec["title"],
                                      "format": "DOCX", "filename": f, "category": spec["category"]})
                else:
                    artifacts.append({"id": aid, "doc_id": spec["doc_id"], "title": spec["title"],
                                      "format": "PDF", "filename": f, "category": spec["category"]})
        else:  # xlsx
            data = render_xlsx_register(spec, context)
            fname = f"{spec['doc_id']}_{safe_title}.xlsx"
            zip_files[f"registers/{fname}"] = data
            aid = new_id()
            await db.generated_documents.insert_one({
                "id": aid, "org_id": sub["org_id"], "submission_id": sub["id"],
                "doc_id": spec["doc_id"], "title": spec["title"], "filename": fname,
                "format": "xlsx", "category": spec["category"],
                "template_class": spec["template_class"],
                "classification": _resolved_class(spec),
                "clause_refs": spec.get("clause_refs", []),
                "data_b64": base64.b64encode(data).decode(), "version": context["doc_control"]["version"],
                "created_at": now_iso(),
            })
            artifacts.append({"id": aid, "doc_id": spec["doc_id"], "title": spec["title"],
                              "format": "XLSX", "filename": fname, "category": spec["category"]})

    # index + manifest + matrices
    import json as _json
    manifest = {"organization": context["org"]["legal_name"], "standard": std["name"],
                "generated": list(zip_files.keys()), "count": len(zip_files)}
    zip_files["toolkit_manifest.json"] = _json.dumps(manifest, indent=2).encode()
    matrix_rows = "".join(
        f"<tr><td>{s['doc_id']}</td><td>{s['title']}</td><td>{', '.join(s.get('clause_refs', []))}</td></tr>"
        for s in specs)
    matrix = (f"<html><body><h1>{context['org']['legal_name']} — Clause-to-Document Matrix</h1>"
              f"<table border=1 cellpadding=6><tr><th>Doc ID</th><th>Title</th><th>Clause</th></tr>"
              f"{matrix_rows}</table></body></html>")
    zip_files["clause_to_document_matrix.html"] = matrix.encode()
    index = (f"<html><body><h1>{context['org']['legal_name']} — {std['name']}</h1>"
             f"<p>Toolkit index — {len(specs)} documents.</p><ul>"
             + "".join(f"<li>{k}</li>" for k in zip_files) + "</ul></body></html>")
    zip_files["index.html"] = index.encode()

    zip_bytes = build_zip(zip_files)
    await db.generated_documents.delete_many({"submission_id": sub["id"], "format": "zip"})
    zip_id = new_id()
    await db.generated_documents.insert_one({
        "id": zip_id, "org_id": sub["org_id"], "submission_id": sub["id"],
        "doc_id": "ZIP", "title": f"{std['short']} — Complete Toolkit Package",
        "filename": f"{std['slug']}_toolkit.zip", "format": "zip", "category": "package",
        "template_class": "Package", "classification": "Confidential", "clause_refs": [],
        "data_b64": base64.b64encode(zip_bytes).decode(), "version": context["doc_control"]["version"],
        "created_at": now_iso(),
    })

    await db.generation_jobs.update_one({"id": job["id"]}, {"$set": {
        "status": "generated", "artifact_count": len(artifacts), "completed_at": now_iso()}})
    await db.submissions.update_one({"id": sub["id"]}, {"$set": {
        "generation_status": "generated", "generated_at": now_iso(), "job_id": job["id"]}})
    await audit("documents_generated", admin, sub["org_id"],
                {"submission_id": sub["id"], "count": len(artifacts)})
    return {"job_id": job["id"], "status": "generated", "artifact_count": len(artifacts), "zip_id": zip_id}


@api.post("/admin/generate/{sub_id}")
async def admin_generate(sub_id: str, admin: dict = Depends(require_admin)):
    sub = await db.submissions.find_one({"id": sub_id})
    if not sub:
        raise HTTPException(404, "Submission not found")
    if sub.get("status") != "approved":
        raise HTTPException(400, "Onboarding must be approved before generation")
    result = await _run_generation(sub, admin)
    return result


@api.post("/admin/publish/{sub_id}")
async def admin_publish(sub_id: str, admin: dict = Depends(require_admin)):
    sub = await db.submissions.find_one({"id": sub_id})
    if not sub or sub.get("generation_status") != "generated":
        raise HTTPException(400, "Nothing generated to publish")
    await db.submissions.update_one({"id": sub_id}, {"$set": {"generation_status": "published",
                                                              "published_at": now_iso()}})
    await audit("documents_published", admin, sub["org_id"], {"submission_id": sub_id})
    return {"status": "published"}


@api.get("/admin/jobs")
async def list_jobs(admin: dict = Depends(require_admin)):
    jobs = await db.generation_jobs.find().sort("created_at", -1).to_list(200)
    return [clean(j) for j in jobs]


# --------------------------------------------------------------------------- #
# Downloads (tenant-isolated)
# --------------------------------------------------------------------------- #
@api.get("/downloads")
async def list_downloads(slug: Optional[str] = None, user: dict = Depends(require_client)):
    if not user.get("org_id"):
        return {"published": False, "documents": []}
    query = {"org_id": user["org_id"]}
    subs = await db.submissions.find({"org_id": user["org_id"]}).to_list(50)
    if slug:
        subs = [s for s in subs if s["standard_slug"] == slug]
    sub_ids = [s["id"] for s in subs if s.get("generation_status") in ("generated", "published")]
    if not sub_ids:
        return {"published": False, "documents": []}
    docs = await db.generated_documents.find({"org_id": user["org_id"], "submission_id": {"$in": sub_ids}}).to_list(500)
    out = []
    for d in docs:
        out.append({k: d.get(k) for k in
                    ("id", "doc_id", "title", "filename", "format", "category",
                     "template_class", "classification", "clause_refs", "version")})
    published = any(s.get("generation_status") == "published" for s in subs)
    return {"published": published, "documents": out}


@api.get("/downloads/{artifact_id}")
async def download_artifact(artifact_id: str, user: dict = Depends(get_current_user)):
    doc = await db.generated_documents.find_one({"id": artifact_id})
    if not doc:
        raise HTTPException(404, "Not found")
    # tenant isolation — clients only access their org's files
    if user["role"] == "client" and doc["org_id"] != user.get("org_id"):
        raise HTTPException(403, "Forbidden")
    await db.downloads.insert_one({"id": new_id(), "artifact_id": artifact_id,
                                   "org_id": doc["org_id"], "by": user["id"], "at": now_iso()})
    data = base64.b64decode(doc["data_b64"])
    mimes = {
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "pdf": "application/pdf", "zip": "application/zip",
    }
    return StreamingResponse(io.BytesIO(data), media_type=mimes.get(doc["format"], "application/octet-stream"),
                             headers={"Content-Disposition": f'attachment; filename="{doc["filename"]}"'})


# --------------------------------------------------------------------------- #
# Additional requirements + quotations
# --------------------------------------------------------------------------- #
@api.post("/additional-requirements")
async def create_addl(body: AdditionalReqIn, user: dict = Depends(require_client)):
    if not user.get("org_id"):
        raise HTTPException(400, "Create your organization first")
    req = {"id": new_id(), "org_id": user["org_id"], "title": body.title,
           "description": body.description, "category": body.category,
           "status": "submitted", "created_at": now_iso(), "quotation": None}
    await db.additional_requirements.insert_one(dict(req))
    await audit("additional_requirement_submitted", user, meta={"id": req["id"]})
    return clean(req)


@api.get("/additional-requirements")
async def list_addl(user: dict = Depends(require_client)):
    if not user.get("org_id"):
        return []
    docs = await db.additional_requirements.find({"org_id": user["org_id"]}).sort("created_at", -1).to_list(100)
    return [clean(d) for d in docs]


@api.get("/admin/additional-requirements")
async def admin_list_addl(admin: dict = Depends(require_admin)):
    docs = await db.additional_requirements.find().sort("created_at", -1).to_list(300)
    out = []
    for d in docs:
        org = await db.organizations.find_one({"id": d["org_id"]})
        out.append({**clean(d), "org_name": (org or {}).get("legal_name", "—")})
    return out


@api.post("/admin/additional-requirements/{req_id}/quote")
async def quote_addl(req_id: str, body: QuotationIn, admin: dict = Depends(require_admin)):
    req = await db.additional_requirements.find_one({"id": req_id})
    if not req:
        raise HTTPException(404, "Not found")
    quotation = {"id": new_id(), "amount": body.amount, "description": body.description,
                 "status": "pending", "created_at": now_iso()}
    await db.additional_requirements.update_one({"id": req_id}, {"$set": {
        "status": "quoted", "quotation": quotation}})
    await audit("quotation_created", admin, req["org_id"], {"req_id": req_id})
    return clean(await db.additional_requirements.find_one({"id": req_id}))


@api.post("/additional-requirements/{req_id}/respond")
async def respond_addl(req_id: str, body: dict, user: dict = Depends(require_client)):
    req = await db.additional_requirements.find_one({"id": req_id, "org_id": user["org_id"]})
    if not req or not req.get("quotation"):
        raise HTTPException(404, "No quotation to respond to")
    accept = bool(body.get("accept"))
    new_status = "accepted" if accept else "rejected"
    q = req["quotation"]
    q["status"] = new_status
    await db.additional_requirements.update_one({"id": req_id}, {"$set": {
        "status": new_status, "quotation": q}})
    return clean(await db.additional_requirements.find_one({"id": req_id}))


@api.post("/additional-requirements/{req_id}/pay")
async def pay_addl(req_id: str, user: dict = Depends(require_client)):
    req = await db.additional_requirements.find_one({"id": req_id, "org_id": user["org_id"]})
    if not req or req.get("status") != "accepted":
        raise HTTPException(400, "Quotation must be accepted first")
    q = req["quotation"]; q["status"] = "paid"
    await db.additional_requirements.update_one({"id": req_id}, {"$set": {"status": "paid", "quotation": q}})
    await audit("additional_payment", user, meta={"req_id": req_id})
    return clean(await db.additional_requirements.find_one({"id": req_id}))


# --------------------------------------------------------------------------- #
# Admin dashboards + management
# --------------------------------------------------------------------------- #
@api.get("/admin/dashboard/executive")
async def exec_dashboard(admin: dict = Depends(require_admin)):
    total_clients = await db.organizations.count_documents({})
    paid_orders = await db.orders.find({"status": "paid"}).to_list(1000)
    revenue = sum(o["amount"] for o in paid_orders)
    pending_reviews = await db.submissions.count_documents({"status": "submitted"})
    pending_addl = await db.additional_requirements.count_documents({"status": "submitted"})
    failed_jobs = await db.generation_jobs.count_documents({"status": "generation_failed"})
    # most purchased
    by_std: Dict[str, int] = {}
    for o in paid_orders:
        by_std[o["standard_name"]] = by_std.get(o["standard_name"], 0) + 1
    active_ents = await db.entitlements.count_documents({"active": True})
    return {
        "total_clients": total_clients, "active_entitlements": active_ents,
        "toolkit_sales": len(paid_orders), "revenue": revenue,
        "pending_reviews": pending_reviews, "pending_additional": pending_addl,
        "failed_jobs": failed_jobs,
        "most_purchased": sorted(by_std.items(), key=lambda x: -x[1]),
    }


@api.get("/admin/dashboard/commerce")
async def commerce_dashboard(admin: dict = Depends(require_admin)):
    orders = await db.orders.find().sort("created_at", -1).to_list(500)
    invoices = await db.invoices.find().sort("created_at", -1).to_list(500)
    coupons = await db.coupons.find().to_list(100)
    by_std: Dict[str, float] = {}
    for o in orders:
        if o["status"] == "paid":
            by_std[o["standard_name"]] = by_std.get(o["standard_name"], 0) + o["amount"]
    return {"orders": [clean(o) for o in orders], "invoices": [clean(i) for i in invoices],
            "coupons": [clean(c) for c in coupons], "revenue_by_standard": by_std}


@api.get("/admin/dashboard/content")
async def content_dashboard(admin: dict = Depends(require_admin)):
    out = []
    for s in cp.STANDARDS:
        manifest = cp.manifest_summary(s)
        out.append({"slug": s["slug"], "name": s["name"], "version": s["version"],
                    "document_count": len(manifest), "status": "published"})
    return {"standards": out}


@api.get("/admin/clients")
async def admin_clients(admin: dict = Depends(require_admin)):
    orgs = await db.organizations.find().sort("created_at", -1).to_list(500)
    out = []
    for o in orgs:
        ent = await db.entitlements.count_documents({"org_id": o["id"], "active": True})
        out.append({**clean(o), "entitlements": ent})
    return out


@api.get("/admin/audit-logs")
async def admin_audit(admin: dict = Depends(require_admin)):
    logs = await db.audit_logs.find().sort("at", -1).to_list(300)
    return [clean(l) for l in logs]


@api.post("/admin/coupons")
async def create_coupon(body: CouponIn, admin: dict = Depends(require_admin)):
    existing = await db.coupons.find_one({"code": body.code.upper()})
    if existing:
        await db.coupons.update_one({"code": body.code.upper()},
                                    {"$set": {"percent_off": body.percent_off, "active": body.active}})
    else:
        await db.coupons.insert_one({"id": new_id(), "code": body.code.upper(),
                                     "percent_off": body.percent_off, "active": body.active,
                                     "created_at": now_iso()})
    return clean(await db.coupons.find_one({"code": body.code.upper()}))


@api.get("/health")
async def health():
    return {"status": "ok", "service": "faizzab", "time": now_iso()}


app.include_router(api)
app.add_middleware(
    CORSMiddleware, allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"], allow_headers=["*"],
)
