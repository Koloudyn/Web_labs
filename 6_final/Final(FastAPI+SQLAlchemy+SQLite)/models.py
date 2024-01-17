from sqlalchemy import Column, Integer, String, Boolean, \
    ForeignKey
from sqlalchemy.orm import relationship
from database import base


class BaseModel(base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Role(BaseModel):
    __tablename__ = 'user_role'

    value = Column(String, nullable=False)

    admin = relationship("Admin")
    client = relationship("Client")

class Admin(BaseModel):
    __tablename__ = 'admin'

    user_role_id = Column(Integer, ForeignKey('user_role.id', ondelete='CASCADE'), nullable=False)
    surname_name = Column(String, nullable=False)
    rub_hour = Column(Integer, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Client(BaseModel):
    __tablename__ = 'client'

    user_role_id = Column(Integer, ForeignKey('user_role.id', ondelete='CASCADE'), nullable=False)
    surname_name = Column(String, nullable=False)
    e_mail = Column(String, unique=True, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    game_hour = relationship("GameHour")


class Room(BaseModel):
    __tablename__ = 'room'

    allow_night = Column(Boolean, nullable=False)

    computer = relationship("Computer")

class Computer(BaseModel):
    __tablename__ = 'computer'

    room_id = Column(Integer, ForeignKey('room.id', ondelete='CASCADE'), nullable=False)
    motherboard = Column(String, nullable=False)
    cpu = Column(String, nullable=False)
    ram = Column(String, nullable=False)
    gpu = Column(String, nullable=True)
    power_supply = Column(String, nullable=False)
    drives = Column(String, nullable=False)
    case = Column(String, nullable=True)

    game_hour = relationship("GameHour")


class WorkDay(BaseModel):
    __tablename__ = 'work_day'

    admin_id = Column(Integer, ForeignKey('admin.id', ondelete='CASCADE'), nullable=False)
    day = Column(String, unique=True, nullable=False)

    game_hour = relationship("GameHour")


class GameHour(BaseModel):
    __tablename__ = 'game_hour'

    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'), nullable=False)
    work_day_id = Column(Integer, ForeignKey('work_day.id', ondelete='CASCADE'), nullable=False)
    computer_id = Column(Integer, ForeignKey('computer.id', ondelete='CASCADE'), nullable=False)
    start_hour = Column(Integer, nullable=False)


