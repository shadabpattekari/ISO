"""
FaizZab content packs — approved standards + toolkit manifests + document
template specs. Deterministic, template-driven (no uncontrolled AI free-text).

Each document spec is consumed by toolkit_engine to produce DOCX / XLSX / PDF.
Variables use {{org.*}}, {{roles.*}}, {{doc_control.*}} tokens resolved at
generation time from the client's approved onboarding data + brand profile.
"""
from __future__ import annotations
from typing import Any, Dict, List

# --------------------------------------------------------------------------- #
# Standard metadata
# --------------------------------------------------------------------------- #
STANDARDS: List[Dict[str, Any]] = [
    {
        "slug": "iso-27001",
        "code": "ISO/IEC 27001",
        "version": "2022",
        "name": "ISO/IEC 27001:2022 — Information Security Management",
        "short": "Information Security Management System (ISMS)",
        "purpose": "Establish, implement, maintain and continually improve an information security "
                   "management system to protect the confidentiality, integrity and availability of information.",
        "intended_for": "Any organization that wants to manage information security risks systematically — "
                        "especially IT, SaaS, cybersecurity and data-driven businesses.",
        "industries": ["Information Technology", "SaaS", "Cybersecurity", "Professional Consulting", "Financial Services"],
        "doc_prefix": "ISMS",
        "legal_disclaimer": "",
        "accent": "#1F3A5F",
    },
    {
        "slug": "dpdpa",
        "code": "India DPDP Act",
        "version": "2023 + Rules 2025",
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
        "slug": "iso-9001",
        "code": "ISO 9001",
        "version": "2015",
        "name": "ISO 9001:2015 — Quality Management System",
        "short": "Quality Management System (QMS)",
        "purpose": "Establish a quality management system that consistently meets customer and regulatory "
                   "requirements and drives continual improvement.",
        "intended_for": "Any organization wanting to demonstrate consistent quality and customer satisfaction — "
                        "manufacturing, services, logistics and more.",
        "industries": ["Manufacturing", "Logistics", "Professional Consulting", "E-commerce and Retail", "Education"],
        "doc_prefix": "QMS",
        "legal_disclaimer": "",
        "accent": "#7C3F1D",
    },
]

TEMPLATE_CLASSES = [
    "Mandatory documented information",
    "Conditionally mandatory",
    "Core implementation document",
    "Recommended document",
    "Operational record",
    "Audit evidence template",
]


# --------------------------------------------------------------------------- #
# Reusable section content builders (rich, real content with variables)
# --------------------------------------------------------------------------- #
def _sec(heading: str, body: str, mandatory: bool = False, bullets: List[str] | None = None) -> Dict[str, Any]:
    d = {"heading": heading, "body": body, "mandatory": mandatory}
    if bullets:
        d["bullets"] = bullets
    return d


def _std_name(std: Dict[str, Any]) -> str:
    return f"{std['code']} {std['version']}"


