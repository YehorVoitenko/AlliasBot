class Translation:
    def __init__(
            self, unsupported_request,
            team_name_request, team_registered, plus, minus,
            team_count_request, team_random, team_custom, start_message, end_message
    ):
        self.unsupported_request = unsupported_request
        self.team_count_request = team_count_request
        self.team_name_request = team_name_request
        self.team_registered = team_registered
        self.start_message = start_message
        self.team_random = team_random
        self.team_custom = team_custom
        self.end_message = end_message
        self.minus = minus
        self.plus = plus
