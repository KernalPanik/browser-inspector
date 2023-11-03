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

from models import Visit, VisitInfo, VisitedUrl

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

def get_hisotry_data(path_to_root: str) -> list[VisitInfo]:
    '''
        Function that gets browser history data such as visited URL and time of visits.
        Arguments:
        path_to_root: str - a path to browser profile root folder.

        Return:
        list - of URL visited
    '''
    browser_profile_root = os.path.join(path_to_root)
    if (not os.path.isdir(browser_profile_root)):
        print("Directory at {} seem to not exist.".format(browser_profile_root))
        exit(1)

    visits = get_visits(browser_profile_root)
    urls = get_urls(browser_profile_root)

    url_visits = map_visits_to_urls(urls, visits)

    return url_visits

def dump_json(data: list[VisitInfo]) -> str:
    return json.dumps(data, indent=4, cls=CustomEncoder)