from __future__ import annotations


def test_core_imports():
    import samaj
    from samaj.config.settings import AppSettings
    from samaj.core.anti_hallucination import VerificationStatus
    from samaj.core.safety import SafetyPolicy

    assert samaj.APP_NAME == "Samaj"
    assert AppSettings().anti_hallucination_mode is True
    assert VerificationStatus.OBSERVED.value == "observed"
    assert SafetyPolicy()

