"""
FaizZab content packs — approved standards + toolkit manifests + document
template specs (deterministic, template-driven; no uncontrolled AI free-text).

Each spec is consumed by toolkit_engine to produce DOCX / XLSX / PDF.
Variables use {{org.*}}, {{roles.*}}, {{doc_control.*}} tokens resolved at
generation time from approved onboarding data + brand profile.

This pack is intentionally rich: ~50+ artifacts per standard covering policies,
procedures, registers, audit packs, forms, plans, matrices and checklists.
"""
from __future__ import annotations
from typing import Any, Dict, List

# --------------------------------------------------------------------------- #
# Standard metadata
# --------------------------------------------------------------------------- #
STANDARDS: List[Dict[str, Any]] = [
    {
        "slug": "iso-27001", "code": "ISO/IEC 27001", "version": "2022",
        "name": "ISO/IEC 27001:2022 — Information Security Management",
        "short": "Information Security Management System (ISMS)",
        "purpose": "Establish, implement, maintain and continually improve an information security "
                   "management system to protect the confidentiality, integrity and availability of information.",
        "intended_for": "Any organization that wants to manage information security risks systematically — "
                        "especially IT, SaaS, cybersecurity and data-driven businesses.",
        "industries": ["Information Technology", "SaaS", "Cybersecurity", "Professional Consulting", "Financial Services"],
        "doc_prefix": "ISMS", "legal_disclaimer": "", "accent": "#1F3A5F",
    },
    {
        "slug": "dpdpa", "code": "India DPDP Act", "version": "2023 + Rules 2025",
        "name": "India DPDP Act 2023 & DPDP Rules 2025 — Data Protection Toolkit",
        "short": "Digital Personal Data Protection readiness",
        "purpose": "Help organizations act responsibly as a Data Fiduciary under India's Digital Personal "
                   "Data Protection Act, 2023 and the DPDP Rules, 2025.",
        "intended_for": "Any organization processing digital personal data of individuals in India, "
                        "including e-commerce, SaaS, healthcare, education and financial services.",
        "industries": ["SaaS", "E-commerce and Retail", "Healthcare", "Education", "Financial Services"],
        "doc_prefix": "DPDP",
        "legal_disclaimer": "This toolkit assists with DPDP Act readiness and does NOT constitute legal "
                            "advice. Independent legal review is required before relying on any document.",
        "accent": "#0F766E",
    },
    {
        "slug": "iso-9001", "code": "ISO 9001", "version": "2015",
        "name": "ISO 9001:2015 — Quality Management System",
        "short": "Quality Management System (QMS)",
        "purpose": "Establish a quality management system that consistently meets customer and regulatory "
                   "requirements and drives continual improvement.",
        "intended_for": "Any organization wanting to demonstrate consistent quality and customer satisfaction — "
                        "manufacturing, services, logistics and more.",
        "industries": ["Manufacturing", "Logistics", "Professional Consulting", "E-commerce and Retail", "Education"],
        "doc_prefix": "QMS", "legal_disclaimer": "", "accent": "#7C3F1D",
    },
]

TEMPLATE_CLASSES = [
    "Mandatory documented information", "Conditionally mandatory", "Core implementation document",
    "Recommended document", "Operational record", "Audit evidence template",
]

MANDATORY = "Mandatory documented information"
CORE = "Core implementation document"
RECOMMENDED = "Recommended document"
RECORD = "Operational record"
EVIDENCE = "Audit evidence template"


# --------------------------------------------------------------------------- #
# Compact DSL
# --------------------------------------------------------------------------- #
def S(heading: str, body: str, mandatory: bool = False, bullets: List[str] | None = None) -> Dict[str, Any]:
    d = {"heading": heading, "body": body, "mandatory": mandatory}
    if bullets:
        d["bullets"] = bullets
    return d


def _std_name(std):
    return f"{std['code']} {std['version']}"


def D(std, kind, num, title, clause, tclass, klass, category, purpose, owner, secs,
      kpis=None, ncs=None, aqs=None, related=None, disclaimer=None):
    """Build a DOCX document spec (auto-enriched with full controlled structure)."""
    d = {
        "doc_id": f"{std['doc_prefix']}-{kind}-{num:03d}",
        "title": title, "standard": _std_name(std), "format": "docx", "category": category,
        "template_class": tclass, "classification": klass, "purpose": purpose,
        "clause_refs": clause if isinstance(clause, list) else [clause],
        "owner_role": owner, "sections": list(secs),
    }
    if kpis: d["kpis"] = kpis
    if ncs: d["common_nonconformities"] = ncs
    if aqs: d["audit_questions"] = aqs
    if related: d["related_documents"] = related
    if disclaimer: d["disclaimer"] = disclaimer
    _enrich(d)
    return d


