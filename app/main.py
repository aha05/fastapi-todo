from fastapi import FastAPI, HTTPException
from app.schemas import Todo, TodoCreate
from app.models import todos

app = FastAPI(title="Todo API")

@app.get("/")
def root():
    return {"message": "FastAPI Todo App"}

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo = Todo(
        id=len(todos) + 1,
        title=todo.title,
        description=todo.description,
        completed=False
    )
    todos.append(new_todo)
    return new_todo

@app.get("/todos", response_model=list[Todo])
def get_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated: TodoCreate):
    for todo in todos:
        if todo.id == todo_id:
            todo.title = updated.title
            todo.description = updated.description
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found")