# --------------------------------------------------------------------------- #
# Common management-system documents (parameterised per standard)
# --------------------------------------------------------------------------- #
def _management_system_manual(std: Dict[str, Any], n: int) -> Dict[str, Any]:
    sname = _std_name(std)
    return {
        "doc_id": f"{std['doc_prefix']}-MAN-{n:03d}",
        "title": f"{std['short']} Manual",
        "standard": sname, "format": "docx", "category": "manual",
        "template_class": "Core implementation document",
        "classification": "Confidential",
        "purpose": f"Top-level description of the {std['short']} at the organization.",
        "clause_refs": ["4", "5", "6"],
        "owner_role": "{{roles.ms_coordinator}}",
        "sections": [
            _sec("Purpose", f"This manual describes the {std['short']} implemented by {{{{org.legal_name}}}} "
                            f"to meet the requirements of {sname}. It provides the framework for managing "
                            f"{std['short'].lower()} across {{{{org.locations}}}}.", True),
            _sec("Organization Context", "The organization {{org.trade_name}} operates in the {{org.industry}} "
                 "sector delivering {{org.products_services}}. Internal and external issues relevant to the "
                 "management system are documented in the Context of the Organization Register.", True),
            _sec("Scope of the Management System",
                 "The scope covers the services, processes, locations and technologies defined during onboarding "
                 "and recorded in the Scope Statement. Any exclusions are justified in that document.", True),
            _sec("Leadership and Commitment",
                 "Top management ({{roles.top_management}}) demonstrates leadership by establishing the policy, "
                 "assigning responsibilities, providing resources and reviewing performance.", True),
            _sec("Process Approach",
                 "The organization adopts a process approach and the Plan-Do-Check-Act cycle to achieve intended "
                 "outcomes and continual improvement."),
        ],
        "responsibilities": [
            ("{{roles.top_management}}", "Accountability, policy approval and resource provision."),
            ("{{roles.ms_coordinator}}", "Coordination, monitoring and maintenance of the management system."),
            ("All personnel", "Adherence to documented information relevant to their role."),
        ],
        "kpis": ["Management review conducted at planned intervals.",
                 "Percentage of objectives achieved (target ≥ 80%)."],
        "common_nonconformities": ["Scope not aligned with actual operations.",
                                    "No evidence of leadership involvement."],
        "audit_questions": ["Is the scope defined and available as documented information?",
                            "Can top management demonstrate commitment to the management system?"],
        "related_documents": ["Management System Scope", "Management System Policy", "Objectives and KPI Register"],
    }


def _ms_policy(std: Dict[str, Any], n: int) -> Dict[str, Any]:
    sname = _std_name(std)
    return {
        "doc_id": f"{std['doc_prefix']}-POL-{n:03d}",
        "title": f"{std['short']} Policy",
        "standard": sname, "format": "docx", "category": "policy",
        "template_class": "Mandatory documented information",
        "classification": "{{doc_control.classification}}",
        "purpose": f"Statement of top-management commitment for the {std['short']}.",
        "clause_refs": ["5.2"],
        "owner_role": "{{roles.top_management}}",
        "sections": [
            _sec("Policy Statement", f"{{{{org.legal_name}}}} is committed to {std['purpose']} This policy is "
                                     f"appropriate to the purpose and context of {{{{org.trade_name}}}}.", True),
            _sec("Commitments", "The organization commits to:", True, bullets=[
                "Satisfy applicable requirements including legal, regulatory and contractual obligations.",
                "Set and review measurable objectives.",
                "Provide adequate resources and competent personnel.",
                "Continually improve the effectiveness of the management system.",
            ]),
            _sec("Communication", "This policy is communicated to all personnel and made available to relevant "
                 "interested parties as documented information."),
        ],
        "kpis": ["Policy reviewed at least annually.", "100% of staff acknowledged the policy."],
        "common_nonconformities": ["Policy not communicated.", "Policy not reviewed after major change."],
        "audit_questions": ["Is the policy approved by top management?", "Is the policy available to interested parties?"],
        "related_documents": [f"{std['short']} Manual", "Objectives and KPI Register"],
    }


def _scope_statement(std: Dict[str, Any], n: int) -> Dict[str, Any]:
    sname = _std_name(std)
    return {
        "doc_id": f"{std['doc_prefix']}-DOC-{n:03d}",
        "title": "Management System Scope Statement",
        "standard": sname, "format": "docx", "category": "policy",
        "template_class": "Mandatory documented information",
        "classification": "Internal",
        "purpose": "Defines the boundaries and applicability of the management system.",
        "clause_refs": ["4.3"],
        "owner_role": "{{roles.ms_coordinator}}",
        "sections": [
            _sec("Scope", "The management system of {{org.legal_name}} applies to the provision of "
                 "{{org.products_services}} at the following locations: {{org.locations}}.", True),
            _sec("Boundaries", "The scope considers internal and external issues, the requirements of interested "
                 "parties, and the organization's products, services and interfaces.", True),
            _sec("Exclusions", "Any exclusions and their justification are recorded here based on the onboarding "
                 "declaration. Exclusions must not affect the organization's ability to meet requirements."),
        ],
        "related_documents": ["Context of the Organization Register", "Interested Parties Register"],
    }


