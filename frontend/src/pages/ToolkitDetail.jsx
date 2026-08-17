import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api, { rupee } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Disclaimer } from "@/components/common/Disclaimer";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ArrowLeft, ShieldCheck, FileText, FileSpreadsheet, CheckCircle2 } from "lucide-react";

const fmtIcon = (f) => (f === "XLSX" ? FileSpreadsheet : FileText);

export default function ToolkitDetail() {
  const { slug } = useParams();
  const nav = useNavigate();
  const { user } = useAuth();
  const [t, setT] = useState(null);

  useEffect(() => { api.get(`/catalogue/${slug}`).then((r) => setT(r.data)).catch(() => {}); }, [slug]);

  if (!t) return <div className="min-h-screen flex items-center justify-center text-[hsl(var(--muted-foreground))]">Loading toolkit…</div>;

  const buy = () => {
    if (!user) { nav("/login", { state: { next: `/app/checkout/${slug}` } }); return; }
    nav(`/app/checkout/${slug}`);
  };

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b bg-white/90 backdrop-blur">
        <div className="max-w-6xl mx-auto flex h-16 items-center justify-between px-4 sm:px-6">
          <button onClick={() => nav("/")}><Logo /></button>
          <Button variant="outline" size="sm" onClick={() => nav(user ? (user.role==="admin"?"/admin":"/app") : "/login")}>{user ? "Dashboard" : "Login"}</Button>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <button onClick={() => nav("/")} className="inline-flex items-center gap-1 text-sm text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))] mb-4"><ArrowLeft className="h-4 w-4" /> Back to catalogue</button>

        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-start gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-xl text-white shrink-0" style={{ background: t.accent }}><ShieldCheck className="h-7 w-7" /></div>
              <div>
                <h1 className="text-2xl sm:text-3xl font-display">{t.name}</h1>
                <p className="mt-1 text-sm text-[hsl(var(--muted-foreground))]">{t.purpose}</p>
              </div>
            </div>

            <Card className="card-shadow p-5">
              <div className="grid sm:grid-cols-2 gap-4 text-sm">
                <div><div className="text-[hsl(var(--muted-foreground))] text-xs uppercase tracking-wide mb-1">Intended for</div>{t.intended_for}</div>
                <div><div className="text-[hsl(var(--muted-foreground))] text-xs uppercase tracking-wide mb-1">Industries</div><div className="flex flex-wrap gap-1.5">{t.industries.map((i) => <Badge key={i} variant="outline">{i}</Badge>)}</div></div>
              </div>
              <div className="mt-4 flex flex-wrap gap-2">
                {Object.entries(t.categories).map(([k, v]) => <Badge key={k} variant="secondary" className="capitalize">{v} {k}{v>1?"s":""}</Badge>)}
              </div>
              <div className="mt-4 flex flex-wrap gap-1.5 text-xs">Formats: {t.formats.map((f) => <Badge key={f} className="bg-[hsl(var(--accent))] text-[hsl(var(--accent-foreground))] border-0">{f}</Badge>)}</div>
            </Card>

            {t.legal_disclaimer && <Disclaimer>{t.legal_disclaimer}</Disclaimer>}

            <div>
              <h2 className="text-lg font-display mb-3">Toolkit manifest · {t.document_count} documents</h2>
              <Card className="card-shadow overflow-hidden">
                <div className="max-h-[560px] overflow-auto">
                  <Table>
                    <TableHeader className="sticky top-0 bg-white z-10">
                      <TableRow>
                        <TableHead className="w-[110px]">Doc ID</TableHead>
                        <TableHead>Document</TableHead>
                        <TableHead className="w-[90px]">Format</TableHead>
                        <TableHead className="hidden md:table-cell">Classification</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {t.manifest.map((d) => {
                        const Icon = fmtIcon(d.format);
                        return (
                          <TableRow key={d.doc_id} data-testid={`manifest-row-${d.doc_id}`}>
                            <TableCell className="font-mono text-xs">{d.doc_id}</TableCell>
                            <TableCell>
                              <div className="font-medium">{d.title}</div>
                              <div className="text-xs text-[hsl(var(--muted-foreground))]">{d.template_class}</div>
                            </TableCell>
                            <TableCell><Badge variant="outline" className="gap-1"><Icon className="h-3 w-3" />{d.format}</Badge></TableCell>
                            <TableCell className="hidden md:table-cell text-xs">{d.classification}</TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </div>
              </Card>
            </div>
          </div>

          {/* Purchase panel */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 space-y-4">
              <Card className="card-shadow p-6">
                <div className="text-sm text-[hsl(var(--muted-foreground))]">One-time price</div>
                <div className="font-display text-4xl font-bold mt-1">{rupee(t.price)}</div>
                <div className="text-xs text-[hsl(var(--muted-foreground))] mt-1">+ {Math.round(t.gst_rate*100)}% GST at checkout</div>
                <ul className="mt-4 space-y-2 text-sm">
                  {["Complete predefined toolkit", "Editable DOCX & XLSX + reference PDFs", "Full ZIP package", "Guided onboarding", "Regeneration after approved changes"].map((x) => (
                    <li key={x} className="flex items-start gap-2"><CheckCircle2 className="h-4 w-4 text-[hsl(var(--teal))] mt-0.5 shrink-0" />{x}</li>
                  ))}
                </ul>
                <Button className="w-full mt-5" size="lg" onClick={buy} data-testid="buy-toolkit-button">Buy this toolkit</Button>
                <p className="mt-3 text-[11px] text-[hsl(var(--muted-foreground))] text-center">Access granted only after verified payment. Documents generated after admin approval.</p>
              </Card>
              <Card className="card-shadow p-4 text-xs text-[hsl(var(--muted-foreground))]">
                Onboarding sections: {t.onboarding_sections.map((s) => s.title).join(" · ")}
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
