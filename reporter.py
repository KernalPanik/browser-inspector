from models import VisitInfo
from ploter import Ploter
from analyzer import Analyzer
from browser_inspector import BrowserInspector
from config import PATH_TO_BROWSER, START_DATE, END_DATE, SUSPICIOUS_SITES, SUSPICIOUS_KEYWORDS
import os
import utilities as utils
import shutil
import pdf_engine

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
        self.report_document_path = os.path.join(self.report_folder, report_name)

        if (os.path.exists(self.report_folder)):
            print("path at {} already exists! will delete it".format(self.report_folder))
            shutil.rmtree(self.report_folder)
        os.mkdir(self.report_folder)

        """
        if len(report_name.split('.')) > 0 and report_name.split('.')[:-1] == "pdf":
            if report_name.split('.')[:-1] == "pdf":
                self.reportFileHandler = pdf_engine.pdf_start_markdown(self.report_document_path)
            else:
                self.reportFileHandler = pdf_engine.pdf_start_markdown(self.report_document_path)
        """

    def _prepare_plots_to_report(self) -> str:
        diagrams_path = os.path.join(self.report_folder, "diagrams.png")
        self.plotter.plot(diagrams_path)
        return diagrams_path

    def _prepare_sus_visits_graph(self) -> [str]:
        title_based_hierarchy_list = self.browser_inspector.filter_suspicious_sites_by_title()
        title_based_hierarchies = []
        for tbh in title_based_hierarchy_list:
            title_based_hierarchies.append(self.browser_inspector.build_sus_link_hierarchy(tbh))

        index = 0
        graph_paths = []
        for tbh in title_based_hierarchies:
            path = os.path.join(self.report_folder, "sus_sites_titles_{}.png")
            utils.plot_node_dependencies(tbh, path)
            graph_paths.append(path)
            index += 1

        return graph_paths

    def _prepare_ip_call_report(self) -> (str, str):
        header = "Suspicious calls to IP addresses"
        no_host_visits_str = ""
        if len(self.browser_inspector.direct_ip_calls) > 0:
            #pdf_engine.pdf_append_small_header(self.reportFileHandler, "Suspicious calls to IP addresses")
            for ip in self.browser_inspector.direct_ip_calls:
                no_host_visits_str = no_host_visits_str + str(ip) + "\n"
            #pdf_engine.pdf_append_paragraph(self.reportFileHandler, "Visits to sites without a hostname were detected: {}\n".format(no_host_visits_str))

        return header, no_host_visits_str

    def build_report(self) -> str:
        diagrams = self._prepare_plots_to_report()
        graphs = self._prepare_sus_visits_graph()
        ip_report_header, ip_report_paragraph = self._prepare_ip_call_report() # if paragraph returned is empty, do not use
        return self.report_document_path