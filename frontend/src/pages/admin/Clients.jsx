import React, { useEffect, useState } from "react";
import api from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Building2 } from "lucide-react";

export default function Clients() {
  const [rows, setRows] = useState([]);
  useEffect(() => { api.get("/admin/clients").then((r) => setRows(r.data)).catch(() => {}); }, []);
  return (
    <AppShell admin>
      <div className="mb-6"><h1 className="text-2xl font-display">Clients</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">All client organizations on the platform.</p></div>
      <Card className="card-shadow overflow-hidden">
        <Table>
          <TableHeader><TableRow><TableHead>Organization</TableHead><TableHead>Industry</TableHead><TableHead>Employees</TableHead><TableHead>Locations</TableHead><TableHead>Toolkits</TableHead></TableRow></TableHeader>
          <TableBody>
            {rows.length === 0 ? <TableRow><TableCell colSpan={5} className="text-center py-8 text-sm text-[hsl(var(--muted-foreground))]"><Building2 className="h-6 w-6 mx-auto mb-2" />No clients yet.</TableCell></TableRow> :
              rows.map((o) => (
                <TableRow key={o.id} data-testid={`client-row-${o.id}`}>
                  <TableCell><div className="font-medium">{o.legal_name}</div><div className="text-xs text-[hsl(var(--muted-foreground))]">{o.trade_name}</div></TableCell>
                  <TableCell className="text-sm">{o.industry || "—"}</TableCell>
                  <TableCell className="tabular-nums">{o.employee_count || "—"}</TableCell>
                  <TableCell className="text-sm max-w-[220px] truncate">{o.locations || "—"}</TableCell>
                  <TableCell><Badge variant="secondary">{o.entitlements}</Badge></TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </Card>
    </AppShell>
  );
}
