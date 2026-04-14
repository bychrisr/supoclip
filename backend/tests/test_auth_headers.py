from __future__ import annotations

import time

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from src.auth_headers import (
    SIGNATURE_HEADER,
    TIMESTAMP_HEADER,
    USER_ID_HEADER,
    _expected_signature,
    get_signed_user_id,
)
from src.config import Config


def _make_request(headers: dict[str, str]) -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "headers": [(k.lower().encode(), v.encode()) for k, v in headers.items()],
    }
    return Request(scope)


@pytest.mark.unit
def test_expected_signature_is_deterministic() -> None:
    sig1 = _expected_signature("secret", "user_1", "123")
    sig2 = _expected_signature("secret", "user_1", "123")
    assert sig1 == sig2
    assert len(sig1) == 64


@pytest.mark.unit
def test_get_signed_user_id_requires_all_headers() -> None:
    cfg = Config()
    cfg.backend_auth_secret = "secret"

    req = _make_request({USER_ID_HEADER: "u"})
    with pytest.raises(HTTPException) as e:
        get_signed_user_id(req, cfg)
    assert e.value.status_code == 401


@pytest.mark.unit
def test_get_signed_user_id_requires_server_secret_configured() -> None:
    cfg = Config()
    cfg.backend_auth_secret = None

    req = _make_request(
        {
            USER_ID_HEADER: "u",
            TIMESTAMP_HEADER: str(int(time.time())),
            SIGNATURE_HEADER: "x",
        }
    )
    with pytest.raises(HTTPException) as e:
        get_signed_user_id(req, cfg)
    assert e.value.status_code == 500


@pytest.mark.unit
def test_get_signed_user_id_rejects_expired_signature(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = Config()
    cfg.backend_auth_secret = "secret"
    cfg.auth_signature_ttl_seconds = 10

    now = 1_700_000_000
    monkeypatch.setattr(time, "time", lambda: now)

    old_ts = now - 999
    req = _make_request(
        {
            USER_ID_HEADER: "u1",
            TIMESTAMP_HEADER: str(old_ts),
            SIGNATURE_HEADER: _expected_signature(cfg.backend_auth_secret, "u1", str(old_ts)),
        }
    )
    with pytest.raises(HTTPException) as e:
        get_signed_user_id(req, cfg)
    assert e.value.status_code == 401
    assert "Expired" in str(e.value.detail)


@pytest.mark.unit
def test_get_signed_user_id_accepts_valid_signature(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = Config()
    cfg.backend_auth_secret = "secret"
    cfg.auth_signature_ttl_seconds = 300

    now = 1_700_000_000
    monkeypatch.setattr(time, "time", lambda: now)

    ts = str(now)
    sig = _expected_signature(cfg.backend_auth_secret, "u_ok", ts)
    req = _make_request(
        {USER_ID_HEADER: "u_ok", TIMESTAMP_HEADER: ts, SIGNATURE_HEADER: sig}
    )
    assert get_signed_user_id(req, cfg) == "u_ok"

