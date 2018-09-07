import os
import json
import pickle
from lookup import Lookup

uri_full_path = 'uri_full/'
uri_path = 'uri/'
finish_fn = 'uri/finish'
max_hits = 1000
fin_list = []

def get_wd(fn):
    wd_list = []
    with open(fn, 'r') as wd_read:
        for word in wd_read.readlines():
            wd_list.append(word.strip().lower())
    return wd_list


def get_full_entity(word):
    q = Lookup()
    q.query_str = word
    q.max_hits = max_hits
    ent_list = q.query()['results']

    # while ent_list[-1]['refCount'] != 0:
    #     q.max_hits += 200
    #     ent_list = q.query()['results']

    ent_list_len = len(ent_list)
    i = 1
    while ent_list[ent_list_len - i]['refCount'] == 0:
        i += 1
    ent_list = ent_list[0:ent_list_len-i+1]
    return ent_list

def record_entitys(wrods):
    global fin_list
    for word in wrods:
        print(word)
        if word not in fin_list:
            ents = get_full_entity(word)
            full_entitys_path = os.path.join(uri_full_path, word)
            we_write1 = open(full_entitys_path, 'w')
            json.dump(ents, we_write1)
            we_write1.close()

            simple_ents = [[x['uri'], x['refCount']] for x in ents]
            part_entitys_path = os.path.join(uri_path, word)
            we_write2 = open(part_entitys_path, 'w')
            json.dump(simple_ents, we_write2)
            we_write2.close()
            fin_list.append(word)

def run():
    global fin_list
    fin_list = pickle.load(open(finish_fn, 'rb'))
    words = get_wd('wd_set')
    record_entitys(words)

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)
    finally:
        fin = open(finish_fn, 'wb')
        pickle.dump(fin_list, fin)
        fin.close()