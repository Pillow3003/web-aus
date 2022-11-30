from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Calplan(Base):
    __tablename__ = "calplans"
    id = Column(Integer, primary_key=True)


class Calendars(Base):
    __tablename__ = "calendars"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    order = Column(Integer)
    type = Column(Integer)
    is_default = Column(Boolean)


class CalplanCalendars(Base):
    __tablename__ = "calplan_calendars"
    calplan_id = Column(Integer, primary_key=True)
    calendar_id = Column(Integer)


class CalendarShifts(Base):
    __tablename__ = "calendar_shifts"
    calendar_id = Column(Integer, primary_key=True)
    shift_id = Column(Integer)
    hours = Column(Integer)


class CalplanParams(Base):
    __tablename__ = "calplan_params"
    calplan_id = Column(Integer, primary_key=True)
    param_id = Column(Integer)
    param_value = Column(Integer)
