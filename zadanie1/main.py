from fastapi import FastAPI

app = FastAPI(title="Hello World API")


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello {name}"}


@app.get("/info")
def info():
    return {
        "nazwa": "Hello World API",
        "wersja": "1.0.0",
        "autor": "Student"
    }
