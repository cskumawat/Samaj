"""Proxy safety policy."""

PROXY_MANDATORY_STATEMENT = (
    "Proxy features must not be used for illegal activity, abuse, bypassing bans, "
    "bypassing rate limits, unauthorized scraping, credential attacks, or hiding "
    "unauthorized activity."
)


def validate_proxy_test_request(approved: bool, test_url: str) -> tuple[bool, str]:
    if not approved:
        return False, "Proxy testing requires explicit user approval."
    if not test_url.startswith(("https://", "http://")):
        return False, "Proxy testing requires a user-approved HTTP(S) endpoint."
    return False, "Live proxy testing is not implemented in this foundation phase."
