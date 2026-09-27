import inspect
import ipaddress
import time
from dataclasses import dataclass
from urllib.parse import urlsplit
from pydantic import Field, SecretStr
from services.northena.execution_models import Frozen, Held
from services.northena.execution_gate_checks import finite_timeout
from services.activation.receipts import NativeReceipts, SignedReceipt


class ProviderState(Frozen):
    grant: SignedReceipt | None = None
    url: SecretStr | None = Field(default=None, repr=False)
    completion: SignedReceipt | None = None


def origin_of(url):
    try:
        if not isinstance(url, str) or any(ord(c) <= 32 or ord(c) >= 127 for c in url) or '\\' in url or len(url) > 8192:
            raise ValueError()
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.fragment:
            raise ValueError()
        host = parsed.hostname.lower()
        if host.endswith('.') or '%' in parsed.netloc or parsed.netloc.endswith(':'):
            raise ValueError()
        try:
            ipaddress.ip_address(host)
        except ValueError:
            if host == 'localhost' or host.endswith('.localhost'):
                raise ValueError()
        else:
            raise ValueError()
        port = parsed.port
        if port is not None and not 1 <= port <= 65535:
            raise ValueError()
        return 'https://' + host + (f':{port}' if port and port != 443 else '')
    except (ValueError, TypeError):
        raise Held('CUSTODY_ORIGIN_INVALID') from None


@dataclass(frozen=True)
class CustodyBinding:
    receipts: NativeReceipts
    provider: object
    custodian_principal_id: str
    allowed_origins: tuple[str, ...]
    max_grant_seconds: int
    timeout_seconds: float
    clock: object = time.time

    def __post_init__(self):
        finite_timeout(self.timeout_seconds)
        if (not isinstance(self.receipts, NativeReceipts) or self.receipts.admitted_keys is None
                or not self.custodian_principal_id or type(self.max_grant_seconds) is not int or self.max_grant_seconds <= 0
                or not self.allowed_origins or len(set(self.allowed_origins)) != len(self.allowed_origins)):
            raise ValueError('An existing admitted custody provider and explicit bounds are required.')
        if any(origin_of(v) != v or urlsplit(v).path for v in self.allowed_origins):
            raise ValueError('Exact HTTPS origins are required, not prefixes or wildcard domains.')
        if any(not inspect.iscoroutinefunction(getattr(self.provider, name, None)) for name in ('prepare', 'status')):
            raise ValueError('Custody providers must expose bounded async metadata operations.')