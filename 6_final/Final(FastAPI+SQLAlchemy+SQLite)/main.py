from fastapi import FastAPI, Body, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from database import engine, session_local


app = FastAPI()

models.base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()


class Person(BaseModel):
    surname_name: str = Field(min_length=1)
    e_mail: str = Field(min_length=1)
    login: str = Field(min_length=1)
    password: str = Field(min_length=1)

# ------------------ADMIN-------------------
@app.get("/")
def get_admins(db: Session = Depends(get_db)):
    return db.query(models.Admin).all()

@app.get("/admin/{id}")
def get_admin(id, db: Session = Depends(get_db)):
    person = db.query(models.Admin).filter(models.Admin.id == id).first()
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Admin is not found"})
    return person

# ------------------CLIENT-------------------
@app.get("/clients")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.get("/client/{id}")
def get_admin(id, db: Session = Depends(get_db)):
    person = db.query(models.Client).filter(models.Client.id == id).first()
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Client is not found"})
    return person

@app.post("/client_create")
def client_create(person: Person, db: Session = Depends(get_db)):
    if db.query(models.Client).filter(models.Client.login == person.login).first() != None:
        return JSONResponse(status_code=404, content={"message": "Client already exists"})

    person_model = models.Client(user_role_id=2, surname_name=person.surname_name,
                                 e_mail=person.e_mail, login=person.login, password=person.password)

    db.add(person_model)
    db.commit()
    return person

@app.delete("/client_delete/{id}")
def client_delete(id, db: Session = Depends(get_db)):
    person = db.query(models.Client).filter(models.Client.id == id).first()
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Client is not found"})

    db.delete(person)
    db.commit()
    return {"message": "Client delete was successful"}

@app.put("/client_update")
def client_create(person: Person, db: Session = Depends(get_db)):
    temp = db.query(models.Client).filter(models.Client.login == person.login).first()
    if temp == None:
        return JSONResponse(status_code=404, content={"message": "Client is not found"})

    temp.surname_name = person.surname_name
    temp.e_mail = person.e_mail
    temp.password = person.password

    db.commit()
    return {"message": "Client update was successful"}

# ------------------ROOM-------------------
