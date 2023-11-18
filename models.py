class Visit:
    def __init__(self, id, url, visit_time, from_visit, visit_duration) -> None:
        self.id = id
        self.url = url
        self.visit_time = visit_time
        self.visit_duration = visit_duration
        self.from_visit = from_visit

    def as_dict(self):
        return {'id': self.id, 'url': self.url, 'visit_time': self.visit_time, 'visit_duration': self.visit_duration, 'from_visit':self.from_visit}

class VisitedUrl:
    def __init__(self, id, url, title, visit_count, typed_count, last_visit_time) -> None:
        self.id = id
        self.url = url
        self.title = title
        self.visit_count = visit_count
        self.typed_count = typed_count
        self.last_visit_time = last_visit_time

    def as_dict(self):
        return {"id": self.id, "url": self.url, "title": self.title, "visit_count": self.visit_count, 
                "typed_count": self.typed_count, "last_visit_time": self.last_visit_time}

class VisitInfo:
    def __init__(self, visitedUrl: VisitedUrl) -> None:
        self.id = visitedUrl.id
        self.url = visitedUrl.url
        self.title = visitedUrl.title
        self.visit_count = visitedUrl.visit_count
        self.typed_count = visitedUrl.typed_count
        self.last_visit_time = visitedUrl.last_visit_time
        self.visits: [Visit] = []

    def as_dict(self):
        return {'id': self.id, 'url': self.url, 'title': self.title, 'visit_count': self.visit_count,
                'typed_count': self.typed_count, 'last_visit_time': self.last_visit_time, "visits": [x.as_dict() for x in self.visits]}