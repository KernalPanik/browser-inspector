from analyzer import Analyzer
from config import PATH_TO_BROWSER
from browser_inspector import get_hisotry_data
from pdf_engine import *
from ploter import Ploter

if __name__ == "__main__":
    path_to_root = PATH_TO_BROWSER
    browser_data = get_hisotry_data(path_to_root)

    analyzer = Analyzer(browser_data)
    # analyzer.analyze_history()

    ploter = Ploter()
    ploter.plot_column(analyzer.prep_data_for_time_spent(analyzer.visited_url, analyzer.visits), "Time spent")

    # Some testing of PDF engine, delete later
    # md = pdf_start_markdown("testmd.md")
    # pdf_append_large_header(md, "Hello world")
    # pdf_append_paragraph(md, "Kind of Lorem Ipsum")
    # pdf_append_paragraph(md, "paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright")
    # pdf_append_small_header(md, "A bit of a smaller header")
    # pdf_append_image(md, "test image", "cat.png", "test image", 40, 40)
    # pdf_close_markdown(md)
    # pandoc_call("testmd.md", "test-report.pdf", True)