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
        self.report_name = report_name
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

    def _prepare_plots_to_report(self) -> (str, str, str):
        diagrams_header = "Search statistics"
        diagrams_paragraph = "This diagram shows the top 5 websites visited and overall session duration. Overall session duration is a sum of all visit durations combined."
        diagrams_path = os.path.join(self.report_folder, "diagrams.png")
        self.plotter.plot(diagrams_path)
        return diagrams_path

    def _prepare_sus_visits_graph(self) -> (str, str, [str]):
        sus_visits_header = "Suspicious visit graph"
        sus_visit_paragraph = "This section provides insights into the browsing 'tree', showing what led to a suspicious site visited."
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
            for ip in self.browser_inspector.direct_ip_calls:
                no_host_visits_str = no_host_visits_str + str(ip) + "\n"

        return header, no_host_visits_str

    def _prepare_basic_information_section(self) -> (str, str):
        large_header = "{}".format(self.report_name)
        time_frame_paragraph = ""
        start_date_entry = ""
        end_date_entry = ""

        if START_DATE == "none":
            start_date_entry = "There was no start of timeframe provided, information collected was from the first visit."
        else:
            start_date_entry = "Start of timeframe was at {}".format(START_DATE)
        if END_DATE == "none":
            end_date_entry = "There was no end of timeframe provided, information collected was until the last visit."
        else:
            end_date_entry = "End of timeframe was at {}".format(END_DATE)

        time_frame_paragraph = "Browsing data was collected from this timeframe: {}. {}\n".format(start_date_entry, end_date_entry)

        sus_keywords_entry = ""
        if len(SUSPICIOUS_KEYWORDS) > 0:
            sus_keywords_entry = "Was looking for visited website titles with such keywords: "
            for keyword in SUSPICIOUS_KEYWORDS:
                sus_keywords_entry = sus_keywords_entry + "{}; ".format(keyword)
            sus_keywords_entry = sus_keywords_entry + "\n"

        sus_sites_entry = ""
        if len(SUSPICIOUS_SITES) > 0:
            sus_sites_entry = "Was looking for visited website titles with such keywords: "
            for keyword in SUSPICIOUS_SITES:
                sus_sites_entry = sus_sites_entry + "{}; ".format(keyword)
            sus_sites_entry = sus_sites_entry + "\n"

        paragraph = "The browsing history was collected from {}.\n {}\n {}\n {}\n".format(PATH_TO_BROWSER, time_frame_paragraph, sus_keywords_entry, sus_sites_entry)
        return large_header, paragraph

    def build_report(self) -> str:
        diagrams = self._prepare_plots_to_report()
        graphs = self._prepare_sus_visits_graph()
        ip_report_header, ip_report_paragraph = self._prepare_ip_call_report() # if paragraph returned is empty, do not use
        large_header, paragraph=  self._prepare_basic_information_section()
        pdf_engine.pdf_start_markdown(self.report_document_path)
        pdf_engine.pdf_append_large_header(large_header)
        pdf_engine.pdf_append_paragraph(paragraph)
        return self.report_document_path