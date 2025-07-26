# main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Dict

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# In-memory storage
todos: List[Dict] = []
next_id = 1

class ChatRequest(BaseModel):
    message: str

class TodoIn(BaseModel):
    title: str
    due: date

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # ตรงนี้ไม่ต้องส่ง todos ไป—React จะ fetch เองผ่าน API
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(req: ChatRequest):
    # แสดงเป็น echo ก่อน เปลี่ยนเป็น AI logic จริงตามต้องการ
    return {"reply": f"Echo: {req.message}"}

@app.get("/todos")
async def get_todos():
    return todos

@app.get("/todos/upcoming")
async def get_upcoming():
    today = date.today()
    return [t for t in todos if t["due"] >= today]

@app.post("/todos")
async def create_todo(payload: TodoIn):
    global next_id
    todo = {"id": next_id, "title": payload.title, "due": payload.due.isoformat()}
    todos.append(todo)
    next_id += 1
    return todo

@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, payload: TodoIn):
    for t in todos:
        if t["id"] == todo_id:
            t["title"] = payload.title
            t["due"] = payload.due.isoformat()
            return t
    return {"error": "Not found"}

@app.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    # no body
