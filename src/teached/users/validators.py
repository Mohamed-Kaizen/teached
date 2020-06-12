"""Reusable validators."""
from typing import Callable

from confusable_homoglyphs import confusables

from teached import settings

CONFUSABLE = "This name cannot be registered.Please choose a different name."

CONFUSABLE_EMAIL = (
    "This email address cannot be registered. "
    "Please supply a different email address."
)

# Below we construct a large but non-exhaustive list of names which
# users probably should not be able to register with, due to various
# risks:
#
# * For a site which creates email addresses from username, important
#   common addresses must be reserved.
#
# * For a site which creates subdomains from usernames, important
#   common hostnames/domain names must be reserved.
#
# * For a site which uses the username to generate a URL to the user's
#   profile, common well-known filenames must be reserved.
#
# etc., etc.
#
# Credit for basic idea and most of the list to Geoffrey Thomas's blog
# post about names to reserve:
# https://ldpreload.com/blog/names-to-reserve
SPECIAL_HOSTNAMES = [
    # Hostnames with special/reserved meaning.
    "autoconfig",  # Thunderbird autoconfig
    "autodiscover",  # MS Outlook/Exchange autoconfig
    "broadcasthost",  # Network broadcast hostname
    "isatap",  # IPv6 tunnel autodiscovery
    "localdomain",  # Loopback
    "localhost",  # Loopback
    "wpad",  # Proxy autodiscovery
]

PROTOCOL_HOSTNAMES = [
    # Common protocol hostnames.
    "email",
    "ftp",
    "imap",
    "mail",
    "mx",
    "news",
    "ns0",
    "ns1",
    "ns2",
    "ns3",
    "ns4",
    "ns5",
    "ns6",
    "ns7",
    "ns8",
    "ns9",
    "pop",
    "pop3",
    "smtp",
    "usenet",
    "uucp",
    "webmail",
    "www",
]

ADMIN_USERNAMES = [
    # Admin-ish username
    "domainadmin",
    "domainadministrator",
    "administration",
    "owner",
    "sys",
    "system",
]

CA_ADDRESSES = [
    # Email addresses known used by certificate authorities during
    # verification.
    "admin",
    "administrator",
    "domainadmin",
    "domainadministrator",
    "hostmaster",
    "info",
    "is",
    "it",
    "mis",
    "postmaster",
    "root",
    "ssladmin",
    "ssladministrator",
    "sslwebmaster",
    "sysadmin",
    "webmaster",
]

RFC_2142 = [
    # RFC-2142-defined names not already covered.
    "abuse",
    "marketing",
    "noc",
    "sales",
    "security",
    "support",
    "unsenet",
]

NOREPLY_ADDRESSES = [
    # Common no-reply email addresses.
    "mailer-daemon",
    "mailerdaemon",
    "nobody",
    "noreply",
    "no-reply",
]

SENSITIVE_FILENAMES = [
    # Sensitive filenames.
    "clientaccesspolicy.xml",  # Silverlight cross-domain policy file.
    "crossdomain.xml",  # Flash cross-domain policy file.
    "favicon.ico",
    "humans.txt",
    "keybase.txt",  # Keybase ownership-verification URL.
    "robots.txt",
    "security.txt",
    ".htaccess",
    ".htpasswd",
    ".well-known",
    ".well-known/",
    "/.well-known",
    "/.well-known/",
]

