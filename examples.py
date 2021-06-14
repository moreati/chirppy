import json
import sys
import time

import requests

results = []
for i in range(30):
    url = "http://example.org?foo=%i" % i
    r = requests.post('https://api.chirp.io/0/chirp',
                      json.dumps({'url': url,
                                  'mimetype': 'text/x-url'}),
                      headers={'content-type': 'application/json'})
    d = r.json()
    d['url'] = url
    results.appaend(d)
    time.sleep(3)

json.dump(results, sys.stdout)
