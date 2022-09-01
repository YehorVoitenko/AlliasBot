from typing import List

from sqlalchemy import func

from Allias.models.team import Team
from Allias.repositories.base import Session

session = Session()


def get_team_by_position(position: int):
    teams: List[Team] = session \
        .query(Team) \
        .filter(Team.position == position - 1) \
        .all()

    return teams


def get_max_score_teams():
    subquery = session.query(func.max(Team.score))
    team: List[Team] = session \
        .query(Team) \
        .filter(Team.score == subquery) \
        .all()

    return team
