import os
import math
import time
import numpy as np
from functools import reduce

ent_embedding = dict()
ret_path = "result/"

def run_time(func):
    def wrapper(*argv):
        s = time.time()
        f = func(*argv)
        e = time.time()
        print(func.__name__ + ' runtime: ' + str(e-s))
        return f
    return wrapper

def print_log(fn, str_log):
    with open(fn, 'a') as log_out:
        log_out.write(str_log)

@run_time
def get_word_pairs(dir_path):
    data_set = dict()
    for fn in os.listdir(dir_path):
        fn_dat = os.path.join(dir_path, fn)
        with open(fn_dat, 'r') as dat_in:
            word_pair = dict()
            for line in dat_in.readlines():
                line = line.strip().split(';')
                key = ':'.join(line[0:-1])
                val = float(line[-1])
                # unify the sr scores to [0,10]
                if not 'wordsim' in fn_dat:
                    val = val / 4 * 10;
                word_pair[key] = val # word_pair[w1:w2] = val
            data_set[fn] = word_pair
    return data_set

def compress_uri(uri):
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

    for prefix in prefix_list:
       if prefix in uri:
           uri = uri.replace(prefix, prefix_dict[prefix])
    return uri

@run_time
def get_uri(ent_path):
    uri_path = dict()
    for word in os.listdir(ent_path):
        fn = os.path.join(ent_path, word)
        with open(fn, 'r') as ent_in:
            uri_list = []
            for line in ent_in.readlines():
                line = compress_uri(line.strip())
                # compress the representation of uri(ent, ref_count)
                uri_list.append(line)
        uri_path[word] = uri_list
    return uri_path

@run_time
def get_ent_embedding(fn):
    global ent_embedding
    with open(fn, 'r') as ent_in:
        for line in ent_in.readlines():
            line = line.strip().split('\t')
            key = line[0].strip().lower()
            vec = [float(x) for x in line[1:]]
            ent_embedding[key] = vec

