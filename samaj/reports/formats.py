"""Report format labels for future exporters."""

from enum import StrEnum


class ReportFormat(StrEnum):
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"
    EXCEL = "excel"
    PDF = "pdf"
