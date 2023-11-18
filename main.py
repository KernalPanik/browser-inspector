from analyzer import Analyzer
from config import PATH_TO_BROWSER, START_DATE, END_DATE
from pdf_engine import *
from utilities import *
from adaptors.chromium_inspector import ChromiumInspector

import utilities

if __name__ == "__main__":
    #path_to_root = PATH_TO_BROWSER
    #browser_data = get_history_data(path_to_root)

    # print(browser_data)

    #analyzer = Analyzer(browser_data)
    #analyzer.analyze_history()

    # Some testing of PDF engine, delete later
    #md = pdf_start_markdown("testmd.md")
    #pdf_append_large_header(md, "Hello world")
    #pdf_append_paragraph(md, "Kind of Lorem Ipsum")
    #pdf_append_paragraph(md, "paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright")
    #pdf_append_small_header(md, "A bit of a smaller header")
    #pdf_append_image(md, "test image", "cat.png", "test image", 40, 40)
    #pdf_close_markdown(md)
    #pandoc_call("testmd.md", "test-report.pdf", True)

    path_to_root = PATH_TO_BROWSER
    browser_inspector = ChromiumInspector()
    browser_data = browser_inspector.get_history_data(path_to_root, utilities.date_to_epoch(START_DATE, TimeEpochFormat.ISO_8601_EPOCH), utilities.date_to_epoch(END_DATE, TimeEpochFormat.ISO_8601_EPOCH))
    browser_data_json = browser_inspector.dump_json()
    print(browser_data_json)