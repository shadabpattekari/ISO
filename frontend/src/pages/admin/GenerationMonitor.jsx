import React, { useEffect, useState } from "react";
import api from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export default function GenerationMonitor() {
  const [jobs, setJobs] = useState([]);
  useEffect(() => { api.get("/admin/jobs").then((r) => setJobs(r.data)).catch(() => {}); }, []);
  return (
    <AppShell admin>
      <div className="mb-6"><h1 className="text-2xl font-display">Generation monitor</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Document generation jobs and validation results.</p></div>
      <Card className="card-shadow overflow-hidden">
        <Table>
          <TableHeader><TableRow><TableHead>Job ID</TableHead><TableHead>Standard</TableHead><TableHead>Status</TableHead><TableHead>Artifacts</TableHead><TableHead>Created</TableHead></TableRow></TableHeader>
          <TableBody>
            {jobs.length === 0 ? <TableRow><TableCell colSpan={5} className="text-center py-8 text-sm text-[hsl(var(--muted-foreground))]">No generation jobs yet.</TableCell></TableRow> :
              jobs.map((j) => {
                const errs = (j.validation || []).filter((v) => !v.ok);
                return (
                  <TableRow key={j.id} data-testid={`job-row-${j.id}`}>
                    <TableCell className="font-mono text-xs">{j.id.slice(0, 8)}</TableCell>
                    <TableCell className="text-sm">{j.standard_slug}</TableCell>
                    <TableCell><StatusBadge status={j.status} />{errs.length > 0 && <div className="text-xs text-[hsl(var(--danger-fg))] mt-1">{errs.length} validation errors</div>}</TableCell>
                    <TableCell className="tabular-nums">{j.artifact_count || "—"}</TableCell>
                    <TableCell className="text-xs">{new Date(j.created_at).toLocaleString("en-IN")}</TableCell>
                  </TableRow>
                );
              })}
          </TableBody>
        </Table>
      </Card>
    </AppShell>
  );
}
