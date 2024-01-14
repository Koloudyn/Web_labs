from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
import models
from database import engine, session_local
import uvicorn


app = FastAPI()

models.base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()


class Person(BaseModel):
    name: str = Field(min_length=1)
    todo: str = Field(min_length=1)


@app.get("/")
def get_api():
    return {"message": "working"}

@app.post("/user")
def create_person(person: Person):
    person_model = models.Persons()
    person_model.name = person.name
    person_model.todo = person.todo

    db = session_local()
    db.add(person_model)
    db.commit()

    return person

@app.get("/todo")
def get_todo():
    db = session_local()
    res = db.query(models.Persons).all()
    db.close()
    return res

@app.put("/todo/{user_id}")
def edit_person(user_id: int, person: Person):
    db = session_local()

    user = db.query(models.Persons).filter(models.Persons.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})

    user.todo = person.todo
    db.commit()

    db.close()
    return {"message": "Change is complete"}

@app.delete("/user/{user_id}")
def delete_person(user_id: int):
    db = session_local()

    user = db.query(models.Persons).filter(models.Persons.id == user_id).first()
    if user == None:
        return JSONResponse(status_code=404, content={"message": "User is not found"})

    db.delete(user)
    db.commit()

    db.close()
    return {"message": "The user has been successfully deleted"}
