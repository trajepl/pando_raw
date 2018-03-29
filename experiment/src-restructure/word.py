import os

root_dat = '../dataset'

def word_file_list(root):
    fn_list = []
    for fn in os.listdir(root):
        fn_list.append(os.path.join(root, fn))
    return fn_list

def word_set(fn_list):
    wd_set = set()
    for fn in fn_list:
        with open(fn, 'r') as out:
            for line in out.readlines():
                line = line.strip().split(';')
                wd_set.add(line[0])
                wd_set.add(line[1])
    return wd_set

def record_wd(fn, wd_set):
    with open(fn, 'w') as wd_in:
        for word in wd_set: 
            wd_in.write(word + '\n')

def run():
    fn_list = word_file_list(root_dat)
    wd_set = word_set(fn_list)
    record_wd('wd_set', wd_set)

if __name__ == '__main__':
    run()
