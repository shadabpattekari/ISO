import React, { useEffect, useState } from "react";
import api from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { toast } from "sonner";
import { Upload, Save } from "lucide-react";

const INDUSTRIES = ["Information Technology","SaaS","Cybersecurity","Professional Consulting","Healthcare","Financial Services","Manufacturing","Education","E-commerce and Retail","Logistics"];

export default function OrgProfile() {
  const { org, refresh } = useAuth();
  const [f, setF] = useState({ legal_name:"", trade_name:"", website:"", industry:"", employee_count:"", registered_address:"", locations:"", primary_contact:"", contact_email:"", contact_mobile:"", gstin:"", registration_number:"", products_services:"", logo_base64:"" });
  const [busy, setBusy] = useState(false);
  const set = (k) => (e) => setF((s) => ({ ...s, [k]: e?.target ? e.target.value : e }));

  useEffect(() => { if (org) setF((s) => ({ ...s, ...org })); }, [org]);

  const onLogo = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 1024 * 1024) return toast.error("Logo must be under 1MB");
    const reader = new FileReader();
    reader.onload = () => setF((s) => ({ ...s, logo_base64: reader.result }));
    reader.readAsDataURL(file);
  };

  const save = async () => {
    if (!f.legal_name || !f.trade_name) return toast.error("Legal name and trade name are required");
    setBusy(true);
    try {
      if (org) await api.put("/org", f); else await api.post("/org", f);
      await refresh();
      toast.success("Organization saved");
    } catch (e) { toast.error(e?.response?.data?.detail || "Save failed"); } finally { setBusy(false); }
  };

  const Field = ({ label, k, type, ph, area }) => (
    <div>
      <Label>{label}</Label>
      {area ? <Textarea value={f[k]||""} onChange={set(k)} placeholder={ph} data-testid={`org-${k}`} />
            : <Input type={type||"text"} value={f[k]||""} onChange={set(k)} placeholder={ph} data-testid={`org-${k}`} />}
    </div>
  );

  return (
    <AppShell>
      <div className="mb-6"><h1 className="text-2xl font-display">Organization profile</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">This information brands your generated documents.</p></div>
      <div className="grid lg:grid-cols-3 gap-6">
        <Card className="card-shadow p-5 lg:col-span-2">
          <div className="grid sm:grid-cols-2 gap-4">
            <Field label="Legal entity name *" k="legal_name" ph="Acme Technologies Private Limited" />
            <Field label="Trade / brand name *" k="trade_name" ph="Acme" />
            <Field label="Website" k="website" ph="acme.io" />
            <div><Label>Industry</Label>
              <Select value={f.industry||""} onValueChange={set("industry")}>
                <SelectTrigger data-testid="org-industry"><SelectValue placeholder="Select industry" /></SelectTrigger>
                <SelectContent>{INDUSTRIES.map((i) => <SelectItem key={i} value={i}>{i}</SelectItem>)}</SelectContent>
              </Select>
            </div>
            <Field label="Employee count" k="employee_count" type="number" ph="35" />
            <Field label="GSTIN" k="gstin" ph="22AAAAA0000A1Z5" />
            <Field label="CIN / Registration number" k="registration_number" />
            <Field label="Primary contact" k="primary_contact" />
            <Field label="Contact email" k="contact_email" type="email" />
            <Field label="Contact mobile" k="contact_mobile" />
          </div>
          <div className="mt-4 grid gap-4">
            <Field label="Registered address" k="registered_address" area ph="Full registered address" />
            <Field label="Operating locations (comma separated)" k="locations" ph="Bengaluru HQ, Pune Office" />
            <Field label="Products and services" k="products_services" area ph="Describe what you offer" />
          </div>
          <Button className="mt-5" onClick={save} disabled={busy} data-testid="save-org-button"><Save className="h-4 w-4 mr-1" />Save organization</Button>
        </Card>

        <Card className="card-shadow p-5">
          <Label>Organization logo</Label>
          <div className="mt-2 flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-6 text-center">
            {f.logo_base64 ? <img src={f.logo_base64} alt="logo" className="h-24 w-24 object-contain rounded" /> : <Upload className="h-8 w-8 text-[hsl(var(--muted-foreground))]" />}
            <label className="mt-3 cursor-pointer">
              <span className="text-sm text-[hsl(var(--teal))] font-medium">{f.logo_base64 ? "Change logo" : "Upload logo"}</span>
              <input type="file" accept="image/png,image/jpeg" className="hidden" onChange={onLogo} data-testid="org-logo-input" />
            </label>
            <p className="mt-1 text-xs text-[hsl(var(--muted-foreground))]">PNG or JPG, under 1MB</p>
          </div>
        </Card>
      </div>
    </AppShell>
  );
}
