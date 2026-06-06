"""Safe command runner boundary.

External command execution is planned for Phase 9. The current foundation
exposes preview objects only so later modules have a clear boundary without
running tools.
"""

from __future__ import annotations

from dataclasses import dataclass

from samaj.core.exceptions import NotImplementedPhaseError
from samaj.core.safety import PreflightAnswers, SafetyDecision, SafetyPolicy


@dataclass(frozen=True)
class CommandPreview:
    argv: tuple[str, ...]
    target: str | None
    risk_summary: str
    safety_decision: SafetyDecision


class SafeCommandRunner:
    def __init__(self, safety_policy: SafetyPolicy | None = None) -> None:
        self.safety_policy = safety_policy or SafetyPolicy()

    def preview(
        self,
        argv: list[str] | tuple[str, ...],
        *,
        target: str | None = None,
        answers: PreflightAnswers | None = None,
    ) -> CommandPreview:
        decision = self.safety_policy.evaluate_action(
            action="external_command",
            answers=answers,
            target=target,
        )
        return CommandPreview(
            argv=tuple(argv),
            target=target,
            risk_summary="External commands are not executable in the current foundation.",
            safety_decision=decision,
        )

    def run(self, argv: list[str] | tuple[str, ...], *, target: str | None = None) -> None:
        raise NotImplementedPhaseError(
            "External command execution is planned for Phase 9 and is not implemented "
            "in the current foundation."
        )