def _enrich(d: Dict[str, Any]) -> None:
    """Add the full controlled document structure so every document is rich,
    multi-page and genuinely useful (applies to policies, procedures, forms, etc.)."""
    secs = d["sections"]
    headings = {s["heading"].lower() for s in secs}
    owner = d.get("owner_role", "the Document Owner")

    def has(*words):
        return any(any(w in h for w in words) for h in headings)

    # Ensure a Scope section
    if not has("scope"):
        secs.append(S("Scope", "This document applies across {{org.legal_name}} (trading as {{org.trade_name}}), "
                     "covering the personnel, processes, locations ({{org.locations}}) and technologies within the "
                     "defined management-system scope. Where activities are outsourced, the organization remains "
                     "responsible for ensuring the requirements of this document are met."))

    # Definitions
    if not has("definition"):
        secs.append(S("Definitions", "For the purposes of this document the following definitions apply:", bullets=[
            "Organization — {{org.legal_name}}, trading as {{org.trade_name}}.",
            "Top management — the person or group who directs and controls the organization at the highest level "
            "({{roles.top_management}}).",
            "Documented information — information required to be controlled and maintained, and its medium.",
            "Nonconformity — non-fulfilment of a requirement.",
            "Corrective action — action to eliminate the cause of a nonconformity and prevent recurrence.",
            "Interested party — a person or organization that can affect, be affected by, or perceive itself to be "
            "affected by a decision or activity.",
        ]))

    # Roles & Responsibilities (as a table the engine renders)
    if "responsibilities" not in d and not has("roles", "responsib"):
        d["responsibilities"] = [
            ("{{roles.top_management}}", "Provide leadership, approve this document and ensure adequate resources."),
            (owner, "Own, maintain and communicate this document and ensure it is implemented and reviewed."),
            ("{{roles.internal_auditor}}", "Independently audit conformity with this document and report findings."),
            ("All personnel", "Understand and comply with the requirements relevant to their role and report issues."),
        ]

    # Implementation Guidance
    if not has("implementation", "guidance"):
        secs.append(S("Implementation Guidance", "Practical steps for {{org.trade_name}} to implement this document "
                     "effectively, proportionate to an organization of approximately {{org.employee_count}} people:", bullets=[
            "Assign the document owner and confirm responsibilities with the individuals named above.",
            "Communicate the document to affected personnel and provide any training that is required.",
            "Put the described controls and steps into day-to-day operation and integrate them with existing tools.",
            "Create and retain the records and evidence listed below as proof of operation.",
            "Review the document at the planned frequency and after any significant change to the organization.",
            "Where roles are combined in a smaller organization, preserve independence for audit and approval activities.",
        ]))

    # Records & Evidence
    if not has("record", "evidence"):
        secs.append(S("Records and Evidence Expected", "The following records demonstrate that this document is "
                     "effectively implemented and are expected to be available during an audit:", bullets=[
            "Approved, version-controlled copy of this document (see the Master Document Register).",
            "Communication and awareness records showing relevant personnel were informed.",
            "Completed registers, logs or forms referenced within this document.",
            "Review history showing the document is current and fit for purpose.",
        ]))

    # Exceptions & Escalation
    if not has("exception", "escalation"):
        secs.append(S("Exceptions and Escalation", "Any exception to this document must be risk-assessed, documented "
                     "and approved by {{roles.top_management}} for a defined period. Issues, breaches or uncertainties "
                     "relating to this document must be escalated to " + owner + " and, where significant, to top management."))

    # Defaults for the summary/audit sections
    d.setdefault("kpis", [
        "Percentage of relevant personnel aware of this document (target 100%).",
        "This document reviewed within its defined review period (target: on time).",
        "Number of nonconformities related to this area (target: reducing trend).",
    ])
    d.setdefault("common_nonconformities", [
        "Document not formally approved or not communicated to affected personnel.",
        "No objective evidence that the document is being implemented in practice.",
        "Document not reviewed within its defined review period.",
        "Records or registers referenced in this document not maintained.",
    ])
    d.setdefault("audit_questions", [
        "Is this document approved, version-controlled and available to those who need it?",
        "Can personnel describe how its requirements apply to their day-to-day work?",
        "Is there objective evidence that the document is being followed?",
        "Has the document been reviewed and kept up to date after changes?",
    ])
    d.setdefault("related_documents", [
        "{{org.trade_name}} Management System Manual", "Master Document Register",
        "Internal Audit Programme", "Corrective Action Register",
    ])


def R(std, num, title, sheet, clause, tclass, cols, rows=None, category="register", kind="REG"):
    """Build an XLSX register / matrix / checklist spec. cols: list of (label,key,width)."""
    return {
        "doc_id": f"{std['doc_prefix']}-{kind}-{num:03d}",
        "title": title, "standard": _std_name(std), "format": "xlsx", "category": category,
        "template_class": tclass, "classification": "Internal", "purpose": f"{title}.",
        "clause_refs": [clause], "sheet_name": sheet,
        "columns": [{"label": l, "key": k, "width": w} for (l, k, w) in cols],
        "rows": rows or [],
    }


