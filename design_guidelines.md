{
  "product": {
    "name": "FaizZab ISO & DPDPA Toolkit Generator",
    "design_personality": {
      "keywords": [
        "authoritative",
        "secure",
        "enterprise-grade",
        "calm",
        "approachable for non-experts",
        "India-first (₹, GST, DPDP Act)"
      ],
      "style_fusion": {
        "palette_inspiration": "fintech/enterprise navy + sand neutrals + sage/teal trust accents",
        "layout_inspiration": "GRC workflow-first dashboards + bento KPI grid + dense tables with sticky headers",
        "typography_inspiration": "neo-grotesk display + highly legible body (IBM Plex)"
      },
      "public_vs_app_surface": {
        "public": "lighter, editorial, conversion-focused; more whitespace; subtle hero background treatment",
        "authenticated_app": "denser, operational; stronger borders; clearer status colors; persistent navigation",
        "client_vs_admin": "same system, but Admin uses higher-density tables, more filters, and stronger status emphasis"
      }
    }
  },

  "design_tokens": {
    "fonts": {
      "google_fonts_to_add": [
        {
          "family": "Space Grotesk",
          "weights": ["400", "500", "600", "700"],
          "usage": "Headings, KPI numbers, marketing hero"
        },
        {
          "family": "IBM Plex Sans",
          "weights": ["400", "500", "600"],
          "usage": "Body, forms, tables"
        },
        {
          "family": "IBM Plex Mono",
          "weights": ["400", "500"],
          "usage": "IDs, invoice numbers, job IDs, hashes, timestamps"
        }
      ],
      "css_vars": {
        "--font-sans": "'IBM Plex Sans', ui-sans-serif, system-ui",
        "--font-display": "'Space Grotesk', ui-sans-serif, system-ui",
        "--font-mono": "'IBM Plex Mono', ui-monospace, SFMono-Regular"
      },
      "tailwind_usage": {
        "headings": "font-[var(--font-display)]",
        "body": "font-[var(--font-sans)]",
        "mono": "font-[var(--font-mono)]"
      }
    },

    "color_system": {
      "notes": [
        "Avoid purple (AI/chat restriction).",
        "Use navy as trust anchor; sage/teal as positive/active; sand as warm neutral.",
        "Gradients only as subtle section backgrounds (<=20% viewport)."
      ],
      "core": {
        "bg": "210 33% 98%",
        "surface": "0 0% 100%",
        "surface_2": "36 45% 96%",
        "text": "222 47% 11%",
        "muted_text": "215 16% 40%",
        "border": "214 20% 90%"
      },
      "brand": {
        "navy": {
          "name": "Anchor Navy",
          "hex": "#111A4A",
          "hsl": "229 63% 18%",
          "usage": "Primary buttons, top nav, key headings"
        },
        "teal": {
          "name": "Verification Teal",
          "hex": "#0F766E",
          "hsl": "174 78% 26%",
          "usage": "Progress, active states, links, success-adjacent accents"
        },
        "sage": {
          "name": "Sage",
          "hex": "#B1CA85",
          "hsl": "83 38% 66%",
          "usage": "Chart series, subtle highlights (sparingly)"
        },
        "sand": {
          "name": "Sand",
          "hex": "#FBF0DF",
          "hsl": "34 78% 93%",
          "usage": "Marketing section tint, callouts, empty states"
        }
      },
      "semantic": {
        "info": { "bg": "199 89% 96%", "fg": "199 89% 22%", "border": "199 70% 85%" },
        "success": { "bg": "152 55% 95%", "fg": "152 55% 22%", "border": "152 40% 84%" },
        "warning": { "bg": "43 96% 95%", "fg": "30 90% 25%", "border": "43 80% 85%" },
        "danger": { "bg": "0 86% 96%", "fg": "0 72% 35%", "border": "0 70% 88%" }
      },
      "status_badges": {
        "payment": {
          "unpaid": { "badge": "bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))] border-[hsl(var(--border))]" },
          "paid": { "badge": "bg-[hsl(var(--success-bg))] text-[hsl(var(--success-fg))] border-[hsl(var(--success-border))]" },
          "refunded": { "badge": "bg-[hsl(var(--warning-bg))] text-[hsl(var(--warning-fg))] border-[hsl(var(--warning-border))]" }
        },
        "generation": {
          "waiting": { "badge": "bg-[hsl(var(--muted))] text-[hsl(var(--muted-foreground))]" },
          "generating": { "badge": "bg-[hsl(var(--info-bg))] text-[hsl(var(--info-fg))]" },
          "qc": { "badge": "bg-[hsl(var(--warning-bg))] text-[hsl(var(--warning-fg))]" },
          "generated": { "badge": "bg-[hsl(var(--success-bg))] text-[hsl(var(--success-fg))]" },
          "published": { "badge": "bg-[hsl(174_78%_92%)] text-[hsl(174_78%_22%)]" },
          "failed": { "badge": "bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger-fg))]" }
        },
        "review": {
          "needs-review": { "badge": "bg-[hsl(var(--warning-bg))] text-[hsl(var(--warning-fg))]" },
          "changes-requested": { "badge": "bg-[hsl(34_78%_93%)] text-[hsl(229_63%_18%)]" },
          "approved": { "badge": "bg-[hsl(var(--success-bg))] text-[hsl(var(--success-fg))]" },
          "rejected": { "badge": "bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger-fg))]" }
        }
      },
      "gradients": {
        "allowed_background_gradients": [
          {
            "name": "Public hero wash (navy→sand)",
            "css": "radial-gradient(1200px 600px at 20% 10%, rgba(17,26,74,0.10), transparent 60%), radial-gradient(900px 500px at 80% 0%, rgba(251,240,223,0.85), transparent 55%)",
            "usage": "Landing hero background only (max 20% viewport height)"
          },
          {
            "name": "App header tint (teal→transparent)",
            "css": "linear-gradient(90deg, rgba(15,118,110,0.10), transparent 55%)",
            "usage": "Top-of-page header strip behind breadcrumbs/title"
          }
        ],
        "restriction": "Follow GRADIENT RESTRICTION RULE from General UI UX Design Guidelines. No saturated/dark gradients."
      }
    },

    "radius_shadow_spacing": {
      "radius": {
        "--radius": "12px",
        "card": "rounded-xl",
        "button": "rounded-lg",
        "input": "rounded-md"
      },
      "shadows": {
        "card": "shadow-[0_1px_0_rgba(17,26,74,0.06),0_10px_30px_rgba(17,26,74,0.06)]",
        "popover": "shadow-[0_12px_40px_rgba(17,26,74,0.14)]",
        "focus_ring": "focus-visible:ring-2 focus-visible:ring-[hsl(var(--ring))] focus-visible:ring-offset-2"
      },
      "spacing": {
        "page_padding": "px-4 sm:px-6 lg:px-8",
        "section_gap": "py-10 sm:py-14",
        "card_padding": "p-4 sm:p-6",
        "form_gap": "gap-4 sm:gap-6"
      },
      "grid": {
        "marketing_container": "max-w-6xl mx-auto",
        "app_container": "max-w-[1200px] mx-auto",
        "dashboard_bento": "grid grid-cols-1 md:grid-cols-12 gap-4",
        "bento_card_spans": {
          "kpi": "md:col-span-3",
          "wide": "md:col-span-6",
          "full": "md:col-span-12"
        }
      }
    }
  },

  "typography_scale": {
    "h1": "text-4xl sm:text-5xl lg:text-6xl font-[var(--font-display)] tracking-tight",
    "h2": "text-base md:text-lg font-[var(--font-sans)] text-muted-foreground",
    "h3": "text-xl sm:text-2xl font-[var(--font-display)]",
    "section_title": "text-2xl sm:text-3xl font-[var(--font-display)]",
    "body": "text-sm sm:text-base font-[var(--font-sans)] leading-relaxed",
    "small": "text-xs sm:text-sm text-muted-foreground",
    "kpi_number": "text-2xl sm:text-3xl font-[var(--font-display)] tabular-nums"
  },

  "layout_blueprints": {
    "public_marketing": {
      "header": {
        "pattern": "sticky top nav with subtle border + CTA",
        "left": "FaizZab logo + nav (Toolkits, Pricing, How it works, FAQs)",
        "right": "Login + Primary CTA (View Toolkits)",
        "components": ["navigation-menu", "button", "sheet (mobile nav)"]
      },
      "landing_hero": {
        "layout": "Split hero: left copy + trust bullets; right product preview card stack",
        "hero_background": "Use allowed gradient wash + subtle noise overlay",
        "trust_row": "ISO/DPDPA badges + 'No certification guarantee' disclaimer link",
        "primary_cta": "Browse Toolkits",
        "secondary_cta": "See manifest before payment",
        "components": ["card", "badge", "button", "separator"]
      },
      "catalogue": {
        "layout": "Card grid with filters (Standard, Industry, Price fixed ₹4,999, Delivery formats)",
        "card": "Toolkit card shows: standard name, doc count, onboarding time estimate, last updated, ₹ price",
        "components": ["card", "badge", "tabs", "input", "select", "pagination"]
      },
      "toolkit_detail": {
        "layout": "Two-column: left manifest + sample previews; right sticky purchase panel",
        "manifest": "Table with doc name, format (DOCX/XLSX/PDF), purpose, clause mapping",
        "sample_previews": "Carousel of watermarked sample pages (PDF images) + disclaimer",
        "purchase_panel": "₹4,999 + GST note + coupon input + checkout button",
        "components": ["table", "carousel", "card", "input", "button", "alert"]
      }
    },

    "authenticated_app": {
      "shell": {
        "pattern": "App layout with left sidebar (desktop) + top bar; mobile uses Sheet",
        "sidebar_sections": [
          "Client: Dashboard, Onboarding, Downloads, Quotations, Invoices, Org Profile",
          "Admin: Executive, Review Queue, Generation Monitor, Standards, Commerce, Audit Logs"
        ],
        "components": ["sheet", "navigation-menu (optional)", "breadcrumb", "separator"]
      },
      "client_dashboard": {
        "top": "Bento KPI row: Toolkit purchased, Onboarding completion %, Review status, Generation status",
        "middle": "Next actions card (Continue onboarding / Fix requested changes / Download package)",
        "bottom": "Recent downloads + invoices table",
        "components": ["card", "progress", "badge", "table", "button"]
      },
      "admin_executive_dashboard": {
        "kpis": "Clients, Revenue (₹), Pending reviews, Failed jobs",
        "charts": "Revenue trend + pipeline statuses",
        "tables": "Latest submissions + generation failures",
        "components": ["card", "table", "tabs", "badge"]
      },
      "review_queue": {
        "layout": "Dense table with filters + row actions; right-side Drawer for quick review",
        "row": "Org name, standard, completion %, submitted at, flags, reviewer, status",
        "actions": "Open, Request correction, Approve, Reject",
        "components": ["table", "dropdown-menu", "drawer", "dialog", "textarea", "button"]
      },
      "onboarding_wizard": {
        "pattern": "Split-screen wizard: left vertical stepper + completion; right form panel",
        "sections": [
          "A Org identity",
          "B Business profile",
          "C Org structure",
          "D Management-system scope",
          "E Process inventory",
          "F Technology profile",
          "G Legal/regulatory",
          "H Standard-specific",
          "I Branding & document control"
        ],
        "save_model": "Autosave draft + explicit Save button; show last saved timestamp",
        "components": ["progress", "tabs (optional)", "accordion (for long sections)", "form", "input", "textarea", "select", "calendar", "checkbox", "radio-group"]
      },
      "downloads_center": {
        "layout": "Header with package status + Download ZIP; below: master list table + filters",
        "table": "Doc name, format, version, owner role, clause mapping, download",
        "components": ["card", "badge", "table", "button", "tooltip"]
      },
      "generation_tracker": {
        "pattern": "Timeline-like status with steps (Waiting→Generating→QC→Generated→Published)",
        "components": ["progress", "badge", "separator", "skeleton"]
      }
    }
  },

  "component_path": {
    "primary_shadcn_components": {
      "buttons": "/app/frontend/src/components/ui/button.jsx",
      "cards": "/app/frontend/src/components/ui/card.jsx",
      "tables": "/app/frontend/src/components/ui/table.jsx",
      "badges": "/app/frontend/src/components/ui/badge.jsx",
      "forms": "/app/frontend/src/components/ui/form.jsx",
      "inputs": "/app/frontend/src/components/ui/input.jsx",
      "textarea": "/app/frontend/src/components/ui/textarea.jsx",
      "select": "/app/frontend/src/components/ui/select.jsx",
      "dialog": "/app/frontend/src/components/ui/dialog.jsx",
      "drawer": "/app/frontend/src/components/ui/drawer.jsx",
      "sheet": "/app/frontend/src/components/ui/sheet.jsx",
      "tabs": "/app/frontend/src/components/ui/tabs.jsx",
      "progress": "/app/frontend/src/components/ui/progress.jsx",
      "calendar": "/app/frontend/src/components/ui/calendar.jsx",
      "toast": "Use sonner: /app/frontend/src/components/ui/sonner.jsx",
      "breadcrumb": "/app/frontend/src/components/ui/breadcrumb.jsx",
      "tooltip": "/app/frontend/src/components/ui/tooltip.jsx",
      "pagination": "/app/frontend/src/components/ui/pagination.jsx",
      "skeleton": "/app/frontend/src/components/ui/skeleton.jsx"
    },
    "recommended_new_components_to_create": [
      {
        "name": "AppShell",
        "path": "/app/frontend/src/components/layout/AppShell.jsx",
        "purpose": "Shared authenticated layout: sidebar + topbar + breadcrumb + content container"
      },
      {
        "name": "RoleGate",
        "path": "/app/frontend/src/components/auth/RoleGate.jsx",
        "purpose": "Client vs Admin UI gating + nav items"
      },
      {
        "name": "StatusBadge",
        "path": "/app/frontend/src/components/common/StatusBadge.jsx",
        "purpose": "Central mapping for payment/review/generation statuses to Badge variants"
      },
      {
        "name": "WizardStepper",
        "path": "/app/frontend/src/components/onboarding/WizardStepper.jsx",
        "purpose": "Vertical stepper with completion %, section validation, and jump-to"
      },
      {
        "name": "ManifestTable",
        "path": "/app/frontend/src/components/toolkits/ManifestTable.jsx",
        "purpose": "Toolkit manifest table with format chips + clause mapping"
      },
      {
        "name": "KpiStatCard",
        "path": "/app/frontend/src/components/dashboard/KpiStatCard.jsx",
        "purpose": "Reusable KPI card with icon, number, delta, and sparkline slot"
      }
    ],
    "optional_blocks_inspiration": {
      "shadcn_blocks": [
        "https://www.shadcn.io/blocks/account-compliance-status",
        "https://www.shadcn.io/blocks/onboarding-compliance-checklist",
        "https://www.shadcn.io/blocks/kanban-compliance-board"
      ]
    }
  },

  "component_specs": {
    "buttons": {
      "tone": "Professional / Corporate",
      "variants": {
        "primary": "bg-[hsl(var(--primary))] text-[hsl(var(--primary-foreground))] hover:bg-[hsl(229_63%_14%)]",
        "secondary": "bg-[hsl(var(--secondary))] text-[hsl(var(--secondary-foreground))] hover:bg-[hsl(36_45%_92%)]",
        "ghost": "hover:bg-[hsl(var(--accent))]"
      },
      "motion": "hover: translateY(-1px) on primary only; active: scale-[0.98]; no transition-all",
      "data_testid_examples": [
        "data-testid=\"catalogue-primary-cta-button\"",
        "data-testid=\"checkout-pay-now-button\"",
        "data-testid=\"onboarding-save-draft-button\""
      ]
    },
    "cards": {
      "style": "White surface, hairline border, soft shadow; header uses display font",
      "hover": "Marketing cards: hover shadow increases slightly + border darkens",
      "class_recipe": "rounded-xl border bg-card text-card-foreground shadow-[0_1px_0_rgba(17,26,74,0.06),0_10px_30px_rgba(17,26,74,0.06)]"
    },
    "tables": {
      "density": {
        "default": "text-sm",
        "admin": "text-xs sm:text-sm",
        "row_height": "py-2.5 (dense) / py-3 (default)"
      },
      "ux": [
        "Sticky header for long lists",
        "Row hover highlight: bg-[hsl(var(--accent))]",
        "Right-aligned numeric columns with tabular-nums",
        "Use Tooltip for truncated cells"
      ],
      "empty_state": "Use Card with sand tint + clear next action button"
    },
    "wizard_stepper": {
      "pattern": "Left rail with sections A–I; each item shows status dot + completion; right panel is form",
      "validation": "Show per-section errors count; prevent final submit until required sections complete",
      "microcopy": "Explain why each section matters (1 line) to reduce anxiety",
      "components": ["progress", "badge", "collapsible", "accordion"]
    },
    "badges": {
      "rule": "Badges must encode status, not decoration. Always include text label.",
      "examples": [
        "Payment: Paid",
        "Review: Changes requested",
        "Generation: QC"
      ]
    },
    "disclaimer_blocks": {
      "style": "Use Alert component with info semantic colors; keep copy short; link to full disclaimer",
      "placements": [
        "Toolkit detail page (above purchase)",
        "Checkout page",
        "Downloads center header"
      ],
      "data_testid": "data-testid=\"compliance-disclaimer-alert\""
    }
  },

  "motion_microinteractions": {
    "library": {
      "recommended": "framer-motion",
      "install": "npm i framer-motion",
      "usage": [
        "Page transitions: fade+slide (y: 8px) for marketing pages",
        "Card hover: subtle lift",
        "Wizard step change: crossfade + slight slide",
        "Status changes: animate badge background fade"
      ]
    },
    "principles": [
      "Prefer 120–180ms for hover, 180–240ms for panel transitions",
      "Use ease-out for entrances, ease-in for exits",
      "Respect prefers-reduced-motion"
    ],
    "tailwind_examples": {
      "card_hover": "transition-shadow duration-200 hover:shadow-[0_12px_40px_rgba(17,26,74,0.12)]",
      "button_hover": "transition-colors duration-150 active:scale-[0.98]",
      "nav_item": "transition-colors duration-150"
    }
  },

  "data_viz": {
    "library": {
      "recommended": "recharts",
      "install": "npm i recharts",
      "use_cases": [
        "Admin revenue trend",
        "Pipeline status distribution",
        "Onboarding completion over time"
      ]
    },
    "chart_palette": {
      "series": ["#111A4A", "#0F766E", "#B1CA85", "#E7CBA0", "#64748B"],
      "rules": [
        "Never rely on color alone; add labels/legends",
        "Use muted gridlines (border color)"
      ]
    }
  },

  "image_urls": {
    "marketing_hero": [
      {
        "url": "https://images.pexels.com/photos/7581119/pexels-photo-7581119.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
        "description": "Small business team meeting; use as subtle right-side hero image with overlay tint"
      }
    ],
    "trust_and_docs": [
      {
        "url": "https://images.unsplash.com/photo-1531256379416-9f000e90aacc?crop=entropy&cs=srgb&fm=jpg&ixlib=rb-4.1.0&q=85",
        "description": "Desk flatlay with documents; use for catalogue section background card"
      }
    ],
    "texture_optional": [
      {
        "url": "https://images.unsplash.com/photo-1603248410724-69a3c8b87a8a?crop=entropy&cs=srgb&fm=jpg&ixlib=rb-4.1.0&q=85",
        "description": "Abstract teal texture; use as very low-opacity overlay (5–8%) in hero only"
      }
    ]
  },

  "accessibility": {
    "requirements": [
      "WCAG AA contrast for text and interactive elements",
      "Visible focus states on all controls (ring + offset)",
      "Keyboard navigable tables (row actions reachable)",
      "Use aria-labels for icon-only buttons",
      "Do not encode status only by color; always include label"
    ],
    "form_a11y": [
      "Every input must have Label",
      "Error text must be programmatically associated",
      "Use helper text for compliance jargon"
    ]
  },

  "testing_data_testid": {
    "rules": [
      "All interactive and key informational elements MUST include data-testid",
      "Use kebab-case describing role, not appearance",
      "Examples: onboarding-next-button, review-approve-button, downloads-zip-button"
    ],
    "high_priority_elements": [
      "Primary CTAs",
      "Checkout/payment buttons",
      "Wizard navigation (next/back/save/submit)",
      "Status badges (payment/review/generation)",
      "Download links/buttons",
      "Admin approve/reject/request-correction actions",
      "Error banners and disclaimer alerts"
    ]
  },

  "instructions_to_main_agent": {
    "global_css_updates": [
      "Remove/avoid .App { text-align:center } patterns (current App.css is CRA default; do not use App-header styles for real UI).",
      "Update /app/frontend/src/index.css :root tokens to match the palette above (primary=navy, ring=teal, secondary=sand tint).",
      "Add font imports in index.html or via CSS @import; set body font to var(--font-sans) and headings to var(--font-display).",
      "Add semantic CSS vars: --success-bg/fg/border, --warning-*, --info-*, --danger-* for consistent badges/alerts."
    ],
    "public_pages": [
      "Implement landing/catalogue with editorial spacing, hero wash gradient (<=20% viewport), and conversion CTAs.",
      "Toolkit detail must show full manifest BEFORE payment; include watermarked sample preview carousel and disclaimer alert.",
      "Use Card + Table for manifest; sticky purchase panel on desktop."
    ],
    "app_pages": [
      "Build AppShell with sidebar + topbar; mobile nav via Sheet.",
      "Onboarding wizard: split layout with left stepper; autosave + explicit save; show last saved timestamp.",
      "Admin review queue: dense table + Drawer quick review; actions in row dropdown + confirm dialogs.",
      "Downloads center: status header + ZIP download + master list table with filters."
    ],
    "libraries": [
      "Install framer-motion for micro-interactions and step transitions.",
      "Install recharts for admin KPI charts."
    ],
    "icons": [
      "Use lucide-react icons only (no emoji)."
    ],
    "pwa": [
      "Ensure touch targets >= 44px; sticky bottom action bar for wizard on mobile."
    ]
  },

  "General UI UX Design Guidelines": "- You must **not** apply universal transition. Eg: `transition: all`. This results in breaking transforms. Always add transitions for specific interactive elements like button, input excluding transforms\n- You must **not** center align the app container, ie do not add `.App { text-align: center; }` in the css file. This disrupts the human natural reading flow of text\n- NEVER: use AI assistant Emoji characters like`🤖🧠💭💡🔮🎯📚🎭🎬🎪🎉🎊🎁🎀🎂🍰🎈🎨🎰💰💵💳🏦💎🪙💸🤑📊📈📉💹🔢🏆🥇 etc for icons. Always use **FontAwesome cdn** or **lucid-react** library already installed in the package.json\n\n **GRADIENT RESTRICTION RULE**\nNEVER use dark/saturated gradient combos (e.g., purple/pink) on any UI element.  Prohibited gradients: blue-500 to purple 600, purple 500 to pink-500, green-500 to blue-500, red to pink etc\nNEVER use dark gradients for logo, testimonial, footer etc\nNEVER let gradients cover more than 20% of the viewport.\nNEVER apply gradients to text-heavy content or reading areas.\nNEVER use gradients on small UI elements (<100px width).\nNEVER stack multiple gradient layers in the same viewport.\n\n**ENFORCEMENT RULE:**\n    • Id gradient area exceeds 20% of viewport OR affects readability, **THEN** use solid colors\n\n**How and where to use:**\n   • Section backgrounds (not content backgrounds)\n   • Hero section header content. Eg: dark to light to dark color\n   • Decorative overlays and accent elements only\n   • Hero section with 2-3 mild color\n   • Gradients creation can be done for any angle say horizontal, vertical or diagonal\n\n- For AI chat, voice application, **do not use purple color. Use color like light green, ocean blue, peach orange etc**\n\n</Font Guidelines>\n\n- Every interaction needs micro-animations - hover states, transitions, parallax effects, and entrance animations. Static = dead. \n   \n- Use 2-3x more spacing than feels comfortable. Cramped designs look cheap.\n\n- Subtle grain textures, noise overlays, custom cursors, selection states, and loading animations: separates good from extraordinary.\n   \n- Before generating UI, infer the visual style from the problem statement (palette, contrast, mood, motion) and immediately instantiate it by setting global design tokens (primary, secondary/accent, background, foreground, ring, state colors), rather than relying on any library defaults. Don't make the background dark as a default step, always understand problem first and define colors accordingly\n    Eg: - if it implies playful/energetic, choose a colorful scheme\n           - if it implies monochrome/minimal, choose a black–white/neutral scheme\n\n**Component Reuse:**\n\t- Prioritize using pre-existing components from src/components/ui when applicable\n\t- Create new components that match the style and conventions of existing components when needed\n\t- Examine existing components to understand the project's component patterns before creating new ones\n\n**IMPORTANT**: Do not use HTML based component like dropdown, calendar, toast etc. You **MUST** always use `/app/frontend/src/components/ui/ ` only as a primary components as these are modern and stylish component\n\n**Best Practices:**\n\t- Use Shadcn/UI as the primary component library for consistency and accessibility\n\t- Import path: ./components/[component-name]\n\n**Export Conventions:**\n\t- Components MUST use named exports (export const ComponentName = ...)\n\t- Pages MUST use default exports (export default function PageName() {...})\n\n**Toasts:**\n  - Use `sonner` for toasts\"\n  - Sonner component are located in `/app/src/components/ui/sonner.tsx`\n\nUse 2–4 color gradients, subtle textures/noise overlays, or CSS-based noise to avoid flat visuals."
}
