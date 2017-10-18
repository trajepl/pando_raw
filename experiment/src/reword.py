import os
import math
import json

# number_of_triple = 438336517
number_of_triple = 2400000000
pf_ipf_ret = 'pf_ipf_ret'
root_uri = 'http://dbpedia.org/resource/'

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
                    # path_in = os.path.join(path4, entity)
                    path_in = path4
                    pf_ipf_path2 = os.path.join(pf_ipf_path1, entity)

                    tmp_list = path_in.split('/')
                    tmp_list[0] = 'predicate_out'
                    path_out = '/'.join(tmp_list)

                    ret.append([path_in, path_out, pf_ipf_path2])
    return ret

def pf_ipf(p, q, r):
    p = int(p)
    q = int(q)
    r = int(r)
    if r == 0 or q == 0:
        return 0
    return abs(p / q) * math.log(number_of_triple / r)

def path_info():
    pass

def predicate_info():
    info_list = predicate_info_file('predicate_in')
    for entry in info_list:
        with open(entry[0], 'r') as pre_in:
            tmp_str = pre_in.read()
            pre_in_info = json.loads(tmp_str)
            for result in pre_in_info['bindings']:
                pf_ipf_value(entry, result, 'in')

        with open(entry[1], 'r') as pre_out:
            tmp_str = pre_out.read()
            pre_in_info = json.loads(tmp_str)
            for result in pre_in_info['bindings']:
                pf_ipf_value(entry, result, 'out')

def pf_ipf_value(entry, result, way):
    predicate_uri = result['predicate']['value']
    predicate_fn = predicate_uri.replace('/', '-') + '-' + way
    entity_uri = root_uri + entry[-1].split('/')[-1]
    
    param1 = result['number']['value']
    param2 = get_target_number(entity_uri, 'entity')
    param3 = get_target_number(predicate_uri, 'predicate')
    pf_ipf_v = pf_ipf(param1, param2, param3)

    if len(predicate_fn) > 200:
        predicate_fn = predicate_fn[0:100]
    if not os.path.isdir(entry[-1]):
        os.makedirs(entry[-1])

    pre_fp = os.path.join(entry[-1], predicate_fn)
    if os.path.exists(pre_fp):
        print('file exists.')
        return 
    print(pre_fp)
    with open(pre_fp, 'w') as out:
        out.write(str(pf_ipf_v))

def get_target_number(uri, way):
    fn = uri.replace('/', '-')

    if len(fn) > 200:
        fn = fn[0:100]
    if way == 'predicate':
        target_fp = 'pf_ipf_info/predicate/'+fn
    elif way == 'entity':
        target_fp = 'pf_ipf_info/entity/'+fn

    if not os.path.exists(target_fp):
         return 0
    
    with open(target_fp, 'r') as read_in:
        ret = read_in.read().strip()    
    return int(ret)

def semantic_vec():
    pass

if __name__ == '__main__':
    predicate_info()