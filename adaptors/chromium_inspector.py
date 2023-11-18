import sys
import sqlite3
import os
from json import JSONEncoder
import json

from utilities import HistoryEncoder
from models import Visit, VisitInfo, VisitedUrl
from browser_inspector import BrowserInspector

class ChromiumInspector(BrowserInspector):
    def _collect_visits(self, profile_root: str) -> None:
        con = sqlite3.connect(os.path.join(profile_root, "Default", "History"))
        cur = con.cursor()
        res = cur.execute("SELECT id, url, visit_time, from_visit, visit_duration FROM visits").fetchall()

        visits = []
        for v in res:
            visits.append(Visit(v[0], v[1], v[2], v[3], v[4]))

        self.url_visits = visits
    
    def _collect_urls(self, profile_root: str) -> None:
        con = sqlite3.connect(os.path.join(profile_root, "Default", "History"))
        cur = con.cursor()
        res = cur.execute("SELECT urls.id, urls.url, urls.title, urls.visit_count, urls.typed_count, urls.last_visit_time FROM urls").fetchall()
        urls = []
        for r in res:
            urls.append(VisitedUrl(r[0], r[1], r[2], r[3], r[4], r[5]))

        self.urls = urls
    
    def _map_visits_to_urls(self) -> None:
        url_visits = []
        for u in self.urls:
            url_visits.append(VisitInfo(u))

        for v in self.visits:
            for u in url_visits:
                #print("v.url {} | u.visitedUrl.url {}".format(v.url, u.visitedUrl.id))
                if (v.url == u.id):
                    u.visits.append(v)

        self.url_visits = url_visits

    def get_history_data(self, profile_root):
        return super().get_history_data(profile_root)
    
    def dump_json(self):
        return super().dump_json()