import os
import json

from utilities import HistoryEncoder
from models import VisitInfo

class BrowserInspector():
    def __init__(self) -> None:
        self.visit_infos = []
        self.visits = []
        self.urls = []

    def _collect_visits(self, profile_root: str, start_timestamp: int, end_timestamp: int) -> None:
        pass

    def _collect_urls(self, profile_root: str) -> None:
        pass

    def _map_visits_to_urls(self) -> None:
        pass

    def get_history_data(self, profile_root: str, start_timestamp: int, end_timestamp: int) -> []:
        '''
        Function that gets browser history data such as visited URL and time of visits.
        Arguments:
        path_to_root: str - a path to browser profile root folder.

        Return:
        list - of URL visited as a VisitedUrl object
        '''
        browser_profile_root = os.path.join(profile_root)
        if (not os.path.isdir(browser_profile_root)):
            print("Directory at {} seem to not exist.".format(browser_profile_root))
            exit(1)

        self._collect_visits(browser_profile_root, start_timestamp, end_timestamp)
        self._collect_urls(browser_profile_root)
        self._map_visits_to_urls()

        return self.visit_infos

    '''
    Locates suspicious site visit information based on provided site names.
    input: a list of sites in a form of domain names
    '''
    def filter_suspicious_sites(self, profile_root: str, start_timestamp: int, end_timestamp: int, susp_sites: []) -> []:
        visit_infos: VisitInfo = self.get_history_data(profile_root, start_timestamp, end_timestamp)
        suspicous_visits = []
        for visit_info in visit_infos:
            for site in susp_sites:
                actual_url = visit_info.url.split("/")[2]
                if site in actual_url:
                    print(visit_info.as_dict)
                    suspicous_visits.append(visit_info)

        return suspicous_visits

    def dump_json(self):
            return json.dumps(self.visit_infos, indent=4, cls=HistoryEncoder)