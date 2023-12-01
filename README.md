# Browser History Inspector

To run the tool, configure it in the `config.py` file and run using

```
python main.py
```

## Prerequisites

Required tools can be installed by using provided `tools-uploader` scripts.

In order to run this tool, a set of tools need to be installed. Please refer to requirements.txt for pip packages, and use provided tool-installer scripts for external tools like Pandoc.

```
brew install pandoc
choco install pandoc
```

For Pandoc to work properly, LaTeX engine which supports pdflatex, will be needed. For macOS we suggest mactex, and for windows -- MikTex.

```
brew install mactex
choco install MikTex
```

Graph generation requires `dot` tool, which can be installed as a part of graphviz package:

```
brew install graphviz 
conda install graphviz
```

## Usage overview

The only way to configure the tool is to use `config.py` file. Please set selected configurations as described in the comments. By tweaking the configuration, you can choose the timeframe of the browsing by using `START_DATE` and `END_DATE` entries. The keywords an inspector should look for are defined in `SUSPICIOUS_SITES` and `SUSPICIOUS_KEYWORDS` arrays. By default, Browser History Inspector considers any visit to a IP instead of regular hostname as suspicious activity. It can be disabled using `IGNORE_IP` flag.

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

## Reporter module

This module collects all the previous modules and uses them to generate every component which will later be turned into a PDF report. The basic usage of our tools is simple:

```
    inspector = ChromiumInspector()
    history = inspector.get_history_data(PATH_TO_BROWSER, date_to_epoch(START_DATE, TimeEpochFormat.ISO_8601_EPOCH), date_to_epoch(END_DATE, TimeEpochFormat.ISO_8601_EPOCH))
    reporter = Reporter("test-report", history, inspector)
    reporter.build_report()
```

This will create a test-report folder in the call root. The folder will contain the PDF report, csv sheets showing suspicious activities, diagrams and graphs.

## PDF Generation

To generate PDF report, Pandoc is needed. It can be installed using tool-installer scripts. PDF is generated from markdown file, and functions needed to build such a markdown are defined in `pdf_engine` module.