OTHER_SENSITIVE_NAMES = [
    # Other names which could be problems depending on URL/subdomain
    # structure.
    "about",
    "account",
    "accounts",
    "app",
    "auth",
    "authorize",
    "blog",
    "buy",
    "cart",
    "clients",
    "contact",
    "contactus",
    "contact-us",
    "copyright",
    "css",
    "dashboard",
    "dev",
    "developer",
    "developers",
    "doc",
    "docs",
    "download",
    "downloads",
    "enquiry",
    "error",
    "errors",
    "events",
    "example",
    "examples",
    "faq",
    "faqs",
    "feature",
    "features",
    "guest",
    "guests",
    "help",
    "image",
    "images",
    "img",
    "inquiry",
    "license",
    "js",
    "login",
    "logout",
    "me",
    "media",
    "myaccount",
    "new",
    "oauth",
    "pay",
    "payment",
    "payments",
    "plans",
    "portfolio",
    "preferences",
    "pricing",
    "privacy",
    "profile",
    "register",
    "secure",
    "settings",
    "signin",
    "signup",
    "signout",
    "src",
    "ssl",
    "status",
    "store",
    "subscribe",
    "terms",
    "tos",
    "tutorial",
    "tutorials",
    "user",
    "users",
    "weblog",
    "work",
]

DEFAULT_RESERVED_NAMES = (
    SPECIAL_HOSTNAMES
    + PROTOCOL_HOSTNAMES
    + ADMIN_USERNAMES
    + CA_ADDRESSES
    + RFC_2142
    + NOREPLY_ADDRESSES
    + SENSITIVE_FILENAMES
    + OTHER_SENSITIVE_NAMES
    + getattr(settings, "CUSTOM_RESERVED_NAMES", [])
)


def validate_confusables(*, value: str, exception_class: Callable) -> None:
    """Disallows 'dangerous' usernames likely to represent homograph attacks.

    A username is 'dangerous' if it is mixed-script (as defined by
    Unicode 'Script' property) and contains one or more characters
    appearing in the Unicode Visually Confusable Characters file.

    Args:
        value: string.
        exception_class: Callable Exception class

    Examples:
        >>> from teached.users import validators
        >>> validators.validate_confusables(value="ΑlaskaJazz", exception_class=ValueError)  # noqa: B950
        Traceback (most recent call last):
            ...
        ValueError: This name cannot be registered.Please choose a different name.
        >>> validators.validate_confusables(value="123", exception_class=ValueError)
        None

    Raises:
        exception_class: call the exception class if the value is dangerous.
    """
    if confusables.is_dangerous(value):
        raise exception_class(CONFUSABLE)


def validate_confusables_email(
    *, local_part: str, domain: str, exception_class: Callable
) -> None:
    """Disallows 'dangerous' email addresses likely to represent homograph attacks.

    An email address is 'dangerous' if either the local-part or the
    domain, considered on their own, are mixed-script and contain one
    or more characters appearing in the Unicode Visually Confusable
    Characters file.

    Args:
        local_part: the local part of the email addres, before @.
        domain: the domain part of the email addres, after @.
        exception_class: Callable Exception class

    Examples:
        >>> from teached.users import validators
        >>> validators.validate_confusables_email(local_part="ΑlaskaJazz", domain="ΑlaskaJazz", exception_class=ValueError)  # noqa: B950
        Traceback (most recent call last):
            ...
        ValueError: This email address cannot be registered. Please supply a different email address.
        >>> validators.validate_confusables_email(local_part="123", domain="123", exception_class=ValueError)
        None

    Raises:
        exception_class: call the exception class if the value is dangerous.
    """
    if confusables.is_dangerous(local_part) or confusables.is_dangerous(domain):
        raise exception_class(CONFUSABLE_EMAIL)


def validate_reserved_name(*, value: str, exception_class: Callable) -> None:
    """Disallows many reserved names as form field values.

    Args:
        value: string.
        exception_class: Callable Exception class.

    Examples:
        >>> from teached.users import validators
        >>> validators.validate_reserved_name(value="admin", exception_class=ValueError)  # noqa: B950
        Traceback (most recent call last):
            ...
        ValueError: admin is reserved and cannot be registered.
        >>> validators.validate_reserved_name(value="123", exception_class=ValueError)
        None

    Raises:
        exception_class: call the exception class if the value is dangerous.
    """
    if value in DEFAULT_RESERVED_NAMES or value.startswith(".well-known"):
        raise exception_class(f"{value} is reserved and cannot be registered.")
