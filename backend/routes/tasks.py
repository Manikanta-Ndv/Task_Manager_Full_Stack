from fastapi import APIRouter, Depends, HTTPException, Query
from database import tasks_collection, users_collection, db
from schemas import TaskCreate, TaskResponse
from auth import get_current_user
from bson import ObjectId
from typing import List, Optional
from pymongo import ASCENDING, DESCENDING
from datetime import datetime, timezone
from pydantic import BaseModel, validator
import dateutil.parser
from enum import Enum
from bson import ObjectId

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str  # "low", "medium", "high"
    due_date: datetime  # Expecting datetime in UTC format
    assigned_to : str
    completed: Optional[bool] = False

    @validator("due_date", pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return dateutil.parser.isoparse(value)  # Parses "Z" format properly
        return value

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None  # ✅ Now optional

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

router = APIRouter(prefix="/tasks")

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    task_data = task.dict()
    task_data["due_date"] = task.due_date  # Ensure it's a Python datetime
    task_data["_id"] = ObjectId()  # Generate a unique ObjectId
    task_data["completed"] = task.completed  # ✅ Ensure completed is stored
    task_data["assigned_to"] = task.assigned_to

    result = await tasks_collection.insert_one(task_data)
    
    created_task = await tasks_collection.find_one({"_id": result.inserted_id})
    
    if not created_task:
        raise HTTPException(status_code=500, detail="Task creation failed")

    created_task["id"] = str(created_task["_id"])  # Convert ObjectId to string
    created_task.pop("_id")  # Remove raw MongoDB "_id"

    return created_task

# @router.post("/", response_model=TaskResponse) #use it if dont work
# async def create_task(task: TaskCreate):
#     task_data = task.dict()
#     task_data["due_date"] = task.due_date  # Ensure it's a Python datetime
#     task_data["_id"] = ObjectId()  # Generate a unique ObjectId

#     result = await tasks_collection.insert_one(task_data)
    
#     # ✅ Fetch the inserted task and return it as a dictionary
#     created_task = await tasks_collection.find_one({"_id": result.inserted_id})
    
#     if not created_task:
#         raise HTTPException(status_code=500, detail="Task creation failed")

#     # ✅ Convert ObjectId to string and return a dictionary
#     created_task["id"] = str(created_task["_id"])  # Convert ObjectId to string
#     created_task.pop("_id")  # Remove raw MongoDB "_id"

#     return created_task
# def create_task(task: TaskCreate, user: dict = Depends(get_current_user)):
#     if not user:
#         raise HTTPException(status_code=403, detail="Not authenticated")

#     if task.priority not in ["High", "Medium", "Low"]:
#         raise HTTPException(status_code=400, detail="Priority must be High, Medium, or Low")

#     new_task = {
#         "title": task.title,
#         "description": task.description,
#         "priority": task.priority,
#         "due_date": task.due_date.isoformat(),  # Convert to string for MongoDB
#         "assigned_to": task.assigned_to,
#         "user_id": str(user["_id"])  # Creator's user ID
#     }

#     result = db.tasks.insert_one(new_task)
#     new_task["_id"] = str(result.inserted_id)  # Convert ObjectId to string for response
#     return new_task

# @router.get("/")
# async def get_tasks(
#     user=Depends(get_current_user),
#     priority: Optional[str] = Query(None),
#     completed: Optional[bool] = None,
#     due_date_sort: Optional[str] = Query(None, regex="^(asc|desc)$"),
#     page: int = 1,
#     page_size: int = 10
# ):
#     """Fetch paginated tasks with filtering and sorting"""

#     query = {"owner_id": str(user["_id"])}

#     # ✅ Case-insensitive priority handling
#     if priority:
#         priority = priority.lower().strip()
#         if priority not in {"low", "medium", "high"}:
#             raise HTTPException(status_code=400, detail="Invalid priority. Use 'low', 'medium', or 'high'")
#         query["priority"] = priority

#     if completed is not None:
#         query["completed"] = completed

#     # Sorting
#     sort_order = []
#     cursor = tasks_collection.find(query)
#     if sort_order:  # ✅ Apply sorting only if it's not empty
#         cursor = cursor.sort(sort_order)
#     tasks = await cursor.skip(skip).limit(page_size).to_list(None)


#     # Pagination
#     skip = (page - 1) * page_size
#     tasks = await tasks_collection.find(query).sort(sort_order).skip(skip).limit(page_size).to_list(None)

#     # ✅ Convert `_id` to string and `due_date` to ISO format
#     tasks_list = []
#     for task in tasks:
#         task_dict = {**task, "id": str(task["_id"])}  # Convert `_id` to string
#         task_dict.pop("_id")  # Remove raw MongoDB `_id`
        
#         if "due_date" in task_dict and isinstance(task_dict["due_date"], datetime):
#             task_dict["due_date"] = task_dict["due_date"].isoformat()  # Convert datetime to string
        
#         tasks_list.append(task_dict)

#     return tasks_list

# @router.get("/")
# async def get_tasks(user=Depends(get_current_user)):
#     """Fetch all tasks for the logged-in user"""

#     # ✅ Ensure user authentication
#     if not user or "_id" not in user:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     # ✅ Fetch all tasks for the user
#     tasks = await tasks_collection.find({"owner_id": str(user["_id"])}).to_list(None)

#     # ✅ Convert `_id` to string and `due_date` to ISO format
#     tasks_list = []
#     for task in tasks:
#         task_dict = {**task, "id": str(task["_id"])}
#         task_dict.pop("_id")  # Remove MongoDB `_id`
        
#         if "due_date" in task_dict and isinstance(task_dict["due_date"], datetime):
#             task_dict["due_date"] = task_dict["due_date"].isoformat()

#         tasks_list.append(task_dict)

#     return tasks_list

# @router.get("/")
# async def get_tasks(user=Depends(get_current_user)):
#     """Fetch all tasks for the logged-in user"""

#     # ✅ Ensure user authentication
#     if not user or "_id" not in user:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     # ✅ Fetch tasks for the user
#     tasks = await tasks_collection.find({"owner_id": str(user["_id"])}).to_list(None)

#     # ✅ Convert `_id` to string and `due_date` to ISO format
#     tasks_list = []
#     for task in tasks:
#         task_dict = {**task, "id": str(task["_id"])}
#         task_dict.pop("_id")  # Remove MongoDB `_id`
        
#         if "due_date" in task_dict and isinstance(task_dict["due_date"], datetime):
#             task_dict["due_date"] = task_dict["due_date"].isoformat()

#         tasks_list.append(task_dict)

#     # ✅ Add pagination (Hardcoded for now, modify as needed)
#     total_tasks = len(tasks_list)  # Replace with actual count from DB if paginated
#     page_size = 5  # Modify based on frontend request
#     total_pages = (total_tasks + page_size - 1) // page_size  # Calculate total pages

#     return {
#         "tasks": tasks_list,
#         "totalPages": total_pages
#     }
@router.get("/")
async def get_all_tasks():
    """Fetch all tasks from the database"""

    # ✅ Fetch all tasks (removing user-specific filter)
    tasks = await tasks_collection.find({}).to_list(None)

    # ✅ Convert `_id` to string and `due_date` to ISO format
    tasks_list = []
    for task in tasks:
        task_dict = {**task, "id": str(task["_id"])}
        task_dict.pop("_id")  # Remove MongoDB `_id`

        if "due_date" in task_dict and isinstance(task_dict["due_date"], datetime):
            task_dict["due_date"] = task_dict["due_date"].isoformat()

        tasks_list.append(task_dict)

    return {"tasks": tasks_list, "totalPages": 1}  # Simplified pagination

# @router.get("/", dependencies=[Depends(get_current_user)])
# async def get_tasks(
#     user=Depends(get_current_user),
#     priority: Optional[PriorityEnum] = None,
#     completed: Optional[bool] = None,
#     due_date_sort: Optional[str] = Query(None, regex="^(asc|desc)$"),
#     page: int = 1,
#     page_size: int = 10
# ):
#     """Fetch paginated tasks with filtering and sorting"""

#     query = {"owner_id": str(user["_id"])}

#     # Apply filters
#     if priority:
#         query["priority"] = priority
#     if completed is not None:
#         query["completed"] = completed

#     # Apply sorting
#     sort_order = []
#     if due_date_sort:
#         sort_order.append(("due_date", ASCENDING if due_date_sort == "asc" else DESCENDING))

#     # Calculate skip value for pagination
#     skip = (page - 1) * page_size

#     # Fetch tasks with pagination
#     tasks = await tasks_collection.find(query).sort(sort_order).skip(skip).limit(page_size).to_list(None)

#     # ✅ Convert `_id` to string and `due_date` to ISO format
#     tasks_list = []
#     for task in tasks:
#         task_dict = {**task, "id": str(task["_id"])}  # Convert `_id` to string
#         task_dict.pop("_id")  # Remove raw MongoDB `_id`
        
#         if "due_date" in task_dict and isinstance(task_dict["due_date"], datetime):
#             task_dict["due_date"] = task_dict["due_date"].isoformat()  # Convert datetime to string
        
#         tasks_list.append(task_dict)

#     return tasks_list
# @router.get("/", dependencies=[Depends(get_current_user)])
# async def get_tasks(
#     user=Depends(get_current_user),
#     priority: Optional[str] = Query(None, pattern="^(low|medium|high)$"),
#     completed: Optional[bool] = None,
#     due_date_sort: Optional[str] = Query(None, pattern="^(asc|desc)$"),
#     page: int = 1,
#     page_size: int = 10
# ):
#     """Fetch paginated tasks with filtering and sorting"""

#     query = {"owner_id": str(user["_id"])}

#     # Apply filters
#     if priority:
#         query["priority"] = priority
#     if completed is not None:
#         query["completed"] = completed

#     # Apply sorting
#     sort_order = []
#     if due_date_sort:
#         sort_order.append(("due_date", ASCENDING if due_date_sort == "asc" else DESCENDING))

#     # Calculate skip value for pagination
#     skip = (page - 1) * page_size

#     # Fetch tasks with pagination
#     tasks = await tasks_collection.find(query).sort(sort_order).skip(skip).limit(page_size).to_list(None)

#     for task in tasks:
#         task["_id"] = str(task["_id"])
    
#     return tasks

@router.get("/count")
async def get_task_count(user=Depends(get_current_user)):
    """Returns total task count for the user"""
    count = await tasks_collection.count_documents({"owner_id": str(user["_id"])})
    return {"total_tasks": count}


# @router.put("/{task_id}", response_model=TaskResponse)
# async def update_task(task_id: str, updated_task: TaskCreate, user=Depends(get_current_user)):
#     existing_task = await tasks_collection.find_one({"_id": ObjectId(task_id), "owner_id": str(user["_id"])})
#     if not existing_task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     update_data = updated_task.dict(exclude_unset=True)
#     await tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})

#     updated_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
#     updated_task["id"] = str(updated_task["_id"])
#     return updated_task
# @router.put("/{task_id}", response_model=TaskResponse)
# async def update_task(task_id: str, updated_task: TaskCreate, user=Depends(get_current_user)):
#     existing_task = await tasks_collection.find_one({"_id": ObjectId(task_id), "owner_id": str(user["_id"])})
    
#     if not existing_task:
#         raise HTTPException(status_code=404, detail="Task not found")

#     update_data = updated_task.dict(exclude_unset=True)

#     result = await tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})

#     if result.modified_count == 0:
#         raise HTTPException(status_code=400, detail="Task update failed")

#     updated_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
#     updated_task["id"] = str(updated_task["_id"])
    
#     return updated_task


# @router.put("/{task_id}", response_model=TaskResponse) 3before update patch
# async def update_task(task_id: str, updated_task: TaskCreate):
#     print(f"🔍 Received task_id: {task_id}")

#     # Validate if the ID is a valid ObjectId
#     if not ObjectId.is_valid(task_id):
#         print("❌ Invalid ObjectId format")
#         raise HTTPException(status_code=400, detail="Invalid task ID format")

#     existing_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
#     if not existing_task:
#         print("❌ Task not found in database")
#         raise HTTPException(status_code=404, detail="Task not found")

#     update_data = updated_task.dict(exclude_unset=True)
#     result = await tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})

#     if result.modified_count == 0:
#         raise HTTPException(status_code=400, detail="Task update failed")

#     updated_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
#     updated_task["id"] = str(updated_task["_id"])
    
#     print("✅ Task updated successfully")
#     return updated_task
@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, updated_task: TaskUpdate):
    existing_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = updated_task.dict(exclude_unset=True)  # ✅ Only update provided fields
    await tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})

    updated_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    updated_task["id"] = str(updated_task["_id"])
    return updated_task

