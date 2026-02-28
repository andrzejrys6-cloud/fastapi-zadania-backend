from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Todo List API")

# Prosta lista w pamięci zamiast bazy danych
todos = []
next_id = 1


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    completed: bool = False


class Todo(TodoCreate):
    id: int


def znajdz_todo(todo_id: int):
    """Szuka zadania po ID, zwraca None jeśli nie ma."""
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None


@app.get("/todos")
def get_todos():
    return todos


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    todo = znajdz_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono zadania")
    return todo


@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = {
        "id": next_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed
    }
    todos.append(new_todo)
    next_id += 1
    return new_todo


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated: TodoCreate):
    todo = znajdz_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono zadania")
    todo["title"] = updated.title
    todo["description"] = updated.description
    todo["completed"] = updated.completed
    return todo


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    todo = znajdz_todo(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Nie znaleziono zadania")
    todos.remove(todo)
