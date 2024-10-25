from fastapi import FastAPI, APIRouter, HTTPException
from conf import collection
from database.schemas import all_tasks
from database.models import ToDo
from bson.objectid import ObjectId
from datetime import datetime

app = FastAPI()
router = APIRouter()

@router.get("/")
async def get_tasks():
    # data = collection.find()
    data = collection.find({"is_deleted": False})
    return all_tasks(data) 


@router.post("/")
async def create_task(new_task: ToDo):
    try:
        resp = collection.insert_one(dict(new_task))
        return {"status_code": 201, "message": "Task created successfully", "task_id": str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(status_code = 500, detail = str(e))
        

@router.put("/{task_id}")
async def update_task(task_id, updated_task: ToDo):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id":id}, {"is_deleted": False})
        if not existing_doc:
            return {"status_code": 404, "message": "Task not found"}
        
        updated_task.updated_at = int(datetime.timestamp(datetime.now()))
        resp = collection.update_one({"_id": id}, {"$set": dict(updated_task)})
        return {"status_code": 200, "message": "Task updated successfully"}

    except Exception as e:
        return HTTPException(status_code = 500, detail = str(e))
    

@router.delete("/{task_id}")
async def delete_task(task_id):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id":id}, {"is_deleted": False})
        if not existing_doc:
            return {"status_code": 404, "message": "Task not found"}
        
        resp = collection.update_one({"_id": id}, {"$set": {"is_deleted": True}})
        return {"status_code": 200, "message": "Task deleted successfully"}

    except Exception as e:
        return HTTPException(status_code = 500, detail = str(e))
    

app.include_router(router)



# zdHHPLLPMxQZKn5T


