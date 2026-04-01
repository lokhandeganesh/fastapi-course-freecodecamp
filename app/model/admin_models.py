# app/model/models.py
from sqlalchemy import Column, Integer, String, JSON  # , Table, MetaData
from app.db_files.database import Base


class Village(Base):
    __tablename__ = "mh_village"
    __table_args__ = {"schema": "admin_layer"}

    id = Column(Integer, primary_key=True)
    dtncode = Column(Integer)
    dtname = Column(String)
    dtmname = Column(String)
    thncode = Column(Integer)
    thname = Column(String)
    thmname = Column(String)
    vincode = Column(Integer)
    vlname = Column(String)
    vilmname = Column(String)
    is_pocra = Column(Integer)
    phase = Column(Integer)
    extent = Column(JSON)
