import http.client
import json
import ssl


def http_request(base_url: str, url: str, method: str = 'GET', headers: dict = None, body=None):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    conn = http.client.HTTPSConnection(base_url, context=ssl._create_unverified_context())
    if body is None:
        conn.request(method, url, headers=headers)
    else:
        conn.request(method, url, body, headers=headers)
    response = conn.getresponse()
    print('RESPONSE')
    print(response.getcode(), response.reason, '\n' + str(response.msg))
    data = response.read()
    if data != b'':
        data = json.loads(data)
    else:
        data = None
    conn.close()
    return response, data
