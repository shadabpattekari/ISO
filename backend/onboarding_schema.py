"""
Modular onboarding schema — Sections A to I, dynamic questions and simple
conditional rules. Section H (standard-specific) varies by toolkit standard.

A question:
  {id, label, type, required, options?, help?, placeholder?, show_if?}
show_if: {"field": "<question id>", "in": [values...]} — simple client+server rule.
"""
from __future__ import annotations
from typing import Any, Dict, List

INDUSTRIES = [
    "Information Technology", "SaaS", "Cybersecurity", "Professional Consulting",
    "Healthcare", "Financial Services", "Manufacturing", "Education",
    "E-commerce and Retail", "Logistics",
]


def _q(qid, label, qtype="text", required=False, **kw):
    d = {"id": qid, "label": label, "type": qtype, "required": required}
    d.update(kw)
    return d


BASE_SECTIONS: List[Dict[str, Any]] = [
    {
        "id": "A", "title": "Organization Identity", "icon": "building-2",
        "why": "This information brands every generated document with your legal identity.",
        "questions": [
            _q("legal_name", "Legal Entity Name", required=True, placeholder="Acme Technologies Private Limited"),
            _q("trade_name", "Trade / Brand Name", required=True, placeholder="Acme"),
            _q("website", "Website Domain", placeholder="acme.io"),
            _q("registration_number", "CIN / Registration Number"),
            _q("gstin", "GSTIN (if applicable)"),
            _q("registered_address", "Registered Address", "textarea", required=True),
            _q("locations", "Operating Locations (comma separated)", "text", required=True,
               placeholder="Bengaluru HQ, Pune Office"),
            _q("employee_count", "Employee Count", "number", required=True, placeholder="35"),
            _q("primary_contact", "Primary Contact Name", required=True),
            _q("contact_email", "Contact Email", "email", required=True),
            _q("contact_mobile", "Contact Mobile", required=True),
        ],
    },
    {
        "id": "B", "title": "Business Profile", "icon": "briefcase",
        "why": "Describes what your organization does, shaping scope and examples in documents.",
        "questions": [
            _q("industry", "Industry", "select", required=True, options=INDUSTRIES),
            _q("products_services", "Products and Services", "textarea", required=True,
               placeholder="Multi-tenant SaaS analytics platform"),
            _q("customers", "Types of Customers", "text", placeholder="Enterprises, SMBs"),
            _q("markets", "Markets / Countries Served", "text", placeholder="India, US, EU"),
            _q("business_hours", "Business Hours", "text", placeholder="Mon-Fri 9:00-18:00 IST"),
        ],
    },
    {
        "id": "C", "title": "Organizational Structure", "icon": "users",
        "why": "Named roles are inserted as document owners, reviewers and approvers. In small companies one person may hold several roles.",
        "questions": [
            _q("top_management", "Top Management (Name & Title)", required=True, placeholder="Anita Desai (CEO)"),
            _q("ms_coordinator", "Management System Coordinator", required=True, placeholder="Priya Sharma"),
            _q("internal_auditor", "Internal Auditor", required=True, placeholder="Rahul Verma"),
            _q("privacy_contact", "Privacy / Data Protection Contact", placeholder="Priya Sharma"),
            _q("security_contact", "Information Security Contact", placeholder="Priya Sharma"),
            _q("departments", "Department Names (comma separated)", "text", placeholder="Engineering, Sales, HR, Finance"),
        ],
    },
    {
        "id": "D", "title": "Management-System Scope", "icon": "target",
        "why": "Defines the boundaries of your management system and any exclusions.",
        "questions": [
            _q("included_services", "Services included in scope", "textarea", required=True),
            _q("included_locations", "Locations included in scope", "text", required=True),
            _q("exclusions", "Exclusions and justification", "textarea"),
            _q("internal_issues", "Key internal issues", "textarea"),
            _q("external_issues", "Key external issues", "textarea"),
            _q("interested_parties", "Key interested parties", "textarea",
               placeholder="Customers, employees, regulators, suppliers"),
        ],
    },
    {
        "id": "E", "title": "Process Inventory", "icon": "workflow",
        "why": "Lists the processes your management system will cover.",
        "questions": [
            _q("processes", "Select the processes in scope", "multiselect", required=True, options=[
                "Sales", "Customer Onboarding", "Service Delivery", "Product Development",
                "Procurement", "Human Resources", "Finance", "IT", "Support", "Operations",
                "Legal and Compliance", "Business Continuity",
            ]),
            _q("outsourced", "Outsourced activities", "textarea", placeholder="Payroll, cloud hosting"),
        ],
    },
    {
        "id": "F", "title": "Technology Profile", "icon": "server",
        "why": "Determines conditional technical content (cloud, remote work, AI).",
        "questions": [
            _q("uses_cloud", "Do you use cloud services?", "boolean", required=True),
            _q("cloud_providers", "Cloud providers", "text", show_if={"field": "uses_cloud", "in": [True, "true", "yes"]},
               placeholder="AWS, GCP, Azure"),
            _q("remote_work", "Do employees work remotely?", "boolean", required=True),
            _q("uses_ai", "Do you use Artificial Intelligence in operations?", "boolean"),
            _q("applications", "Key business applications", "textarea", placeholder="CRM, ERP, code repositories"),
            _q("data_hosting", "Where is data hosted?", "text", placeholder="India region, EU region"),
            _q("backup", "Backup arrangements", "text"),
        ],
    },
    {
        "id": "G", "title": "Legal and Regulatory Profile", "icon": "scale",
        "why": "Captures obligations that generated documents must reference.",
        "questions": [
            _q("jurisdiction", "Primary country / state of operation", "text", required=True, placeholder="India / Karnataka"),
            _q("processes_personal_data", "Do you process personal data?", "boolean", required=True),
            _q("cross_border", "Cross-border data transfer?", "boolean",
               show_if={"field": "processes_personal_data", "in": [True, "true", "yes"]}),
            _q("sector_regulation", "Sector-specific regulation (if any)", "text"),
            _q("customer_security_reqs", "Specific customer security requirements", "textarea"),
        ],
    },
]

