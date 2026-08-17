import React, { useCallback, useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/common/StatusBadge";
import { toast } from "sonner";
import { ArrowLeft, Check, X, MessageSquareWarning, Cog, Rocket, FileText } from "lucide-react";

export default function ReviewDetail() {
  const { id } = useParams();
  const nav = useNavigate();
  const [data, setData] = useState(null);
  const [comment, setComment] = useState("");
  const [busy, setBusy] = useState(false);

  const load = useCallback(() => api.get(`/admin/reviews/${id}`).then((r) => setData(r.data)).catch(() => {}), [id]);
  useEffect(() => { load(); }, [load]);

  if (!data) return <AppShell admin><div className="text-[hsl(var(--muted-foreground))]">Loading…</div></AppShell>;
  const { submission: s, org, schema } = data;

  const act = async (fn, msg) => { setBusy(true); try { await fn(); toast.success(msg); await load(); } catch (e) { toast.error(e?.response?.data?.detail || "Action failed"); } finally { setBusy(false); } };
  const approve = () => act(() => api.post(`/admin/reviews/${id}/approve`), "Onboarding approved");
  const reject = () => act(() => api.post(`/admin/reviews/${id}/reject`, { comment }), "Submission rejected");
  const requestCorrection = () => { if (!comment) return toast.error("Add a comment"); act(() => api.post(`/admin/reviews/${id}/request-correction`, { comment }), "Correction requested"); };
  const generate = () => act(async () => { const { data: res } = await api.post(`/admin/generate/${id}`); if (res.status === "generation_failed") throw new Error("Generation failed validation"); }, "Documents generated");
  const publish = () => act(() => api.post(`/admin/publish/${id}`), "Published to client");

  return (
    <AppShell admin>
      <button onClick={() => nav("/admin/reviews")} className="inline-flex items-center gap-1 text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))] mb-4"><ArrowLeft className="h-4 w-4" />Back to queue</button>
      <div className="flex flex-wrap items-start justify-between gap-3 mb-4">
        <div><h1 className="text-2xl font-display">{org?.legal_name}</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">{s.standard_slug} · {s.completion}% complete</p></div>
        <div className="flex items-center gap-2"><StatusBadge status={s.status} />{s.generation_status && <StatusBadge status={s.generation_status} />}</div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          {schema.sections.map((sec) => (
            <Card key={sec.id} className="card-shadow p-4">
              <h3 className="font-display font-medium mb-2">Section {sec.id}: {sec.title}</h3>
              <div className="grid sm:grid-cols-2 gap-x-6 gap-y-2 text-sm">
                {sec.questions.map((q) => {
                  const v = s.answers?.[q.id];
                  if (v === undefined || v === "" || (Array.isArray(v) && v.length === 0)) return null;
                  return (<div key={q.id}><div className="text-xs text-[hsl(var(--muted-foreground))]">{q.label}</div><div className="font-medium break-words">{Array.isArray(v) ? v.join(", ") : String(v)}</div></div>);
                })}
              </div>
            </Card>
          ))}
        </div>

        <div className="space-y-4">
          <Card className="card-shadow p-4 sticky top-24">
            <h3 className="font-display font-medium mb-3">Verification actions</h3>
            <Textarea placeholder="Comment / correction note…" value={comment} onChange={(e) => setComment(e.target.value)} data-testid="review-comment" className="mb-3" />
            {s.status !== "approved" && (
              <div className="grid grid-cols-1 gap-2">
                <Button onClick={approve} disabled={busy} data-testid="approve-button"><Check className="h-4 w-4 mr-1" />Approve onboarding</Button>
                <Button variant="outline" onClick={requestCorrection} disabled={busy} data-testid="request-correction-button"><MessageSquareWarning className="h-4 w-4 mr-1" />Request correction</Button>
                <Button variant="outline" onClick={reject} disabled={busy} data-testid="reject-button"><X className="h-4 w-4 mr-1" />Reject</Button>
              </div>
            )}
            {s.status === "approved" && (
              <div className="grid grid-cols-1 gap-2">
                <Button onClick={generate} disabled={busy} data-testid="generate-button"><Cog className="h-4 w-4 mr-1" />{s.generation_status ? "Regenerate documents" : "Generate documents"}</Button>
                {s.generation_status === "generated" && <Button variant="outline" onClick={publish} disabled={busy} data-testid="publish-button"><Rocket className="h-4 w-4 mr-1" />Publish to client</Button>}
                {s.generation_status && <div className="flex items-center gap-2 text-sm text-[hsl(var(--success-fg))]"><FileText className="h-4 w-4" />Documents generated</div>}
              </div>
            )}
          </Card>
          {(s.comments || []).length > 0 && (
            <Card className="card-shadow p-4"><h3 className="font-display font-medium mb-2">Comments</h3><div className="space-y-2">{s.comments.map((c) => (<div key={c.id} className="text-sm border-l-2 pl-2 border-[hsl(var(--border))]"><div>{c.text}</div><div className="text-xs text-[hsl(var(--muted-foreground))]">{c.by} · {new Date(c.at).toLocaleString("en-IN")}</div></div>))}</div></Card>
          )}
        </div>
      </div>
    </AppShell>
  );
}
