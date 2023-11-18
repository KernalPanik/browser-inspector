from json import JSONEncoder

class HistoryEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
    