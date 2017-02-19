import dataset
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

    def query(self):
        pass

