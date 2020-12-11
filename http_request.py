import http.client
import json
import ssl
from printer import printer

_log_prefix = '[HTTP-CLIENT] >'
_log_width = 80


def log(*args, center: str = None):
    printer(*args, prefix=_log_prefix, width=_log_width, center=center)


def http_request(base_url: str, url: str, method: str = 'GET', headers: dict = None, body: dict = None,
                 verbose: bool = False, log_width=80):
    global _log_width
    _log_width = log_width

    if headers is None:
        headers = {'Content-Type': 'application/json'}
    conn = http.client.HTTPSConnection(base_url, context=ssl._create_unverified_context())
    if verbose:
        log('REQUESTING DATA TO ' + base_url)
    if body is None:
        conn.request(method, url, headers=headers)
    else:
        conn.request(method, url, json.dumps(body), headers=headers)
    response = conn.getresponse()
    if verbose:
        log('HTTP RESPONSE')
        log(response.getcode(), response.reason)
        log(str(response.msg))
    data = response.read()
    if data != b'':
        data = json.loads(data)
    else:
        data = None
    conn.close()
    return response, data
