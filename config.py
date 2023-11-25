from pathlib import Path

# Files paths differ for users. Descriptions possible file paths for different OS can be found in README file
# Uncomment the configuration based on your system:
#PATH_TO_BROWSER = "C:/Users/<USER>/AppData/Local/Google/Chrome/User Data" # Windows
PATH_TO_BROWSER = "{}/Library/Application Support/Google/Chrome".format(Path.home()) # macOS

# Date format YYYY-MM-DD as a string
# Browsing history data collection period
# Use 'none' if exact timestamps are not important
START_DATE = "none" # none if want whatever date 
END_DATE = "none" #"2023-11-04"

SUSPICIOUS_SITES = []
SUSPICIOUS_KEYWORDS = [] # Checks for suspicious words in website title