import os
import sys
import json
import time
import pickle
from SPARQLWrapper import SPARQLWrapper, JSON

triple = 'triple'
fin_list = []
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

def rel_data(fn, dataset):
    global fin_list
    fin_list_p = open('finish', 'rb')
    fin_list = pickle.load(fin_list_p)

    uri_path = '../uri/'
    with open(fn, 'r') as word_pair:
        cnt = 0
        for line in word_pair.readlines():
            line = line.strip().split(';')

            path1 = os.path.join(triple, line[0])
            path2 = os.path.join(triple, line[1])
            if not path1 in fin_list:
                fn_uri_1 = os.path.join(uri_path, dataset, str(cnt), line[0])
                word_uri_1 = ent_uri(fn_uri_1)
                record_one_step(path1, word_uri_1)
                fin_list.append(path1)

            if not path2 in fin_list:
                fn_uri_2 = os.path.join(uri_path, dataset, str(cnt), line[1])
                word_uri_2 = ent_uri(fn_uri_2)
                record_one_step(path2, word_uri_2)
                fin_list.append(path2)

            cnt += 1


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


def isnot_literal(ent):
    ent = '<' + ent.strip() + '>'
    return """
    select * where {
        { 
            """ + ent + """ ?p ?o.
            filter(!isliteral(?o)) 
        } 
    }
    """
    # union {
    #         ?s ?p1 """ + ent + """.
    #     }

def ent_head(ent):
    ent = '<' + ent.strip() + '>'
    return """
    select * where {
        { 
            ?s ?p """ + ent + """. 
        } 
    }
    """

def is_english(ent):
    ent = '<' + ent.strip() + '>'
    return """
    select * where {
        {
            """ + ent + """ ?p ?o.
            filter(lang(?o)="en")
        }
    }
    """

def outdicts(fnpt, ent, rets):
    tab = '    '
    for value in rets['results']['bindings']:
        triple = ent + tab + value['p']['value'] + tab + value['o']['value']
        fnpt.write(triple + '\n')
    
def indicts(fnpt, ent, rets):
    tab = '    '
    for value in rets['results']['bindings']:
        triple = value['s']['value'] + tab + value['p']['value'] + tab + ent
        fnpt.write(triple + '\n')

@run_time
def dfs(fn, ent):
    print(fn)
    cat_out = open(fn, 'a')
    step = 0

    def ent_dfs(ent, step):
        if step > 0 or len(ent) == 0: 
            return 
        rets = query(ent_head(ent))
        indicts(cat_out, ent, rets)

        rets = query(is_english(ent))
        outdicts(cat_out, ent, rets)

        ent_list = []
        rets = query(isnot_literal(ent))
        outdicts(cat_out, ent, rets)

        for value in rets['results']['bindings']:
            item = value['o']['value']
            ent_list.append(item)
            ent_dfs(item, step+1)
            

    ent_dfs(ent, step)
    cat_out.close()

def record_one_step(fn, ret_list):
    with open(fn, 'w') as t:
        pass
    for ret in ret_list:
        dfs(fn, ret)
            
if __name__ == '__main__':
    try:
        rel_data('../../../dataset/rg.csv', 'rg.csv')
    except Exception as e:
        print(e)
    finally:
        fin =  open('finish', 'wb')
        pickle.dump(fin_list, fin)
        fin.close()