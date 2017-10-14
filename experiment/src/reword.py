import os
import math
import json

# number_of_triple = 438336517
number_of_triple = 2400000000
pf_ipf_ret = 'pf_ipf_ret'
root_uri = 'http://dbpedia.org/resorce/'

def predicate_info_file(dirpath):
    ret = []
    for dataset in os.listdir(dirpath):
        path1 = os.path.join(dirpath, dataset)
        for num in os.listdir(path1):
            path2 = os.path.join(path1, num)

            for word in os.listdir(path2):
                path3 = os.path.join(path2, word)
                pf_ipf_path1 = os.path.join(pf_ipf_ret, word)
                if not os.path.isdir(pf_ipf_path1):
                    os.makedirs(pf_ipf_path1)

                for entity in os.listdir(path3):
                    path4 = os.path.join(path3, entity)
                    path_in = os.path.join(path4, entity)
                    pf_ipf_path2 = os.path.join(pf_ipf_path1, entity)

                    tmp_list = path_in.split('/')
                    tmp_list[0] = 'predicate_out'
                    path_out = '/'.join(tmp_list)

                    ret.append([path_in, path_out, pf_ipf_path2])
    return ret

def pf_ipf(p, q, r):
    return abs(p / q) * math.log(abs(number_of_triple) / r)

def path_info():
    pass

def predicate_info():
    info_list = predicate_info_file('predicate_in')
    for entry in info_list:
        with open(entry[0], 'r') as pre_in:
            tmp_str = pre_in.read()
            pre_in_info = json.loads(tmp_str)
            for result in pre_in_info:
                pf_ipf_value(entry, result, 'in')
                pf_ipf_value(entry, result, 'out')

def pf_ipf_value(entry, result, way):
    predicate_uri = result['predicate']
    predicate_fn = predicate_uri.replace('/', '-') + '-' + way
    pre_fp = os.path.join(entry[-1], predicate_fn)
    entity_uri = root_uri + entry[-1].split('/')[-1]

    param1 = result['number']['value']
    param2 = get_target_number(entity_uri, 'entity')
    param3 = get_target_number(predicate_uri, 'predicate')
    pf_ipf_v = pf_ipf(param1, param2, param3)
    with open(predicate_fn, 'w') as out:
        out.write(pf_ipf_v)

def get_target_number(uri, way):
    fn = uri.replace('/', '-')
    if way == 'predicate':
        target_fp = 'pf_ipf_info/predicate/'+fn
    elif way == 'entity':
        target_fp = 'pf_ipf_info/entity/'+fn
    
    with open(target_fp, 'r') as read_in:
        ret = read_in.read().strip()

    return int(ret)

def semantic_vec():
    pass

if __name__ == '__main__':
    predicate_info()