def _internal_audit_procedure(std: Dict[str, Any], n: int) -> Dict[str, Any]:
    sname = _std_name(std)
    return {
        "doc_id": f"{std['doc_prefix']}-PROC-{n:03d}",
        "title": "Internal Audit Procedure",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Mandatory documented information",
        "classification": "Internal",
        "purpose": "Defines how internal audits are planned, conducted and reported.",
        "clause_refs": ["9.2"],
        "owner_role": "{{roles.internal_auditor}}",
        "sections": [
            _sec("Purpose", "To ensure the management system of {{org.trade_name}} conforms to the requirements "
                 f"of {sname} and is effectively implemented and maintained.", True),
            _sec("Audit Programme", "An annual audit programme is maintained by {{roles.internal_auditor}} "
                 "considering the importance of processes and results of previous audits.", True),
            _sec("Conducting Audits", "Auditors are independent of the area audited. Findings are classified as "
                 "major nonconformity, minor nonconformity, or observation.", True),
            _sec("Reporting", "Audit results are documented and reported to top management as input to management "
                 "review. Corrective actions are tracked to closure."),
        ],
        "kpis": ["Audit programme completed on schedule (target 100%).",
                 "Corrective actions closed within agreed timeframe."],
        "common_nonconformities": ["Auditors not independent.", "Audit programme not risk-based."],
        "audit_questions": ["Is there an audit programme?", "Are auditors competent and impartial?"],
        "related_documents": ["Internal Audit Programme", "Internal Audit Checklist", "Corrective Action Register"],
    }


def _mgmt_review_procedure(std: Dict[str, Any], n: int) -> Dict[str, Any]:
    sname = _std_name(std)
    return {
        "doc_id": f"{std['doc_prefix']}-PROC-{n:03d}",
        "title": "Management Review Procedure",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Mandatory documented information",
        "classification": "Internal",
        "purpose": "Defines how top management reviews the management system.",
        "clause_refs": ["9.3"],
        "owner_role": "{{roles.top_management}}",
        "sections": [
            _sec("Purpose", "To ensure top management of {{org.legal_name}} reviews the management system at "
                 "planned intervals to ensure its continuing suitability, adequacy and effectiveness.", True),
            _sec("Inputs", "Reviews consider audit results, performance against objectives, nonconformities, "
                 "risk changes, feedback from interested parties and improvement opportunities.", True),
            _sec("Outputs", "Decisions on improvement, resource needs and any changes to the management system "
                 "are documented in the Management Review Minutes.", True),
        ],
        "audit_questions": ["Is management review conducted at planned intervals?",
                            "Are review inputs and outputs documented?"],
        "related_documents": ["Management Review Agenda", "Management Review Minutes"],
    }


def _nc_capa_procedure(std: Dict[str, Any], n: int) -> Dict[str, Any]:
    sname = _std_name(std)
    return {
        "doc_id": f"{std['doc_prefix']}-PROC-{n:03d}",
        "title": "Nonconformity and Corrective Action Procedure",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Mandatory documented information",
        "classification": "Internal",
        "purpose": "Defines how nonconformities are handled and corrective actions taken.",
        "clause_refs": ["10.2"],
        "owner_role": "{{roles.ms_coordinator}}",
        "sections": [
            _sec("Purpose", "To ensure {{org.trade_name}} reacts to nonconformities, evaluates the need for "
                 "action to eliminate causes, and implements corrective actions.", True),
            _sec("Root Cause Analysis", "The cause of each nonconformity is investigated using a structured "
                 "method before corrective action is determined.", True),
            _sec("Effectiveness", "The effectiveness of each corrective action is reviewed and recorded in the "
                 "Corrective Action Register."),
        ],
        "related_documents": ["Corrective Action Register", "Continual Improvement Register"],
    }


