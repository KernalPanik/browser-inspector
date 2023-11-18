import pandas as pd
from io import StringIO

from models import VisitInfo

class Analyzer:

    def __init__(self, browser_data: list[VisitInfo]) -> None:
        self.browser_data = browser_data

    def analyze_history(self):
        '''
        A method to structure the data and provide insigts
        '''
        for entry in self.browser_data:
            print(entry)

        df = pd.DataFrame([ x.as_dict() for x in self.browser_data])
        
        print(df[["id", 'url', 'title']])

        df.info()
    