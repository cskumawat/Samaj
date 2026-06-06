from __future__ import annotations

from samaj.core.os_detect import OperatingSystem, detect_os


def test_detect_os_windows(monkeypatch, tmp_path):
    monkeypatch.setattr("samaj.core.os_detect.platform.system", lambda: "Windows")

    assert detect_os(tmp_path / "missing") == OperatingSystem.WINDOWS


def test_detect_os_kali_linux(monkeypatch, tmp_path):
    monkeypatch.setattr("samaj.core.os_detect.platform.system", lambda: "Linux")
    release = tmp_path / "os-release"
    release.write_text('ID=kali\nPRETTY_NAME="Kali GNU/Linux Rolling"\n', encoding="utf-8")

    assert detect_os(release) == OperatingSystem.KALI_LINUX
