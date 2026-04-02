# app/model/models.py
from sqlalchemy import Column, Integer, String, JSON, UUID  # , Table, MetaData
from app.db_files.database import Base


class Village(Base):
    __tablename__ = "mh_village"
    __table_args__ = {"schema": "admin_layer"}

    id = Column(Integer, primary_key=True)
    district_id = Column(UUID)
    taluka_id = Column(UUID)
    village_id = Column(UUID)
    grampanchayat_id = Column(UUID)
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


class Taluka(Base):
    __tablename__ = "mh_taluka"
    __table_args__ = {"schema": "admin_layer"}

    id = Column(Integer, primary_key=True)
    district_id = Column(UUID)
    taluka_id = Column(UUID)
    dtncode = Column(Integer)
    dtname = Column(String)
    dtmname = Column(String)
    thncode = Column(Integer)
    thname = Column(String)
    thmname = Column(String)
    is_pocra = Column(Integer)
    phase = Column(Integer)
    extent = Column(JSON)
