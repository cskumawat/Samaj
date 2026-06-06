"""Proxy chain policy placeholder."""

PROXY_CHAIN_ENABLED_BY_DEFAULT = False


def proxy_chain_status() -> str:
    return (
        "Proxy chain/nested proxy is disabled by default and not implemented in "
        "this foundation phase."
    )