# ---- Registers (XLSX) ------------------------------------------------------
def _register(std, n, title, sheet, cols_rows, clause, tclass="Operational record", cat="register"):
    columns, rows = cols_rows
    return {
        "doc_id": f"{std['doc_prefix']}-REG-{n:03d}",
        "title": title, "standard": _std_name(std), "format": "xlsx", "category": cat,
        "template_class": tclass, "classification": "Internal",
        "purpose": f"{title} maintained by the organization.",
        "clause_refs": [clause], "sheet_name": sheet,
        "columns": columns, "rows": rows,
    }


def _risk_register(std, n):
    cols = [
        {"label": "Risk ID", "key": "id", "width": 12},
        {"label": "Asset / Process", "key": "asset", "width": 28},
        {"label": "Threat / Cause", "key": "threat", "width": 28},
        {"label": "Likelihood", "key": "l", "width": 12},
        {"label": "Impact", "key": "i", "width": 12},
        {"label": "Risk Level", "key": "level", "width": 12},
        {"label": "Treatment", "key": "treat", "width": 30},
        {"label": "Owner", "key": "owner", "width": 22},
    ]
    rows = [
        {"id": "R-001", "asset": "Customer data — {{org.trade_name}}", "threat": "Unauthorized access",
         "l": "Medium", "i": "High", "level": "High", "treat": "Access control + MFA", "owner": "{{roles.ms_coordinator}}"},
        {"id": "R-002", "asset": "Key business process", "threat": "Disruption",
         "l": "Low", "i": "High", "level": "Medium", "treat": "Business continuity plan", "owner": "{{roles.ms_coordinator}}"},
    ]
    return _register(std, n, "Risk and Opportunity Register", "Risk Register", (cols, rows), "6.1")


def _master_doc_register(std, n):
    cols = [
        {"label": "Doc ID", "key": "id", "width": 14},
        {"label": "Title", "key": "title", "width": 40},
        {"label": "Owner", "key": "owner", "width": 22},
        {"label": "Version", "key": "ver", "width": 10},
        {"label": "Classification", "key": "cls", "width": 16},
        {"label": "Review Date", "key": "rev", "width": 16},
    ]
    return _register(std, n, "Master Document Register", "Documents",
                     (cols, []), "7.5", "Mandatory documented information")


def _interested_parties(std, n):
    cols = [
        {"label": "Interested Party", "key": "party", "width": 26},
        {"label": "Needs & Expectations", "key": "needs", "width": 40},
        {"label": "Requirement Type", "key": "type", "width": 20},
        {"label": "How Addressed", "key": "addr", "width": 30},
    ]
    rows = [
        {"party": "Customers of {{org.trade_name}}", "needs": "Reliable, secure delivery of {{org.products_services}}",
         "type": "Contractual", "addr": "Service agreements and controls"},
        {"party": "Employees", "needs": "Safe workplace, clear responsibilities", "type": "Legal", "addr": "Policies and training"},
        {"party": "Regulators", "needs": "Compliance with applicable law", "type": "Statutory", "addr": "Legal register"},
    ]
    return _register(std, n, "Interested Parties Register", "Interested Parties", (cols, rows), "4.2",
                     "Mandatory documented information")


def _corrective_action_register(std, n):
    cols = [
        {"label": "CAR ID", "key": "id", "width": 12},
        {"label": "Nonconformity", "key": "nc", "width": 34},
        {"label": "Root Cause", "key": "rc", "width": 28},
        {"label": "Action", "key": "act", "width": 30},
        {"label": "Owner", "key": "owner", "width": 20},
        {"label": "Status", "key": "st", "width": 14},
    ]
    return _register(std, n, "Corrective Action Register", "CAPA", (cols, []), "10.2")


