from Allias.models.team import Team
from Allias.repositories.base import Session

session = Session()


def save_team(position: int, name: str):
    t = Team(position=position, name=name)
    session.add(t)
    session.commit()
