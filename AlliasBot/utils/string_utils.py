# TODO: Think how we can translate this :)

def get_team_registered_message(team: str, message: str):
    return f"Team <b>{team}</b> {message}"


def get_end_message(team: str, message: str):
    return f"Team <b>{team}</b> won! {message}"


def get_start_message(team: str, message: str):
    return f"Team <b>{team}</b>. {message}"


def get_score_message(score: int):
    return f"Team score is: <b>{score}</b>"
