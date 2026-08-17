import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "@/lib/api";
import { AppShell } from "@/components/layout/AppShell";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { StatusBadge } from "@/components/common/StatusBadge";
import { Progress } from "@/components/ui/progress";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowRight } from "lucide-react";

export default function ReviewQueue() {
  const [rows, setRows] = useState([]);
  const [filter, setFilter] = useState("all");
  const nav = useNavigate();
  useEffect(() => { api.get("/admin/reviews").then((r) => setRows(r.data)).catch(() => {}); }, []);
  const filtered = rows.filter((r) => filter === "all" ? true : r.status === filter);

  return (
    <AppShell admin>
      <div className="mb-6"><h1 className="text-2xl font-display">Review queue</h1><p className="text-sm text-[hsl(var(--muted-foreground))]">Verify client onboarding before document generation.</p></div>
      <Tabs value={filter} onValueChange={setFilter} className="mb-4">
        <TabsList>
          <TabsTrigger value="all" data-testid="filter-all">All</TabsTrigger>
          <TabsTrigger value="submitted" data-testid="filter-submitted">Needs review</TabsTrigger>
          <TabsTrigger value="changes_requested">Changes requested</TabsTrigger>
          <TabsTrigger value="approved">Approved</TabsTrigger>
        </TabsList>
      </Tabs>
      <Card className="card-shadow overflow-hidden">
        <Table>
          <TableHeader><TableRow><TableHead>Organization</TableHead><TableHead>Standard</TableHead><TableHead className="w-[140px]">Completion</TableHead><TableHead>Status</TableHead><TableHead>Generation</TableHead><TableHead className="w-[80px]"></TableHead></TableRow></TableHeader>
          <TableBody>
            {filtered.length === 0 ? <TableRow><TableCell colSpan={6} className="text-center py-8 text-sm text-[hsl(var(--muted-foreground))]">No submissions.</TableCell></TableRow> :
              filtered.map((r) => (
                <TableRow key={r.id} className="cursor-pointer" onClick={() => nav(`/admin/reviews/${r.id}`)} data-testid={`review-row-${r.id}`}>
                  <TableCell><div className="font-medium">{r.org_name}</div><div className="text-xs text-[hsl(var(--muted-foreground))]">{r.org_trade}</div></TableCell>
                  <TableCell className="text-sm">{r.standard_slug}</TableCell>
                  <TableCell><div className="flex items-center gap-2"><Progress value={r.completion} className="h-1.5 w-20" /><span className="text-xs tabular-nums">{r.completion}%</span></div></TableCell>
                  <TableCell><StatusBadge status={r.status} /></TableCell>
                  <TableCell>{r.generation_status ? <StatusBadge status={r.generation_status} /> : <span className="text-xs text-[hsl(var(--muted-foreground))]">—</span>}</TableCell>
                  <TableCell><Button size="icon" variant="ghost"><ArrowRight className="h-4 w-4" /></Button></TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </Card>
    </AppShell>
  );
}
