"""Owner-authorized control-plane diagnostic, never a census execution path.

Pin the server before one auth_none request. No credentials, channels or remote
commands. Not routed to HTTP; the receipted runner must be invoked explicitly.
"""
import hmac
import logging
import math
import os
import socket

import paramiko


METHODS = frozenset({"none", "publickey", "password", "keyboard-interactive",
                     "hostbased", "gssapi-with-mic", "gssapi-keyex"})
_LOG = "akki.recovery.auth_none"
logging.getLogger(_LOG).addHandler(logging.NullHandler())
logging.getLogger(_LOG).propagate = False


def _row(config, pin=False, methods=(), authenticated=False, error=None):
    return {"host_alias": config.name, "pin_match": pin,
            "allowed_methods": sorted({m for m in methods if isinstance(m, str) and m in METHODS}),
            "authenticated": authenticated, "error_code": error}


def diagnose_host(config, timeout=8.0):
    if not math.isfinite(timeout) or not 0 < timeout <= 10:
        return _row(config, error="INVALID_TIMEOUT")
    try:
        pins = paramiko.HostKeys(os.environ["SSH_KNOWN_HOSTS_PATH"])
        lookup = config.host if config.port == 22 else f"[{config.host}]:{config.port}"
        pinned = pins.lookup(lookup)
    except Exception:
        return _row(config, error="KNOWN_HOSTS_UNAVAILABLE")
    if not pinned:
        return _row(config, error="HOST_KEY_MISSING")

    transport = sock = None
    matched = False
    try:
        sock = socket.create_connection((config.host, config.port), timeout=timeout)
        transport = paramiko.Transport(sock)
        transport.set_log_channel(_LOG)
        transport.banner_timeout = timeout
        transport.auth_timeout = timeout
        transport.handshake_timeout = timeout
        security = transport.get_security_options()
        compatible = set(pinned)
        if "ssh-rsa" in compatible:
            compatible.update(("rsa-sha2-512", "rsa-sha2-256"))
        key_types = tuple(k for k in security.key_types if k in compatible)
        if not key_types:
            return _row(config, error="PINNED_KEY_TYPE_UNSUPPORTED")
        security.key_types = key_types
        transport.start_client(timeout=timeout)
        server_key = transport.get_remote_server_key()
        expected = pinned.get(server_key.get_name())
        matched = expected is not None and hmac.compare_digest(expected.asbytes(), server_key.asbytes())
        if not matched:
            return _row(config, error="HOST_KEY_CHANGED")
        try:
            methods = transport.auth_none(config.username)
            return _row(config, pin=True, methods=methods, authenticated=transport.is_authenticated())
        except paramiko.BadAuthenticationType as exc:
            return _row(config, pin=True, methods=exc.allowed_types, error="AUTH_NONE_REJECTED")
    except (socket.timeout, TimeoutError):
        return _row(config, pin=matched, error="TIMEOUT")
    except Exception:
        # Never reflect a provider exception, banner, address or username.
        return _row(config, pin=matched, error="SSH_PROTOCOL_ERROR")
    finally:
        try:
            if transport is not None:
                transport.close()
        finally:
            if sock is not None:
                sock.close()


def run_once():
    from services.census_autonomy.auth_methods_receipts import run_once as banked_run
    return banked_run(diagnose_host)