SECTION_I = {
    "id": "I", "title": "Branding and Document Control", "icon": "palette",
    "why": "Controls the look and document-control metadata of every generated file.",
    "questions": [
        _q("brand_color", "Primary Brand Colour (hex)", "text", required=True, placeholder="#1F3A5F"),
        _q("classification", "Default Document Classification", "select", required=True,
           options=["Public", "Internal", "Confidential", "Restricted"]),
        _q("version", "Document Version", "text", required=True, placeholder="1.0"),
        _q("effective_date", "Effective Date", "text", required=True, placeholder="01 Feb 2026"),
        _q("review_date", "Next Review Date", "text", required=True, placeholder="01 Feb 2027"),
        _q("prepared_by", "Prepared By (name)", required=True),
        _q("reviewed_by", "Reviewed By (name)", required=True),
        _q("approved_by", "Approved By (name)", required=True),
    ],
}

# Section H — standard specific
STANDARD_SPECIFIC: Dict[str, Dict[str, Any]] = {
    "iso-27001": {
        "id": "H", "title": "ISO 27001 — Information Security", "icon": "shield-check",
        "why": "Drives ISMS-specific content and control applicability.",
        "questions": [
            _q("info_assets", "Most critical information assets", "textarea", required=True,
               placeholder="Customer data, source code, financial records"),
            _q("has_dev", "Do you develop software?", "boolean"),
            _q("privileged_access", "Who has privileged/admin access?", "text"),
            _q("prev_incidents", "Any security incidents in the last 12 months?", "boolean"),
            _q("mfa_enabled", "Is MFA enabled for critical systems?", "boolean"),
        ],
    },
    "dpdpa": {
        "id": "H", "title": "DPDP Act — Data Protection", "icon": "lock",
        "why": "Drives DPDP-specific content. Documents include a legal-review disclaimer.",
        "questions": [
            _q("data_categories", "Categories of personal data processed", "textarea", required=True,
               placeholder="Name, email, phone, payment info"),
            _q("processes_children", "Do you process children's data?", "boolean", required=True),
            _q("uses_processors", "Do you use third-party data processors?", "boolean", required=True),
            _q("consent_mechanism", "How is consent collected?", "text", placeholder="Web form, app"),
            _q("is_sdf", "Are you a Significant Data Fiduciary?", "boolean"),
        ],
    },
    "iso-9001": {
        "id": "H", "title": "ISO 9001 — Quality", "icon": "badge-check",
        "why": "Drives QMS-specific content.",
        "questions": [
            _q("key_products", "Key products/services to certify", "textarea", required=True),
            _q("has_design", "Do you perform design and development?", "boolean", required=True),
            _q("has_production", "Do you have production/manufacturing?", "boolean"),
            _q("measuring_equipment", "Do you use measuring/monitoring equipment?", "boolean"),
            _q("key_suppliers", "Key suppliers", "text"),
        ],
    },
}


def build_schema(slug: str) -> Dict[str, Any]:
    sections = list(BASE_SECTIONS)
    if slug in STANDARD_SPECIFIC:
        sections = sections + [STANDARD_SPECIFIC[slug]]
    sections = sections + [SECTION_I]
    return {"slug": slug, "sections": sections}


def all_question_ids(slug: str) -> List[str]:
    ids = []
    for sec in build_schema(slug)["sections"]:
        for q in sec["questions"]:
            ids.append(q["id"])
    return ids


def required_question_ids(slug: str, answers: Dict[str, Any]) -> List[str]:
    """Required questions, honoring show_if conditional visibility."""
    req = []
    for sec in build_schema(slug)["sections"]:
        for q in sec["questions"]:
            if not q.get("required"):
                continue
            cond = q.get("show_if")
            if cond:
                val = answers.get(cond["field"])
                if val not in cond["in"]:
                    continue
            req.append(q["id"])
    return req


def completion_percent(slug: str, answers: Dict[str, Any]) -> int:
    req = required_question_ids(slug, answers or {})
    if not req:
        return 0
    filled = sum(1 for qid in req if str(answers.get(qid, "")).strip() not in ("", "None", "[]"))
    return int(round(filled / len(req) * 100))
