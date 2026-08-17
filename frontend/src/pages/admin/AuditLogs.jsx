import React, { useEffect, useState } from "react";
import api from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);
  useEffect(() => { api.get("/admin/audit-logs").then((r) => setLogs(r.data)).catch(() => {}); }, []);
  return (
    <AppShell admin>
      <div className="mb-6"><h1 className="text-2xl font-display">Audit logs</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Security and operational events.</p></div>
      <Card className="card-shadow overflow-hidden">
        <Table>
          <TableHeader><TableRow><TableHead>Action</TableHead><TableHead>Actor</TableHead><TableHead>Details</TableHead><TableHead>Time</TableHead></TableRow></TableHeader>
          <TableBody>
            {logs.length === 0 ? <TableRow><TableCell colSpan={4} className="text-center py-8 text-sm text-[hsl(var(--muted-foreground))]">No events yet.</TableCell></TableRow> :
              logs.map((l) => (
                <TableRow key={l.id} data-testid={`audit-row-${l.id}`}>
                  <TableCell><Badge variant="outline" className="font-mono text-xs">{l.action}</Badge></TableCell>
                  <TableCell className="text-sm">{l.actor_role || "—"}</TableCell>
                  <TableCell className="text-xs font-mono max-w-[280px] truncate">{JSON.stringify(l.meta || {})}</TableCell>
                  <TableCell className="text-xs">{new Date(l.at).toLocaleString("en-IN")}</TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </Card>
    </AppShell>
  );
}
