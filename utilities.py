import json

import time


def read_json(json_path):
    with open(json_path, 'r') as f_in:
        data = json.load(f_in)
    return data


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap


if __name__ == '__main__':
    json_path = '/home/joanna/studia/misows/aws/conf.json'
    read_json(json_path)


