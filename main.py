from analyzer import Analyzer
from config import PATH_TO_BROWSER, START_DATE, END_DATE, SUSPICIOUS_SITES, SUSPICIOUS_KEYWORDS
from browser_inspector import BrowserInspector
from adaptors.chromium_inspector import ChromiumInspector
from config import PATH_TO_BROWSER, START_DATE, END_DATE, REPORT_NAME
from pdf_engine import *
from ploter import Ploter
from utilities import *
from reporter import Reporter

# Since we are too lazy to have proper tests, let's have simple "helpers" -- a functions which should do one thing like generate pdf
# If the action gets completed and we can verify it, then this test considered as 'passed'
def pdf_generation_test_helper() -> None:
    md = pdf_start_markdown("testmd.md")
    pdf_append_large_header(md, "Hello world")
    pdf_append_paragraph(md, "Kind of Lorem Ipsum")
    pdf_append_paragraph(md, "paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright")
    pdf_append_small_header(md, "A bit of a smaller header")
    pdf_append_image(md, "test image", "cat.png", "test image", 40, 40)
    pdf_close_markdown(md)
    pandoc_call("testmd.md", "test-report.pdf", True)

def suspicious_link_tree_generation_based_on_site_test_helper() -> None:
    path_to_root = PATH_TO_BROWSER
    browser_inspector = ChromiumInspector()
    sus = browser_inspector.filter_suspicious_sites_by_url(path_to_root, date_to_epoch(START_DATE, TimeEpochFormat.ISO_8601_EPOCH), date_to_epoch(END_DATE, TimeEpochFormat.ISO_8601_EPOCH), SUSPICIOUS_SITES)

    i = 0
    for vi in sus:
        sus_hier = browser_inspector.build_sus_link_hierarchy(vi)
        print(sus_hier)
        plot_node_dependencies(sus_hier, "suspicious_sites_{}.png".format(i))
        i += 1

def suspicious_link_tree_generation_based_on_title_test_helper():
    path_to_root = PATH_TO_BROWSER
    browser_inspector = ChromiumInspector()
    sus = browser_inspector.filter_suspicious_sites_by_title(path_to_root, date_to_epoch(START_DATE, TimeEpochFormat.ISO_8601_EPOCH), date_to_epoch(END_DATE, TimeEpochFormat.ISO_8601_EPOCH), SUSPICIOUS_KEYWORDS)

    i = 0;
    for vi in sus:
        sus_hier = browser_inspector.build_sus_link_hierarchy(vi)
        print(sus_hier)
        plot_node_dependencies(sus_hier, "suspicious_titles_{}.png".format(i))
        i += 1

if __name__ == "__main__":
    """path_to_root = PATH_TO_BROWSER
    bi = BrowserInspector()
    browser_data = bi.get_history_data(path_to_root, START_DATE, END_DATE)

    analyzer = Analyzer(browser_data)
    # analyzer.analyze_history()

    ploter = Ploter(analyzer)
    ploter.plot("Awensome plots")"""

    inspector = ChromiumInspector()
    history = inspector.get_history_data(PATH_TO_BROWSER, date_to_epoch(START_DATE, TimeEpochFormat.ISO_8601_EPOCH), date_to_epoch(END_DATE, TimeEpochFormat.ISO_8601_EPOCH))
    reporter = Reporter(REPORT_NAME, history, inspector)
    reporter.build_report()