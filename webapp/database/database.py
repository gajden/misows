import dataset
import psycopg2

from utilities import read_json


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

    def disconnect(self):
        pass

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

    def query_products_bought_by_user(self, user_id, limit=50):
        activities = self.db['activities'].find(user_id=user_id, bought=True, _limit=limit)
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

    def query_products_viewed_by_user(self, user_id, limit=50):
        activities = self.db['activities'].find(user_id=user_id, bought=False, _limit=limit)
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
    db = Database('./config.json')
    db.connect()
    # db.insert('users', {"username": "tom"})
    img = open('../../data/test.jpg', 'rb').read()
    img = psycopg2.Binary(img)
    # db.insert('products', {"description": "pretty dress", "category": "dress",
    #                        "color": "black", "picture": img})
    print db.query_users()
    prod = db.query_products(None, None)
    with open('hello.jpg', 'wb') as f_out:
        f_out.write(prod)
    print db.db


