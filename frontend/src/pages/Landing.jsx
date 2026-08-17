import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import api, { rupee } from "@/lib/api";
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Disclaimer } from "@/components/common/Disclaimer";
import { ShieldCheck, FileText, CheckCircle2, ArrowRight, FileCheck2, ListChecks, Package, Building2 } from "lucide-react";

const STEPS = [
  { icon: Package, t: "See the exact manifest", d: "Review every document included before you pay — no surprises." },
  { icon: FileCheck2, t: "Guided onboarding", d: "Answer a modular questionnaire about your organization." },
  { icon: ShieldCheck, t: "FaizZab verification", d: "Our experts verify your information before generation." },
  { icon: FileText, t: "Branded documents", d: "Get org-specific DOCX, XLSX, PDF and a full ZIP package." },
];

export default function Landing() {
  const [data, setData] = useState({ toolkits: [], price: 4999 });
  const nav = useNavigate();
  useEffect(() => { api.get("/catalogue").then((r) => setData(r.data)).catch(() => {}); }, []);

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-30 border-b bg-white/90 backdrop-blur">
        <div className="max-w-6xl mx-auto flex h-16 items-center justify-between px-4 sm:px-6">
          <Logo />
          <div className="flex items-center gap-2">
            <a href="#toolkits" className="hidden sm:inline text-sm px-3 py-2 text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]">Toolkits</a>
            <a href="#how" className="hidden sm:inline text-sm px-3 py-2 text-[hsl(var(--muted-foreground))] hover:text-[hsl(var(--foreground))]">How it works</a>
            <Button variant="outline" size="sm" onClick={() => nav("/login")} data-testid="header-login-button">Login</Button>
            <Button size="sm" onClick={() => nav("/login")} data-testid="header-cta-button">Get started</Button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="hero-wash border-b">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-16 sm:py-20 grid lg:grid-cols-2 gap-10 items-center">
          <div>
            <Badge className="mb-4 bg-[hsl(var(--accent))] text-[hsl(var(--accent-foreground))] border-0">ISO &amp; India DPDP Act ready</Badge>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-display tracking-tight leading-[1.05]">
              Generate your ISO &amp; DPDPA documentation, branded for your business
            </h1>
            <p className="mt-5 text-base sm:text-lg text-[hsl(var(--muted-foreground))] leading-relaxed max-w-xl">
              A professionally structured, organization-specific documentation system using your own name, logo, industry, processes and operating environment — for a flat {rupee(data.price)}.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Button size="lg" onClick={() => document.getElementById("toolkits").scrollIntoView({ behavior: "smooth" })} data-testid="hero-browse-button">
                Browse toolkits <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button size="lg" variant="outline" onClick={() => nav("/login")}>Sign in</Button>
            </div>
            <div className="mt-6 flex flex-wrap gap-x-6 gap-y-2 text-sm text-[hsl(var(--muted-foreground))]">
              {["See manifest before payment", "Editable DOCX & XLSX", "Admin-verified generation"].map((x) => (
                <span key={x} className="inline-flex items-center gap-1.5"><CheckCircle2 className="h-4 w-4 text-[hsl(var(--teal))]" />{x}</span>
              ))}
            </div>
          </div>
          <div className="space-y-3">
            {data.toolkits.slice(0, 3).map((t, i) => (
              <Card key={t.slug} className="card-shadow p-4 flex items-center gap-4" style={{ marginLeft: i * 16 }}>
                <div className="flex h-11 w-11 items-center justify-center rounded-lg text-white shrink-0" style={{ background: t.accent }}>
                  <ShieldCheck className="h-6 w-6" />
                </div>
                <div className="min-w-0">
                  <div className="font-medium truncate">{t.code} {t.version}</div>
                  <div className="text-xs text-[hsl(var(--muted-foreground))]">{t.document_count} documents · {rupee(t.price)}</div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="max-w-6xl mx-auto px-4 sm:px-6 py-14">
        <h2 className="text-2xl sm:text-3xl font-display text-center">How it works</h2>
        <div className="mt-8 grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {STEPS.map((s, i) => (
            <Card key={i} className="card-shadow p-5">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[hsl(var(--accent))] text-[hsl(var(--accent-foreground))]"><s.icon className="h-5 w-5" /></div>
              <div className="mt-3 font-medium">{s.t}</div>
              <p className="mt-1 text-sm text-[hsl(var(--muted-foreground))]">{s.d}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* Catalogue */}
      <section id="toolkits" className="bg-[hsl(var(--secondary))]/40 border-y">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-14">
          <div className="flex items-end justify-between mb-6">
            <div>
              <h2 className="text-2xl sm:text-3xl font-display">Toolkit catalogue</h2>
              <p className="text-sm text-[hsl(var(--muted-foreground))] mt-1">Every toolkit is a flat {rupee(data.price)}. See the full document list before you buy.</p>
            </div>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
            {data.toolkits.map((t) => (
              <Card key={t.slug} className="card-shadow card-shadow-hover p-5 flex flex-col" data-testid={`toolkit-card-${t.slug}`}>
                <div className="flex items-center gap-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-lg text-white shrink-0" style={{ background: t.accent }}><ShieldCheck className="h-6 w-6" /></div>
                  <div>
                    <div className="font-display font-semibold">{t.code}</div>
                    <div className="text-xs text-[hsl(var(--muted-foreground))]">{t.version}</div>
                  </div>
                </div>
                <p className="mt-3 text-sm text-[hsl(var(--muted-foreground))] line-clamp-3 flex-1">{t.purpose}</p>
                <div className="mt-4 flex flex-wrap gap-1.5">
                  <Badge variant="secondary" className="gap-1"><FileText className="h-3 w-3" />{t.document_count} docs</Badge>
                  {t.industries.slice(0, 2).map((ind) => <Badge key={ind} variant="outline">{ind}</Badge>)}
                </div>
                <div className="mt-4 flex items-center justify-between border-t pt-4">
                  <div className="font-display text-lg font-semibold">{rupee(t.price)}</div>
                  <Button size="sm" onClick={() => nav(`/toolkits/${t.slug}`)} data-testid={`view-toolkit-${t.slug}`}>
                    View manifest <ArrowRight className="ml-1 h-4 w-4" />
                  </Button>
                </div>
              </Card>
            ))}
          </div>
          <div className="mt-8"><Disclaimer>Purchasing a toolkit does not guarantee certification and does not by itself make your organization compliant. Generated documents require implementation. DPDPA documents are not legal advice.</Disclaimer></div>
        </div>
      </section>

      <footer className="border-t bg-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <Logo />
          <p className="text-xs text-[hsl(var(--muted-foreground))] text-center">FaizZab is an independent provider and is not ISO. ISO has not approved this toolkit. © {new Date().getFullYear()} FaizZab.</p>
        </div>
      </footer>
    </div>
  );
}
