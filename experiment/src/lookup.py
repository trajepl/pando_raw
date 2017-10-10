import os
import sys
import json
import requests

url = 'http://lookup.dbpedia.org/api/search/KeywordSearch'

def path_gold(fn):
    """
    Parameters:
        param1 - path of summary of gold standard dataset
    Return:
        a list of path of kinds of gold standard dataset
    """
    path_collection = []
    with open(fn, 'r') as pre_in:
        root_path = pre_in.read()
    
    for name in os.listdir(root_path):
        name = os.path.join(root_path, name)
        if not os.path.isdir(name):
            path_collection.append(name)

    return path_collection


def file_csv(fn):
    """
    Parameters:
        param1 - file of format 'csv' (gold standard dataset)
    Return:
        word pairs in file of csv
    """
    word_pairs = []
    with open(fn, 'r') as csv:
        for line in csv.readlines():
            word_pairs.append(line.split(';'))
    return word_pairs

def lookup_dbpedia(url, header, param):
    """
    Parameters:
        param1 - url
        param2 - header of http request
        param3 - param of http request
    Return:
        result of request dbpedia look-up service
    """
    ret = requests.get(url, headers = header, params=param)
    return ret

def gen_ret(fn, dict):
    """
    Parameters:
        param1 - path of storing results by http request
        param2 - results by http request
    Return:
        null
    """
    text = json.dumps(dict)
    with open(fn, 'w') as out:
        out.write(text)
    print(fn)
    
def run():
    """
    function main 
    """
    if len(sys.argv) > 1:
        for fn in path_gold(sys.argv[1]):
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