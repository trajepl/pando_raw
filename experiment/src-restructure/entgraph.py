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

def ent_tail(ent):
    ent = '<' + ent.strip() + '>'
    return """
    select * where {
        { 
            ?s ?p """ + ent + """. 
        } 
    }
    """

def ent_head(ent):
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
        triple = ent.strip() + tab + value['p']['value'] + tab + value['o']['value']
        fnpt.write(triple + '\n')
    
def indicts(fnpt, ent, rets):
    tab = '    '
    for value in rets['results']['bindings']:
        triple = value['s']['value'] + tab + value['p']['value'] + tab + ent.strip()
        fnpt.write(triple + '\n')

@run_time
def dfs(ent):
    ent_fn = os.path.join('entity', ent.replace('/','-'))
    ent_write = open(ent_fn, 'w')

    if len(ent) == 0:
        return 
    cnt = 0
    rets_in = query(ent_tail(ent))
    indicts(ent_write, ent, rets_in)
    cnt += len(rets_in['results']['bindings'])
    print(cnt)

    rets_out = query(ent_head(ent))
    outdicts(ent_write, ent, rets_out)
    cnt += len(rets_out['results']['bindings'])
    print(cnt)
    ent_write.close()

def run():
    global fin_list
    fin_list = pickle.load(open('entity/finish', 'rb'))

    with open('ent_set', 'r') as ent_read:
        for line in ent_read.readlines():
            entity = line.strip().split(' ')[0]
            print(entity)
            if not entity in fin_list:
                dfs(entity)
                fin_list.append(entity)
    

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)
    finally:
        fin = open('entity/finish', 'wb')
        pickle.dump(fin_list, fin)
        fin.close()