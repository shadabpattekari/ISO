import React, { useEffect, useState } from "react";
import api, { rupee } from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Receipt } from "lucide-react";

export default function Invoices() {
  const [invoices, setInvoices] = useState([]);
  useEffect(() => { api.get("/invoices").then((r) => setInvoices(r.data)).catch(() => {}); }, []);
  return (
    <AppShell>
      <div className="mb-6"><h1 className="text-2xl font-display">Invoices</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Receipts for your purchases.</p></div>
      <Card className="card-shadow">
        {invoices.length === 0 ? <div className="p-8 text-center text-sm text-[hsl(var(--muted-foreground))]"><Receipt className="h-8 w-8 mx-auto mb-2" />No invoices yet.</div> : (
          <Table>
            <TableHeader><TableRow><TableHead>Invoice #</TableHead><TableHead>Date</TableHead><TableHead className="text-right">Amount</TableHead></TableRow></TableHeader>
            <TableBody>
              {invoices.map((i) => (
                <TableRow key={i.id} data-testid={`invoice-row-${i.number}`}>
                  <TableCell className="font-mono text-xs">{i.number}</TableCell>
                  <TableCell>{new Date(i.created_at).toLocaleDateString("en-IN")}</TableCell>
                  <TableCell className="text-right tabular-nums">{rupee(i.amount)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Card>
    </AppShell>
  );
}
