import os
import json
import query 

entity_path = 'entity'
predicate_path = 'predicate'
predicate_in_path = 'predicate_in'
pre_path = 'pf_ipf_info'

def predicate_info_file(dirpath):
    ret = []
    for name in os.listdir(dirpath):
        path1 = os.path.join(dirpath, name)
        for dataset in os.listdir(path1):
            path2 = os.path.join(path1, dataset)
        for num in os.listdir(path2):
            path3 = os.path.join(path2, num)

            for word in os.listdir(path3):
                path3_in = os.path.join(path3, word)
                tmp_list = path3_in.split('/')
                tmp_list[0] = 'predicate_out'
                path3_out = '/'.join(tmp_list)

                ret.append([path3_in, path3_out])
    return ret

def file_list(dirpath):
    ret = []
    for name in os.listdir(dirpath):
        uripath1 = os.path.join(dirpath, name)
        for fn in os.listdir(uripath1):
            uripath2 = os.path.join(uripath1, fn)

            word_pair = os.listdir(uripath2)
            uripath3 = os.path.join(uripath2, word_pair[0])
            ret.append([word_pair[0], uripath3])

            uripath3 = os.path.join(uripath2, word_pair[1])
            ret.append([word_pair[1], uripath3])
    return ret

def entity_number():
    entity_dir = 'pf_ipf_info/entity'
    if not os.path.isdir(entity_dir):
        os.makedirs(entity_dir)

    entitys = file_list('uri')
    for entity in entitys:
        with open(entity[-1], 'r') as word_in:
            e_list = word_in.readlines()
            for e in e_list:
                filename = os.path.join(entity_dir, e.replace('/', '-'))
                if os.path.exists(filename):
                    print('File exists. Query already done.')
                    continue
                entity_num = entity_num_query(e)
                print(entity_num)
                ret = query.query(entity_num)['results']
                
                record_number(filename, ret)

def predicate_number():
    predicate_dir = 'pf_ipf_info/predicate'
    if not os.path.isdir(predicate_dir):
        os.makedirs(predicate_dir)

    path_info_list = predicate_info_file(predicate_in_path)
    for path_info in path_info_list:
        read_predicate_num(path_info[-1], predicate_dir)
        read_predicate_num(path_info[-2], predicate_dir)
        

def read_predicate_num(fn, predicate_dir):
    with open(fn, 'r') as pre_in:
        predicate_num = pre_in.read()
        predicate_num = json.loads(predicate_num)

        for predicate in predicate_num['bindings']:
            predicate = predicate['predicate']['value']
            tmp_str = predicate_num_query(predicate)

            predicate_change = predicate.replace('/','-')
            predicate_path = os.path.join(predicate_dir, predicate_change)
            if os.path.exists(predicate_path):
                continue
            
            print(tmp_str)
            ret = query.query(tmp_str)['results']
            record_number(predicate_path, ret)
            
def entity_num_query(entity):
    entity = entity.strip()
    return query.prefix + """
    select count(?p1)+count(?p2) as ?count
    where { 
        {<""" + entity + """> ?p1 ?o.} 
        union
        {?s ?p2 <""" + entity + """>.} 
    }
    """

def predicate_num_query(predicate):
    predicate = predicate.strip()
    return query.prefix + """
    select count(?s) as ?count
    where { 
        {?s <""" + predicate + """> ?o.} 
    }
    """
def record_number(fn, content):
    print(content)
    with open(fn, 'w') as out:
        out.write(content['bindings'][0]['count']['value'])

def run():
    entity_number()
    # predicate_number()
        
if __name__ == '__main__':
    run()