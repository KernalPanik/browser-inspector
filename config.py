from pathlib import Path

# Files paths differ for users. Descriptions possible file paths for different OS can be found in README file
#PATH_TO_BROWSER = "C:/Users/<USER>/AppData/Local/Google/Chrome/User Data"
PATH_TO_BROWSER = "{}/Library/Application Support/Google/Chrome".format(Path.home())

# Date format YYYY-MM-DD as a string
START_DATE = "none" # none if want whatever date # "2023-11-03"
END_DATE = "none" #"2023-11-04"

SUSPICIOUS_SITES = ["telegraph"]