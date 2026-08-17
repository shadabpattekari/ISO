import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api, { rupee } from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { Users, IndianRupee, ShoppingCart, ClipboardCheck, AlertTriangle, Package, ArrowRight } from "lucide-react";

const Kpi = ({ icon: Icon, label, value, tone = "" }) => (
  <Card className="card-shadow p-4">
    <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] text-xs uppercase tracking-wide"><Icon className="h-4 w-4" />{label}</div>
    <div className={`mt-2 font-display text-3xl font-semibold tabular-nums ${tone}`}>{value}</div>
  </Card>
);

export default function AdminDashboard() {
  const [d, setD] = useState(null);
  const nav = useNavigate();
  useEffect(() => { api.get("/admin/dashboard/executive").then((r) => setD(r.data)).catch(() => {}); }, []);
  if (!d) return <AppShell admin><div className="text-[hsl(var(--muted-foreground))]">Loading…</div></AppShell>;

  const chartData = (d.most_purchased || []).map(([name, count]) => ({ name: name.split("\u2014")[0].trim().slice(0, 16), count }));

  return (
    <AppShell admin>
      <div className="mb-6"><h1 className="text-2xl font-display">Executive dashboard</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Platform overview.</p></div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Kpi icon={Users} label="Total clients" value={d.total_clients} />
        <Kpi icon={IndianRupee} label="Revenue" value={rupee(d.revenue)} />
        <Kpi icon={ShoppingCart} label="Toolkit sales" value={d.toolkit_sales} />
        <Kpi icon={Package} label="Active entitlements" value={d.active_entitlements} />
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
        <Card className="card-shadow p-4 flex items-center justify-between">
          <div><div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] text-xs uppercase tracking-wide"><ClipboardCheck className="h-4 w-4" />Pending reviews</div><div className="mt-2 font-display text-3xl font-semibold">{d.pending_reviews}</div></div>
          <Button size="sm" variant="outline" onClick={() => nav("/admin/reviews")} data-testid="goto-reviews">Open<ArrowRight className="ml-1 h-4 w-4" /></Button>
        </Card>
        <Kpi icon={AlertTriangle} label="Failed jobs" value={d.failed_jobs} tone={d.failed_jobs ? "text-[hsl(var(--danger-fg))]" : ""} />
        <Kpi icon={Package} label="Pending additional" value={d.pending_additional} />
      </div>
      <Card className="card-shadow p-5 mt-4">
        <h2 className="font-display text-lg mb-4">Most purchased standards</h2>
        {chartData.length === 0 ? <p className="text-sm text-[hsl(var(--muted-foreground))]">No sales yet.</p> : (
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={chartData}><CartesianGrid strokeDasharray="3 3" stroke="#eee" /><XAxis dataKey="name" tick={{ fontSize: 12 }} /><YAxis allowDecimals={false} tick={{ fontSize: 12 }} /><Tooltip /><Bar dataKey="count" fill="#111A4A" radius={[6, 6, 0, 0]} /></BarChart>
          </ResponsiveContainer>
        )}
      </Card>
    </AppShell>
  );
}
