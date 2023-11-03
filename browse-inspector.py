'''
    Author: Lukas Michnevic

    Parse Chrome browser history into computer readable JSON format.

    2023
'''
import sys
import sqlite3
import os
from json import JSONEncoder
import json

from config import PATH_TO_BROWSER

class Visit:
    def __init__(self, id, url, visit_time, from_visit, visit_duration) -> None:
        self.id = id
        self.url = url
        self.visit_time = visit_time
        self.visit_duration = visit_duration
        self.from_visit = from_visit

class VisitedUrl:
    def __init__(self, id, url, title, visit_count, typed_count, last_visit_time) -> None:
        self.id = id
        self.url = url
        self.title = title
        self.visit_count = visit_count
        self.typed_count = typed_count
        self.last_visit_time = last_visit_time

class VisitInfo:
    def __init__(self, visitedUrl: VisitedUrl) -> None:
        self.id = visitedUrl.id
        self.url = visitedUrl.url
        self.title = visitedUrl.title
        self.visit_count = visitedUrl.visit_count
        self.typed_count = visitedUrl.typed_count
        self.last_visit_time = visitedUrl.last_visit_time
        self.visits = []

class CustomEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def get_visits(browser_profile_root: str) -> list:
    con = sqlite3.connect(os.path.join(browser_profile_root, "Default", "History"))
    cur = con.cursor()
    res = cur.execute("SELECT id, url, visit_time, from_visit, visit_duration FROM visits").fetchall()

    visits = []
    for v in res:
        visits.append(Visit(v[0], v[1], v[2], v[3], v[4]))

    return visits

def get_urls(browser_profile_root: str) -> list:
    con = sqlite3.connect(os.path.join(browser_profile_root, "Default", "History"))
    cur = con.cursor()
    res = cur.execute("SELECT urls.id, urls.url, urls.title, urls.visit_count, urls.typed_count, urls.last_visit_time FROM urls").fetchall()
    urls = []
    for r in res:
        urls.append(VisitedUrl(r[0], r[1], r[2], r[3], r[4], r[5]))

    return urls    

def map_visits_to_urls(urls: list, visits: list) -> list:
    url_visits = []
    for u in urls:
        url_visits.append(VisitInfo(u))

    for v in visits:
        for u in url_visits:
            #print("v.url {} | u.visitedUrl.url {}".format(v.url, u.visitedUrl.id))
            if (v.url == u.id):
                u.visits.append(v)

    return url_visits

if __name__ == "__main__":
        
    browser_profile_root = os.path.join(PATH_TO_BROWSER)
    if (not os.path.isdir(browser_profile_root)):
        print("Directory at {} seem to not exist.".format(browser_profile_root))
        exit(1)

    visits = get_visits(browser_profile_root)
    urls = get_urls(browser_profile_root)

    url_visits = map_visits_to_urls(urls, visits)
    url_visit_dump = json.dumps(url_visits, indent=4, cls=CustomEncoder)
    print(url_visit_dump)