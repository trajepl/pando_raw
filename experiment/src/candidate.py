import os
import sys
import json

uripath = 'uri'

def travel(dirpath):
    for name in os.listdir(dirpath):
        filepath1 = os.path.join(dirpath, name)
        uripath1 = os.path.join(uripath, name)

        for fn in os.listdir(filepath1):
            filepath2 = os.path.join(filepath1, fn)
            uripath2 = os.path.join(uripath1, fn)

            for word in os.listdir(filepath2):
                filepath3 = os.path.join(filepath2, word)
                uripath3 = os.path.join(uripath2, word)
                if not os.path.isdir(uripath2):
                    os.makedirs(uripath2)

                print(filepath3)
                with open(filepath3, 'r') as pre_in:
                    uri_dict = json.loads(pre_in.read())
                    
                extract(uri_dict, uripath3)

def extract(dict, filepath):
    with open(filepath, 'w') as out:
        for ret in dict['results']:
            out.write(ret['uri'] + '\n')

def run():
    tmp_file = 'tmp'
    travel(tmp_file)


if __name__ == '__main__':
    run()