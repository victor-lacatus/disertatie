from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from matplotlib.font_manager import json_load
from rdflib import Dataset
from models import DataSet, db, User
from bson.objectid import ObjectId
import json

app = FastAPI()
app2 = FastAPI()


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
        user = User(**user)   
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

@app.post('/datasets')
async def create_dataSet(data: DataSet):
    if hasattr(data, 'id'):
        delattr(data, 'id')
    ret = db.datasets.insert_one(data.dict(by_alias=True))
    data.id = ret.inserted_id
    return {'data': data}

@app.get('/datasets')
async def get_datasets():
    datas = []
    for data in db.datasets.find():
        data = DataSet(**data)
        data ={'id':str(data.id),
               'created_by': str(data.created_by)}
        datas.append(data)    
    return{'data': datas}



@app.delete('/user/{email}')
async def delete_user(email):
    ret = db.users.delete_one({"email" : email})
    ret = { "id" if k == "_id" else k:v for k,v in ret.items() }
    ret["id"] = str(ret["id"])
    return ret

@app.delete('/dataset/{key}={value}')
async def delete_dataset(key, value):
    if key == 'id' or key == '_id':
        ret = db.datasets.delete_one({"_id" : ObjectId(id)})
    else:
        ret = db.datasets.delete_one({key : value})
    return {'res': ret.deleted_count,
            'acknoledgement':ret.raw_result}

@app.get("/dataset/download/{id}")
def download_fle(id):
    
    ret = db.datasets.find_one({"_id" : ObjectId(id)})
    print(ret)
    if ret is None:
        return {"error": "No such file!"}
    ret["_id"] = str(ret["_id"])
    response = JSONResponse(ret)
    response.headers["Content-Disposition"] = f"attachment; filename={ret['_id']}.json"
    return response

@app.post("/dataset/upload/")
async def create_upload_file(userid, file: UploadFile = File()):
    
    data = json.load(file.file)
    
    tmp={"created_by": userid,
         "data": data}
    tmp = DataSet(**tmp)
    
    if hasattr(tmp, 'id'):
        delattr(tmp, 'id')
        
    ret = db.datasets.insert_one(tmp.dict(by_alias=True))
    
    return {"filename": file.filename}
