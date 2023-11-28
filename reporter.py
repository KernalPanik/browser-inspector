from models import VisitInfo
from ploter import Ploter
from analyzer import Analyzer
from browser_inspector import BrowserInspector
from config import PATH_TO_BROWSER, START_DATE, END_DATE, SUSPICIOUS_SITES, SUSPICIOUS_KEYWORDS
import os
import utilities as utils
import shutil

"""
The main report creation method of this Class will produce a report folder,
containing the report itself and all the connected data, like graphs and images
"""
class Reporter:
    def __init__(self, report_name: str, browsing_history: list[VisitInfo], inspector: BrowserInspector) -> None:
        self.report_folder = os.path.join(os.getcwd(), report_name)
        self.browsing_history = browsing_history
        self.plotter = Ploter(Analyzer(browsing_history))
        self.browser_inspector = inspector
        if (os.path.exists(self.report_folder)):
            print("path at {} already exists! will delete it".format(self.report_folder))
            shutil.rmtree(self.report_folder)
        os.mkdir(self.report_folder)

    def _prepare_plots_to_report(self) -> None:
        self.plotter.plot(os.path.join(self.report_folder, "diagrams"))

    def _prepare_sus_visits_graph(self) -> None:
        title_based_hierarchy_list = self.browser_inspector.filter_suspicious_sites_by_title()
        title_based_hierarchies = []
        for tbh in title_based_hierarchy_list:
            title_based_hierarchies.append(self.browser_inspector.build_sus_link_hierarchy(tbh))

        index = 0
        for tbh in title_based_hierarchies:        
            utils.plot_node_dependencies(tbh, os.path.join(self.report_folder, "sus_sites_titles_{}".format(index)))
            index += 1

    def build_report(self) -> str:
        report_file = "report.pdf"
        self._prepare_plots_to_report()
        self._prepare_sus_visits_graph()
        return os.path.join(self.report_folder, report_file)