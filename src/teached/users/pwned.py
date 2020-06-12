"""Direct access to the Pwned Passwords API."""
import hashlib
from typing import Optional

import requests

from teached import settings

API_ENDPOINT = "https://api.pwnedpasswords.com/range/"
PWNED_REQUEST_TIMEOUT = 1.0  # 1 second


def pwned_password(*, password: str) -> Optional[int]:
    """Check for compromised password.

    Args:
        password: plain text.

    Returns:
        int or None

    Examples:
        >>> from teached.users import pwned
        >>> result = pwned.pwned_password(password="123456")
        >>> type(result) == int
        True
    """
    password_hash = hashlib.sha1(password.encode()).hexdigest().upper()  # noqa: S303

    prefix, suffix = password_hash[:5], password_hash[5:]

    try:

        response = requests.get(
            f"{API_ENDPOINT}{prefix}",
            timeout=getattr(settings, "PWNED_REQUEST_TIMEOUT", PWNED_REQUEST_TIMEOUT),
        )

        response.raise_for_status()

    except requests.RequestException as e:
        settings.logger.error(f"Skipped Pwned Passwords check due to error: {e}")
        return None

    results = {}

    for line in response.text.splitlines():

        line_suffix, _, times = line.partition(":")

        results.update({f"{line_suffix}": int(times)})

    return results.get(suffix, 0)
