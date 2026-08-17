import React, { useEffect, useState } from "react";
import api from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { StatusBadge } from "@/components/common/StatusBadge";

export default function Content() {
  const [d, setD] = useState({ standards: [] });
  useEffect(() => { api.get("/admin/dashboard/content").then((r) => setD(r.data)).catch(() => {}); }, []);
  return (
    <AppShell admin>
      <div className="mb-6"><h1 className="text-2xl font-display">Content</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Published standards and toolkit versions.</p></div>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {d.standards.map((s) => (
          <Card key={s.slug} className="card-shadow p-5" data-testid={`content-card-${s.slug}`}>
            <div className="flex items-center justify-between"><div className="font-display font-semibold">{s.name.split("\u2014")[0]}</div><StatusBadge status="published" /></div>
            <div className="mt-3 flex items-center gap-2 text-sm"><Badge variant="outline">v{s.version}</Badge><Badge variant="secondary">{s.document_count} documents</Badge></div>
            <p className="mt-3 text-xs text-[hsl(var(--muted-foreground))]">Toolkit version is locked at time of purchase (immutable entitlement).</p>
          </Card>
        ))}
      </div>
    </AppShell>
  );
}
