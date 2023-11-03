from analyzer import Analyzer
from config import PATH_TO_BROWSER
from browser_inspector import get_hisotry_data

if __name__ == "__main__":
    path_to_root = PATH_TO_BROWSER
    browser_data = get_hisotry_data(path_to_root)

    # print(browser_data)

    analyzer = Analyzer(browser_data)
    analyzer.analyze_history()