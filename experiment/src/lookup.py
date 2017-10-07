import os
import sys
import json
import requests

url = 'http://lookup.dbpedia.org/api/search/KeywordSearch'

def path_gold(fn):
    path_collection = []
    with open(fn, 'r') as pre_in:
        root_path = pre_in.read()
    
    for name in os.listdir(root_path):
        name = os.path.join(root_path, name)
        if not os.path.isdir(name):
            path_collection.append(name)
    
    return path_collection

def file_csv(fn):
    word_pairs = []
    with open(fn, 'r') as csv:
        for line in csv.readlines():
            word_pairs.append(line.split(';'))
    return word_pairs

def lookup_dbpedia(url, header, param):
    ret = requests.get(url, headers = header, params=param)
    return ret

def gen_ret(fn, dict):
    text = json.dumps(dict)
    with open(fn, 'w') as out:
        out.write(text)
    
def run():
    if len(sys.argv) > 1:
        for fn in path_gold(sys.argv[1]):
            print(fn)
            newdir = 'tmp/' + fn.split('/')[-1] + '/'
            if not os.path.isdir(newdir):
                os.makedirs(newdir)

            cnt = 0
            for word_pair in file_csv(fn):
                tmpnewdir = newdir + str(cnt) + '/'
                if not os.path.isdir(tmpnewdir):
                    os.makedirs(tmpnewdir)
                
                header = {'Accept':'application/json'}
                params = {'QueryString':word_pair[0]}
                ret = lookup_dbpedia(url, header, params)
                gen_ret(tmpnewdir + word_pair[0], ret.json())

                params = {'QueryString':word_pair[1]}
                ret = lookup_dbpedia(url, header, params)
                gen_ret(tmpnewdir + word_pair[1], ret.json())

                cnt += 1
    else:
        print('need path of gold-standard.')

    
if __name__ == '__main__':
    run()