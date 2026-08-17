import React from "react";
import { Info } from "lucide-react";

export const Disclaimer = ({ children, tone = "info" }) => (
  <div data-testid="compliance-disclaimer-alert"
    className="flex gap-3 rounded-lg border p-3 text-sm bg-[hsl(var(--info-bg))] text-[hsl(var(--info-fg))] border-[hsl(var(--info-border))]">
    <Info className="h-4 w-4 mt-0.5 shrink-0" />
    <div className="leading-relaxed">{children}</div>
  </div>
);