# ---- Checklist -------------------------------------------------------------
def _cert_readiness(std, n):
    return {
        "doc_id": f"{std['doc_prefix']}-CHK-{n:03d}",
        "title": "Certification Readiness Checklist",
        "standard": _std_name(std), "format": "xlsx", "category": "checklist",
        "template_class": "Audit evidence template", "classification": "Internal",
        "purpose": "Self-assessment checklist to gauge readiness before certification.",
        "clause_refs": ["All"], "sheet_name": "Readiness",
        "columns": [
            {"label": "#", "key": "n", "width": 6},
            {"label": "Requirement", "key": "req", "width": 50},
            {"label": "Evidence Expected", "key": "ev", "width": 40},
            {"label": "Status", "key": "st", "width": 16},
        ],
        "rows": [
            {"n": 1, "req": "Scope defined and documented", "ev": "Scope Statement", "st": "Pending"},
            {"n": 2, "req": "Policy approved by top management", "ev": "Signed policy", "st": "Pending"},
            {"n": 3, "req": "Risks assessed and treated", "ev": "Risk register", "st": "Pending"},
            {"n": 4, "req": "Internal audit conducted", "ev": "Audit report", "st": "Pending"},
            {"n": 5, "req": "Management review conducted", "ev": "Review minutes", "st": "Pending"},
        ],
    }


def _common_docs(std: Dict[str, Any], start: int = 1) -> List[Dict[str, Any]]:
    n = start
    docs = [
        _management_system_manual(std, n),
        _ms_policy(std, n),
        _scope_statement(std, n + 1),
        _interested_parties(std, 1),
        _risk_register(std, 2),
        _internal_audit_procedure(std, n + 2),
        _mgmt_review_procedure(std, n + 3),
        _nc_capa_procedure(std, n + 4),
        _corrective_action_register(std, 3),
        _master_doc_register(std, 4),
        _cert_readiness(std, 1),
    ]
    return docs


