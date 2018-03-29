import os
import json
import requests

uri_path = 'uri/'
url = 'http://lookup.dbpedia.org/api/search/KeywordSearch'
maxhist = 5

def get_wd(fn):
    with open(fn, 'r') as wd_read:
        wd_list = wd_read.readlines()
        return wd_list
    
def set_query(wd_list):
    candidate_set = set()
    header = {'Accept':'application/json'} 
    for word in wd_list:
        print(word)
        param = {'QueryString':word,
                 'MaxHits':maxhist}
        ret_json = requests.get(url, headers = header, params = param).json()

        word_ent_path = os.path.join(uri_path, word)
        with open(word_ent_path, 'w') as we_write:
            for candidate in ret_json['results']:
                candidate_info = candidate['uri'] + ' ' + str(candidate['refCount'])
                print(candidate_info)
                we_write.write(candidate_info + '\n')
                candidate_set.add(candidate_info)

    return candidate_set

def write_ent(fn, ent_set):
    with open(fn, 'w') as target:
        for ent in ent_set:
            target.write(ent + '\n')

def run():
    wd_list = get_wd('wd_set')
    ent_set = set_query(wd_list)
    print(ent_set)
    write_ent('ent_set', ent_set)


if __name__ == '__main__':
    run()