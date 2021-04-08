class MatchResultsList:

    results_list = []

    def __init__(self, results_list):
        self.results_list = results_list

    def add_match(match):
        self.results_list.append(match)

    def get_match(start_date, end_date=""):
        if end_date == "":
            end_date = start_date

        output = []

        for result in self.results_list:
            if result.match_date >= start_date and result.match_date <= end_date:
                output.append(result)

        return output
