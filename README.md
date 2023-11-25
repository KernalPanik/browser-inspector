# Browser History Inspector

## Usage overview

This script expects a path to a browser profile root directory. In Chromium browsers, this can be found in: 

- Windows: ~/Users/AppData/Local/BraveSoftware/Brave-browser/User Data/ 
- macOS: ~/Library/Application Support/BraveSoftware/Brave-browser/ 
- Linux: ~/.config/BraveSoftware/Brave-Browser/

**Please note** that Browser instance must be closed, because otherwise you'll get `Database Locked` Error.

**Also note** that this tool does not obfuscate browsing history in any way.

This script is expected to work with any Chromium based browser, tested with Brave and Chrome browsers.

## Browser inspector module 

Parses Browser history data into computer readable JSON file containing URL and relevant visit info. This JSON file can be used for further analysis outside of this tool. Data collected using `get_history_data` or `filter_suspicious_sites` functions is later used to generate graphs depicting suspicious visit trees.

## Utilities module

This module is mainly used for internal, purposes, however the most interesting function is `plot_node_dependencies`, which can be used to generate graphs showing the visit hierarchy. This is useful when you want to get a picture of how a certain suspicious URL was reached, maybe user got there from sites which were not considered 'suspicious'

## PDF Generation

To generate PDF report, Pandoc is needed. It can be installed using tool-installer scripts. PDF is generated from markdown file, and functions needed to build such a markdown are defined in `pdf_engine` module.