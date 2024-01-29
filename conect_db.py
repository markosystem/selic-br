from mongotransactions import Database, Transaction
from dotenv import load_dotenv
import os
load_dotenv()

class ConnectMongoDB:
    def __init__(self):
        self.credentials = os.environ['user'] + ':' + os.environ['password']
        self.db = os.environ['database']

    def database(self):
        try:
            database = Database('mongodb+srv://'f'{self.credentials}@cluster0.fgu8y9z.mongodb.net/?retryWrites=true&w=majority')
            database.set_database(self.db)
            return Transaction(database)
        except Exception as e:
            print('Não foi possível conectar ao banco de dados: \n', str(e))


    def ping(self):
        self.database().client.admin.command('ping')
        print('Conexão realizada com sucesso com MongoDB!')


test = ConnectMongoDB()
test.ping()
