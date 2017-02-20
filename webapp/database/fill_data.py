import argparse
import random
import string

import psycopg2
from os import listdir

from os.path import join

from webapp.database.database import Database


def fill_database(source_dir, products_num=10000):
    db = Database('./config.json')

    img_files = [join(source_dir, name) for name in listdir(source_dir)]
    img_data = []
    for img_file in img_files:
        with open(img_file, 'rb') as f_in:
            img_data.append(psycopg2.Binary(f_in.read()))

    categories = ["dress", "shoes", "trousers", "hats"]
    colors = ["black", "red", "green", "yellow"]

    for i in xrange(products_num):
        db.insert('products', {
            "description": random_word(100),
            "category": random.choice(categories),
            "color": random.choice(colors),
            "picture": random.choice(img_data)
        })


def random_word(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source_dir', required=True)
    parser.add_argument('-p', '--product_num', required=True)
    args = parser.parse_args()

    fill_database(args.source_dir, args.product_num)


if __name__ == '__main__':
    main()
