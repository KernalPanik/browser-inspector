from pathlib import Path

# Files paths differ for users. Descriptions possible file paths for different OS can be found in README file
# Uncomment the configuration based on your system:
# PATH_TO_BROWSER = "{}/AppData/Local/Google/Chrome/User Data".format(Path.home()).replace("\\", "/") # Windows
PATH_TO_BROWSER = "{}/Library/Application Support/Google/Chrome".format(Path.home()) # macOS

# Date format YYYY-MM-DD as a string
# Browsing history data collection period
# Use 'none' if exact timestamps are not important
START_DATE = "none" # none if want whatever date 
END_DATE = "none" #"2023-11-04"

REPORT_NAME = "test-report-1" # This will be the name of a report folder and the document

SUSPICIOUS_SITES = [] # Checks for suspicious urls or sites
SUSPICIOUS_KEYWORDS = [] # Checks for suspicious words in website title
IGNORE_IP = False # Set to True if you don't want to capture direct calls to IP addresses