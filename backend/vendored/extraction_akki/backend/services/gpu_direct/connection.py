"""One password-auth call to the workbook endpoint. No client-key dependencies."""
import hmac
import logging
import math
import os
import socket

import paramiko

from services.gpu_direct.workbook import DirectConnectionError, get_target

LOG = 'akki.gpu_direct.transport'
logging.getLogger(LOG).addHandler(logging.NullHandler())
logging.getLogger(LOG).propagate = False
METHODS = {'publickey', 'password', 'keyboard-interactive', 'hostbased', 'gssapi-with-mic', 'gssapi-keyex', 'none'}


def connect_target(target, *, environ=None, timeout=None):
    """Return authenticated SSHClient + safe receipt; caller must close the client.

    Failure returns (None, receipt). This function opens no session channels and
    issues no remote commands. Paramiko password→keyboard-interactive fallback is
    deliberately OFF: exactly the password method supplied in the workbook.
    """
    environ = os.environ if environ is None else environ
    receipt = {'host_alias': target.name, 'tcp_connected': False, 'server_identity_verified': False,
               'credential_source': 'owner_workbook', 'auth_method': 'password', 'auth_attempts': 0,
               'authenticated': False, 'remote_commands': 0, 'remote_channels': 0,
               'historical_client_identity_used': False, 'status': 'NOT_ATTEMPTED'}
    sock = transport = None
    transferred = False
    try:
        configured_timeout = float(environ['GPU_DIRECT_TIMEOUT_SECONDS'])
        if not math.isfinite(configured_timeout) or configured_timeout <= 0:
            raise DirectConnectionError('DIRECT_TIMEOUT_INVALID')
        timeout = min(float(timeout), configured_timeout) if timeout is not None else configured_timeout
        if not math.isfinite(timeout) or timeout <= 0:
            raise DirectConnectionError('DIRECT_TIMEOUT_INVALID')
        # SERVER identity only: this file is never used as a client credential.
        pins = paramiko.HostKeys(environ['SSH_KNOWN_HOSTS_PATH'])
        token = target.host if target.port == 22 else f'[{target.host}]:{target.port}'
        pinned = pins.lookup(token)
        if not pinned:
            raise DirectConnectionError('DIRECT_SERVER_IDENTITY_MISSING')
        sock = socket.create_connection((target.host, target.port), timeout=timeout)
        receipt['tcp_connected'] = True
        transport = paramiko.Transport(sock)
        transport.set_log_channel(LOG)
        transport.banner_timeout = timeout
        transport.handshake_timeout = timeout
        transport.auth_timeout = timeout
        algorithms = set(pinned)
        if 'ssh-rsa' in algorithms:
            algorithms.update({'rsa-sha2-256', 'rsa-sha2-512'})
        security = transport.get_security_options()
        supported = tuple(k for k in security.key_types if k in algorithms)
        if not supported:
            raise DirectConnectionError('DIRECT_SERVER_ALGORITHM_UNAVAILABLE')
        security.key_types = supported
        transport.start_client(timeout=timeout)
        server_key = transport.get_remote_server_key()
        expected = pinned.get(server_key.get_name())
        if expected is None or not hmac.compare_digest(server_key.asbytes(), expected.asbytes()):
            raise DirectConnectionError('DIRECT_SERVER_IDENTITY_MISMATCH')
        receipt['server_identity_verified'] = True
        receipt['auth_attempts'] = 1
        methods = transport.auth_password(target.username, target.password, fallback=False)
        receipt['authenticated'] = bool(transport.is_authenticated())
        if not receipt['authenticated']:
            receipt.update(status='DIRECT_ADDITIONAL_AUTH_REQUIRED', allowed_methods=sorted(set(methods or []) & METHODS))
            return None, receipt
        # SSHClient only wraps the already-authenticated transport. No second
        # connect(), agent, key-file search, key comparison or password retry.
        client = paramiko.SSHClient()
        client._transport = transport
        receipt['status'] = 'DIRECT_AUTHENTICATED'
        transferred = True
        return client, receipt
    except DirectConnectionError as exc:
        receipt['status'] = exc.code
    except paramiko.BadAuthenticationType as exc:
        receipt.update(status='DIRECT_PASSWORD_METHOD_NOT_ALLOWED', allowed_methods=sorted(set(exc.allowed_types) & METHODS))
    except paramiko.AuthenticationException:
        receipt['status'] = 'DIRECT_PASSWORD_AUTHENTICATION_FAILED'
    except (socket.timeout, TimeoutError):
        receipt['status'] = 'DIRECT_CONNECTION_TIMEOUT'
    except (KeyError, ValueError):
        receipt['status'] = 'DIRECT_CONNECTION_CONFIGURATION_INVALID'
    except (paramiko.SSHException, OSError, EOFError):
        receipt['status'] = 'DIRECT_CONNECTION_TRANSPORT_FAILED'
    finally:
        if not transferred:
            if transport is not None:
                transport.close()
            if sock is not None:
                sock.close()
    return None, receipt


def connect(name, *, environ=None, timeout=None):
    target = get_target(name, environ)
    client, receipt = connect_target(target, environ=environ, timeout=timeout)
    if client is None:
        raise DirectConnectionError(receipt['status'])
    return client, target