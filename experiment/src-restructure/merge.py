import os
import sys
import time

uri = 'uri/'
entity_path = 'entity/'
data_path = 'data/merge'
data_part_path = 'data/merge_pt'

prefix_list = [
    'http://dbpedia.org/resource/',
    'http://dbpedia.org/',
    'ontology/wikiPageWikiLink',
    'ontology/wikiPageRedirects',
    'ontology/',
    'http://www.w3.org/',
]
prefix_dict = {
    'http://dbpedia.org/resource/' : ' ',
    'http://dbpedia.org/' : '0/',
    'ontology/wikiPageWikiLink' : '1',
    'ontology/wikiPageRedirects' : '2',
    'ontology/' : '3/',
    'http://www.w3.org/' : '4/',
}


def run_time(func):
    def wrapper(*argv):
        s = time.time()
        f = func(*argv)
        e = time.time()
        print(func.__name__ + ' runtime: ' + str(e-s))
        return f
    return wrapper

@run_time
def merge(ent_path, file_op):
    for ent in os.listdir(ent_path):
        if 'finish' in ent:
            continue

        fn = os.path.join(ent_path, ent)
        with open(fn, 'r') as ent_read:
            for triple in ent_read.readlines():
                for prefix in prefix_list:
                    triple = triple.replace(prefix, prefix_dict[prefix])
                file_op.write(triple)


def words(wordset):
    word_list = []
    with open(wordset, 'r') as wd_read:
        for line in wd_read.readlines():
            line = line.strip().split(';')
            word_list.append(line[0])
            word_list.append(line[1])
    return word_list

def uris(word):
    uris_list = []
    fn = os.path.join(uri, word)
    with open(fn, 'r') as uri_read:
        for line in uri_read.readlines():
            line = line.split(' ')[0]
            uris_list.append(line)
    return uris_list

@run_time
def merge_part(wordset, file_op):
    words_list = words(wordset)
    for word in words_list:
        uris_list = uris(word)
        for uri in uris_list:
            # get corrsponding entities
            uri = uri.replace('/', '-')
            fn = os.path.join(entity_path, uri)
            with open(fn, 'r') as ent_read:
                for triple in ent_read.readlines():
                    for prefix in prefix_list:
                        triple = triple.replace(prefix, prefix_dict[prefix])                    
                    file_op.write(triple)

def run_part():
    mc_path = "../dataset/mc.csv"
    file_op = open(data_part_path, 'w')
    merge_part(mc_path, file_op)
    file_op.close()

def run():
    file_op = open(data_path, 'w')
    merge(entity_path, file_op)   
    file_op.close()

if __name__ == '__main__':
    run()
    # run_part()