# --------------------------------------------------------------------------- #
# Common management-system documents (apply to all standards)
# --------------------------------------------------------------------------- #
def _common_docs(std) -> List[Dict[str, Any]]:
    sn = _std_name(std)
    sh = std["short"]
    docs: List[Dict[str, Any]] = []

    docs.append(D(std, "MAN", 1, f"{sh} Manual", ["4", "5", "6"], CORE, "Confidential", "manual",
        f"Top-level description of the {sh}.", "{{roles.ms_coordinator}}", [
        S("Purpose", f"This manual describes the {sh} implemented by {{{{org.legal_name}}}} to meet the "
          f"requirements of {sn} across {{{{org.locations}}}}.", True),
        S("Context", "{{org.trade_name}} operates in the {{org.industry}} sector delivering "
          "{{org.products_services}}. Relevant internal and external issues are recorded in the Context Register.", True),
        S("Scope", "The scope covers the services, processes, locations and technologies defined during onboarding.", True),
        S("Leadership", "Top management ({{roles.top_management}}) provides leadership, resources and direction.", True),
        S("Process Approach", "The organization adopts the Plan-Do-Check-Act cycle for continual improvement."),
    ], kpis=["Management review held at planned intervals.", "≥80% of objectives achieved."],
       aqs=["Is the scope documented?", "Can top management demonstrate commitment?"],
       related=["Management System Policy", "Scope Statement"]))

    docs.append(D(std, "POL", 1, f"{sh} Policy", ["5.2"], MANDATORY, "{{doc_control.classification}}", "policy",
        "Top-management commitment statement.", "{{roles.top_management}}", [
        S("Policy Statement", f"{{{{org.legal_name}}}} is committed to {std['purpose']}", True),
        S("Commitments", "{{org.trade_name}} commits to:", True, [
            "Satisfy applicable legal, regulatory and contractual requirements.",
            "Set and review measurable objectives.", "Provide adequate resources and competent people.",
            "Continually improve the management system."]),
        S("Communication", "This policy is communicated to all personnel and available to interested parties."),
    ], aqs=["Is the policy approved by top management?", "Is it communicated and available?"]))

    docs.append(D(std, "DOC", 2, "Management System Scope Statement", ["4.3"], MANDATORY, "Internal", "policy",
        "Boundaries and applicability of the management system.", "{{roles.ms_coordinator}}", [
        S("Scope", "The management system applies to {{org.products_services}} at {{org.locations}}.", True),
        S("Boundaries", "Considers internal/external issues, interested-party needs and interfaces.", True),
        S("Exclusions", "Exclusions and justification are recorded based on the onboarding declaration."),
    ], related=["Context of the Organization Register", "Interested Parties Register"]))

    docs.append(R(std, 1, "Context of the Organization Register", "Context", "4.1", MANDATORY, [
        ("Issue Type", "type", 16), ("Description", "desc", 44), ("Impact on MS", "impact", 30), ("Action", "act", 26)],
        [{"type": "Internal", "desc": "Skills and resource availability at {{org.trade_name}}", "impact": "Medium", "act": "Training plan"},
         {"type": "External", "desc": "Regulatory change in {{org.industry}}", "impact": "High", "act": "Monitor legal register"}]))

    docs.append(R(std, 2, "Interested Parties Register", "Interested Parties", "4.2", MANDATORY, [
        ("Interested Party", "party", 26), ("Needs & Expectations", "needs", 42), ("Requirement Type", "type", 18), ("How Addressed", "addr", 30)],
        [{"party": "Customers of {{org.trade_name}}", "needs": "Reliable, secure delivery of {{org.products_services}}", "type": "Contractual", "addr": "Agreements & controls"},
         {"party": "Employees", "needs": "Safe workplace, clear responsibilities", "type": "Legal", "addr": "Policies & training"},
         {"party": "Regulators", "needs": "Compliance with applicable law", "type": "Statutory", "addr": "Legal register"}]))

    docs.append(R(std, 3, "Legal and Other Requirements Register", "Legal", "6.1", MANDATORY, [
        ("Ref", "id", 10), ("Requirement", "req", 40), ("Source", "src", 24), ("Applicability", "app", 20), ("Compliance Status", "st", 18)],
        [{"id": "L-001", "req": "Applicable law in {{org.industry}}", "src": "Statute", "app": "{{org.trade_name}}", "st": "Compliant"}]))

    docs.append(R(std, 3 + 100, "Roles and Responsibilities Matrix", "Roles", "5.3", MANDATORY, [
        ("Role", "role", 28), ("Responsibility", "resp", 46), ("Authority", "auth", 26)],
        [{"role": "{{roles.top_management}}", "resp": "Accountability & resources", "auth": "Approve policy"},
         {"role": "{{roles.ms_coordinator}}", "resp": "Operate & maintain the MS", "auth": "Coordinate activities"},
         {"role": "{{roles.internal_auditor}}", "resp": "Independent audits", "auth": "Report findings"}], kind="DOC"))

    docs.append(R(std, 4, "Objectives and KPI Register", "Objectives", "6.2", MANDATORY, [
        ("Objective", "o", 36), ("KPI", "k", 28), ("Target", "t", 14), ("Owner", "ow", 22), ("Status", "s", 14)],
        [{"o": "Improve MS performance", "k": "Objectives achieved %", "t": "≥80%", "ow": "{{roles.ms_coordinator}}", "s": "In progress"}]))

    docs.append(D(std, "PROC", 1, "Risk and Opportunity Methodology", ["6.1"], MANDATORY, "Internal", "procedure",
        "Method for identifying, analysing and evaluating risks and opportunities.", "{{roles.ms_coordinator}}", [
        S("Purpose", "Defines how {{org.trade_name}} assesses risks and opportunities for its MS.", True),
        S("Criteria", "Risk = likelihood × impact on defined scales. Acceptance criteria approved by top management.", True),
        S("Treatment", "Options: modify, retain, avoid or share. Actions tracked in the Risk Register."),
    ], related=["Risk and Opportunity Register"]))

    docs.append(R(std, 5, "Risk and Opportunity Register", "Risks", "6.1", RECORD, [
        ("Risk ID", "id", 12), ("Area", "a", 26), ("Risk/Opportunity", "r", 30), ("L", "l", 8), ("I", "i", 8),
        ("Level", "lv", 12), ("Treatment", "t", 28), ("Owner", "o", 20)],
        [{"id": "R-001", "a": "Customer data — {{org.trade_name}}", "r": "Unauthorized access", "l": "M", "i": "H",
          "lv": "High", "t": "Access control + MFA", "o": "{{roles.ms_coordinator}}"}]))

    docs.append(D(std, "PROC", 2, "Competence and Training Procedure", ["7.2"], CORE, "Internal", "procedure",
        "Ensures personnel are competent for their roles.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To ensure staff of {{org.trade_name}} have the competence needed for the MS.", True),
        S("Training", "Needs are identified in the Training Needs Matrix; records are retained.", True),
    ], related=["Training Needs Matrix"]))

    docs.append(R(std, 6, "Training Needs Matrix", "Training", "7.2", RECORD, [
        ("Employee", "e", 24), ("Role", "r", 22), ("Required Training", "t", 34), ("Due", "d", 14), ("Status", "s", 14)],
        [{"e": "Sample", "r": "Staff", "t": "MS awareness", "d": "Q1", "s": "Planned"}]))

    docs.append(D(std, "PROC", 3, "Communication Procedure", ["7.4"], CORE, "Internal", "procedure",
        "Internal and external communication relevant to the MS.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To manage MS communications at {{org.trade_name}}.", True),
        S("What/When/Whom", "Communications are defined in the Communication Matrix.", True)],
        related=["Communication Matrix"]))

    docs.append(R(std, 7, "Communication Matrix", "Communication", "7.4", RECORD, [
        ("What", "w", 30), ("When", "when", 16), ("Audience", "a", 24), ("Method", "m", 20), ("Owner", "o", 20)],
        [{"w": "Policy updates", "when": "On change", "a": "All staff", "m": "Email", "o": "{{roles.ms_coordinator}}"}]))

    docs.append(D(std, "PROC", 4, "Documented Information Control Procedure", ["7.5"], MANDATORY, "Internal", "procedure",
        "Control of documents and records.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To control creation, approval, distribution and retention of documented information.", True),
        S("Control", "Documents carry ID, version and classification; changes are reviewed and approved.", True)],
        related=["Master Document Register", "Record Retention Register"]))

    docs.append(R(std, 8, "Master Document Register", "Documents", "7.5", MANDATORY, [
        ("Doc ID", "id", 14), ("Title", "t", 40), ("Owner", "o", 22), ("Version", "v", 10),
        ("Classification", "c", 16), ("Review Date", "r", 16)]))

    docs.append(R(std, 9, "Record Retention Register", "Retention", "7.5", RECORD, [
        ("Record", "r", 34), ("Owner", "o", 22), ("Retention Period", "p", 20), ("Disposal Method", "d", 22)],
        [{"r": "Audit records", "o": "{{roles.internal_auditor}}", "p": "3 years", "d": "Secure deletion"}]))

    docs.append(D(std, "PROC", 5, "Change Management Procedure", ["6.3", "8.1"], CORE, "Internal", "procedure",
        "How changes to the MS and operations are controlled.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To manage changes at {{org.trade_name}} without adverse effect on the MS.", True),
        S("Process", "Changes are requested, assessed for risk, approved, implemented and reviewed.", True)]))

    docs.append(D(std, "PROC", 6, "Supplier Management Procedure", ["8.4"], CORE, "Internal", "procedure",
        "Selection, evaluation and monitoring of external providers.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To control external providers relevant to {{org.products_services}}.", True),
        S("Evaluation", "Suppliers are evaluated before use and monitored periodically.", True)],
        related=["Supplier / Approved Vendor Register"]))

    # Internal audit pack
    docs.append(D(std, "PROC", 7, "Internal Audit Procedure", ["9.2"], MANDATORY, "Internal", "procedure",
        "How internal audits are planned, conducted and reported.", "{{roles.internal_auditor}}", [
        S("Purpose", f"To verify the MS conforms to {sn} and is effectively implemented.", True),
        S("Programme", "A risk-based annual programme is maintained by {{roles.internal_auditor}}.", True),
        S("Conduct & Report", "Auditors are independent; findings are classified and tracked to closure.", True)],
        aqs=["Is there an audit programme?", "Are auditors impartial?"],
        related=["Internal Audit Programme", "Internal Audit Checklist", "Internal Audit Report"]))

    docs.append(R(std, 1, "Internal Audit Programme", "Programme", "9.2", EVIDENCE, [
        ("Audit #", "n", 10), ("Area/Process", "a", 30), ("Planned Date", "d", 16), ("Auditor", "au", 22), ("Status", "s", 14)],
        [{"n": "1", "a": "Whole MS", "d": "Q2", "au": "{{roles.internal_auditor}}", "s": "Planned"}], category="checklist", kind="PLAN"))

    docs.append(R(std, 1, "Internal Audit Checklist", "Checklist", "9.2", EVIDENCE, [
        ("#", "n", 6), ("Requirement / Clause", "req", 44), ("Evidence Seen", "ev", 34), ("Result", "res", 16)],
        [{"n": 1, "req": "Scope documented", "ev": "", "res": "Pending"},
         {"n": 2, "req": "Policy approved", "ev": "", "res": "Pending"},
         {"n": 3, "req": "Risks assessed", "ev": "", "res": "Pending"}], category="checklist", kind="CHK"))

    docs.append(D(std, "FORM", 1, "Internal Audit Report", ["9.2"], EVIDENCE, "Internal", "form",
        "Template to report internal audit results.", "{{roles.internal_auditor}}", [
        S("Audit Summary", "Audit of {{org.trade_name}} MS conducted on ____. Scope: ____.", True),
        S("Findings", "Record conformities, nonconformities and observations.", True),
        S("Conclusion", "Overall the MS is / is not effectively implemented.")]))

    docs.append(D(std, "PROC", 8, "Management Review Procedure", ["9.3"], MANDATORY, "Internal", "procedure",
        "How top management reviews the MS.", "{{roles.top_management}}", [
        S("Purpose", "To ensure the MS remains suitable, adequate and effective.", True),
        S("Inputs", "Audit results, objectives, nonconformities, risks and improvement opportunities.", True),
        S("Outputs", "Decisions recorded in Management Review Minutes.", True)],
        related=["Management Review Minutes"]))

    docs.append(D(std, "FORM", 2, "Management Review Minutes", ["9.3"], EVIDENCE, "Internal", "form",
        "Template to record management review outcomes.", "{{roles.top_management}}", [
        S("Attendees & Date", "Recorded here.", True),
        S("Review of Inputs", "Summary of each required input.", True),
        S("Decisions & Actions", "Improvement, resource and change decisions with owners and dates.", True)]))

    docs.append(D(std, "PROC", 9, "Nonconformity and Corrective Action Procedure", ["10.2"], MANDATORY, "Internal", "procedure",
        "How nonconformities and corrective actions are handled.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To react to nonconformities and eliminate their causes at {{org.trade_name}}.", True),
        S("Root Cause", "Causes are investigated before corrective action is defined.", True),
        S("Effectiveness", "Effectiveness is reviewed and recorded.", True)],
        related=["Corrective Action Register"]))

    docs.append(R(std, 10, "Corrective Action Register", "CAPA", "10.2", RECORD, [
        ("CAR ID", "id", 12), ("Nonconformity", "nc", 34), ("Root Cause", "rc", 28), ("Action", "a", 28), ("Owner", "o", 20), ("Status", "s", 14)]))

    docs.append(R(std, 11, "Continual Improvement Register", "Improvement", "10.1", RECORD, [
        ("ID", "id", 10), ("Improvement", "i", 40), ("Benefit", "b", 26), ("Owner", "o", 20), ("Status", "s", 14)]))

    docs.append(R(std, 2, "Certification Readiness Checklist", "Readiness", "All", EVIDENCE, [
        ("#", "n", 6), ("Requirement", "req", 50), ("Evidence Expected", "ev", 40), ("Status", "st", 16)],
        [{"n": 1, "req": "Scope defined and documented", "ev": "Scope Statement", "st": "Pending"},
         {"n": 2, "req": "Policy approved by top management", "ev": "Signed policy", "st": "Pending"},
         {"n": 3, "req": "Risks assessed and treated", "ev": "Risk register", "st": "Pending"},
         {"n": 4, "req": "Internal audit conducted", "ev": "Audit report", "st": "Pending"},
         {"n": 5, "req": "Management review conducted", "ev": "Review minutes", "st": "Pending"}], category="checklist", kind="CHK"))

    docs.append(R(std, 2, "Implementation Project Plan", "Plan", "All", RECOMMENDED, [
        ("Phase", "p", 26), ("Activity", "a", 40), ("Owner", "o", 22), ("Target Date", "d", 16), ("Status", "s", 14)],
        [{"p": "Establish", "a": "Define scope & policy", "o": "{{roles.ms_coordinator}}", "d": "Month 1", "s": "Planned"},
         {"p": "Implement", "a": "Roll out procedures", "o": "{{roles.ms_coordinator}}", "d": "Month 2-3", "s": "Planned"},
         {"p": "Audit", "a": "Internal audit & review", "o": "{{roles.internal_auditor}}", "d": "Month 4", "s": "Planned"}], category="checklist", kind="PLAN"))

    docs.append(R(std, 12, "Evidence Index", "Evidence", "All", EVIDENCE, [
        ("Requirement", "r", 40), ("Evidence / Document", "e", 40), ("Location", "l", 24)]))

    docs.append(R(std, 13, "Clause-to-Document Matrix", "Matrix", "All", EVIDENCE, [
        ("Clause", "c", 14), ("Requirement", "r", 44), ("Document(s)", "d", 40)]))

    return docs


