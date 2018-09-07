import os
import sys
import json
import time
import pickle
from SPARQLWrapper import SPARQLWrapper, JSON

triple = 'triple'
fin_list = []
titleid_entity = {}
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

prefix = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://dbpedia.org/resource/>
PREFIX dbpedia2: <http://dbpedia.org/property/>
PREFIX dbpedia: <http://dbpedia.org/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
"""

def run_time(func):
    def wrapper(*argv):
        s = time.time()
        f = func(*argv)
        e = time.time()
        print(func.__name__ + ' runtime: ' + str(e-s))
        return f
    return wrapper

def ent_uri(fn):
    ret = []
    with open(fn, 'r') as ent_in:
        ret = ent_in.readlines()
    return ret

def query(sparql_str):
    """
    Parameters:
        param1 - string of sparql query
    Return:
        null
    """
    try:
        sparql.setQuery(sparql_str)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
    except Exception as e:
        print(str(e))
        results = {"results": {"bindings": []}}

    return results

def wikiid(ent):
    wikipageid = '<http://dbpedia.org/ontology/wikiPageID>'
    ent = '<' + ent.strip() + '>'
    return """
    select * where {
        { 
            """ + ent + ' ' + wikipageid + """  ?o.
        } 
    }
    """

def get_entity_by_wikiid(wikiid):
    wikipageid = '<http://dbpedia.org/ontology/wikiPageID>'
    return """
    select * where {
        { 
             ?s """  + wikipageid + ' ' + str(wikiid) + """.
        } 
    }
    """

def get_word_entity_from_tfidf(dump_file, titleid_entity_fn):
    global fin_list, titleid_entity
    print('loading handled title...')
    fin_list = pickle.load(open(dump_file, 'rb'))
    titleid_entity = pickle.load(open(titleid_entity_fn, 'rb'))

    print('loading top_100_tf_idf...')
    ret_word_entity = dict()
    top_k_tf_idf = pickle.load(open('./dump/top_100_tf_idf', 'rb'))

    for word, title_tf_idf in top_k_tf_idf.items():
        ent_tf_idf = list()
        for item in title_tf_idf:
            title_tf_idf_dict = dict()
            for title_id, val in item.items():
                if title_id in fin_list:
                    triple_s = titleid_entity[title_id]
                else:
                    query_ret = query(get_entity_by_wikiid(title_id))
                    for value in query_ret['results']['bindings']:
                        triple_s = value['s']['value']
                    titleid_entity[title_id] = triple_s
                    fin_list.append(title_id)
                print(triple_s, val)
                title_tf_idf_dict[triple_s] = float(val)
                ent_tf_idf.append(title_tf_idf_dict)
        print(word + ' query successed!')
        ret_word_entity[word] = ent_tf_idf
    pickle.dump(ret_word_entity, open('./dump/fin_title', 'wb'))

def get_word_entity_from_lookup(func, params):
    global fin_list
    fin_list = pickle.load(open(dump_file, 'rb'))
    ent_id = open('entity_id', 'w')

    with open('wd_set', 'r') as wd_read:
        for line in wd_read.readlines():
            word = line.strip().lower()
            uri_file = os.path.join('uri', word)
            with open(uri_file, 'r') as uri_read:
                uri_list_str = uri_read.readlines()[0]
                uri_list = json.loads(uri_list_str)
                for uri in uri_list:
                    if uri[0] in fin_list: 
                        print(uri[0])
                        continue                        
                    ret = query(func(uri[0]))
                    for value in ret['results']['bindings']:
                        triple_o = value[params]['value']
                        li = uri[0] + ' ' + triple_o
                        ent_id.write(li + '\n')    
                        print(word + " " + li)
                    fin_list.append(uri[0])
    ent_id.close()
    
if __name__ == '__main__':
    try:
        dump_file = 'dump/tf_idf_title_id'
        titleid_entity_fn = 'dump/titleid_entity'
        get_word_entity_from_tfidf(dump_file, titleid_entity_fn)
    except Exception as e:
        print('error', e)
    finally:
        fin = open(dump_file, 'wb')
        pickle.dump(fin_list, fin)
        fin.close()

        fin = open(titleid_entity_fn, 'wb')
        pickle.dump(titleid_entity, fin)
        fin.close()