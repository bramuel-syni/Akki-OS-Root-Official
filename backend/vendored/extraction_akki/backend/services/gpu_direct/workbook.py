"""Read the owner's connection specification in restricted local custody.

Only this workbook supplies endpoint/user/password. No old key, receipt, agent or
identity lookup is imported. Server endpoint verification is handled separately.
"""
import ipaddress
import os
import stat
from dataclasses import dataclass, field
from pathlib import Path

import openpyxl


class DirectConnectionError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class Target:
    name: str
    host: str
    port: int
    username: str
    password: str = field(repr=False)


def read_targets(environ=None):
    environ = os.environ if environ is None else environ
    try:
        path = Path(environ['GPU_DIRECT_CREDENTIALS_XLSX'])
        port = int(environ['GPU_DIRECT_SSH_PORT'])
        if not path.is_absolute() or not 1 <= port <= 65535:
            raise ValueError()
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    except (KeyError, ValueError, OSError):
        raise DirectConnectionError('DIRECT_WORKBOOK_CONFIGURATION_INVALID') from None
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid()
                or info.st_mode & 0o077 or info.st_size > 5 * 1024 * 1024):
            raise DirectConnectionError('DIRECT_WORKBOOK_CUSTODY_INVALID')
        try:
            wb = openpyxl.load_workbook(stream, read_only=True, data_only=True, keep_links=False)
            records, current, cells = [], {}, 0
            for sheet in wb.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    for value in row:
                        cells += 1
                        if cells > 10000:
                            raise DirectConnectionError('DIRECT_WORKBOOK_TOO_LARGE')
                        if value is None:
                            continue
                        label, colon, content = str(value).partition(':')
                        label = label.strip().lower()
                        if not colon or label not in {'hostname', 'username', 'password', 'public ip', 'private ip', 'port', 'ssh port'}:
                            raise DirectConnectionError('DIRECT_WORKBOOK_FIELD_UNSUPPORTED')
                        if label == 'hostname':
                            if set(current) - {'hostname'}:
                                records.append(current)
                            # The supplied file has a hostname-only section title.
                            current = {'hostname': content.strip()}
                            continue
                        if not current or label in current:
                            raise DirectConnectionError('DIRECT_WORKBOOK_AMBIGUOUS')
                        # Remove the label's formatting space only; do not modify
                        # the supplied password's trailing whitespace or punctuation.
                        current[label] = (content[1:] if content.startswith(' ') else content) if label == 'password' else content.strip()
                if set(current) - {'hostname'}:
                    records.append(current)
                current = {}
            wb.close()
            targets = []
            for record in records:
                if not {'hostname', 'username', 'password', 'public ip'} <= record.keys():
                    raise DirectConnectionError('DIRECT_WORKBOOK_TARGET_INCOMPLETE')
                target_port = int(record.get('port', record.get('ssh port', port)))
                if not 1 <= target_port <= 65535 or not all(record[k] for k in ('hostname', 'username', 'password')):
                    raise DirectConnectionError('DIRECT_WORKBOOK_TARGET_INVALID')
                ipaddress.ip_address(record['public ip'])
                targets.append(Target(record['hostname'], record['public ip'], target_port, record['username'], record['password']))
            if (not targets or len(targets) > 16 or len({t.name for t in targets}) != len(targets)
                    or len({(t.host, t.port, t.username) for t in targets}) != len(targets)):
                raise DirectConnectionError('DIRECT_WORKBOOK_TARGET_AMBIGUOUS')
            return tuple(targets)
        except DirectConnectionError:
            raise
        except Exception:
            raise DirectConnectionError('DIRECT_WORKBOOK_INVALID') from None


def get_target(name, environ=None):
    matches = [t for t in read_targets(environ) if t.name == name]
    if len(matches) != 1:
        raise DirectConnectionError('DIRECT_WORKBOOK_TARGET_NOT_FOUND')
    return matches[0]