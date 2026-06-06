"""Operating system detection for Samaj."""

from __future__ import annotations

import platform
from enum import StrEnum
from pathlib import Path


class OperatingSystem(StrEnum):
    WINDOWS = "Windows"
    KALI_LINUX = "Kali Linux"
    DEBIAN_LINUX = "Debian Linux"
    UBUNTU_LINUX = "Ubuntu Linux"
    OTHER_LINUX = "Other Linux"
    UNKNOWN = "Unknown OS"


def detect_os(release_file: Path = Path("/etc/os-release")) -> OperatingSystem:
    system = platform.system().lower()
    if system == "windows":
        return OperatingSystem.WINDOWS
    if system != "linux":
        return OperatingSystem.UNKNOWN

    data = _read_os_release(release_file)
    distro_id = data.get("id", "").lower()
    distro_like = data.get("id_like", "").lower()
    pretty = data.get("pretty_name", "").lower()

    if "kali" in {distro_id, distro_like} or "kali" in pretty:
        return OperatingSystem.KALI_LINUX
    if distro_id == "ubuntu" or "ubuntu" in distro_like:
        return OperatingSystem.UBUNTU_LINUX
    if distro_id == "debian" or "debian" in distro_like:
        return OperatingSystem.DEBIAN_LINUX
    return OperatingSystem.OTHER_LINUX


def _read_os_release(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip().lower()] = value.strip().strip('"')
    return values

