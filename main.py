from analyzer import Analyzer
from config import PATH_TO_BROWSER
from browser_inspector import get_hisotry_data
from pdf_engine import *

if __name__ == "__main__":
    #path_to_root = PATH_TO_BROWSER
    #browser_data = get_hisotry_data(path_to_root)

    # print(browser_data)

    #analyzer = Analyzer(browser_data)
    #analyzer.analyze_history()

    # Some testing of PDF engine, delete later
    md = start_markdown("testmd.md")
    append_large_header(md, "Hello world")
    append_paragraph(md, "Kind of Lorem Ipsum")
    append_paragraph(md, "paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright paragraph which should be quite large, probably loaded from another file, but for testing it's alright")
    append_small_header(md, "A bit of a smaller header")
    append_image(md, "test image", "cat.png", "test image", 40, 40)
    close_markdown(md)
    pandoc_call("testmd.md", "test-report.pdf", True)