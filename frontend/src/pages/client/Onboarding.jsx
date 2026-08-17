import React, { useEffect, useMemo, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { Switch } from "@/components/ui/switch";
import { Progress } from "@/components/ui/progress";
import { StatusBadge } from "@/components/common/StatusBadge";
import { toast } from "sonner";
import { Save, Send, CheckCircle2, AlertTriangle, ChevronLeft, ChevronRight, MessageSquare } from "lucide-react";

const truthy = (v) => v === true || v === "true" || v === "yes";

export default function Onboarding() {
  const { slug: routeSlug } = useParams();
  const nav = useNavigate();
  const [ents, setEnts] = useState([]);
  const [slug, setSlug] = useState(routeSlug || null);
  const [schema, setSchema] = useState(null);
  const [answers, setAnswers] = useState({});
  const [sub, setSub] = useState(null);
  const [active, setActive] = useState(0);
  const [declaration, setDeclaration] = useState(false);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    api.get("/entitlements").then((r) => {
      setEnts(r.data);
      if (!slug && r.data[0]) setSlug(r.data[0].standard_slug);
    });
  }, []); // eslint-disable-line

  const load = useCallback(async (s) => {
    if (!s) return;
    const sch = await api.get(`/onboarding/schema/${s}`).then((r) => r.data);
    setSchema(sch);
    const existing = await api.get(`/onboarding/submission/${s}`).then((r) => r.data).catch(() => null);
    if (existing) { setSub(existing); setAnswers(existing.answers || {}); setDeclaration(!!existing.declaration); }
    else { setSub(null); setAnswers({}); setDeclaration(false); }
    setActive(0);
  }, []);

  useEffect(() => { if (slug) load(slug); }, [slug, load]);

  const visibleQuestions = (sec) => sec.questions.filter((q) => {
    if (!q.show_if) return true;
    return q.show_if.in.map(String).includes(String(answers[q.show_if.field]));
  });

  const sectionComplete = (sec) => {
    const req = visibleQuestions(sec).filter((q) => q.required);
    return req.every((q) => String(answers[q.id] ?? "").trim() !== "" && String(answers[q.id]) !== "[]");
  };

  const completion = useMemo(() => {
    if (!schema) return 0;
    let req = [], filled = 0;
    schema.sections.forEach((sec) => visibleQuestions(sec).filter((q) => q.required).forEach((q) => {
      req.push(q.id);
      const v = answers[q.id];
      if (v !== undefined && v !== null && String(v).trim() !== "" && String(v) !== "[]") filled++;
    }));
    return req.length ? Math.round((filled / req.length) * 100) : 0;
  }, [schema, answers]); // eslint-disable-line

  const setAns = (id, v) => setAnswers((s) => ({ ...s, [id]: v }));

  const saveDraft = async () => {
    setBusy(true);
    try { const { data } = await api.post("/onboarding/draft", { standard_slug: slug, answers }); setSub(data); toast.success("Draft saved"); }
    catch (e) { toast.error(e?.response?.data?.detail || "Save failed"); } finally { setBusy(false); }
  };

  const submit = async () => {
    if (!declaration) return toast.error("Please accept the declaration");
    setBusy(true);
    try { const { data } = await api.post("/onboarding/submit", { standard_slug: slug, answers, declaration }); setSub(data); toast.success("Submitted for verification"); nav("/app"); }
    catch (e) { toast.error(e?.response?.data?.detail || "Submission incomplete"); } finally { setBusy(false); }
  };

  if (!slug) return <AppShell><Card className="card-shadow p-8 text-center"><p className="text-sm text-[hsl(var(--muted-foreground))]">No toolkit purchased yet.</p><Button className="mt-3" onClick={() => nav("/")}>Browse catalogue</Button></Card></AppShell>;
  if (!schema) return <AppShell><div className="text-[hsl(var(--muted-foreground))]">Loading questionnaire…</div></AppShell>;

  const readonly = sub?.status === "submitted" || sub?.status === "approved";
  const isLast = active === schema.sections.length;
  const sec = schema.sections[active];

  const renderQ = (q) => {
    const v = answers[q.id] ?? (q.type === "multiselect" ? [] : q.type === "boolean" ? false : "");
    const common = { "data-testid": `q-${q.id}`, disabled: readonly };
    switch (q.type) {
      case "textarea": return <Textarea value={v} onChange={(e) => setAns(q.id, e.target.value)} placeholder={q.placeholder} {...common} />;
      case "number": return <Input type="number" value={v} onChange={(e) => setAns(q.id, e.target.value)} placeholder={q.placeholder} {...common} />;
      case "email": return <Input type="email" value={v} onChange={(e) => setAns(q.id, e.target.value)} placeholder={q.placeholder} {...common} />;
      case "select": return (
        <Select value={v} onValueChange={(val) => setAns(q.id, val)} disabled={readonly}>
          <SelectTrigger data-testid={`q-${q.id}`}><SelectValue placeholder="Select…" /></SelectTrigger>
          <SelectContent>{q.options.map((o) => <SelectItem key={o} value={o}>{o}</SelectItem>)}</SelectContent>
        </Select>
      );
      case "multiselect": return (
        <div className="grid sm:grid-cols-2 gap-2">
          {q.options.map((o) => {
            const arr = Array.isArray(v) ? v : [];
            const on = arr.includes(o);
            return (
              <label key={o} className="flex items-center gap-2 rounded-md border p-2 text-sm cursor-pointer">
                <Checkbox checked={on} disabled={readonly} onCheckedChange={(c) => setAns(q.id, c ? [...arr, o] : arr.filter((x) => x !== o))} data-testid={`q-${q.id}-${o}`} />
                {o}
              </label>
            );
          })}
        </div>
      );
      case "boolean": return (
        <div className="flex items-center gap-2"><Switch checked={truthy(v)} disabled={readonly} onCheckedChange={(c) => setAns(q.id, c)} data-testid={`q-${q.id}`} /><span className="text-sm text-[hsl(var(--muted-foreground))]">{truthy(v) ? "Yes" : "No"}</span></div>
      );
      default: return <Input value={v} onChange={(e) => setAns(q.id, e.target.value)} placeholder={q.placeholder} {...common} />;
    }
  };

  return (
    <AppShell>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-display">Guided onboarding</h1>
          <p className="text-sm text-[hsl(var(--muted-foreground))]">Answer questions to generate your organization-specific documents.</p>
        </div>
        <div className="flex items-center gap-3">
          {ents.length > 1 && (
            <Select value={slug} onValueChange={setSlug}>
              <SelectTrigger className="w-56" data-testid="onboarding-standard-select"><SelectValue /></SelectTrigger>
              <SelectContent>{ents.map((e) => <SelectItem key={e.standard_slug} value={e.standard_slug}>{e.standard_name.split("—")[0]}</SelectItem>)}</SelectContent>
            </Select>
          )}
          {sub && <StatusBadge status={sub.status} />}
        </div>
      </div>

      {sub?.status === "changes_requested" && (
        <Card className="card-shadow p-4 mb-4 bg-[hsl(var(--warning-bg))] text-[hsl(var(--warning-fg))]">
          <div className="flex items-center gap-2 font-medium"><AlertTriangle className="h-4 w-4" />Corrections requested</div>
          <div className="mt-2 space-y-1 text-sm">
            {(sub.comments || []).filter((c) => c.type === "correction" || c.text).map((c) => (
              <div key={c.id} className="flex gap-2"><MessageSquare className="h-3.5 w-3.5 mt-0.5" /><span>{c.text}{c.section_id ? ` (Section ${c.section_id})` : ""}</span></div>
            ))}
          </div>
        </Card>
      )}

      <div className="grid lg:grid-cols-4 gap-6">
        {/* Stepper */}
        <div className="lg:col-span-1">
          <Card className="card-shadow p-4 sticky top-24">
            <div className="flex items-center justify-between text-sm mb-2"><span className="font-medium">Progress</span><span className="tabular-nums">{completion}%</span></div>
            <Progress value={completion} className="h-2 mb-4" />
            <div className="space-y-1">
              {schema.sections.map((s, i) => (
                <button key={s.id} onClick={() => setActive(i)} data-testid={`step-${s.id}`}
                  className={`w-full flex items-center gap-2 rounded-md px-2.5 py-2 text-sm text-left transition-colors ${active === i ? "bg-[hsl(var(--primary))] text-white" : "hover:bg-[hsl(var(--accent))]"}`}>
                  <span className={`flex h-5 w-5 items-center justify-center rounded-full text-[10px] shrink-0 ${sectionComplete(s) ? "bg-[hsl(var(--teal))] text-white" : active === i ? "bg-white/25" : "bg-[hsl(var(--muted))]"}`}>
                    {sectionComplete(s) ? <CheckCircle2 className="h-3.5 w-3.5" /> : s.id}
                  </span>
                  <span className="truncate">{s.title}</span>
                </button>
              ))}
              <button onClick={() => setActive(schema.sections.length)} data-testid="step-declaration"
                className={`w-full flex items-center gap-2 rounded-md px-2.5 py-2 text-sm text-left transition-colors ${isLast ? "bg-[hsl(var(--primary))] text-white" : "hover:bg-[hsl(var(--accent))]"}`}>
                <span className="flex h-5 w-5 items-center justify-center rounded-full text-[10px] bg-[hsl(var(--muted))]">✓</span>Declaration &amp; submit
              </button>
            </div>
          </Card>
        </div>

        {/* Form */}
        <div className="lg:col-span-3">
          <Card className="card-shadow p-5">
            {!isLast ? (
              <>
                <div className="mb-4"><h2 className="font-display text-lg">{sec.title}</h2><p className="text-sm text-[hsl(var(--muted-foreground))]">{sec.why}</p></div>
                <div className="space-y-4">
                  {visibleQuestions(sec).map((q) => (
                    <div key={q.id}>
                      <Label>{q.label}{q.required && <span className="text-[hsl(var(--danger-fg))]"> *</span>}</Label>
                      <div className="mt-1">{renderQ(q)}</div>
                      {q.help && <p className="mt-1 text-xs text-[hsl(var(--muted-foreground))]">{q.help}</p>}
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <>
                <h2 className="font-display text-lg mb-3">Declaration</h2>
                <p className="text-sm text-[hsl(var(--muted-foreground))] mb-4">Before submitting for FaizZab verification, please confirm:</p>
                <ul className="space-y-2 text-sm mb-4">
                  {["The information provided is complete and accurate.","Authorized persons have approved this information.","Generated documents require implementation to be effective.","Legal and regulatory obligations require independent validation.","This toolkit does not guarantee certification."].map((x) => (
                    <li key={x} className="flex items-start gap-2"><CheckCircle2 className="h-4 w-4 text-[hsl(var(--teal))] mt-0.5" />{x}</li>
                  ))}
                </ul>
                <label className="flex items-center gap-2 rounded-md border p-3 cursor-pointer">
                  <Checkbox checked={declaration} disabled={readonly} onCheckedChange={setDeclaration} data-testid="declaration-checkbox" />
                  <span className="text-sm">I confirm the above declaration on behalf of my organization.</span>
                </label>
              </>
            )}

            {/* Nav actions */}
            <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t pt-4">
              <div className="flex gap-2">
                <Button variant="outline" size="sm" disabled={active === 0} onClick={() => setActive((a) => Math.max(0, a - 1))} data-testid="prev-section-button"><ChevronLeft className="h-4 w-4" />Back</Button>
                {!isLast && <Button variant="outline" size="sm" onClick={() => setActive((a) => a + 1)} data-testid="next-section-button">Next<ChevronRight className="h-4 w-4" /></Button>}
              </div>
              <div className="flex gap-2">
                {!readonly && <Button variant="secondary" onClick={saveDraft} disabled={busy} data-testid="save-draft-button"><Save className="h-4 w-4 mr-1" />Save draft</Button>}
                {isLast && !readonly && <Button onClick={submit} disabled={busy} data-testid="submit-onboarding-button"><Send className="h-4 w-4 mr-1" />Submit for verification</Button>}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </AppShell>
  );
}
