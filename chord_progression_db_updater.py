import http.client
import ssl
from pymusicFP.pymusicFP import *
from client_credentials import client_credentials, url
from http_request import http_request


sentiments = ['anger', 'fear', 'love', 'joy', 'sadness', 'surprise']

music_information = []

for sentiment in sentiments:
    [music_information.append(mir('sheetmusic/' + sentiment + str(x + 1) + '.musicxml')) for x in range(8)]

[print(x) for x in music_information]

json_data = {'data': music_information}

print('\nREQUESTING ACCES TO MUSERES API')
response, auth = http_request(url, '/oauth/token', "POST", body=client_credentials, verbose=True)
if response.getcode() == 200:
    print('MUSERES API ACCESS GRANTED\n')
else:
    print('MUSERES API ACCESS DENIED\n')
    exit(401)

headers = {'Content-Type': 'application/json', 'Authorization': auth['token_type'] + ' ' + auth['access_token']}

print('\nREQUESTING MUSERES API TO UPDATE CHORD PROGRESSIONS ON DB WITH DATA:\n', json_data)
response, data = http_request(url, '/api/mir/update', "PUT", headers, json_data, verbose=True)
if response.getcode() == 200:
    print('DB CHORD PROGRESSIONS UPDATED')
else:
    print('MUSERES API ERROR, PLEASE VERIFY REQUEST\n', json_data)
    exit(500)
