from flask import Flask, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class RESTWorker(Resource):
    def __init__(self, **kwargs):
        super(RESTWorker, self).__init__()

    def post(self):
        pass

    def get(self):
        pass


def main():
    api.add_resource(RESTWorker, '/', )
    port = 9000
    app.run(port=port, threaded=True)

if __name__ == '__main__':
    main()
