"""Manual proxy list importer."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProxyImportEntry:
    ip: str
    port: int
    proxy_type: str = "unknown"


def parse_proxy_lines(lines: list[str] | tuple[str, ...]) -> list[ProxyImportEntry]:
    entries: list[ProxyImportEntry] = []
    for line in lines:
        cleaned = line.strip()
        if not cleaned or cleaned.startswith("#"):
            continue
        proxy_type = "unknown"
        endpoint = cleaned
        if "://" in cleaned:
            proxy_type, endpoint = cleaned.split("://", 1)
        if ":" not in endpoint:
            continue
        host, port_text = endpoint.rsplit(":", 1)
        try:
            port = int(port_text)
        except ValueError:
            continue
        entries.append(ProxyImportEntry(ip=host.strip(), port=port, proxy_type=proxy_type.strip()))
    return entries

