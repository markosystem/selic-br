from datetime import datetime
from bson import json_util
from flask_restful import request, abort, Resource
from conect_db import ConnectMongoDB
import json
import os
from dotenv import load_dotenv
load_dotenv()

class SelicAPI(Resource):
    def get(self, active):
        conn = get_connection(self)
        single = get_item_active(active, conn.collection)
        if(single == None):
            abort(404)
        return {
            'data': to_json(single)
        }
    
class SelicListAPI(Resource):    
    def get(self):
        conn = get_connection(self)
        all = conn.collection.find()
        return {
            'data': to_json(all)
        }
 
class SelicSaveAPI(Resource):
    def post(self):
        conn = get_connection(self)
        self.user = request.json['user']
        self.value = request.json['value']
        if(self.user == None or self.user == '' or self.value == None or self.value == ''):
            return {
                'message': 'As informações user ou value são obrigatórias!'
            }, 400
        try:
            print('\nIniciando o registro da nova taxa selic!\n')
            item = get_item_active(True, conn.collection)
        
            if(item != None):
                deactivate_item_old(item, self.user, conn.db, conn.collection)
            
            Selic = item_model(self.user, self.value)

            result = conn.db.insert(conn.collection.name, Selic)
            print('\nInserido com sucesso:\n' + str(result) + '\n')

            conn.db.run()
            print('Inserção efetivada com sucesso! (commit)')
            
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
    print('Desativando o item ativo anterior com ID\n' + str(id))
    item_update = database.update_one(collection.name, {'_id': id}, { "$set": { "activate": False, "date_change": datetime.now(), "user_old": user } })
    print('\nItem anterior desativado com sucesso!\n' + str(item_update))
    if(len(item_update.transactions) <= 0):
        raise RuntimeError('Não foi possível inativar o registro antigo!')
        
def get_item_active(active, collection):
    return collection.find_one({'activate': (active == True or active == 'true' or active == 'True')})

def to_json(object):
    return json.loads(json_util.dumps(object))
