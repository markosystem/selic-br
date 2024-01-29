from datetime import datetime
from bson import json_util
from flask import Flask
from flask_restful import request, abort, Api, Resource
from conect_db import ConnectMongoDB
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
api = Api(app)

def __init__(self):
    self.mongodb = ConnectMongoDB()
    self.db = self.mongodb.database()
    self.collection = self.db.database.get_collection(os.environ['collection'])

class SelicAPI(Resource):
    def get(self, active):
        single = get_item_active(active, self.collection)
        if(single == None):
            abort(404)
        return {
            'data': to_json(single)
        }
    
class SelicListAPI(Resource):    
    def get(self):
        all = self.collection.find()
        return {
            'data': to_json(all)
        }
 
class SelicSaveAPI(Resource):
    def post(self):
        self = get_connection(self)
        self.user = request.json['user']
        self.value = request.json['value']
        if(self.user == None or self.user == '' or self.value == None or self.value == ''):
            return {
                'message': 'As informações user ou value são obrigatórias!'
            }, 400
        try:
            item = get_item_active(True, self.collection)
        
            if(item != None):
                deactivate_item_old(item, self.user, self.db, self.collection)
            
            Selic = item_model(self.user, self.value)

            result = self.db.insert(self.collection.name, Selic)
            print('Inserido com sucesso:\n' + str(result) + '\n')

            self.db.run()
            print('Inserção comitado com sucesso!')
            
            return {
                'message': 'Registro inserido com sucesso!'
            }, 201
        except Exception as e:
            print('Houve uma Exceção: \n', str(e))
        return {
            'message':'Houve um erro ao realizar o registro Favor, procure adm da API!'
        }, 500

def get_connection(self):
    self.mongodb = ConnectMongoDB()
    self.db = self.mongodb.database()
    self.collection = self.db.database.get_collection(os.environ['collection'])
    return self

def item_model(user, value):
    Selic = {}
    Selic['user'] = user
    Selic['user_old'] = None
    Selic['value'] = value
    Selic['activate'] = True
    Selic['date_insertion'] = datetime.now()
    Selic['date_change'] = None
    return Selic

def deactivate_item_old(item, user, database, collection):
    id = item['_id']
    item_update = database.update_one(collection.name, {'_id': id}, { "$set": { "activate": False, "date_change": datetime.now(), "user_old": user } })
    if(len(item_update.transactions) <= 0):
        raise RuntimeError('Não foi possível inativar o registro antigo!')
        
def get_item_active(active, collection):
    return collection.find_one({'activate': (active == True or active == 'true' or active == 'True')})

def to_json(object):
    return json.loads(json_util.dumps(object))

api.add_resource(SelicAPI, '/list/<active>')
api.add_resource(SelicListAPI, '/list')
api.add_resource(SelicSaveAPI, '/save')

if __name__ == '__main__':
    app.run(debug=True)