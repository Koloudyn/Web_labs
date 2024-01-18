from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models
import create_models
from database import engine, session_local


app = FastAPI()

models.base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()

# ---------------------------------------FUNCTIONS: ADMIN---------------------------------------------------------------
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
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.get("/client/{id}")
def get_client(id, db: Session = Depends(get_db)):
    person = db.query(models.Client).filter(models.Client.id == id).first()
    if person == None:
        return JSONResponse(status_code=404, content={"message": "Client is not found"})
    return person

@app.post("/client_create")
def client_create(person: create_models.Person, db: Session = Depends(get_db)):
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
def client_update(person: create_models.Person, db: Session = Depends(get_db)):
    temp = db.query(models.Client).filter(models.Client.login == person.login).first()
    if temp == None:
        return JSONResponse(status_code=404, content={"message": "Client is not found"})

    temp.surname_name = person.surname_name
    temp.e_mail = person.e_mail
    temp.password = person.password

    db.commit()
    return {"message": "Client update was successful"}


# ------------------ROOM-------------------
@app.get("/rooms")
def get_rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()

@app.get("/room/{id}")
def get_room(id, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == id).first()
    if room == None:
        return JSONResponse(status_code=404, content={"message": "Room is not found"})
    return room

@app.post("/room_create")
def room_create(room: create_models.Place, db: Session = Depends(get_db)):
    db.add(models.Room(allow_night=room.allow_night))
    db.commit()
    return room

@app.delete("/room_delete/{id}")
def room_delete(id, db: Session = Depends(get_db)):
    room = db.query(models.Room).filter(models.Room.id == id).first()
    if room == None:
        return JSONResponse(status_code=404, content={"message": "Room is not found"})

    db.delete(room)
    db.commit()
    return {"message": "Room delete was successful"}

@app.put("/room_update/{id}")
def room_update(id, room: create_models.Place, db: Session = Depends(get_db)):
    temp = db.query(models.Room).filter(models.Room.id == id).first()
    if temp == None:
        return JSONResponse(status_code=404, content={"message": "Room is not found"})

    temp.allow_night = room.allow_night

    db.commit()
    return {"message": "Room update was successful"}


# ------------------COMPUTER-------------------
@app.get("/computers")
def get_computers(db: Session = Depends(get_db)):
    return db.query(models.Room).all()

@app.get("/computer/{id}")
def get_computer(id, db: Session = Depends(get_db)):
    computer = db.query(models.Computer).filter(models.Computer.id == id).first()
    if computer == None:
        return JSONResponse(status_code=404, content={"message": "Computer is not found"})
    return computer

@app.post("/computer_create")
def computer_create(computer: create_models.PC, db: Session = Depends(get_db)):
    computer_model = models.Computer(room_id=computer.room_id, motherboard=computer.motherboard,
                                 cpu=computer.cpu, ram=computer.ram, gpu=computer.gpu,
                                 power_supply=computer.power_supply, drives=computer.drives, case=computer.case)

    db.add(computer_model)
    db.commit()
    return computer

@app.delete("/computer_delete/{id}")
def computer_delete(id, db: Session = Depends(get_db)):
    computer = db.query(models.Computer).filter(models.Computer.id == id).first()
    if computer == None:
        return JSONResponse(status_code=404, content={"message": "Computer is not found"})

    db.delete(computer)
    db.commit()
    return {"message": "Computer delete was successful"}

@app.put("/computer_update/{id}")
def computer_update(id, computer: create_models.PC, db: Session = Depends(get_db)):
    temp = db.query(models.Computer).filter(models.Computer.id == id).first()
    if temp == None:
        return JSONResponse(status_code=404, content={"message": "Computer is not found"})

    temp.room_id = computer.room_id
    temp.motherboard = computer.motherboard
    temp.cpu = computer.cpu
    temp.ram = computer.ram
    temp.gpu = computer.gpu
    temp.power_supply = computer.power_supply
    temp.drives = computer.drives
    temp.case = computer.case

    db.commit()
    return {"message": "Computer update was successful"}

# ------------------GAME HOUR-------------------
@app.get("/game_hours")
def get_game_hours(db: Session = Depends(get_db)):
    return db.query(models.GameHour).all()

@app.get("/game_hour/{id}")
def get_game_hour(id, db: Session = Depends(get_db)):
    hour = db.query(models.GameHour).filter(models.GameHour.id == id).first()
    if hour == None:
        return JSONResponse(status_code=404, content={"message": "Game hour is not found"})
    return hour

@app.post("/game_hour")
def game_hour_create(game: create_models.HourGame, db: Session = Depends(get_db)):
    game_model = models.GameHour(client_id=game.client_id, computer_id=game.computer_id,
                                 start_hour=game.start_hour, start_date=game.start_date)

    db.add(game_model)
    db.commit()
    return game

@app.delete("/game_hour/{id}")
def game_hour_delete(id, db: Session = Depends(get_db)):
    hour = db.query(models.GameHour).filter(models.GameHour.id == id).first()
    if hour == None:
        return JSONResponse(status_code=404, content={"message": "Game hour is not found"})

    db.delete(hour)
    db.commit()
    return {"message": "Game hour delete was successful"}

@app.put("/game_hour/{id}")
def game_hour_update(id, hour: create_models.HourGame, db: Session = Depends(get_db)):
    temp = db.query(models.GameHour).filter(models.GameHour.id == id).first()
    if temp == None:
        return JSONResponse(status_code=404, content={"message": "Game hour is not found"})

    temp.client_id = hour.client_id
    temp.computer_id = hour.computer_id
    temp.start_hour = hour.start_hour
    temp.start_date = hour.start_date

    db.commit()
    return {"message": "Game hour update was successful"}

# ---------------------------------------FUNCTIONS: CLIENT---------------------------------------------------------------
@app.get("/client_get_room_and_computer")
def client_get_room_and_computer(db: Session = Depends(get_db)):
    return db.query(models.Room).all(), db.query(models.Computer).all()

@app.get("/client_get_game_hours/{login}")
def client_get_room_and_computer(login, db: Session = Depends(get_db)):
    temp = db.query(models.Client).filter(models.Client.login == login).first()
    if temp == None:
        return JSONResponse(status_code=404, content={"message": "Client is not found"})


    return db.query(models.GameHour).filter(models.GameHour.client_id == temp.id).all()

