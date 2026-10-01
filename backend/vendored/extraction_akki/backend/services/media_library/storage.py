"""Managed object storage. No public URLs, browser credentials or pretend hard deletion."""
import os
import threading
from urllib.parse import quote

import requests

_key = None
_lock = threading.Lock()
_last_error = None


class StorageError(Exception):
    def __init__(self, status):
        self.status = status
        super().__init__('Storage temporarily unavailable' if status in (500,503) else 'Storage request refused')


def base():
    return os.environ['INTEGRATION_PROXY_URL'].rstrip('/')+'/objstore/api/v1/storage'


def initialize(force=False):
    global _key, _last_error
    with _lock:
        if _key and not force:
            return _key
        try:
            response = requests.post(base()+'/init',json={'emergent_key':os.environ['EMERGENT_LLM_KEY']},timeout=30)
            if response.status_code != 200:
                raise StorageError(response.status_code)
            _key = response.json()['storage_key']
            _last_error = None
            return _key
        except (requests.RequestException,KeyError,ValueError):
            _last_error = 'Storage connection unavailable'
            raise StorageError(503)
        except StorageError:
            _last_error = 'Storage connection unavailable'
            raise


def ready():
    return bool(_key), _last_error


def _request(method,path,*,stream=False,data=None,content_type=None):
    for attempt in range(2):
        try:
            headers = {'X-Storage-Key':initialize(force=attempt==1)}
            if content_type: headers['Content-Type']=content_type
            if data is not None: data.seek(0)
            response=requests.request(method,base()+'/objects/'+quote(path,safe='/'),headers=headers,
                                      data=data,stream=stream,timeout=(15,120))
        except requests.RequestException:
            raise StorageError(503)
        if response.status_code==404 and attempt==0:
            response.close()
            continue
        if not response.ok:
            status=response.status_code; response.close()
            raise StorageError(status)
        return response
    raise StorageError(503)


def put(path,file,content_type):
    response=_request('PUT',path,data=file,content_type=content_type)
    try:
        result=response.json()
        if not isinstance(result.get('path'),str) or not result['path']:
            raise StorageError(503)
        return result
    finally: response.close()


def download(path):
    return _request('GET',path,stream=True)