# @router.put("/{task_id}", response_model=TaskResponse)
# async def update_task(task_id: str, updated_task: TaskCreate):
#     print(f"🔍 Updating task ID: {task_id}")

#     existing_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
#     if not existing_task:
#         print("❌ Task not found")
#         raise HTTPException(status_code=404, detail="Task not found")

#     update_data = updated_task.dict(exclude_unset=True)
#     result = await tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})

#     if result.modified_count == 0:
#         raise HTTPException(status_code=400, detail="Task update failed")

#     updated_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
#     updated_task["id"] = str(updated_task["_id"])

#     print("✅ Task updated successfully")
#     return updated_task

# @router.delete("/{task_id}")
# async def delete_task(task_id: str, user=Depends(get_current_user)):
#     result = await tasks_collection.delete_one({"_id": ObjectId(task_id), "owner_id": str(user["_id"])})
    
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Task not found")
    
#     return {"message": "Task deleted successfully"}
@router.delete("/{task_id}")
async def delete_task(task_id: str):
    print(f"🔍 Deleting task ID: {task_id}")

    if not ObjectId.is_valid(task_id):
        print("❌ Invalid ObjectId format")
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    existing_task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not existing_task:
        print("❌ Task not found in database")
        raise HTTPException(status_code=404, detail="Task not found")

    result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 0:
        print("❌ Task deletion failed")
        raise HTTPException(status_code=404, detail="Task not found")

    print("✅ Task deleted successfully")
    return {"message": "Task deleted successfully"}


# @router.delete("/{task_id}")
# async def delete_task(task_id: str, user=Depends(get_current_user)):
#     result = await tasks_collection.delete_one({"_id": ObjectId(task_id), "owner_id": str(user["_id"])})
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return {"message": "Task deleted successfully"}
