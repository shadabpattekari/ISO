import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api, { rupee } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Building2, FileText, ShieldCheck, Download, ArrowRight, Package, ShoppingCart } from "lucide-react";

const Kpi = ({ icon: Icon, label, value, sub }) => (
  <Card className="card-shadow p-4">
    <div className="flex items-center gap-2 text-[hsl(var(--muted-foreground))] text-xs uppercase tracking-wide"><Icon className="h-4 w-4" />{label}</div>
    <div className="mt-2 font-display text-2xl font-semibold tabular-nums">{value}</div>
    {sub && <div className="mt-1 text-xs text-[hsl(var(--muted-foreground))]">{sub}</div>}
  </Card>
);

export default function ClientDashboard() {
  const { user, org } = useAuth();
  const nav = useNavigate();
  const [ents, setEnts] = useState([]);
  const [subs, setSubs] = useState({});
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    (async () => {
      const e = await api.get("/entitlements").then((r) => r.data).catch(() => []);
      setEnts(e);
      const o = await api.get("/orders").then((r) => r.data).catch(() => []);
      setOrders(o);
      const map = {};
      for (const ent of e) {
        const s = await api.get(`/onboarding/submission/${ent.standard_slug}`).then((r) => r.data).catch(() => null);
        if (s) map[ent.standard_slug] = s;
      }
      setSubs(map);
    })();
  }, []);

  const primary = ents[0];
  const primarySub = primary ? subs[primary.standard_slug] : null;

  return (
    <AppShell>
      <div className="mb-6">
        <h1 className="text-2xl font-display">Welcome{user?.name ? `, ${user.name.split(" ")[0]}` : ""}</h1>
        <p className="text-sm text-[hsl(var(--muted-foreground))]">{org ? org.legal_name : "Set up your organization to get started."}</p>
      </div>

      {!org && (
        <Card className="card-shadow p-6 mb-6 bg-[hsl(var(--secondary))]/50">
          <div className="flex items-center gap-3"><Building2 className="h-6 w-6 text-[hsl(var(--primary))]" /><div><div className="font-medium">Create your organization profile</div><div className="text-sm text-[hsl(var(--muted-foreground))]">Add your legal name, logo and details — they brand every document.</div></div></div>
          <Button className="mt-4" onClick={() => nav("/app/organization")} data-testid="setup-org-button">Set up organization <ArrowRight className="ml-1 h-4 w-4" /></Button>
        </Card>
      )}

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Kpi icon={Package} label="Toolkits" value={ents.length} sub="Active entitlements" />
        <Kpi icon={FileText} label="Onboarding" value={`${primarySub?.completion || 0}%`} sub={primary?.standard_name?.split("\u2014")[0] || "—"} />
        <Kpi icon={ShieldCheck} label="Review" value={<StatusBadge status={primarySub?.status || "draft"} />} />
        <Kpi icon={Download} label="Documents" value={<StatusBadge status={primarySub?.generation_status || "waiting"} />} />
      </div>

      <div className="grid lg:grid-cols-3 gap-6 mt-6">
        <Card className="card-shadow p-5 lg:col-span-2">
          <h2 className="font-display text-lg mb-4">Your toolkits</h2>
          {ents.length === 0 ? (
            <div className="text-center py-8">
              <ShoppingCart className="h-8 w-8 mx-auto text-[hsl(var(--muted-foreground))]" />
              <p className="mt-2 text-sm text-[hsl(var(--muted-foreground))]">No toolkits yet.</p>
              <Button className="mt-3" variant="outline" onClick={() => nav("/")}>Browse catalogue</Button>
            </div>
          ) : (
            <div className="space-y-3">
              {ents.map((e) => {
                const s = subs[e.standard_slug];
                return (
                  <div key={e.id} className="flex items-center justify-between gap-4 border rounded-lg p-3" data-testid={`ent-row-${e.standard_slug}`}>
                    <div className="min-w-0">
                      <div className="font-medium truncate">{e.standard_name}</div>
                      <div className="mt-1 flex items-center gap-2">
                        <StatusBadge status={s?.status || "draft"} />
                        {s?.generation_status && <StatusBadge status={s.generation_status} />}
                      </div>
                      <div className="mt-2 w-40"><Progress value={s?.completion || 0} className="h-1.5" /></div>
                    </div>
                    <div className="flex flex-col gap-2 shrink-0">
                      {s?.generation_status ? (
                        <Button size="sm" onClick={() => nav("/app/downloads")} data-testid={`download-cta-${e.standard_slug}`}><Download className="h-4 w-4 mr-1" />Downloads</Button>
                      ) : (
                        <Button size="sm" onClick={() => nav(`/app/onboarding/${e.standard_slug}`)} data-testid={`onboard-cta-${e.standard_slug}`}>{s?.status === "changes_requested" ? "Fix & resubmit" : "Continue onboarding"}</Button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </Card>

        <Card className="card-shadow p-5">
          <h2 className="font-display text-lg mb-4">Recent orders</h2>
          {orders.length === 0 ? <p className="text-sm text-[hsl(var(--muted-foreground))]">No orders yet.</p> : (
            <div className="space-y-3">
              {orders.slice(0, 5).map((o) => (
                <div key={o.id} className="flex items-center justify-between text-sm">
                  <div className="min-w-0"><div className="truncate">{o.standard_name?.split("\u2014")[0]}</div><div className="font-mono text-xs text-[hsl(var(--muted-foreground))]">{rupee(o.amount)}</div></div>
                  <StatusBadge status={o.status} />
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </AppShell>
  );
}
