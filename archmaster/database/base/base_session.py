
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


class BaseSession(Session):
    _metadata = None

    def __init__(self, path):
        self.path = Path(path)
        created = not self.path.exists()
        engine = create_engine(f'sqlite:///{self.path}')
        if created:
            self._base.metadata.create_all(engine)
            with engine.begin() as conn:
                conn.exec_driver_sql(
                    f"PRAGMA user_version = {self._version}")
        else:
            with engine.begin() as conn:
                self.check_version(conn.exec_driver_sql(
                    "PRAGMA user_version"
                ).scalar_one())
        super().__init__(engine)

    def metadata(self):
        return {
            m.key: m.value
            for m in self.query(self._metadata).all()
        }

    def update_metadata(self, **kw):
        for k, v in kw.items():
            m = self.get(self._metadata, k)
            if m is None:
                self.add(self._metadata(key=k, value=str(v)))
            else:
                m.value = str(v)
