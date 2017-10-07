"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib

query = 'Cat'
service_url = 'http://lookup.dbpedia.org/api/search/KeywordSearch'
params = {
    'QueryString': query,
    'QueryClass':'',
    'MaxHits':1,
}
url = service_url + '?' + urllib.urlencode(params)
response = urllib.urlopen(url).read().decode()
print response
