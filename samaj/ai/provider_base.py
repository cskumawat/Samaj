"""AI provider base placeholders for Phase 11."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AIRequest:
    prompt: str
    authorization_context: str
    evidence_summary: str = ""


@dataclass(frozen=True)
class AIResponse:
    text: str
    provider: str
    audited: bool = False


class AIProvider:
    name = "base"

    def generate(self, request: AIRequest) -> AIResponse:
        raise NotImplementedError("AI providers are planned for Phase 11.")

