import React from "react";

const MAP = {
  // payment / order
  created: { c: "bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]", t: "Created" },
  paid: { c: "bg-[hsl(var(--success-bg))] text-[hsl(var(--success-fg))]", t: "Paid" },
  failed: { c: "bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger-fg))]", t: "Failed" },
  refunded: { c: "bg-[hsl(var(--warning-bg))] text-[hsl(var(--warning-fg))]", t: "Refunded" },
  // review
  draft: { c: "bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]", t: "Draft" },
  submitted: { c: "bg-[hsl(var(--warning-bg))] text-[hsl(var(--warning-fg))]", t: "Needs Review" },
  changes_requested: { c: "bg-[hsl(34_78%_90%)] text-[hsl(229_63%_18%)]", t: "Changes Requested" },
  approved: { c: "bg-[hsl(var(--success-bg))] text-[hsl(var(--success-fg))]", t: "Approved" },
  rejected: { c: "bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger-fg))]", t: "Rejected" },
  // generation
  waiting: { c: "bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]", t: "Waiting" },
  validating: { c: "bg-[hsl(var(--info-bg))] text-[hsl(var(--info-fg))]", t: "Validating" },
  generating: { c: "bg-[hsl(var(--info-bg))] text-[hsl(var(--info-fg))]", t: "Generating" },
  generation_failed: { c: "bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger-fg))]", t: "Generation Failed" },
  generated: { c: "bg-[hsl(var(--success-bg))] text-[hsl(var(--success-fg))]", t: "Generated" },
  published: { c: "bg-[hsl(174_78%_92%)] text-[hsl(174_78%_22%)]", t: "Published" },
  // additional requirements
  quoted: { c: "bg-[hsl(var(--info-bg))] text-[hsl(var(--info-fg))]", t: "Quoted" },
  accepted: { c: "bg-[hsl(var(--success-bg))] text-[hsl(var(--success-fg))]", t: "Accepted" },
};

export const StatusBadge = ({ status, className = "" }) => {
  const m = MAP[status] || { c: "bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]", t: status || "\u2014" };
  return (
    <span data-testid={`status-badge-${status}`}
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${m.c} ${className}`}>
      {m.t}
    </span>
  );
};
