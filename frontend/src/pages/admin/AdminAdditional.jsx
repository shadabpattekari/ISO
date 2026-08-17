import React, { useEffect, useState } from "react";
import api, { rupee } from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { toast } from "sonner";

export default function AdminAdditional() {
  const [items, setItems] = useState([]);
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(null);
  const [q, setQ] = useState({ amount: 2999, description: "" });
  const load = () => api.get("/admin/additional-requirements").then((r) => setItems(r.data)).catch(() => {});
  useEffect(() => { load(); }, []);

  const openQuote = (it) => { setActive(it); setQ({ amount: 2999, description: "" }); setOpen(true); };
  const submitQuote = async () => { await api.post(`/admin/additional-requirements/${active.id}/quote`, { amount: Number(q.amount), description: q.description }); toast.success("Quotation sent"); setOpen(false); load(); };

  return (
    <AppShell admin>
      <div className="mb-6"><h1 className="text-2xl font-display">Additional requests</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Review requests and issue quotations.</p></div>
      {items.length === 0 ? <Card className="card-shadow p-10 text-center text-sm text-[hsl(var(--muted-foreground))]">No requests yet.</Card> : (
        <div className="space-y-3">
          {items.map((it) => (
            <Card key={it.id} className="card-shadow p-4" data-testid={`admin-addl-${it.id}`}>
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0"><div className="font-medium">{it.title}</div><div className="text-xs text-[hsl(var(--muted-foreground))]">{it.org_name} · {it.category}</div><p className="mt-1 text-sm">{it.description}</p>{it.quotation && <div className="mt-2 text-sm">Quoted: <b>{rupee(it.quotation.amount)}</b></div>}</div>
                <div className="flex flex-col items-end gap-2"><StatusBadge status={it.status} />{it.status === "submitted" && <Button size="sm" onClick={() => openQuote(it)} data-testid={`quote-button-${it.id}`}>Create quotation</Button>}</div>
              </div>
            </Card>
          ))}
        </div>
      )}
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader><DialogTitle>Create quotation</DialogTitle></DialogHeader>
          <div className="space-y-3">
            <div><Label>Amount (INR)</Label><Input type="number" value={q.amount} onChange={(e) => setQ((s) => ({ ...s, amount: e.target.value }))} data-testid="quote-amount" /></div>
            <div><Label>Description</Label><Textarea value={q.description} onChange={(e) => setQ((s) => ({ ...s, description: e.target.value }))} data-testid="quote-description" /></div>
          </div>
          <DialogFooter><Button onClick={submitQuote} data-testid="send-quote-button">Send quotation</Button></DialogFooter>
        </DialogContent>
      </Dialog>
    </AppShell>
  );
}