# --------------------------------------------------------------------------- #
# ISO 27001 specific
# --------------------------------------------------------------------------- #
def _iso27001(std) -> List[Dict[str, Any]]:
    d = []
    d.append(D(std, "PROC", 20, "Information Security Risk Assessment Methodology", ["6.1.2"], MANDATORY, "Confidential", "procedure",
        "Method for assessing information security risks.", "{{roles.security_contact}}", [
        S("Purpose", "Defines how {{org.trade_name}} assesses information security risks to its assets.", True),
        S("Risk Criteria", "Likelihood and impact scales; acceptance criteria approved by {{roles.top_management}}.", True),
        S("Treatment", "Controls selected from Annex A and justified in the Statement of Applicability.", True)],
        related=["Information Security Risk Register", "Statement of Applicability"]))
    d.append(R(std, 20, "Information Security Risk Register", "InfoSec Risks", "6.1.2", RECORD, [
        ("Risk ID", "id", 12), ("Asset", "a", 26), ("Threat", "th", 26), ("Vulnerability", "v", 24),
        ("L", "l", 8), ("I", "i", 8), ("Level", "lv", 12), ("Treatment", "t", 26), ("Owner", "o", 20)],
        [{"id": "IR-001", "a": "Customer data", "th": "Unauthorized access", "v": "Weak access control",
          "l": "M", "i": "H", "lv": "High", "t": "MFA + least privilege", "o": "{{roles.security_contact}}"}]))
    d.append(D(std, "DOC", 20, "Risk Treatment Plan", ["6.1.3"], MANDATORY, "Confidential", "policy",
        "Plan of controls to treat identified information security risks.", "{{roles.security_contact}}", [
        S("Purpose", "Documents how {{org.trade_name}} treats each risk above the acceptance threshold.", True),
        S("Controls", "Each treatment references Annex A controls, owner and target date.", True)]))
    d.append(R(std, 21, "Statement of Applicability (SoA)", "SoA", "6.1.3", MANDATORY, [
        ("Control", "c", 12), ("Title", "t", 40), ("Applicable", "a", 14), ("Justification", "j", 40), ("Status", "s", 16)],
        [{"c": "A.5.1", "t": "Policies for information security", "a": "Yes", "j": "Required", "s": "Implemented"},
         {"c": "A.5.15", "t": "Access control", "a": "Yes", "j": "Systems require control", "s": "Planned"},
         {"c": "A.8.24", "t": "Use of cryptography", "a": "Conditional", "j": "If sensitive data stored", "s": "Review"}]))
    d.append(D(std, "POL", 20, "Access Control Policy", ["A.5.15", "A.8.3"], CORE, "Confidential", "policy",
        "Rules for granting, reviewing and revoking access.", "{{roles.security_contact}}", [
        S("Purpose", "To control access to information and systems on least-privilege and need-to-know basis.", True),
        S("Provisioning", "Access is role-based, owner-approved and reviewed periodically.", True),
        S("Authentication", "MFA is required for remote and privileged access.", True)],
        kpis=["% privileged accounts with MFA (target 100%).", "Access reviews completed on schedule."],
        related=["Access Rights Register"]))
    d.append(R(std, 22, "Access Rights Register", "Access", "A.5.18", RECORD, [
        ("User", "u", 24), ("Role", "r", 20), ("System", "s", 24), ("Access Level", "a", 18), ("Reviewed", "rev", 14)]))
    d.append(D(std, "POL", 21, "Asset Management Policy", ["A.5.9"], CORE, "Confidential", "policy",
        "Identification and handling of information assets.", "{{roles.security_contact}}", [
        S("Purpose", "To ensure information assets of {{org.trade_name}} are identified and protected.", True),
        S("Ownership", "Each asset has an owner and classification in the Asset Register.", True)],
        related=["Information Asset Register"]))
    d.append(R(std, 23, "Information Asset Register", "Assets", "A.5.9", MANDATORY, [
        ("Asset ID", "id", 12), ("Asset", "a", 30), ("Type", "t", 16), ("Owner", "o", 22), ("Classification", "c", 16), ("Location", "l", 22)],
        [{"id": "AST-001", "a": "Customer database", "t": "Information", "o": "{{roles.security_contact}}", "c": "Confidential", "l": "{{org.locations}}"}]))
    d.append(D(std, "POL", 22, "Acceptable Use Policy", ["A.5.10"], CORE, "Internal", "policy",
        "Rules for acceptable use of information and assets.", "{{roles.security_contact}}", [
        S("Purpose", "To define acceptable use of {{org.trade_name}} information, systems and devices.", True),
        S("Rules", "Users must protect credentials, avoid unauthorized software and report incidents.", True)]))
    d.append(D(std, "POL", 23, "Cryptography Policy", ["A.8.24"], CORE, "Confidential", "policy",
        "Use and management of cryptographic controls.", "{{roles.security_contact}}", [
        S("Purpose", "To protect information using appropriate cryptography.", True),
        S("Key Management", "Keys are generated, stored and rotated securely.", True)]))
    d.append(D(std, "POL", 24, "Backup Policy", ["A.8.13"], CORE, "Internal", "policy",
        "Backup and restoration of information.", "{{roles.security_contact}}", [
        S("Purpose", "To ensure {{org.trade_name}} can recover information after loss.", True),
        S("Backups", "Backups follow defined frequency, retention and are tested for restoration.", True)]))
    d.append(D(std, "PROC", 21, "Logging and Monitoring Procedure", ["A.8.15", "A.8.16"], CORE, "Confidential", "procedure",
        "Logging of events and monitoring for anomalies.", "{{roles.security_contact}}", [
        S("Purpose", "To detect and investigate security events at {{org.trade_name}}.", True),
        S("Logging", "Relevant events are logged, protected and reviewed.", True)]))
    d.append(D(std, "PROC", 22, "Vulnerability Management Procedure", ["A.8.8"], CORE, "Confidential", "procedure",
        "Identification and remediation of technical vulnerabilities.", "{{roles.security_contact}}", [
        S("Purpose", "To manage technical vulnerabilities in {{org.trade_name}} systems.", True),
        S("Process", "Vulnerabilities are identified, prioritized by risk and remediated within SLA.", True)]))
    d.append(D(std, "PROC", 23, "Malware Protection Procedure", ["A.8.7"], CORE, "Internal", "procedure",
        "Protection against malware.", "{{roles.security_contact}}", [
        S("Purpose", "To protect systems from malicious software.", True),
        S("Controls", "Endpoint protection, updates and user awareness are maintained.", True)]))
    d.append(D(std, "PROC", 24, "Information Security Incident Management Procedure", ["A.5.24", "A.5.26"], MANDATORY, "Confidential", "procedure",
        "How security incidents are reported and resolved.", "{{roles.security_contact}}", [
        S("Purpose", "To ensure a consistent approach to managing security incidents.", True),
        S("Reporting", "Staff report suspected incidents to {{roles.security_contact}} promptly.", True),
        S("Response", "Incidents are triaged, contained, eradicated, recovered and reviewed.", True)],
        related=["Information Security Incident Register"]))
    d.append(R(std, 24, "Information Security Incident Register", "Incidents", "A.5.24", RECORD, [
        ("Incident ID", "id", 12), ("Date", "d", 14), ("Description", "desc", 40), ("Severity", "sev", 12), ("Status", "st", 14)]))
    d.append(D(std, "PROC", 25, "Supplier Security Procedure", ["A.5.19", "A.5.21"], CORE, "Confidential", "procedure",
        "Security requirements for suppliers.", "{{roles.security_contact}}", [
        S("Purpose", "To manage information security risks from suppliers of {{org.trade_name}}.", True),
        S("Requirements", "Suppliers are assessed for security and bound by agreements.", True)],
        related=["Supplier Risk Register"]))
    d.append(R(std, 25, "Supplier Risk Register", "Suppliers", "A.5.19", RECORD, [
        ("Supplier", "s", 28), ("Service", "sv", 26), ("Data Accessed", "da", 24), ("Risk", "r", 14), ("Status", "st", 14)]))
    d.append(D(std, "POL", 25, "Secure Development Policy", ["A.8.25"], RECOMMENDED, "Confidential", "policy",
        "Security in the software development lifecycle.", "{{roles.security_contact}}", [
        S("Purpose", "To build security into development at {{org.trade_name}}.", True),
        S("Practices", "Secure coding, code review, testing and separation of environments are required.", True)]))
    d.append(D(std, "PROC", 26, "Business Continuity Procedure", ["A.5.29", "A.5.30"], CORE, "Confidential", "procedure",
        "Continuity of information security during disruption.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To maintain security and recover operations during disruption.", True),
        S("Strategy", "Critical activities, recovery objectives and DR steps are defined and tested.", True)]))
    d.append(D(std, "PROC", 27, "Physical and Environmental Security Procedure", ["A.7.1"], CORE, "Internal", "procedure",
        "Protection of physical premises and equipment.", "{{roles.security_contact}}", [
        S("Purpose", "To protect {{org.locations}} and equipment from physical threats.", True),
        S("Controls", "Access to secure areas is restricted, monitored and logged.", True)]))
    d.append(D(std, "PROC", 28, "Human Resource Security Procedure", ["A.6.1"], CORE, "Confidential", "procedure",
        "Security before, during and after employment.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To manage security responsibilities of personnel.", True),
        S("Lifecycle", "Screening, terms, awareness, disciplinary process and off-boarding are defined.", True)]))
    d.append(D(std, "PROC", 29, "Data Classification Procedure", ["A.5.12"], CORE, "Confidential", "procedure",
        "Classification and labelling of information.", "{{roles.security_contact}}", [
        S("Purpose", "To classify information of {{org.trade_name}} by sensitivity.", True),
        S("Levels", "Public, Internal, Confidential, Restricted with handling rules.", True)]))
    d.append(D(std, "PROC", 30, "Data Retention and Disposal Procedure", ["A.8.10"], CORE, "Internal", "procedure",
        "Retention and secure disposal of information.", "{{roles.security_contact}}", [
        S("Purpose", "To retain and dispose of information appropriately.", True),
        S("Disposal", "Media is securely wiped or destroyed and recorded.", True)]))
    d.append(D(std, "POL", 26, "Remote Working Policy", ["A.6.7"], CORE, "Internal", "policy",
        "Security for remote and hybrid work.", "{{roles.security_contact}}", [
        S("Purpose", "To secure remote work at {{org.trade_name}}.", True),
        S("Controls", "Secure connectivity, device controls and physical precautions apply.", True)]))
    d.append(D(std, "POL", 27, "Mobile Device and Teleworking Policy", ["A.8.1"], RECOMMENDED, "Internal", "policy",
        "Security for mobile devices.", "{{roles.security_contact}}", [
        S("Purpose", "To protect information on mobile devices.", True),
        S("Controls", "Encryption, screen lock and remote wipe are required.", True)]))
    return d


