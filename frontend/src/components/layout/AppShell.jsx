import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { Logo } from "@/components/common/Logo";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import {
  LayoutDashboard, Building2, FileText, Download, ClipboardList, Receipt,
  Menu, LogOut, ShieldCheck, Users, ListChecks, BarChart3, ScrollText,
  Boxes, PlusCircle,
} from "lucide-react";

const CLIENT_NAV = [
  { to: "/app", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/app/organization", label: "Organization", icon: Building2 },
  { to: "/app/onboarding", label: "Onboarding", icon: FileText },
  { to: "/app/downloads", label: "Downloads", icon: Download },
  { to: "/app/additional", label: "Additional Requests", icon: PlusCircle },
  { to: "/app/invoices", label: "Invoices", icon: Receipt },
];

const ADMIN_NAV = [
  { to: "/admin", label: "Executive", icon: LayoutDashboard, end: true },
  { to: "/admin/reviews", label: "Review Queue", icon: ListChecks },
  { to: "/admin/generation", label: "Generation Monitor", icon: Boxes },
  { to: "/admin/clients", label: "Clients", icon: Users },
  { to: "/admin/commerce", label: "Commerce", icon: BarChart3 },
  { to: "/admin/content", label: "Content", icon: ClipboardList },
  { to: "/admin/additional", label: "Additional Requests", icon: PlusCircle },
  { to: "/admin/audit", label: "Audit Logs", icon: ScrollText },
];

const NavList = ({ items, onNavigate }) => {
  const loc = useLocation();
  return (
    <nav className="flex flex-col gap-1 p-3">
      {items.map((it) => {
        const active = it.end ? loc.pathname === it.to : loc.pathname.startsWith(it.to);
        const Icon = it.icon;
        return (
          <Link key={it.to} to={it.to} onClick={onNavigate}
            data-testid={`nav-${it.label.toLowerCase().replace(/\s+/g, "-")}`}
            className={`flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors ${
              active
                ? "bg-[hsl(var(--primary))] text-white font-medium"
                : "text-[hsl(var(--foreground))] hover:bg-[hsl(var(--accent))]"
            }`}>
            <Icon className="h-4 w-4" />
            {it.label}
          </Link>
        );
      })}
    </nav>
  );
};

export const AppShell = ({ children, admin = false }) => {
  const { user, org, logout } = useAuth();
  const [open, setOpen] = useState(false);
  const nav = useNavigate();
  const items = admin ? ADMIN_NAV : CLIENT_NAV;

  return (
    <div className="min-h-screen bg-[hsl(var(--background))]">
      {/* Topbar */}
      <header className="sticky top-0 z-30 border-b bg-white/90 backdrop-blur">
        <div className="flex h-14 items-center justify-between px-4 sm:px-6">
          <div className="flex items-center gap-3">
            <Sheet open={open} onOpenChange={setOpen}>
              <SheetTrigger asChild className="lg:hidden">
                <Button variant="ghost" size="icon" data-testid="mobile-menu-button"><Menu className="h-5 w-5" /></Button>
              </SheetTrigger>
              <SheetContent side="left" className="w-72 p-0">
                <div className="p-4 border-b"><Logo /></div>
                <NavList items={items} onNavigate={() => setOpen(false)} />
              </SheetContent>
            </Sheet>
            <button onClick={() => nav(admin ? "/admin" : "/app")}><Logo /></button>
            {admin && <span className="hidden sm:inline-flex items-center gap-1 rounded-full bg-[hsl(var(--primary))] px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-white"><ShieldCheck className="h-3 w-3" />Admin</span>}
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden sm:block text-right leading-tight">
              <div className="text-sm font-medium">{user?.name}</div>
              <div className="text-xs text-[hsl(var(--muted-foreground))]">{org?.trade_name || (admin ? "Platform" : "No organization")}</div>
            </div>
            <Button variant="outline" size="sm" onClick={logout} data-testid="logout-button">
              <LogOut className="h-4 w-4 mr-1" /> Logout
            </Button>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="hidden lg:block w-64 shrink-0 border-r bg-white min-h-[calc(100vh-3.5rem)]">
          <NavList items={items} />
        </aside>
        <main className="flex-1 min-w-0 px-4 sm:px-6 lg:px-8 py-6 max-w-[1200px] mx-auto w-full">
          {children}
        </main>
      </div>
    </div>
  );
};