# --------------------------------------------------------------------------- #
# Standard-specific documents
# --------------------------------------------------------------------------- #
def _iso27001_specific(std) -> List[Dict[str, Any]]:
    sname = _std_name(std)
    docs = []
    docs.append({
        "doc_id": "ISMS-PROC-010", "title": "Risk Assessment Methodology",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Mandatory documented information", "classification": "Confidential",
        "purpose": "Method for identifying, analysing and evaluating information security risks.",
        "clause_refs": ["6.1.2"], "owner_role": "{{roles.ms_coordinator}}",
        "sections": [
            _sec("Purpose", "Defines how {{org.trade_name}} assesses information security risks to its assets "
                 "and the delivery of {{org.products_services}}.", True),
            _sec("Risk Criteria", "Risk is evaluated using likelihood and impact scales. Acceptance criteria are "
                 "approved by {{roles.top_management}}.", True),
            _sec("Risk Treatment", "Options include modify, retain, avoid or share. Controls are selected from "
                 "Annex A and justified in the Statement of Applicability.", True),
        ],
        "related_documents": ["Information Security Risk Register", "Statement of Applicability"],
    })
    docs.append({
        "doc_id": "ISMS-DOC-011", "title": "Statement of Applicability (SoA)",
        "standard": sname, "format": "xlsx", "category": "register",
        "template_class": "Mandatory documented information", "classification": "Confidential",
        "purpose": "Lists Annex A controls, applicability and justification.",
        "clause_refs": ["6.1.3"], "sheet_name": "SoA",
        "columns": [
            {"label": "Control", "key": "c", "width": 14},
            {"label": "Title", "key": "t", "width": 40},
            {"label": "Applicable", "key": "a", "width": 14},
            {"label": "Justification", "key": "j", "width": 40},
            {"label": "Status", "key": "s", "width": 16},
        ],
        "rows": [
            {"c": "A.5.1", "t": "Policies for information security", "a": "Yes", "j": "Required for {{org.trade_name}}", "s": "Implemented"},
            {"c": "A.8.1", "t": "User endpoint devices", "a": "Yes", "j": "Staff use endpoints", "s": "Planned"},
            {"c": "A.5.23", "t": "Cloud services security", "a": "Conditional", "j": "Applicable if cloud used", "s": "Review"},
        ],
    })
    docs.append({
        "doc_id": "ISMS-POL-012", "title": "Access Control Policy",
        "standard": sname, "format": "docx", "category": "policy",
        "template_class": "Core implementation document", "classification": "Confidential",
        "purpose": "Rules for granting, reviewing and revoking access.",
        "clause_refs": ["A.5.15", "A.8.3"], "owner_role": "{{roles.ms_coordinator}}",
        "sections": [
            _sec("Purpose", "To control access to information and systems of {{org.legal_name}} on a need-to-know "
                 "and least-privilege basis.", True),
            _sec("Access Provisioning", "Access is granted based on role, approved by the asset owner, and reviewed "
                 "periodically. Privileged access is restricted and logged.", True),
            _sec("Authentication", "Multi-factor authentication is required for remote and privileged access."),
        ],
        "kpis": ["Access reviews completed on schedule.", "Percentage of privileged accounts with MFA (target 100%)."],
        "related_documents": ["Access Rights Register", "Information Security Policy"],
    })
    docs.append({
        "doc_id": "ISMS-PROC-013", "title": "Information Security Incident Management Procedure",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Mandatory documented information", "classification": "Confidential",
        "purpose": "How security incidents are reported, assessed and resolved.",
        "clause_refs": ["A.5.24", "A.5.26"], "owner_role": "{{roles.ms_coordinator}}",
        "sections": [
            _sec("Purpose", "To ensure a consistent and effective approach to managing information security "
                 "incidents at {{org.trade_name}}.", True),
            _sec("Reporting", "All personnel must report suspected incidents promptly to {{roles.ms_coordinator}}.", True),
            _sec("Response", "Incidents are triaged, contained, eradicated and recovered. Lessons learned are captured."),
        ],
        "related_documents": ["Incident Register"],
    })
    docs.append(_register(std, 20, "Information Asset Register", "Assets", (
        [
            {"label": "Asset ID", "key": "id", "width": 12},
            {"label": "Asset", "key": "a", "width": 30},
            {"label": "Type", "key": "t", "width": 18},
            {"label": "Owner", "key": "o", "width": 22},
            {"label": "Classification", "key": "c", "width": 18},
            {"label": "Location", "key": "l", "width": 22},
        ],
        [{"id": "AST-001", "a": "Customer database", "t": "Information", "o": "{{roles.ms_coordinator}}",
          "c": "Confidential", "l": "{{org.locations}}"}]
    ), "A.5.9", "Mandatory documented information"))
    docs.append(_register(std, 21, "Information Security Incident Register", "Incidents", (
        [
            {"label": "Incident ID", "key": "id", "width": 12},
            {"label": "Date", "key": "d", "width": 14},
            {"label": "Description", "key": "desc", "width": 40},
            {"label": "Severity", "key": "sev", "width": 12},
            {"label": "Status", "key": "st", "width": 14},
        ], []
    ), "A.5.24"))
    return docs


