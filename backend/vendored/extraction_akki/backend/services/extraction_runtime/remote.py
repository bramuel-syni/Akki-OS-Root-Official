"""Transport is a deployable unit bound by a runtime descriptor, never by an address in code."""
import asyncio
import json
import logging
import os
import shlex
import time
from services.extraction_runtime.inner_hop import BOOTSTRAP
from services.extraction_runtime.worker_bundle import bundle
from services.northena.execution_models import Held

MAX_OUTPUT = 12 * 1024 * 1024
log = logging.getLogger(__name__)


class SshSeamTransport:
    def __init__(self, host_slug):
        self.host_slug = host_slug

    def connect(self, timeout):
        from services.census_autonomy.remote_dispatch import _connect
        client, config = _connect(self.host_slug, timeout)
        return client, config.hostname_expected


class JumpTransport:
    def connect(self, timeout):
        from services.census_autonomy.jump_dispatch import _connect_jump, _jump_config
        return _connect_jump(_jump_config(), timeout), os.environ['CENSUS_JUMP_HOSTNAME']


def transport_for(descriptor):
    kind = descriptor['transport']['kind']
    if kind == 'ssh_seam':
        return SshSeamTransport(descriptor['transport']['host_slug'])
    if kind == 'jump':
        return JumpTransport()
    raise Held('RUNTIME_TRANSPORT_NOT_ADMITTED')


def call(descriptor, control, *, deadline_seconds):
    """Blocking: one bootstrap exec on the admitted runtime, JSON metadata back, digest-verified."""
    deadline = time.time() + deadline_seconds
    code_b64, code_sha256 = bundle()
    client, expected = transport_for(descriptor).connect(min(20, int(deadline_seconds)))
    try:
        client.get_transport().set_keepalive(30)
        payload = {**control, 'bundle': code_b64, 'code_sha256': code_sha256, 'hostname_expected': expected,
                   'runtime_id': descriptor['runtime_id'], 'state_dir': descriptor['state_dir'],
                   'signer_id': descriptor['principal_id'], 'key_id': descriptor['key_id']}
        channel = client.get_transport().open_session(timeout=15)
        channel.settimeout(deadline_seconds)
        channel.exec_command(shlex.quote(descriptor['python']) + ' -c ' + shlex.quote(BOOTSTRAP))
        channel.sendall(json.dumps(payload).encode())
        channel.shutdown_write()
        output, diagnostic = bytearray(), bytearray()
        while True:
            if channel.recv_ready():
                output.extend(channel.recv(65536))
                if len(output) > MAX_OUTPUT:
                    channel.close()
                    raise Held('RUNTIME_RECEIPT_TOO_LARGE')
            if channel.recv_stderr_ready():
                chunk = channel.recv_stderr(65536)
                diagnostic.extend(chunk[:max(0, 65536 - len(diagnostic))])
            if (channel.exit_status_ready() and getattr(channel, 'eof_received', True)
                    and not channel.recv_ready() and not channel.recv_stderr_ready()):
                break
            if time.time() >= deadline:
                channel.close()
                raise TimeoutError('RUNTIME_CALL_DEADLINE')
            time.sleep(.02)
        if channel.recv_exit_status() != 0:
            tail = diagnostic.decode(errors='replace').strip().splitlines()[-1:] or ['']
            log.warning('RUNTIME_CALL_FAILED runtime=%s mode=%s last_line=%r', descriptor['runtime_id'], control['mode'], tail[0][:300])
            raise Held('RUNTIME_CALL_FAILED')
        value = json.loads(output)
        if value.get('protocol') != 'akki-extraction-runtime/1' or value.get('mode') != control['mode']:
            raise Held('RUNTIME_PROTOCOL_MISMATCH')
        return value
    finally:
        client.close()


async def call_async(descriptor, control, *, deadline_seconds):
    return await asyncio.to_thread(call, descriptor, control, deadline_seconds=deadline_seconds)
