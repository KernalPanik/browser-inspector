import os
import json

from utilities import HistoryEncoder
from models import VisitInfo

class BrowserInspector():
    def __init__(self) -> None:
        self.url_visits = []
        self.visits = []
        self.urls = []

    def _collect_visits(self, profile_root: str) -> None:
        pass

    def _collect_urls(self, profile_root: str) -> None:
        pass

    def _map_visits_to_urls(self) -> None:
        pass

    def get_history_data(self, profile_root) -> []:
        '''
        Function that gets browser history data such as visited URL and time of visits.
        Arguments:
        path_to_root: str - a path to browser profile root folder.

        Return:
        list - of URL visited
        '''
        browser_profile_root = os.path.join(profile_root)
        if (not os.path.isdir(browser_profile_root)):
            print("Directory at {} seem to not exist.".format(browser_profile_root))
            exit(1)

        self._collect_visits(browser_profile_root)
        self._collect_urls(browser_profile_root)
        self._map_visits_to_urls()

        return self.url_visits

    def dump_json(self):
            return json.dumps(self.url_visits, indent=4, cls=HistoryEncoder)