def _dpdpa_specific(std) -> List[Dict[str, Any]]:
    sname = _std_name(std)
    disc = std["legal_disclaimer"]
    docs = []
    docs.append({
        "doc_id": "DPDP-POL-010", "title": "Data Protection Governance Policy",
        "standard": sname, "format": "docx", "category": "policy",
        "template_class": "Core implementation document", "classification": "Confidential",
        "purpose": "How the organization governs personal data as a Data Fiduciary.",
        "clause_refs": ["S.8"], "owner_role": "{{roles.privacy_contact}}", "disclaimer": disc,
        "sections": [
            _sec("Purpose", "This policy sets out how {{org.legal_name}} acts as a Data Fiduciary under the "
                 "Digital Personal Data Protection Act, 2023 when processing digital personal data.", True),
            _sec("Lawful Processing", "{{org.trade_name}} processes personal data only for lawful purposes with "
                 "valid consent or under legitimate uses permitted by the Act.", True),
            _sec("Data Principal Rights", "The organization enables data principals to exercise their rights to "
                 "access, correction, erasure and grievance redressal.", True),
        ],
        "related_documents": ["Processing Activity Register", "Consent Request Template", "Grievance Handling Procedure"],
    })
    docs.append({
        "doc_id": "DPDP-PROC-011", "title": "Data Principal Request Procedure",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Core implementation document", "classification": "Confidential",
        "purpose": "Handling access, correction and erasure requests.",
        "clause_refs": ["S.11", "S.12", "S.13"], "owner_role": "{{roles.privacy_contact}}", "disclaimer": disc,
        "sections": [
            _sec("Purpose", "To ensure {{org.trade_name}} responds to data principal requests within statutory "
                 "timelines.", True),
            _sec("Request Handling", "Requests are logged, verified, actioned and closed. Records are retained as "
                 "evidence of compliance.", True),
        ],
        "related_documents": ["Access Request Form", "Grievance Register"],
    })
    docs.append({
        "doc_id": "DPDP-PROC-012", "title": "Personal Data Breach Response Plan",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Core implementation document", "classification": "Confidential",
        "purpose": "How personal data breaches are detected, contained and notified.",
        "clause_refs": ["S.8(6)"], "owner_role": "{{roles.privacy_contact}}", "disclaimer": disc,
        "sections": [
            _sec("Purpose", "To ensure {{org.legal_name}} responds to personal data breaches and notifies the "
                 "Data Protection Board and affected data principals as required.", True),
            _sec("Response Steps", "Detect, contain, assess, notify and remediate. Each breach is recorded in the "
                 "Breach Register.", True),
        ],
        "related_documents": ["Breach Register"],
    })
    docs.append(_register(std, 20, "Processing Activity Register", "Processing", (
        [
            {"label": "Activity ID", "key": "id", "width": 12},
            {"label": "Processing Activity", "key": "a", "width": 32},
            {"label": "Purpose", "key": "p", "width": 28},
            {"label": "Categories of Data", "key": "c", "width": 26},
            {"label": "Legal Basis", "key": "b", "width": 20},
            {"label": "Retention", "key": "r", "width": 18},
        ],
        [{"id": "PA-001", "a": "Customer account management", "p": "Service delivery",
          "c": "Name, email, phone", "b": "Consent", "r": "As per policy"}]
    ), "S.6"))
    docs.append(_register(std, 21, "Consent Register", "Consent", (
        [
            {"label": "Consent ID", "key": "id", "width": 12},
            {"label": "Data Principal", "key": "d", "width": 24},
            {"label": "Purpose", "key": "p", "width": 26},
            {"label": "Date Given", "key": "g", "width": 16},
            {"label": "Withdrawn", "key": "w", "width": 14},
        ], []
    ), "S.6"))
    docs.append(_register(std, 22, "Grievance Register", "Grievances", (
        [
            {"label": "Ref", "key": "id", "width": 10},
            {"label": "Data Principal", "key": "d", "width": 24},
            {"label": "Grievance", "key": "g", "width": 36},
            {"label": "Received", "key": "r", "width": 16},
            {"label": "Status", "key": "s", "width": 14},
        ], []
    ), "S.13"))
    # add disclaimer to all dpdpa docs missing it
    for d in docs:
        if d["format"] == "docx" and "disclaimer" not in d:
            d["disclaimer"] = disc
    return docs


