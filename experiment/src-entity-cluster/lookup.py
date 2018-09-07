import json
import requests

class Lookup(object):
    url = 'http://lookup.dbpedia.org/api/search/KeywordSearch'

    def __init__(self, query_str='', max_hits=0):
        self.query_str = query_str
        self.max_hits = max_hits

    def query(self):
        candidate_set = set()
        header = {'Accept':'application/json'} 
        param = {'QueryString':self.query_str,
                'MaxHits':self.max_hits}
        ret_json = requests.get(Lookup.url, headers = header, params = param).json()
        return ret_json