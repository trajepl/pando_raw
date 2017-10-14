import os
import sys
import json
from SPARQLWrapper import SPARQLWrapper, JSON

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

predicate_info_in = 'predicate_in'
predicate_info_out = 'predicate_out'
pf_ipf = 'pf_ipf'
path_info = 'path'
uri_file = 'uri'

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
        print_err(str(e))
        results = {"results": {"bindings": []}}

    return results

def file_list(dirpath, flag):
    """
    Parameters:
        param1 - root path of json file
    Return:
        list
    """
    ret = []
    for name in os.listdir(dirpath):
        uripath1 = os.path.join(dirpath, name)
        if flag == 'in':
            pred_path1 = os.path.join(predicate_info_in, name)
        elif flag == 'out':
            pred_path1 = os.path.join(predicate_info_out, name)
        elif flag == 'path':
            pred_path1 = os.path.join(path_info, name)
        elif flag == 'predicate_in':
            pred_path1 = os.path.join(pf_ipf, name)
        else:
            pred_path1 = ''
        
        for fn in os.listdir(uripath1):
            uripath2 = os.path.join(uripath1, fn)
            pred_path2 = os.path.join(pred_path1, fn)
            if not os.path.isdir(pred_path2):
                os.makedirs(pred_path2)

            word_pair = os.listdir(uripath2)
            uripath3 = os.path.join(uripath2, word_pair[0])
            pred_path3 = os.path.join(pred_path2, word_pair[0])
            ret.append([pred_path2, pred_path3, word_pair[0], uripath3])

            uripath3 = os.path.join(uripath2, word_pair[1])
            pred_path3 = os.path.join(pred_path2, word_pair[1])
            ret.append([pred_path2, pred_path3, word_pair[1], uripath3] )
    return ret

def extract(ret_dict, filepath):
    """
    Parameters:
        param1 - dictory of json loads
        param2 - target file path
    Return:
        null
    """
    with open(filepath, 'w') as out:
        out.write(json.dumps(ret_dict))
            

def gen_sparql_predicate_in(uri):
    uri = uri.strip()
    return prefix + """
    select ?predicate (count(?predicate) as ?number) 
    where { <""" + uri + """> ?predicate ?object. 
    }"""

def gen_sparql_predicate_out(uri):
    uri = uri.strip()
    return prefix + """
    select ?predicate (count(?predicate) as ?number) 
    where {  ?object ?predicate <""" + uri + """>. 
    }"""

def gen_sparql_path(uri1, uri2):
    uri1 = uri1.strip()
    uri2 = uri2.strip()
    uri2 = '"' + uri2 + '"'
    ret = prefix + """
    select *
    where { <""" + uri1 + """> ?p1 ?o1. 
    ?o1 ?p2 ?o2.
    ?o2 ?p3 ?o3.
    FILTER (?o1="""+ uri2 + """ || 
            ?o2="""+ uri2 + """ || 
            ?o3="""+ uri2 + """)
    }"""

    return ret

def print_log(content):
    with open('log/log.txt', 'a') as out:
        out.write(content+'\n')

def print_err(content):
    with open('log/err.txt', 'a') as out:
        out.write(content+'\n')        

def run_path():
    uris = file_list(uri_file, 'path')
    for i in range(0, len(uris), 2):
        
        with open(uris[i][-1], 'r') as word_in:
            e_list1 = word_in.readlines()
        with open(uris[i+1][-1], 'r') as word_in:
            e_list2 = word_in.readlines()

        for m in range(0, len(e_list1)):
            for n in range(0, len(e_list2)):
                try:
                    entity1 = e_list1[m].strip().split('/')[-1]
                    entity2 = e_list2[n].strip().split('/')[-1]
                except Exception as e:
                    print_err(e_list1[n] + ':' + str(e))
                    continue
                
                filename = entity1 + '-' + entity2
                filepath = os.path.join(uris[i][0], filename)

                if os.path.exists(filepath) or os.path.exists(filepath + '-0') or entity1 == entity2:
                    print_log('file exits')
                    continue
                
                query_path = gen_sparql_path(e_list1[m], e_list2[n])
                ret_path = query(query_path)['results']
                if len(ret_path['bindings']) == 0:
                    filepath += '-0'
                
                if not os.path.isdir(uris[i][0]):
                        os.makedirs(uris[i][0])
                        
                extract(ret_path, filepath)
                print_log(filepath)


def run():
    """
    function main
    """
    if len(sys.argv) <= 1:
        print('need type of predicate')
    else:
        uris = file_list(uri_file, sys.argv[1])
        for uri in uris:
            with open(uri[-1], 'r') as word_in:
                for entity in word_in.readlines():
                    if sys.argv[1] == 'in':
                        query_pre = gen_sparql_predicate_in(entity)
                    if sys.argv[1] == 'out':
                        query_pre = gen_sparql_predicate_out(entity)

                    ret = query(query_pre)['results']
                    filepath = os.path.join(uri[1], entity.split('/')[-1].strip())
                    print(filepath)
                    
                    if not os.path.isdir(uri[1]):
                        os.makedirs(uri[1])
                    extract(ret, filepath)

if __name__ == '__main__':
    run_path()
    