# measure begin-----------------------
def cosine(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 == 0 or n2 == 0:
        return 0
    ip = np.dot(v1, v2)
    return float(ip / (n1 * n2))

def jaccard(v1, v2):
    ip = np.dot(v1, v2)
    n1 = np.linalg.norm(v1, 2)
    n2 = np.linalg.norm(v2, 2)
    return float(ip / (n1 + n2 - ip))

def spearman():
    pass

def get_sr(fn):
    sr_list = []
    with open(fn, 'r') as sr_in:
        for line in sr_in.readlines():
            line = line.strip().split(';')
            sr_list.append(float(line[-1]))
    sum_sr = sum(sr_list)
    if sum_sr == 0:
        sum_sr = 1e-10
    for i in range(len(sr_list)):
        sr_list[i] = sr_list[i] / sum_sr
    return sr_list

def pearson(v1, v2):
    v1_avg = float(sum(v1)) / len(v1)
    v2_avg = float(sum(v2)) / len(v2)

    head, tail1, tail2 = 1e-10, 1e-10, 1e-10
    for i in range(len(v2)):
        v1_d = v1[i] - v1_avg
        v2_d = v2[i] - v2_avg
        head += v1_d * v2_d
        tail1 += v1_d * v1_d
        tail2 += v2_d * v2_d
    return head / (math.sqrt(tail1) * math.sqrt(tail2))

def cc(v1, v2):
    vc = np.array(v1)
    vb = np.array(v2)
    return np.mean(np.multiply((vc - np.mean(vc)),(vb - np.mean(vb))))/(np.std(vb) * np.std(vc))
# measure end-----------------------

def closest_strategy(word_pair, uri_dict, notexist_out, func_dis):
    cnt = 0;
    closet_val = 0
    w1 = word_pair[0].lower()
    w2 = word_pair[1].lower()
    ent_w1 = uri_dict[w1]
    ent_w2 = uri_dict[w2]
    for e1 in ent_w1:
        e1 = e1.strip().split(' ')[0].lower()
        for e2 in ent_w2:
            e2 = e2.strip().split(' ')[0].lower()
            sr_val = 0
            if e1 in ent_embedding and e2 in ent_embedding:
                # print(e1 + ' ' + w1 + ' ' + e2)
                sr_val = abs(func_dis(ent_embedding[e1], ent_embedding[e2]))
            else:
                if not e1 in ent_embedding:
                    notexist_out.write(w1 + ':' + e1 + '\n')
                if not e2 in ent_embedding:
                    notexist_out.write(w2 + ':' + e2 + '\n')
            closet_val = max(closet_val, sr_val)
    return closet_val

def weighted_strategy(word_pair, uri_dict, alpha, func_dis):
    def sum_ref(e):
        ret = 0
        for item in e:
            ret += item[1]
        return ret

    w1 = word_pair[0].lower()
    w2 = word_pair[1].lower()
    ent_w1 = uri_dict[w1]
    ent_w2 = uri_dict[w2]
    ent1 = [[e1.strip().split(' ')[0].lower(), float(e1.strip().split(' ')[1])] for e1 in ent_w1]
    ent2 = [[e2.strip().split(' ')[0].lower(), float(e2.strip().split(' ')[1])] for e2 in ent_w2]
    ref_sum1 = sum_ref(ent1)
    ref_sum2 = sum_ref(ent2)
    weighted_val = 0
    for e1 in ent1:
        for e2 in ent2:
            if e1[0] in ent_embedding and e2[0] in ent_embedding:
                cosine_val = abs(func_dis(ent_embedding[e1[0]], ent_embedding[e2[0]]))
                weighted_val += (e1[1] / ref_sum1) * (e2[1] / ref_sum2) * pow(cosine_val, alpha)   
    # print_log('result/log', str(max_alpha) + ' ' +  str(weighted_val) + ' ' + w1 + '-' + w2 + '\n')
    return weighted_val

def measure_closest(data_dict, uri_dict, func_dis):
    notexist_out = open('result/notexist', 'w')
    for dataset, word_pairs in data_dict.items():
        fn = 'closest_' + func_dis.__name__ + '_' + dataset
        with open(os.path.join('result', fn), 'w') as data_out:
            for word_pair in word_pairs.keys():
                word_pair = word_pair.split(':')
                closest_val = closest_strategy(word_pair, uri_dict, notexist_out, func_dis)
                str_t = ';'.join([word_pair[0], word_pair[1], str(closest_val)])
                data_out.write(str_t + '\n')
    notexist_out.close()

def measure_weighted_cc(root_path, data_dict, uri_dict, func_dis):
    for dataset, word_pairs in data_dict.items():
        fn = 'weighted_' + func_dis.__name__ + '_' + dataset
        with open(os.path.join('result', fn), 'w') as data_out:
            max_alpha = 0
            max_weighted_sr = []
            p_val = 0
            for alpha in range(1, 11):
                weighted_sr = []
                for word_pair in word_pairs.keys():
                    word_pair = word_pair.split(':')
                    weighted_sr.append([word_pair[0], word_pair[1], weighted_strategy(word_pair, uri_dict, alpha, func_dis)])
                std_sr = get_sr(os.path.join(root_path, dataset))                
                p_tmp = pearson(std_sr, [sr[-1] for sr in weighted_sr])
                if p_val < p_tmp:
                    p_val = p_tmp
                    max_alpha = alpha
                    max_weighted_sr = weighted_sr
            for item in max_weighted_sr:
                str_t = ';'.join([item[0], item[1], str(max_alpha), str(item[2])])
                data_out.write(str_t + '\n')

def cc_scores(root_dir, ret_path, way, func_cc):
    stand_sr = {}
    for dataset in os.listdir(root_dir):
        stand_sr[dataset] = []
        fn = os.path.join(root_dir, dataset)
        stand_sr[dataset] = get_sr(fn)
    
    test_sr = {}
    for dataset in os.listdir(ret_path):
        if dataset.endswith('csv') and dataset.startswith(way):
            fn = os.path.join(ret_path, dataset)
            dataset = dataset.split('_')[-1]
            test_sr[dataset] = get_sr(fn)
    
    for key in stand_sr.keys():
        print(key + ':', end = ' ')
        print(func_cc(stand_sr[key], test_sr[key]))
        
def run():
    ret_path = 'result/'

    root_dat = '../dataset'
    data_dict = get_word_pairs(root_dat)
    # print(data_dict)

    uri_path = 'uri/'
    uri_dict = get_uri(uri_path)
    # print(uri_dict)

    embedding_path = 'merger.tsv'
    get_ent_embedding(embedding_path)

    print("(cosine) closest strategy--------------")
    measure_closest(data_dict, uri_dict, cosine)
    cc_scores(root_dat, ret_path, 'closest', pearson)
    # cc_scores(root_dat, ret_path, cc)

    print("(cosine) weighted strategy-------------")
    measure_weighted_cc(root_dat, data_dict, uri_dict, cosine)
    cc_scores(root_dat, ret_path, 'weighted', pearson)
    print()

    print("(jaccard) closest strategy--------------")
    measure_closest(data_dict, uri_dict, jaccard)
    cc_scores(root_dat, ret_path, 'closest', pearson)
    # cc_scores(root_dat, ret_path, cc)

    print("(jaccard) weighted strategy-------------")
    measure_weighted_cc(root_dat, data_dict, uri_dict, jaccard)
    cc_scores(root_dat, ret_path, 'weighted', pearson)

if __name__ == '__main__':
    run()