# --------------------------------------------------------------------------- #
# DPDPA specific (all docx carry legal disclaimer)
# --------------------------------------------------------------------------- #
def _dpdpa(std) -> List[Dict[str, Any]]:
    disc = std["legal_disclaimer"]
    d = []
    d.append(D(std, "POL", 20, "Data Protection Governance Policy", ["S.8"], CORE, "Confidential", "policy",
        "How the organization governs personal data as a Data Fiduciary.", "{{roles.privacy_contact}}", [
        S("Purpose", "Sets out how {{org.legal_name}} acts as a Data Fiduciary under the DPDP Act, 2023.", True),
        S("Lawful Processing", "Personal data is processed only for lawful purposes with consent or legitimate use.", True),
        S("Rights", "Data principals may access, correct, erase data and raise grievances.", True)], disclaimer=disc,
        related=["Processing Activity Register", "Data Principal Request Procedure"]))
    d.append(R(std, 20, "Digital Personal Data Inventory", "Data Inventory", "S.5", MANDATORY, [
        ("ID", "id", 10), ("Data Element", "de", 28), ("Category", "c", 20), ("System", "s", 24), ("Sensitivity", "se", 16)],
        [{"id": "D-001", "de": "Customer name & email", "c": "Contact", "s": "CRM", "se": "Normal"}]))
    d.append(R(std, 21, "Processing Activity Register", "Processing", "S.6", MANDATORY, [
        ("Activity ID", "id", 12), ("Activity", "a", 30), ("Purpose", "p", 26), ("Categories", "c", 24), ("Legal Basis", "b", 20), ("Retention", "r", 18)],
        [{"id": "PA-001", "a": "Customer account management", "p": "Service delivery", "c": "Name, email, phone", "b": "Consent", "r": "As per policy"}]))
    d.append(R(std, 3 + 200, "Data Fiduciary Responsibility Matrix", "Responsibilities", "S.8", CORE, [
        ("Obligation", "o", 40), ("Owner", "ow", 24), ("Evidence", "e", 30)],
        [{"o": "Provide notice & obtain consent", "ow": "{{roles.privacy_contact}}", "e": "Notice + consent records"}], kind="DOC"))
    d.append(D(std, "FORM", 20, "Privacy Notice Template", ["S.5"], CORE, "Public", "form",
        "Notice given to data principals at collection.", "{{roles.privacy_contact}}", [
        S("Notice", "{{org.legal_name}} collects your personal data for the purposes described below.", True),
        S("Your Rights", "You may access, correct, erase your data and raise grievances with our contact.", True)], disclaimer=disc))
    d.append(D(std, "FORM", 21, "Consent Request Template", ["S.6"], CORE, "Internal", "form",
        "Template to request consent for processing.", "{{roles.privacy_contact}}", [
        S("Consent", "I consent to {{org.trade_name}} processing my personal data for the stated purposes.", True)], disclaimer=disc))
    d.append(D(std, "PROC", 20, "Consent Withdrawal Procedure", ["S.6"], CORE, "Internal", "procedure",
        "How consent withdrawal is handled.", "{{roles.privacy_contact}}", [
        S("Purpose", "To let data principals withdraw consent as easily as it was given.", True),
        S("Process", "Withdrawal is logged, actioned and confirmed; processing stops where required.", True)], disclaimer=disc))
    d.append(D(std, "PROC", 21, "Data Principal Request Procedure", ["S.11", "S.12", "S.13"], CORE, "Confidential", "procedure",
        "Handling access, correction and erasure requests.", "{{roles.privacy_contact}}", [
        S("Purpose", "To respond to data principal requests within statutory timelines.", True),
        S("Handling", "Requests are logged, verified, actioned and closed with records retained.", True)], disclaimer=disc,
        related=["Access Request Form", "Grievance Register"]))
    d.append(D(std, "FORM", 22, "Access Request Form", ["S.11"], EVIDENCE, "Internal", "form",
        "Form for data principals to request access.", "{{roles.privacy_contact}}", [
        S("Request", "I request access to the personal data {{org.trade_name}} holds about me.", True)], disclaimer=disc))
    d.append(D(std, "FORM", 23, "Correction Request Form", ["S.12"], EVIDENCE, "Internal", "form",
        "Form to request correction of personal data.", "{{roles.privacy_contact}}", [
        S("Request", "I request correction of the following personal data.", True)], disclaimer=disc))
    d.append(D(std, "FORM", 24, "Erasure Request Form", ["S.12"], EVIDENCE, "Internal", "form",
        "Form to request erasure of personal data.", "{{roles.privacy_contact}}", [
        S("Request", "I request erasure of my personal data held by {{org.trade_name}}.", True)], disclaimer=disc))
    d.append(D(std, "PROC", 22, "Grievance Handling Procedure", ["S.13"], CORE, "Internal", "procedure",
        "How grievances are received and resolved.", "{{roles.privacy_contact}}", [
        S("Purpose", "To provide a readily available means to register and resolve grievances.", True),
        S("Process", "Grievances are logged, acknowledged, investigated and resolved within timelines.", True)], disclaimer=disc,
        related=["Grievance Register"]))
    d.append(R(std, 22, "Grievance Register", "Grievances", "S.13", RECORD, [
        ("Ref", "id", 10), ("Data Principal", "d", 24), ("Grievance", "g", 36), ("Received", "r", 16), ("Status", "s", 14)]))
    d.append(D(std, "PLAN", 20, "Personal Data Breach Response Plan", ["S.8(6)"], CORE, "Confidential", "procedure",
        "How personal data breaches are detected, contained and notified.", "{{roles.privacy_contact}}", [
        S("Purpose", "To respond to breaches and notify the Data Protection Board and affected principals.", True),
        S("Steps", "Detect, contain, assess, notify and remediate; record in the Breach Register.", True)], disclaimer=disc,
        related=["Breach Register"]))
    d.append(R(std, 23, "Personal Data Breach Register", "Breaches", "S.8(6)", RECORD, [
        ("Ref", "id", 10), ("Date", "d", 14), ("Description", "desc", 38), ("Affected", "a", 16), ("Notified", "n", 14), ("Status", "s", 14)]))
    d.append(D(std, "DOC", 21, "Data Processor Agreement (Template)", ["S.8(2)"], CORE, "Confidential", "policy",
        "Contractual template binding data processors.", "{{roles.privacy_contact}}", [
        S("Purpose", "To bind processors engaged by {{org.legal_name}} to protect personal data.", True),
        S("Obligations", "Processors process only on instructions and implement security safeguards.", True)], disclaimer=disc))
    d.append(R(std, 20, "Processor Due-Diligence Checklist", "Due Diligence", "S.8(2)", EVIDENCE, [
        ("#", "n", 6), ("Check", "c", 46), ("Evidence", "e", 32), ("Status", "s", 14)],
        [{"n": 1, "c": "Security safeguards in place", "e": "", "s": "Pending"},
         {"n": 2, "c": "Contract includes DPDP obligations", "e": "", "s": "Pending"}], category="checklist", kind="CHK"))
    d.append(D(std, "POL", 21, "Security Safeguards Standard", ["S.8(5)"], CORE, "Confidential", "policy",
        "Reasonable security safeguards for personal data.", "{{roles.privacy_contact}}", [
        S("Purpose", "To protect personal data with reasonable security safeguards.", True),
        S("Safeguards", "Access control, encryption, logging and backups protect personal data.", True)], disclaimer=disc))
    d.append(R(std, 24, "Data Retention and Erasure Schedule", "Retention", "S.8(7)", CORE, [
        ("Data Category", "c", 30), ("Purpose", "p", 26), ("Retention", "r", 18), ("Erasure Method", "e", 24)],
        [{"c": "Customer data", "p": "Service", "r": "As required", "e": "Secure deletion"}]))
    d.append(D(std, "DOC", 22, "Children's Data Processing Assessment", ["S.9"], CORE, "Confidential", "policy",
        "Assessment of processing of children's personal data.", "{{roles.privacy_contact}}", [
        S("Purpose", "To ensure lawful processing of children's data with verifiable parental consent.", True),
        S("Controls", "No tracking/targeted advertising to children; age-gating where applicable.", True)], disclaimer=disc))
    d.append(D(std, "PROC", 23, "Consent Manager Interaction Procedure", ["S.6(7)"], RECOMMENDED, "Internal", "procedure",
        "Interaction with registered Consent Managers.", "{{roles.privacy_contact}}", [
        S("Purpose", "To manage consent through Consent Managers where used.", True),
        S("Process", "Consents received and withdrawals honoured via the Consent Manager are recorded.", True)], disclaimer=disc))
    d.append(R(std, 25, "Data Sharing Register", "Data Sharing", "S.8", RECORD, [
        ("Recipient", "r", 28), ("Data Shared", "d", 28), ("Purpose", "p", 24), ("Safeguard", "s", 24)]))
    d.append(D(std, "DOC", 23, "Cross-Border Transfer Assessment", ["S.16"], CORE, "Confidential", "policy",
        "Assessment of transfers of personal data outside India.", "{{roles.privacy_contact}}", [
        S("Purpose", "To assess and control cross-border transfers of personal data.", True),
        S("Controls", "Transfers occur only to permitted countries with appropriate safeguards.", True)], disclaimer=disc))
    d.append(R(std, 3, "Significant Data Fiduciary Readiness Checklist", "SDF Readiness", "S.10", EVIDENCE, [
        ("#", "n", 6), ("Obligation", "o", 50), ("Status", "s", 16)],
        [{"n": 1, "o": "Appoint Data Protection Officer", "s": "Pending"},
         {"n": 2, "o": "Independent data audit", "s": "Pending"},
         {"n": 3, "o": "Data protection impact assessment", "s": "Pending"}], category="checklist", kind="CHK"))
    d.append(D(std, "DOC", 24, "Privacy Training Material", ["S.8"], RECOMMENDED, "Internal", "manual",
        "Awareness material for staff on DPDP obligations.", "{{roles.privacy_contact}}", [
        S("Overview", "Explains DPDP Act basics and staff responsibilities at {{org.trade_name}}.", True),
        S("Do's and Don'ts", "Collect minimally, protect data and report incidents promptly.", True)], disclaimer=disc))
    d.append(R(std, 26, "Compliance Monitoring Checklist", "Monitoring", "S.8", EVIDENCE, [
        ("#", "n", 6), ("Control", "c", 46), ("Frequency", "f", 16), ("Status", "s", 14)],
        [{"n": 1, "c": "Consent records maintained", "f": "Monthly", "s": "Pending"},
         {"n": 2, "c": "Grievances resolved in time", "f": "Monthly", "s": "Pending"}], category="checklist", kind="CHK"))
    return d


