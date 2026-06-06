from __future__ import annotations

from samaj.gui.theme import LOGO_PATH, samaj_stylesheet


def test_theme_asset_exists_and_stylesheet_mentions_safety_colors():
    stylesheet = samaj_stylesheet()

    assert LOGO_PATH.exists()
    assert LOGO_PATH.name == "logo.png"
    assert "#1282d8" in stylesheet
    assert "navigationSidebar" in stylesheet
