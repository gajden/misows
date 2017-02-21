import random

import dataset

from utilities import read_json
from webapp.database.fill_data import random_word


class DatabaseStub(object):
    def __init__(self):
        self.categories = ["dress", "shoes", "trousers", "hats"]
        self.colors = ["black", "red", "green", "yellow"]

    def connect(self):
        pass

    def insert(self, table, data):
        return random.randint(10000)

    def query_users(self):
        users = []
        for i in xrange(random.randint(10000)):
            users.append({
                "id": i,
                "username": random_word(random.randint(5, 20))
            })
        return {"results": users}

    def query_users_products(self, user_id, bought, limit=50):
        bought = []
        for i in xrange(limit):
            bought.append({
                "id": random.randint(10000),
                "description": random_word(random.randint(100, 500)),
                "category": random.choice(self.categories),
                "color": random.choice(self.colors),
                "picture": random_word(55000)
            })

        return {"results": bought}

    def query_products(self, category=None, color=None, limit=50):
        result = []

        for i in xrange(limit):
            result.append({
                "id": random.randint(10000),
                "description": random_word(random.randint(100, 500)),
                "category": random.choice(self.categories),
                "color": random.choice(self.colors),
                "picture": random_word(55000)
            })

        return {"results": result}

    def clean_table(self, table):
        pass

    def remove_user(self, user_id):
        pass


class Database(object):
    def __init__(self, config):
        self.config = read_json(config)
        self.username = self.config["username"]
        self.db_name = self.config["database_name"]
        self.user_pass = self.config["user_pass"]
        self.url = self.config["url"]
        self.port = self.config["port"]

        self.db = None

    def connect(self):
        db_url = 'postgresql://%s:%s@%s:%d/%s' % (self.username, self.user_pass,
                                                  self.url, self.port, self.db_name)
        self.db = dataset.connect(db_url)

    def insert(self, table, data):
        if self.db is not None:
            table = self.db[table]
            table.insert(data)

    def query_users(self):
        users = []
        for user in self.db['users'].all():
            users.append({
                "id": user['id'],
                "username": user['username']
            })
        return {"results": users}

    def query_users_products(self, user_id, bought, limit=50):
        activities = self.db['activities'].find(user_id=user_id, bought=bought, _limit=limit)
        bought = []
        for activity in activities:
            prod = self.db['products'].find_one(id=activity['prod_id'])
            bought.append({
                "id": prod['id'],
                "description": prod['description'],
                "category": prod['category'],
                "color": prod['color'],
                "picture": prod['picture']
            })

        return {"results": bought}

    def query_products(self, category=None, color=None, limit=50):
        products = self.db['products'].find(category=category, color=color, _limit=limit)
        result = []

        for prod in products:
            result.append({
                "id": prod['id'],
                "description": prod['description'],
                "category": prod['category'],
                "color": prod['color'],
                "picture": prod['picture']
            })

        return {"results": result}

    def clean_table(self, table):
        self.db[table].delete()

    def remove_user(self, user_id):
        self.db['users'].delete(id=user_id)


if __name__ == '__main__':
    pass
