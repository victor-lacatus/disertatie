
from fastapi import FastAPI
from models import DataSet, db, User
from bson.objectid import ObjectId

app = FastAPI()

@app.get('/users')
async def list_users():
    users = []
    for user in db.users.find():
        users.append(User(**user))
    return {'users': users}

@app.get('/user/{key}={value}')
async def get_user(key, value):
    if key == "_id":
        value = ObjectId(value)
    user = db.users.find_one({key : value})
    if user is not None:
        user = { "id" if k == "_id" else k:v for k,v in user.items() }
        user["id"] = str(user["id"])   
        return user
    return {"error": "The user with {key} = {value} does not exist!}"}

@app.post('/users')
async def create_user(user: User):
    if hasattr(user, 'id'):
        delattr(user, 'id')
        
    if db.users.find_one({"email": user.email}) is None:
        ret = db.users.insert_one(user.dict(by_alias=True))
        user.id = ret.inserted_id
        return {'user': user}
    
    return {"error":"Another user with same email already exists!"}

@app.put('/datasets')
async def upload_dataSet(data: DataSet):
    if hasattr(data, 'id'):
        delattr(data, 'id')
    ret = db.datasets.insert_one(data.dict(by_alias=True))
    data.id = ret.inserted_id
    return {'data': data}

@app.get('/datasets')
async def get_datasets():
    datas = []
    for data in db.datasets.find():
        datas.append(DataSet(**data))    
    return{'data': datas}



@app.post('/user/{email}')
async def delete_user(email):
    ret = db.users.delete_one({"email" : email})
    ret = { "id" if k == "_id" else k:v for k,v in ret.items() }
    ret["id"] = str(ret["id"])
    return ret

@app.post('/dataset/{key}={value}')
async def delete_dataset(key, value):
    if key == 'id' or key == '_id':
        ret = db.datasets.delete_one({"_id" : ObjectId(id)})
    else:
        ret = db.datasets.delete_one({key : value})
    ret = { "id" if k == "_id" else k:v for k,v in ret.items() }
    ret["id"] = str(ret["id"])
    return ret
