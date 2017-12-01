import math
import numpy

def get_data(fn):
    vector = []
    with open(fn, 'r') as origin:
        for line in origin.readlines():
            line = line.strip().split(';')
            line[-1] = float(line[-1])
            if line[0] > line[1]:
                line[0], line[1] = line[1], line[0]
            vector.append(line)

    return vector

def get_vec(fn1, fn2):
    v1 = get_data(fn1)
    v1 = sorted(v1, key=lambda item: (item[0], item[1]))
    v2 = get_data(fn2)
    v2 = sorted(v2, key=lambda item: (item[0], item[1]))
    v1 = [i[-1] for i in v1]
    v2 = [i[-1] for i in v2]
    return v1, v2

def avg(v):
    return float(sum(v)) / len(v)

def spearman():
    pass

def pearson():
    v1, v2 = get_vec('../../../dataset/rg.csv', 'rg.csv.ret')
    v1_avg =  avg(v1)
    v2_avg =  avg(v2)

    head, tail1, tail2 = 0, 0, 0
    for i in range(len(v1)):
        v1_d = v1[i] - v1_avg
        v2_d = v2[i] - v2_avg

        head += v1_d * v2_d

        tail1 += v1_d * v1_d
        tail2 += v2_d * v2_d

    return head / (math.sqrt(tail1) * math.sqrt(tail2))

if __name__ == '__main__':
    print(pearson())

    # 0.3198519675185866