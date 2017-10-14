import os

# number_of_triple = 438336517
number_of_triple = 2400000000
pf_ipf_ret = 'pf_ipf_ret'

def predicate_info_file(dirpath):
    ret = []
    for name in os.listdir(dirpath):
        path1 = os.path.join(dirpath, name)
        for dataset in os.listdir(path1):
            path2 = os.path.join(path1, dataset)

            for num in os.listdir(path2):
                path3 = os.path.join(path2, num)

                for word in os.listdir(path2):
                    path4 = os.path.join(path3, word)
                    pf_ipf_path1 = os.path.join(pf_ipf_ret, word)
                    if not os.path.isdir(pf_ipf_path1):
                        os.makedirs(pf_ipf_path1)

                    for entity in os.listdir(path4):
                        path_in = os.path.join(path4, entity)
                        pf_ipf_path2 = os.path.join(pf_ipf_path1, entity)

                        tmp_list = path_in.split('/')
                        tmp_list[0] = 'predicate_out'
                        path_out = '/'.join(tmp_list)

                        ret.append([path_in, path_out, pf_ipf_path2])
    return ret

def pf_ipf():
    pass

def path_info():
    pass

def pre_fre(flag):
    pass


def predicate_info():
    file_list = predicate_info_file('predicate_in')
    print(file_list)


def semantic_vec():
    pass

if __name__ == '__main__':
    predicate_info()