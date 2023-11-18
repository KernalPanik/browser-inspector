# Browser History Inspector

## browse-inspector.py

Parses Browser history data into computer readable JSON file containing URL and relevant visit info. This JSON file can be used for further analysis.

This script expects a path to a browser profile root directory. In Chromium browsers, this can be found in: 

- Windows: ~/Users/AppData/Local/BraveSoftware/Brave-browser/User Data/ 
- macOS: ~/Library/Application Support/BraveSoftware/Brave-browser/ 
- Linux: ~/.config/BraveSoftware/Brave-Browser/

**Please note** that Browser instance must be closed, because otherwise you'll get `Database Locked` Error.

**Also note** that this tool does not obfuscate browsing history in any way.

This script is expected to work with any Chromium based browser.

TODO: Describe how to make custom profiles for testing