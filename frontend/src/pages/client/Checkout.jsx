import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api, { rupee } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Disclaimer } from "@/components/common/Disclaimer";
import { toast } from "sonner";
import { CreditCard, Tag, CheckCircle2, Building2 } from "lucide-react";

export default function Checkout() {
  const { slug } = useParams();
  const nav = useNavigate();
  const { org } = useAuth();
  const [t, setT] = useState(null);
  const [coupon, setCoupon] = useState("");
  const [applied, setApplied] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => { api.get(`/catalogue/${slug}`).then((r) => setT(r.data)); }, [slug]);

  const applyCoupon = async () => {
    try { const { data } = await api.post("/coupons/validate", { code: coupon }); setApplied(data); toast.success(`Coupon ${data.code} applied — ${data.percent_off}% off`); }
    catch { toast.error("Invalid coupon"); setApplied(null); }
  };

  const pay = async () => {
    if (!org) { toast.error("Create your organization profile first"); nav("/app/organization"); return; }
    setBusy(true);
    try {
      const { data: order } = await api.post("/orders", { standard_slug: slug, coupon: applied ? coupon : null });
      // Simulated Razorpay checkout — verified server-side.
      const { data } = await api.post(`/orders/${order.id}/verify-payment`, { razorpay_payment_id: "sim_" + Date.now() });
      if (data.status === "paid") { toast.success("Payment verified! Toolkit unlocked."); nav(`/app/onboarding/${slug}`); }
    } catch (e) { toast.error(e?.response?.data?.detail || "Payment failed"); } finally { setBusy(false); }
  };

  if (!t) return <AppShell><div className="text-[hsl(var(--muted-foreground))]">Loading…</div></AppShell>;

  const base = t.price;
  const discount = applied ? Math.round(base * applied.percent_off / 100) : 0;
  const subtotal = base - discount;
  const gst = Math.round(subtotal * t.gst_rate);
  const total = subtotal + gst;

  return (
    <AppShell>
      <div className="mb-6"><h1 className="text-2xl font-display">Checkout</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">{t.name}</p></div>
      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          {!org && <Card className="card-shadow p-4 flex items-center gap-3 bg-[hsl(var(--warning-bg))] text-[hsl(var(--warning-fg))]"><Building2 className="h-5 w-5" /><div className="text-sm">Create your organization profile before purchasing. <button className="underline" onClick={() => nav("/app/organization")}>Set up now</button></div></Card>}
          <Card className="card-shadow p-5">
            <h2 className="font-display text-lg mb-3">What you get</h2>
            <ul className="space-y-2 text-sm">
              {[`${t.document_count} organization-specific documents`, "Editable DOCX & XLSX + reference PDFs", "Complete ZIP package", "Guided onboarding & admin verification", "Regeneration after approved changes"].map((x) => (
                <li key={x} className="flex items-start gap-2"><CheckCircle2 className="h-4 w-4 text-[hsl(var(--teal))] mt-0.5" />{x}</li>
              ))}
            </ul>
          </Card>
          <Disclaimer>This is a simulated payment for demonstration. In production this uses Razorpay with server-side verification. Purchase does not guarantee certification.</Disclaimer>
        </div>
        <div>
          <Card className="card-shadow p-5 sticky top-24">
            <div className="flex gap-2">
              <Input placeholder="Coupon (try LAUNCH20)" value={coupon} onChange={(e) => setCoupon(e.target.value)} data-testid="coupon-input" />
              <Button variant="outline" onClick={applyCoupon} data-testid="apply-coupon-button"><Tag className="h-4 w-4" /></Button>
            </div>
            <div className="mt-4 space-y-2 text-sm">
              <div className="flex justify-between"><span>Base price</span><span className="tabular-nums">{rupee(base)}</span></div>
              {discount > 0 && <div className="flex justify-between text-[hsl(var(--success-fg))]"><span>Discount</span><span className="tabular-nums">-{rupee(discount)}</span></div>}
              <div className="flex justify-between"><span>GST ({Math.round(t.gst_rate*100)}%)</span><span className="tabular-nums">{rupee(gst)}</span></div>
              <div className="border-t pt-2 flex justify-between font-semibold text-base"><span>Total</span><span className="tabular-nums">{rupee(total)}</span></div>
            </div>
            <Button className="w-full mt-4" size="lg" onClick={pay} disabled={busy} data-testid="pay-now-button"><CreditCard className="h-4 w-4 mr-2" />Pay {rupee(total)}</Button>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
