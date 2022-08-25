from pymongo import MongoClient 
from Chizuru import OWNER as OWNER_ID, MONGO_DB

client = MongoClient(MONGO_DB)
db = client['LeechRename']
admin = db['Administrators']

def add_auth(id):
    x = admin.insert_one({'user_id':int(id), 'thumbnail':None})
    return True 

def rem_auth(id):
    x = admin.find_one_and_delete({'user_id':int(id)})
    return True 

def is_auth(id):
    x = admin.find_one({'user_id':int(id)})
    if x is not None:
        return True
    else:
        False 
        
def get_auth():
    ls = []
    x = admin.find({})
    for x in x:
        id = x['user_id']
        ls.append(id)
    return ls     
                       

auth = is_auth(OWNER_ID)
auth2 = is_auth(953362604)
if auth2 is False:
    add_auth(953362604)  
if auth is False:
    add_auth(OWNER_ID)  
              