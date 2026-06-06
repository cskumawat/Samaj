"""Custom exceptions for Samaj."""


class SamajError(Exception):
    """Base exception for Samaj."""


class SafetyPolicyError(SamajError):
    """Raised when a safety policy blocks an action."""


class ScopeError(SamajError):
    """Raised when a target is not in authorized scope."""


class NotImplementedPhaseError(SamajError):
    """Raised when a planned later-phase feature is requested."""


class AntiHallucinationError(SamajError):
    """Raised when unsupported generated content is rejected."""

