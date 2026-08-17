import React, { useEffect, useState } from "react";
import api, { rupee } from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { toast } from "sonner";

export default function Commerce() {
  const [d, setD] = useState({ orders: [], invoices: [], coupons: [], revenue_by_standard: {} });
  const [c, setC] = useState({ code: "", percent_off: 10 });
  const load = () => api.get("/admin/dashboard/commerce").then((r) => setD(r.data)).catch(() => {});
  useEffect(() => { load(); }, []);
  const addCoupon = async () => { if (!c.code) return toast.error("Enter a code"); await api.post("/admin/coupons", { code: c.code, percent_off: Number(c.percent_off), active: true }); toast.success("Coupon saved"); setC({ code: "", percent_off: 10 }); load(); };

  return (
    <AppShell admin>
      <div className="mb-6"><h1 className="text-2xl font-display">Commerce</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Orders, invoices, coupons and revenue.</p></div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {Object.entries(d.revenue_by_standard).map(([k, v]) => (
          <Card key={k} className="card-shadow p-4"><div className="text-xs text-[hsl(var(--muted-foreground))] truncate">{k.split("\u2014")[0]}</div><div className="mt-1 font-display text-xl font-semibold">{rupee(v)}</div></Card>
        ))}
        {Object.keys(d.revenue_by_standard).length === 0 && <Card className="card-shadow p-4 text-sm text-[hsl(var(--muted-foreground))]">No revenue yet.</Card>}
      </div>
      <Tabs defaultValue="orders">
        <TabsList><TabsTrigger value="orders" data-testid="tab-orders">Orders</TabsTrigger><TabsTrigger value="invoices">Invoices</TabsTrigger><TabsTrigger value="coupons">Coupons</TabsTrigger></TabsList>
        <TabsContent value="orders"><Card className="card-shadow overflow-hidden mt-3"><Table><TableHeader><TableRow><TableHead>Standard</TableHead><TableHead>Amount</TableHead><TableHead>Status</TableHead><TableHead>Date</TableHead></TableRow></TableHeader><TableBody>{d.orders.map((o) => (<TableRow key={o.id}><TableCell className="text-sm">{o.standard_name?.split("\u2014")[0]}</TableCell><TableCell className="tabular-nums">{rupee(o.amount)}</TableCell><TableCell><StatusBadge status={o.status} /></TableCell><TableCell className="text-xs">{new Date(o.created_at).toLocaleDateString("en-IN")}</TableCell></TableRow>))}</TableBody></Table></Card></TabsContent>
        <TabsContent value="invoices"><Card className="card-shadow overflow-hidden mt-3"><Table><TableHeader><TableRow><TableHead>Invoice #</TableHead><TableHead>Amount</TableHead><TableHead>Date</TableHead></TableRow></TableHeader><TableBody>{d.invoices.map((i) => (<TableRow key={i.id}><TableCell className="font-mono text-xs">{i.number}</TableCell><TableCell className="tabular-nums">{rupee(i.amount)}</TableCell><TableCell className="text-xs">{new Date(i.created_at).toLocaleDateString("en-IN")}</TableCell></TableRow>))}</TableBody></Table></Card></TabsContent>
        <TabsContent value="coupons">
          <Card className="card-shadow p-4 mt-3">
            <div className="flex flex-wrap items-end gap-3 mb-4">
              <div><Label>Code</Label><Input value={c.code} onChange={(e) => setC((s) => ({ ...s, code: e.target.value.toUpperCase() }))} placeholder="SAVE15" data-testid="coupon-code-input" /></div>
              <div><Label>% off</Label><Input type="number" className="w-24" value={c.percent_off} onChange={(e) => setC((s) => ({ ...s, percent_off: e.target.value }))} data-testid="coupon-percent-input" /></div>
              <Button onClick={addCoupon} data-testid="save-coupon-button">Save coupon</Button>
            </div>
            <div className="flex flex-wrap gap-2">{d.coupons.map((cp) => (<Badge key={cp.id} variant={cp.active ? "default" : "outline"}>{cp.code} · {cp.percent_off}%</Badge>))}</div>
          </Card>
        </TabsContent>
      </Tabs>
    </AppShell>
  );
}