def _iso9001_specific(std) -> List[Dict[str, Any]]:
    sname = _std_name(std)
    docs = []
    docs.append({
        "doc_id": "QMS-PROC-010", "title": "Control of Nonconforming Output Procedure",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Mandatory documented information", "classification": "Internal",
        "purpose": "How nonconforming products/services are identified and controlled.",
        "clause_refs": ["8.7"], "owner_role": "{{roles.ms_coordinator}}",
        "sections": [
            _sec("Purpose", "To ensure outputs of {{org.trade_name}} that do not conform to requirements are "
                 "identified and controlled to prevent unintended use.", True),
            _sec("Handling", "Nonconforming output is segregated, corrected, or concessioned with authorization, "
                 "and records are retained.", True),
        ],
        "related_documents": ["Nonconforming Output Register"],
    })
    docs.append({
        "doc_id": "QMS-PROC-011", "title": "Customer Satisfaction and Complaints Procedure",
        "standard": sname, "format": "docx", "category": "procedure",
        "template_class": "Core implementation document", "classification": "Internal",
        "purpose": "Monitoring customer satisfaction and handling complaints.",
        "clause_refs": ["9.1.2"], "owner_role": "{{roles.ms_coordinator}}",
        "sections": [
            _sec("Purpose", "To monitor customer perceptions and handle complaints for {{org.products_services}}.", True),
            _sec("Measurement", "Satisfaction is measured through surveys and feedback. Complaints are logged and "
                 "resolved with corrective action where needed.", True),
        ],
        "related_documents": ["Customer Complaint Register"],
    })
    docs.append(_register(std, 20, "Approved Supplier Register", "Suppliers", (
        [
            {"label": "Supplier ID", "key": "id", "width": 12},
            {"label": "Supplier", "key": "s", "width": 30},
            {"label": "Product/Service", "key": "p", "width": 28},
            {"label": "Evaluation Score", "key": "e", "width": 16},
            {"label": "Status", "key": "st", "width": 14},
        ],
        [{"id": "SUP-001", "s": "Sample Supplier", "p": "Raw materials", "e": "85%", "st": "Approved"}]
    ), "8.4"))
    docs.append(_register(std, 21, "Quality Objectives and KPI Register", "Objectives", (
        [
            {"label": "Objective", "key": "o", "width": 36},
            {"label": "KPI", "key": "k", "width": 28},
            {"label": "Target", "key": "t", "width": 14},
            {"label": "Owner", "key": "ow", "width": 22},
            {"label": "Status", "key": "s", "width": 14},
        ],
        [{"o": "Improve on-time delivery", "k": "On-time delivery %", "t": "≥95%",
          "ow": "{{roles.ms_coordinator}}", "s": "In progress"}]
    ), "6.2", "Mandatory documented information"))
    docs.append(_register(std, 22, "Customer Complaint Register", "Complaints", (
        [
            {"label": "Ref", "key": "id", "width": 10},
            {"label": "Customer", "key": "c", "width": 24},
            {"label": "Complaint", "key": "cm", "width": 36},
            {"label": "Received", "key": "r", "width": 16},
            {"label": "Status", "key": "s", "width": 14},
        ], []
    ), "9.1.2"))
    return docs


SPECIFIC_BUILDERS = {
    "iso-27001": _iso27001_specific,
    "dpdpa": _dpdpa_specific,
    "iso-9001": _iso9001_specific,
}


def build_manifest(std: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return the full ordered list of document specs for a standard."""
    docs = _common_docs(std)
    docs += SPECIFIC_BUILDERS[std["slug"]](std)
    return docs


def get_standard(slug: str) -> Dict[str, Any] | None:
    for s in STANDARDS:
        if s["slug"] == slug:
            return s
    return None


def manifest_summary(std: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Lightweight manifest for catalogue display (no full section bodies)."""
    out = []
    for d in build_manifest(std):
        classification = d.get("classification", "Internal")
        if "{{" in str(classification):
            classification = "Client-defined"
        out.append({
            "doc_id": d["doc_id"],
            "title": d["title"],
            "format": d["format"].upper(),
            "category": d["category"],
            "template_class": d["template_class"],
            "classification": classification,
            "clause_refs": d.get("clause_refs", []),
            "purpose": d.get("purpose", ""),
        })
    return out