# --------------------------------------------------------------------------- #
# ISO 9001 specific
# --------------------------------------------------------------------------- #
def _iso9001(std) -> List[Dict[str, Any]]:
    d = []
    d.append(D(std, "POL", 20, "Quality Policy", ["5.2"], MANDATORY, "Internal", "policy",
        "Top-management commitment to quality.", "{{roles.top_management}}", [
        S("Policy", "{{org.legal_name}} is committed to consistently meeting customer and regulatory requirements.", True),
        S("Commitments", "We commit to customer satisfaction and continual improvement of the QMS.", True)]))
    d.append(R(std, 20, "Quality Objectives Register", "Quality Objectives", "6.2", MANDATORY, [
        ("Objective", "o", 36), ("KPI", "k", 26), ("Target", "t", 14), ("Owner", "ow", 22), ("Status", "s", 14)],
        [{"o": "Improve on-time delivery", "k": "On-time %", "t": "≥95%", "ow": "{{roles.ms_coordinator}}", "s": "In progress"}]))
    d.append(R(std, 3 + 300, "Process Interaction Map", "Processes", "4.4", CORE, [
        ("Process", "p", 26), ("Inputs", "i", 28), ("Outputs", "o", 28), ("Owner", "ow", 22)],
        [{"p": "Service delivery", "i": "Customer order", "o": "Delivered service", "ow": "{{roles.ms_coordinator}}"}], kind="DOC"))
    d.append(R(std, 21, "Process Register", "Process Register", "4.4", CORE, [
        ("Process ID", "id", 12), ("Process", "p", 30), ("Owner", "o", 22), ("KPI", "k", 24)]))
    d.append(D(std, "PROC", 20, "Customer Requirements and Communication Procedure", ["8.2"], CORE, "Internal", "procedure",
        "Determining and reviewing customer requirements.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To determine, review and communicate customer requirements for {{org.products_services}}.", True),
        S("Review", "Requirements are reviewed before commitment to ensure they can be met.", True)]))
    d.append(D(std, "PROC", 21, "Contract and Order Review Procedure", ["8.2.3"], CORE, "Internal", "procedure",
        "Review of contracts and orders before acceptance.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To ensure {{org.trade_name}} can meet requirements before accepting orders.", True),
        S("Process", "Orders are reviewed for capability, resources and changes are recorded.", True)]))
    d.append(D(std, "PROC", 22, "Design and Development Procedure", ["8.3"], RECOMMENDED, "Internal", "procedure",
        "Control of design and development.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To control design of products/services where applicable to {{org.trade_name}}.", True),
        S("Stages", "Planning, inputs, controls, outputs and changes are managed and recorded.", True)]))
    d.append(D(std, "PROC", 23, "Supplier Evaluation Procedure", ["8.4"], CORE, "Internal", "procedure",
        "Evaluation and selection of external providers.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To evaluate and monitor suppliers to {{org.trade_name}}.", True),
        S("Criteria", "Suppliers are evaluated on quality, delivery and price; results recorded.", True)],
        related=["Approved Supplier Register"]))
    d.append(R(std, 22, "Approved Supplier Register", "Suppliers", "8.4", RECORD, [
        ("Supplier ID", "id", 12), ("Supplier", "s", 30), ("Product/Service", "p", 28), ("Score", "e", 12), ("Status", "st", 14)],
        [{"id": "SUP-001", "s": "Sample Supplier", "p": "Materials", "e": "85%", "st": "Approved"}]))
    d.append(D(std, "PROC", 24, "Purchasing Procedure", ["8.4"], CORE, "Internal", "procedure",
        "Control of purchased products and services.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To ensure purchased items conform to requirements.", True),
        S("Process", "Purchase orders specify requirements; incoming items are verified.", True)]))
    d.append(D(std, "PROC", 25, "Production and Service Provision Control Procedure", ["8.5"], CORE, "Internal", "procedure",
        "Control of production and service delivery.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To control delivery of {{org.products_services}} under defined conditions.", True),
        S("Controls", "Work instructions, monitoring and identification/traceability are applied.", True)]))
    d.append(D(std, "PROC", 26, "Inspection and Testing Procedure", ["8.6"], CORE, "Internal", "procedure",
        "Verification that products/services meet requirements.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To verify outputs of {{org.trade_name}} meet acceptance criteria.", True),
        S("Records", "Inspection results and release authority are recorded.", True)]))
    d.append(R(std, 23, "Calibration Register", "Calibration", "7.1.5", RECORD, [
        ("Equipment ID", "id", 14), ("Equipment", "e", 28), ("Calibration Due", "d", 16), ("Status", "s", 14)]))
    d.append(D(std, "PROC", 27, "Control of Nonconforming Output Procedure", ["8.7"], MANDATORY, "Internal", "procedure",
        "Identification and control of nonconforming output.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To prevent unintended use of nonconforming output.", True),
        S("Handling", "Nonconforming output is segregated, corrected or concessioned and recorded.", True)],
        related=["Nonconforming Output Register"]))
    d.append(R(std, 24, "Nonconforming Output Register", "NC Output", "8.7", RECORD, [
        ("Ref", "id", 10), ("Description", "d", 38), ("Disposition", "disp", 24), ("Owner", "o", 20), ("Status", "s", 14)]))
    d.append(D(std, "PROC", 28, "Customer Complaint Procedure", ["9.1.2"], CORE, "Internal", "procedure",
        "Handling of customer complaints.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To handle complaints about {{org.products_services}} effectively.", True),
        S("Process", "Complaints are logged, investigated, resolved and used for improvement.", True)],
        related=["Customer Complaint Register"]))
    d.append(R(std, 25, "Customer Complaint Register", "Complaints", "9.1.2", RECORD, [
        ("Ref", "id", 10), ("Customer", "c", 24), ("Complaint", "cm", 36), ("Received", "r", 16), ("Status", "s", 14)]))
    d.append(D(std, "PROC", 29, "Customer Satisfaction Procedure", ["9.1.2"], CORE, "Internal", "procedure",
        "Monitoring of customer perception.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To monitor how well {{org.trade_name}} meets customer needs.", True),
        S("Method", "Satisfaction is measured via surveys and feedback and reviewed.", True)]))
    d.append(D(std, "PROC", 30, "Monitoring and Measuring Resources Procedure", ["7.1.5"], RECOMMENDED, "Internal", "procedure",
        "Control of monitoring and measuring resources.", "{{roles.ms_coordinator}}", [
        S("Purpose", "To ensure valid and reliable monitoring and measuring at {{org.trade_name}}.", True),
        S("Calibration", "Equipment is identified, calibrated and safeguarded; see Calibration Register.", True)]))
    return d


SPECIFIC_BUILDERS = {"iso-27001": _iso27001, "dpdpa": _dpdpa, "iso-9001": _iso9001}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def build_manifest(std: Dict[str, Any]) -> List[Dict[str, Any]]:
    docs = _common_docs(std) + SPECIFIC_BUILDERS[std["slug"]](std)
    # ensure unique doc_ids (defensive)
    seen, unique = set(), []
    for d in docs:
        did = d["doc_id"]
        if did in seen:
            n = 2
            while f"{did}-{n}" in seen:
                n += 1
            d["doc_id"] = f"{did}-{n}"
            did = d["doc_id"]
        seen.add(did)
        unique.append(d)
    return unique


def get_standard(slug: str):
    for s in STANDARDS:
        if s["slug"] == slug:
            return s
    return None


def manifest_summary(std: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = []
    for d in build_manifest(std):
        classification = d.get("classification", "Internal")
        if "{{" in str(classification):
            classification = "Client-defined"
        out.append({
            "doc_id": d["doc_id"], "title": d["title"], "format": d["format"].upper(),
            "category": d["category"], "template_class": d["template_class"],
            "classification": classification, "clause_refs": d.get("clause_refs", []),
            "purpose": d.get("purpose", ""),
        })
    return out
