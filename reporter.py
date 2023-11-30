from models import VisitInfo
from ploter import Ploter
from analyzer import Analyzer
from browser_inspector import BrowserInspector
from config import PATH_TO_BROWSER, START_DATE, END_DATE, SUSPICIOUS_SITES, SUSPICIOUS_KEYWORDS, IGNORE_IP
import os
import utilities as utils
import shutil
import pdf_engine
import csv

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
        self.report_document_path = "" #os.path.join(self.report_folder, report_name)
        self.final_report_path = os.path.join(self.report_folder, "report.pdf")
        
        # We're talking about intermim report, which is a markdown doc here:
        if len(report_name.split('.')) > 0:
            if report_name.split('.')[-1] == "md":
                self.report_document_path = os.path.join(self.report_folder, report_name)
            else:
                self.report_document_path = os.path.join(self.report_folder, report_name+".md")
        else:
            self.report_document_path = os.path.join(self.report_folder, report_name+".md")
        
        if (os.path.exists(self.report_folder)):
            print("path at {} already exists! will delete it".format(self.report_folder))
            shutil.rmtree(self.report_folder)
        os.mkdir(self.report_folder)

    def _prepare_plots_to_report(self) -> (str, str, str):
        diagrams_header = "Search statistics"
        diagrams_paragraph = "This diagram shows the top 5 websites visited and overall session duration. Overall session duration is a sum of all visit durations combined."
        diagrams_path = os.path.join(self.report_folder, "diagrams.png")
        self.plotter.plot(diagrams_path)
        return diagrams_header, diagrams_paragraph, diagrams_path
    
    def _get_graphs(self, hierarchy_list: [], graph_file_name: str) -> []:
        hierarchies = []
        for tbh in hierarchy_list:
            hierarchies.append(self.browser_inspector.build_sus_link_hierarchy(tbh))

        index = 0
        graph_paths = []
        for tbh in hierarchies:
            path = os.path.join(self.report_folder, "{}_{}".format(graph_file_name, index))
            utils.plot_node_dependencies(tbh, path)
            graph_paths.append(path + ".png")
            index += 1

        return graph_paths

    def _prepare_sus_visits_graph(self) -> (str, str, [str]):
        sus_visits_header = "Suspicious visit graph"
        sus_visit_paragraph = "This section provides insights into the browsing 'tree', showing what led to a suspicious site visited."
        """title_based_hierarchy_list = self.browser_inspector.filter_suspicious_sites_by_title()
        title_based_hierarchies = []
        for tbh in title_based_hierarchy_list:
            title_based_hierarchies.append(self.browser_inspector.build_sus_link_hierarchy(tbh))

        index = 0
        graph_paths = []
        for tbh in title_based_hierarchies:
            path = os.path.join(self.report_folder, "sus_sites_titles_{}".format(index))
            utils.plot_node_dependencies(tbh, path)
            graph_paths.append(path + ".png")
            index += 1

        return graph_paths"""

        title_graphs = self._get_graphs(self.browser_inspector.filter_suspicious_sites_by_title(), "sus_titles")
        url_graphs = self._get_graphs(self.browser_inspector.filter_suspicious_sites_by_url(), "sus_urls")
        return sus_visits_header, sus_visit_paragraph, title_graphs + url_graphs

    def _prepare_ip_call_report(self) -> (str, str):
        if IGNORE_IP:
            return "", ""

        header = "Calls to IP addresses without providing host name"
        no_host_visits_str = ""
        if len(self.browser_inspector.direct_ip_calls) > 0:
            for ip in self.browser_inspector.direct_ip_calls:
                no_host_visits_str = no_host_visits_str + str(ip) + "\n\n"

        return header, no_host_visits_str

    def _prepare_basic_information_section(self) -> (str, str):
        large_header = "{}".format(self.report_name)
        time_frame_paragraph = ""
        start_date_entry = ""
        end_date_entry = ""

        if START_DATE == "none":
            start_date_entry = "\n\nThere was no start of search timeframe provided, information collected was from the first visit.\n"
        else:
            start_date_entry = "Start of search timeframe was at {}".format(START_DATE)
        if END_DATE == "none":
            end_date_entry = "\n\nThere was no end of search timeframe provided, information collected was until the last visit.\n"
        else:
            end_date_entry = "End of search timeframe was at {}".format(END_DATE)

        time_frame_paragraph = "{}. {}\n".format(start_date_entry, end_date_entry)

        sus_keywords_entry = ""
        if len(SUSPICIOUS_KEYWORDS) > 0:
            sus_keywords_entry = "\n\nWas looking for visited website titles with such keywords: "
            for keyword in SUSPICIOUS_KEYWORDS:
                sus_keywords_entry = sus_keywords_entry + "{}; ".format(keyword)
            sus_keywords_entry = sus_keywords_entry + "\n"

        sus_sites_entry = ""
        if len(SUSPICIOUS_SITES) > 0:
            sus_sites_entry = "\n\nWas looking for visited website titles with such keywords: "
            for keyword in SUSPICIOUS_SITES:
                sus_sites_entry = sus_sites_entry + "{}; ".format(keyword)
            sus_sites_entry = sus_sites_entry + "\n"

        paragraph = "The browsing history was collected from {}\n {} {} {}".format(PATH_TO_BROWSER, time_frame_paragraph, sus_keywords_entry, sus_sites_entry)
        return large_header, paragraph

    def _get_csv_data(self) -> str:
        csv_columns = ['id', 'url', 'title', 'visit_count', 'typed_count', 'last_visit_time', 'visit']
        sus_history_file_path = os.path.join(self.report_folder, "sus_history.csv")
        sus_visit_file_path = os.path.join(self.report_folder, "sus_specific_visits.csv")
        with open(sus_history_file_path, "w+") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)

            with open(sus_visit_file_path, "a+") as susfile:
                w = csv.writer(susfile)
                w_csv_columns = ['id', 'url', 'visit_time', 'visit_duration', 'from_visit']
                w.writerow(w_csv_columns)
                for sus_visit in self.browser_inspector.filter_suspicious_sites_by_title():
                    writer.writerow(sus_visit.as_data_entry())
                    for v in sus_visit.visits:
                        w.writerow(v.as_data_entry())

                for sus_visit in self.browser_inspector.filter_suspicious_sites_by_url():
                    writer.writerow(sus_visit.as_data_entry())
                    for v in sus_visit.visits:
                        w.writerow(v.as_data_entry())
    
        return sus_history_file_path, sus_visit_file_path

    def build_report(self) -> str:
        diagrams_header, diagrams_paragraph, diagrams = self._prepare_plots_to_report()
        graph_header, graph_paragraph, graphs = self._prepare_sus_visits_graph()
        ip_report_header, ip_report_paragraph = self._prepare_ip_call_report() # if paragraph returned is empty, do not use
        large_header, paragraph = self._prepare_basic_information_section()
        handler = pdf_engine.pdf_start_markdown(self.report_document_path)
        pdf_engine.pdf_append_large_header(handler, large_header)
        pdf_engine.pdf_append_paragraph(handler, paragraph)
        if ip_report_paragraph != "":
            pdf_engine.pdf_append_small_header(handler, ip_report_header)
            pdf_engine.pdf_append_paragraph(handler, ip_report_paragraph)
        
        pdf_engine.pdf_append_small_header(handler, diagrams_header)
        pdf_engine.pdf_append_paragraph(handler, diagrams_paragraph)
        pdf_engine.pdf_append_image(handler, diagrams, title="Usage Statisics")
        pdf_engine.pdf_append_paragraph(handler, "\n\n")
        if len(graphs) > 0:
            pdf_engine.pdf_append_small_header(handler, graph_header)
            pdf_engine.pdf_append_paragraph(handler, graph_paragraph)
            index = 1
            for graph in graphs:
                pdf_engine.pdf_append_image(handler, graph, title="Suspicious visits graph-{}".format(index))
                pdf_engine.pdf_append_paragraph(handler, "\n\n")
                index += 1

        pdf_engine.pdf_close_markdown(handler)

        pdf_engine.pandoc_call(self.report_document_path, self.final_report_path, False)
        csv_report, spec_report = self._get_csv_data()
        print("Made csv reports at {} and {}".format(csv_report, spec_report))
        return self.report_document_path