import os
import numpy

vector = {}
tab = '\t'
label = '__label__'

def cosine(v1, v2):
    n1 = numpy.linalg.norm(v1)
    n2 = numpy.linalg.norm(v2)
    ip = numpy.dot(v1, v2)
    return str(float(ip / (n1 * n2)))

def handle_vec(list_l):
    ret = []
    for l in list_l:
        ret.append(float(l))
    return ret

def load_vec(fn):
    print('begin load vector of entity...')
    global vector
    with open(fn, 'r') as v_out:
        for line in v_out.readlines():
            line = line.strip().split(tab)
            line[0] = line[0].strip().replace('/', '-')
            t_line = handle_vec(line[1:])

            vector[line[0]] = t_line
    print('load vector of entity complete!')

def word_pair(dataset):
    cos_ret = open(dataset + '.ret', 'w')

    uri = os.path.join('../uri/', dataset)
    for path1 in os.listdir(uri):
        path1 = os.path.join(uri, path1)
        vector_l = []
        line = ''
        for word in os.listdir(path1):
            line += word + ';'
            word = os.path.join(path1, word) 
            with open(word, 'r') as word_out:
                entity = word_out.readline().strip()
                entity = entity.replace('/', '-')
                entity = entity.lower()
                
                if entity in vector.keys():
                    vector_l.append(vector[entity])
                elif label + entity in vector:
                    vector_l.append(vector[label + entity])
                else:
                     vector_l.append([0]*50)

        rel = cosine(vector_l[0], vector_l[1])
        line += rel
        cos_ret.write(line + '\n')
    cos_ret.close()

if __name__ == '__main__':
    load_vec('../merger.csv')
    word_pair('rg.csv')