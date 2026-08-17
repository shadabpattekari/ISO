import React from "react";
import { ShieldCheck } from "lucide-react";

export const Logo = ({ light = false }) => (
  <div className="flex items-center gap-2 select-none">
    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[hsl(var(--primary))] text-white">
      <ShieldCheck className="h-5 w-5" />
    </div>
    <div className="leading-tight">
      <div className={`font-display font-bold text-[15px] ${light ? "text-white" : "text-[hsl(var(--primary))]"}`}>FaizZab</div>
      <div className={`text-[9px] uppercase tracking-wider ${light ? "text-white/70" : "text-[hsl(var(--muted-foreground))]"}`}>Compliance Toolkit</div>
    </div>
  </div>
);
