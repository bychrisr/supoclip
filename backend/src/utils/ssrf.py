from __future__ import annotations

import ipaddress
import socket
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urlparse


@dataclass(frozen=True)
class UrlSafetyResult:
    ok: bool
    reason: str | None = None


def _is_ip_disallowed(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True

    return bool(
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
    )


def _hostname_in_allowlist(hostname: str, allowed_hosts: set[str]) -> bool:
    host = hostname.lower().rstrip(".")
    if host in allowed_hosts:
        return True
    # Support simple suffix matches (e.g. allow googleusercontent.com covers *.googleusercontent.com)
    for allowed in allowed_hosts:
        allowed_norm = allowed.lower().lstrip(".").rstrip(".")
        if host == allowed_norm:
            return True
        if host.endswith("." + allowed_norm):
            return True
    return False


def validate_external_url(
    url: str,
    *,
    allowed_hosts: set[str],
    allow_http: bool = False,
    allowed_ports: set[int] | None = None,
) -> UrlSafetyResult:
    """
    SSRF guard:
    - only https (or http if explicitly allowed)
    - no credentials in URL
    - host must be allowlisted
    - resolved IPs must not be private/loopback/etc
    """
    if not isinstance(url, str) or not url.strip():
        return UrlSafetyResult(ok=False, reason="Empty URL")

    parsed = urlparse(url.strip())
    scheme = (parsed.scheme or "").lower()
    if scheme not in ({"https"} | ({"http"} if allow_http else set())):
        return UrlSafetyResult(ok=False, reason="Only https URLs are allowed")

    if parsed.username or parsed.password:
        return UrlSafetyResult(ok=False, reason="Credentials in URL are not allowed")

    hostname = parsed.hostname
    if not hostname:
        return UrlSafetyResult(ok=False, reason="Missing hostname")

    if hostname.lower() in {"localhost"}:
        return UrlSafetyResult(ok=False, reason="Localhost is not allowed")

    if not _hostname_in_allowlist(hostname, allowed_hosts):
        return UrlSafetyResult(ok=False, reason="Host is not allowlisted")

    if allowed_ports is None:
        allowed_ports = {443, 80}
    if parsed.port is not None and parsed.port not in allowed_ports:
        return UrlSafetyResult(ok=False, reason="Port is not allowed")

    try:
        infos = socket.getaddrinfo(hostname, parsed.port or (443 if scheme == "https" else 80))
    except socket.gaierror:
        return UrlSafetyResult(ok=False, reason="DNS resolution failed")

    ips: list[str] = []
    for info in infos:
        sockaddr = info[4]
        ip = sockaddr[0]
        ips.append(ip)
        if _is_ip_disallowed(ip):
            return UrlSafetyResult(ok=False, reason="Resolved IP is not allowed")

    if not ips:
        return UrlSafetyResult(ok=False, reason="No resolved IPs")

    return UrlSafetyResult(ok=True, reason=None)


def allowlist_union(*host_iterables: Iterable[str]) -> set[str]:
    out: set[str] = set()
    for it in host_iterables:
        for item in it:
            if item and isinstance(item, str):
                out.add(item.strip())
    return out

