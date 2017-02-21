from flask import Flask, request, make_response
from flask.ext.restful import reqparse
from flask_restful import Resource, Api

from webapp.database.database import Database

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('task', required=True,
                    help="possible values: create_user | get_products | buy")
parser.add_argument('username', required=False)
parser.add_argument('category', required=False,
                    help="What kind of clothes")
parser.add_argument('color', required=False)
parser.add_argument('bought', required=False)
parser.add_argument('product_id', required=False)
parser.add_argument('user_id', required=False)


class RESTWorker(Resource):
    def __init__(self, **kwargs):
        super(RESTWorker, self).__init__()

        self.db = Database('../config.json')

    # used by client only to create user
    def post(self):
        args = parser.parse_args()
        if args['task'] == 'create_user':
            key = self.db.insert('users', {'username': args['username']})
            return key, 201

        elif args['task'] == ['buy']:
            key = self.db.insert('activities', {'user_id': args['user_id'],
                                          'prod_id': args['product_id'], 'bought': True})
            return key, 201

        elif args['task'] == ['get_products']:
            if args['bought'] is None:
                result = self.db.query_products(category=args['category'], color=args['color'])
            else:
                result = self.db.query_users_products(user_id=args['user_id'], bought=args['bought'])
            return result, 200
        else:
            return None, 500


def main():
    api.add_resource(RESTWorker, '/', )
    port = 9000
    app.run(port=port, threaded=True)


if __name__ == '__main__':
    main()
