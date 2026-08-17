import React, { useEffect, useState } from "react";
import api, { rupee } from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { toast } from "sonner";
import { PlusCircle } from "lucide-react";

const CATEGORIES = ["New policy","New SOP","New register","Client-specific format","Sector-specific compliance document","Additional location","Additional legal entity","Combined ISO documentation","Existing document review","Manual consultant review","Major scope change"];

export default function AdditionalRequirements() {
  const [items, setItems] = useState([]);
  const [open, setOpen] = useState(false);
  const [f, setF] = useState({ title: "", description: "", category: CATEGORIES[0] });
  const [busy, setBusy] = useState(false);

  const load = () => api.get("/additional-requirements").then((r) => setItems(r.data)).catch(() => {});
  useEffect(() => { load(); }, []);

  const submit = async () => {
    if (!f.title || !f.description) return toast.error("Title and description required");
    setBusy(true);
    try { await api.post("/additional-requirements", f); toast.success("Request submitted"); setOpen(false); setF({ title: "", description: "", category: CATEGORIES[0] }); load(); }
    catch { toast.error("Failed"); } finally { setBusy(false); }
  };

  const respond = async (id, accept) => { await api.post(`/additional-requirements/${id}/respond`, { accept }); toast.success(accept ? "Quotation accepted" : "Quotation rejected"); load(); };
  const pay = async (id) => { await api.post(`/additional-requirements/${id}/pay`); toast.success("Payment complete"); load(); };

  return (
    <AppShell>
      <div className="mb-6 flex items-center justify-between">
        <div><h1 className="text-2xl font-display">Additional requests</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Request extra documents or customizations — quoted and delivered by FaizZab.</p></div>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger asChild><Button data-testid="new-request-button"><PlusCircle className="h-4 w-4 mr-1" />New request</Button></DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>New additional requirement</DialogTitle></DialogHeader>
            <div className="space-y-3">
              <div><Label>Category</Label>
                <Select value={f.category} onValueChange={(v) => setF((s) => ({ ...s, category: v }))}><SelectTrigger data-testid="req-category"><SelectValue /></SelectTrigger><SelectContent>{CATEGORIES.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent></Select>
              </div>
              <div><Label>Title</Label><Input value={f.title} onChange={(e) => setF((s) => ({ ...s, title: e.target.value }))} data-testid="req-title" /></div>
              <div><Label>Description</Label><Textarea value={f.description} onChange={(e) => setF((s) => ({ ...s, description: e.target.value }))} data-testid="req-description" /></div>
            </div>
            <DialogFooter><Button onClick={submit} disabled={busy} data-testid="submit-request-button">Submit request</Button></DialogFooter>
          </DialogContent>
        </Dialog>
      </div>

      {items.length === 0 ? <Card className="card-shadow p-10 text-center text-sm text-[hsl(var(--muted-foreground))]">No additional requests yet.</Card> : (
        <div className="space-y-3">
          {items.map((it) => (
            <Card key={it.id} className="card-shadow p-4" data-testid={`addl-row-${it.id}`}>
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0"><div className="font-medium">{it.title}</div><div className="text-xs text-[hsl(var(--muted-foreground))]">{it.category}</div><p className="mt-1 text-sm">{it.description}</p></div>
                <StatusBadge status={it.status} />
              </div>
              {it.quotation && (
                <div className="mt-3 border-t pt-3 flex flex-wrap items-center justify-between gap-3">
                  <div className="text-sm"><span className="text-[hsl(var(--muted-foreground))]">Quotation:</span> <b>{rupee(it.quotation.amount)}</b> — {it.quotation.description}</div>
                  <div className="flex gap-2">
                    {it.status === "quoted" && <><Button size="sm" onClick={() => respond(it.id, true)} data-testid={`accept-quote-${it.id}`}>Accept</Button><Button size="sm" variant="outline" onClick={() => respond(it.id, false)}>Reject</Button></>}
                    {it.status === "accepted" && <Button size="sm" onClick={() => pay(it.id)} data-testid={`pay-quote-${it.id}`}>Pay {rupee(it.quotation.amount)}</Button>}
                  </div>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}
    </AppShell>
  );
}
