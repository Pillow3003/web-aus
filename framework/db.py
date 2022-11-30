from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine


class DataBase:
    _engine: Engine

    def __init__(self):
        self._engine = create_engine(
            "postgresql://root:12345@192.168.131.130:5432/calplanDb"
        )
        self.__session = Session(self._engine, future=True, expire_on_commit=False)

    @property
    def session(self) -> Session:
        return self.__session

    def truncate_tables(self, tables: list):
        with self._engine.begin() as conn:
            conn.execute(f'TRUNCATE {", ".join(tables)} CASCADE')

    def execute_sql(self, script: str):
        with self._engine.begin() as conn:
            result = conn.execute(script)
            row = result.fetchall()
        return row
