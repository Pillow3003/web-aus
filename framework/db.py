from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base


class DataBase:
    _engine: Engine

    def __init__(self):
        self._engine = create_engine(
            'postgresql://root:12345@192.168.131.130:5432/calplanDb'
        )

    def get_session(self) -> Session:
        return Session(self._engine, future=True, expire_on_commit=False)

    def truncate_tables(self, tables):
        with self._engine.begin() as conn:
            conn.execute(f'TRUNCATE {", ".join(tables)}')

    def execute_sql(self, script: str):
        with self._engine.begin() as conn:
            result = conn.execute(script)
            row = result.fetchall()
        return row

Base = declarative_base()

class Calplan(Base):
    __tablename__ = 'calplans'
    id = Column(Integer, primary_key=True)

db = DataBase()

calplan_1 = Calplan(id=3)
print(calplan_1)

session = db.get_session()

session.begin()
session.add(calplan_1)
session.commit()


