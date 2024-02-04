from flask import Flask
from flask_restful import Api
from resources.selic import SelicAPI
from resources.selic import SelicListAPI
from resources.selic import SelicSaveAPI

app = Flask(__name__)
api = Api(app)

api.add_resource(SelicAPI, '/list/<active>')
api.add_resource(SelicListAPI, '/list')
api.add_resource(SelicSaveAPI, '/save')

if __name__ == '__main__':
    app.run(debug=True)