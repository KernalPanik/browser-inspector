from config import PATH_TO_BROWSER
from browse_inspector import get_hisotry_data

if __name__ == "__main__":
    path_to_root = PATH_TO_BROWSER
    browser_data = get_hisotry_data(path_to_root)

    print(browser_data)