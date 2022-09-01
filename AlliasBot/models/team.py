from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import String

from Allias.constants.tables import TEAM_TABLE
from Allias.repositories.base import Base as Base


class Team(Base):
    __tablename__ = TEAM_TABLE

    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    name = Column(String(255))
    score = Column(Integer)

    def __init__(
            self,
            position=None,
            name=None,
            score=0,
    ):
        self.position = position
        self.score = score
        self.name = name
