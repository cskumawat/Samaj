"""Mermaid diagram generation for static analysis learning."""

from __future__ import annotations


def static_infection_flow_diagram(indicator_count: int) -> str:
    yes_label = "E[Mark Needs Manual Review]"
    no_label = "F[No obvious static indicator]"
    return "\n".join(
        (
            "flowchart TD",
            "    A[Suspicious File Imported] --> B[Static Analysis]",
            "    B --> C[Strings, Hashes, and Metadata]",
            "    C --> D{Suspicious Static Indicators?}",
            f"    D -->|Yes: {indicator_count}| {yes_label}",
            f"    D -->|No| {no_label}",
            "    E --> G[Containment Guidance]",
            "    F --> G[Containment Guidance]",
            "    G --> H[Removal and Prevention Notes]",
        )
    )
