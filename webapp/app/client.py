import random

import logging
import requests
import time

from utilities import read_json
from webapp.database.fill_data import random_word


class Client(object):
    def __init__(self, url, client_id=0, logger_path=None):
        self.id = client_id
        self.url = url
        self.user_id = None
        self.create_app_client()
        self.last_seen = None
        self.logger_path = logger_path
        if logger_path is not None:
            self.logger = logging.getLogger('myapp')
            hdlr = logging.FileHandler(logger_path)
            formatter = logging.Formatter('%(message)s')
            hdlr.setFormatter(formatter)
            self.logger.addHandler(hdlr)
            self.logger.setLevel(logging.INFO)

        self.categories = ["dress", "shoes", "trousers", "hats"]
        self.colors = ["black", "red", "green", "yellow"]

    def create_app_client(self):
        request_data = {
            'task': 'create_user',
            'username': random_word(random.randint(5, 20))
        }
        start = time.time()
        self.user_id, status = requests.post(self.url, request_data)
        request_time = time.time() - start
        if self.logger is not None:
            self.logger.info('create_user %d %f' % (status, request_time))

    def request_products(self):
        request_data = {
            'task': 'get_products',
            'category': random.choice(self.categories),
            'color': random.choice(self.colors)
        }
        start = time.time()
        products, status = requests.post(self.url, request_data)
        request_time = time.time()
        if status == 200:
            if self.logger is not None:
                self.logger.info('get_products %d %f' % (status, request_time))
            self.last_seen = [product['id'] for product in products]

    def buy_products(self):
        if self.last_seen is not None:
            request_data = {
                'task': 'buy',
                'user_id': self.user_id,
                'product_id': random.choice(self.last_seen)
            }
            start = time.time()
            response, status = requests.post(self.url, request_data)
            response_time = time.time() - start
            if self.logger is not None:
                self.logger.info('buy %d %f' % (status, response_time))

    def check_order_history(self):
        request_data = {
            'task': 'get_products',
            'bought': True,
            'user_id': self.user_id
        }
        start = time.time()
        response, status = requests.post(self.url, request_data)
        response_time = time.time() - start
        if self.logger is not None:
            self.logger.info('check_order %d %f' % (status, response_time))


def run_client(url, port, client_id=0):
    workers_num = 1
    worker_id = 0
    logger_path = '../../worker_%d_%d.log' % (workers_num, worker_id)
    client = Client('%s:%d' % (url, port), client_id, logger_path)

    actions = ['request_product', 'purchase', 'check_orders']
    while True:
        action = random.choice(actions)

        if action == 'request_product':
            client.request_products()
        elif action == 'purchase':
            client.buy_products()
        elif action == 'check_orders':
            client.check_order_history()


def main():
    config_path = ''
    config = read_json(config_path)
    run_client(config['url'], config['port'])


if __name__ == '__main__':
    main()
