import os
import json
from config import SUSPICIOUS_KEYWORDS, SUSPICIOUS_SITES

from utilities import HistoryEncoder
from models import VisitInfo, Visit, VisitedUrl

class BrowserInspector():
    def __init__(self) -> None:
        self.visit_infos = []
        self.visits = []
        self.urls = []
        self.direct_ip_calls = []

    def _collect_visits(self, profile_root: str, start_timestamp: int, end_timestamp: int) -> None:
        pass

    def _collect_urls(self, profile_root: str) -> None:
        pass

    def _map_visits_to_urls(self) -> None:
        pass
    
    '''
        Function that gets browser history data such as visited URL and time of visits.
        Arguments:
        path_to_root: str - a path to browser profile root folder.

        Return:
        list - of URL visited as a VisitedUrl object
    '''
    def get_history_data(self, profile_root: str, start_timestamp: int, end_timestamp: int) -> []:
        browser_profile_root = os.path.join(profile_root)
        if (not os.path.isdir(browser_profile_root)):
            print("Directory at {} seem to not exist.".format(browser_profile_root))
            exit(1)

        self._collect_visits(browser_profile_root, start_timestamp, end_timestamp)
        self._collect_urls(browser_profile_root)
        self._map_visits_to_urls()

        return self.visit_infos

    def _looks_like_ipv4_address(self, url: str) -> bool:
        yes = True
        try:
            for entry in url.split('.'):
                if int(entry) < 0 and int(entry) > 256:
                    yes = False
        except:
            yes = False

        return yes

    '''
    Locates suspicious site visit information based on provided site names, looking at the website url (site)
    input: a list of sites in a form of domain names
    '''
    def filter_suspicious_sites_by_url(self) -> []:
        suspicous_visits = []
        for visit_info in self.visit_infos:
            actual_url = visit_info.url.split("/")[2]
            if self._looks_like_ipv4_address(actual_url):
                self.direct_ip_calls.append(visit_info.url)
                suspicous_visits.append(visit_info)
            for site in SUSPICIOUS_SITES:
                if site in actual_url:
                    # print(visit_info.as_dict)
                    suspicous_visits.append(visit_info)

        return suspicous_visits

    '''
    Locates suspicious site visit information based on provided site names, looking at the website title
    input: a list of sites in a form of domain names
    '''
    def filter_suspicious_sites_by_title(self) -> []:
        suspicous_visits = []
        for visit_info in self.visit_infos:
            for site in SUSPICIOUS_KEYWORDS:
                if site in visit_info.title.lower():
                    suspicous_visits.append(visit_info)

        return suspicous_visits

    def _extract_url_title_from_visit(self, id: int) -> (str, str):
        for v in self.urls:
            if (v.id == id):
                return v.url, v.title

    # Finds relevant from_visit entry
    # returns next visit ID and URL
    def _find_next_visit(self, visit_id: int) -> (int, str):
        for v in self.visits:
            if (visit_id == v.from_visit):
                    return -1, "Unknown"
            if v.id == visit_id:
                return v.from_visit, self._extract_url_title_from_visit(v.url)

        return -1, "Unknown"
    
    def _add_visit_data_to_list(self, target_visit_list: [], data: ()) -> None:
        first = ""
        second = ""
        if len(data[0]) > 50:
            first = data[0][0:30]
        else:
            first = data[0]

        if len(data[1]) > 50:
            second = data[1][0:30]
        else:
            second = data[1]

        target_visit_list.append((first, second))

    def build_sus_link_hierarchy(self, sus_visit_info: VisitInfo) -> []:
        related_visits = [()]
        for visit in sus_visit_info.visits:
            # For each visit in given visit info, iterate over known visits, 
            # and find related visits to form a sequence of redirects
            #print("visit id: {}, from visit {}".format(visit.id, visit.from_visit))
            vip = visit.from_visit
            start_url, start_title = self._extract_url_title_from_visit(visit.url)
            self._add_visit_data_to_list(related_visits, (start_url, start_title))
            #related_visits.append((start_url, start_title))
            while vip != -1:
                vip, visit_data = self._find_next_visit(vip)
                self._add_visit_data_to_list(related_visits, (visit_data[0], visit_data[1]))
                #related_visits.append((visit_data[0], visit_data[1]))
                #print("linked from {}".format(vip))

        return related_visits

    def dump_json(self):
            return json.dumps(self.visit_infos, indent=4, cls=HistoryEncoder)