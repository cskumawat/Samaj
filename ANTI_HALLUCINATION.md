# Anti-Hallucination Mode

Samaj must never invent results.

AI features must follow these rules:

1. Never claim a vulnerability exists unless there is evidence.
2. Never generate fake scan results.
3. Never mark severity without reasoning.
4. Never suggest exploitation outside authorized scope.
5. Always distinguish between:
   - Observed fact
   - Inference
   - Hypothesis
   - Recommendation
   - Needs manual verification
6. Every finding must include:
   - Source
   - Timestamp
   - Tool used
   - Command used
   - Raw evidence
   - Analyst note
   - Confidence score
7. AI must ask for missing evidence instead of guessing.
8. AI must refuse unsafe or unauthorized actions.
9. AI-generated reports must include a verification status.
10. AI must maintain an audit trail of all generated text.

## Required Verification Status Values

```python
class VerificationStatus:
    OBSERVED = "observed"
    INFERRED = "inferred"
    UNVERIFIED = "unverified"
    FALSE_POSITIVE = "false_positive"
    NEEDS_MANUAL_REVIEW = "needs_manual_review"
```

## Current Enforcement Status

Implemented in `samaj/core/anti_hallucination.py`:

- Evidence checker
- Confidence labeler
- Claim validator
- Verification status helper
- Source tracker
- Missing evidence detector
- AI output safety wrapper
- Do-not-guess enforcement helper
- Hallucination warning banner constant
- Tagged statements for generated text
- Tool Catalog fields default to unknown or not verified instead of guessed
- Tool Catalog import/detail viewing requires disclaimer acceptance
- GUI and docs state that catalog presence is not support, endorsement,
  verification, safety, installation, execution, recommendation, or permission

Not implemented yet:

- AI provider calls.
- Full report generation.
- Database-backed AI audit records.
- GUI review workflow for each AI statement.
- Verified support matrix for catalog tools.
- Active tool execution.

Samaj must continue to treat unverified content as unverified until real evidence is attached.

Tool Catalog entry does not mean tool support, endorsement, verification,
safety, installation, execution, recommendation, operational support, or
permission to use.
