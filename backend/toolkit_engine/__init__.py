"""
FaizZab Toolkit Generation Engine.

Deterministic, template-driven generation of organization-specific compliance
documents. NO uncontrolled free-text AI generation — every document is produced
from approved template specs + client / industry / standard variables.

Outputs:
  - DOCX  (policies, procedures, plans)  -> python-docx
  - XLSX  (registers, trackers)          -> openpyxl
  - PDF   (controlled reference copies)  -> reportlab
  - ZIP   (complete toolkit package)     -> zipfile

Public API:
  render_docx_document(spec, context) -> bytes
  render_pdf_document(spec, context)  -> bytes
  render_xlsx_register(spec, context) -> bytes
  build_zip(files) -> bytes
  validate_document(spec, context) -> dict
"""
from .engine import (
    render_docx_document,
    render_pdf_document,
    render_xlsx_register,
    build_zip,
    validate_document,
    resolve_variables,
    flatten_context,
    hex_to_rgb,
)

__all__ = [
    "render_docx_document",
    "render_pdf_document",
    "render_xlsx_register",
    "build_zip",
    "validate_document",
    "resolve_variables",
    "flatten_context",
    "hex_to_rgb",
]
