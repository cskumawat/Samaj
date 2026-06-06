"""Prompt guard constants for future AI integration."""

SAMAJ_AI_SYSTEM_MESSAGE = (
    "You are Samaj AI Assistant. You are operating in Anti-Hallucination Mode. "
    "You must not invent scan results, vulnerabilities, impact, or evidence. "
    "You must clearly label observations, assumptions, and unknowns. "
    "You must refuse unsafe requests. You must only assist with authorized "
    "defensive security testing."
)


def build_guarded_prompt(
    user_prompt: str,
    authorization_context: str,
    evidence_summary: str,
) -> str:
    return (
        f"{SAMAJ_AI_SYSTEM_MESSAGE}\n\n"
        f"Authorization context:\n{authorization_context or 'Not provided.'}\n\n"
        f"Evidence summary:\n{evidence_summary or 'No evidence provided.'}\n\n"
        f"User request:\n{user_prompt}"
    )
