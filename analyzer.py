import json
import pandas as pd
from io import StringIO
import warnings
from pandas.errors import SettingWithCopyWarning

from models import VisitInfo

class Analyzer:

    def __init__(self, browser_data: list[VisitInfo]) -> None:
        self.browser_data = browser_data
        self.df = self.to_dataframe()
        self.visited_url = self.get_visited_url(self.df)
        self.visits = self.get_visit(self.df)
        warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

    def analyze_history(self):
        '''
        A method to structure the data and provide insigts
        '''

        print(self.visited_url)
        print(self.visits)

        self.pred_data_for_to_ip(self.visited_url)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([ x.as_dict() for x in self.browser_data])

    def get_visited_url(self, history_data: pd.DataFrame)-> pd.DataFrame:
        
        df = history_data[["id", "url", "title", "visit_count", "typed_count", "last_visit_time"]]

        df = self.add_domain_collumn(df)

        return df
    
    def get_visit(self, history_data: pd.DataFrame) -> pd.DataFrame:

        tmp_df = history_data[["visits"]]

        data =  tmp_df.to_dict()

        data = data["visits"]

        tmp_list = []

        for i in data:
            tmp = data[i]
            tmp = tmp[0]
            tmp_list.append(tmp)

        df = pd.DataFrame(tmp_list)

        return df

    def prep_data_for_time_spent(self, visited_url: pd.DataFrame, visit: pd.DataFrame) -> pd.DataFrame:
        '''
            New columnm with data is "time_spent"
        '''


        unique_domains = visited_url["domain"].unique()

        inter_df = visited_url[["id", "url", "domain"]]

        inter_df["time_spent"] = inter_df.id.apply(lambda x: visit[visit.url == x]['visit_duration'].values[0])
        
        preped_df = pd.DataFrame(data=unique_domains, columns=["domain"])

        preped_df["time_spent"] = preped_df.domain.apply(lambda x: inter_df[inter_df.domain == x]["time_spent"].sum())

        preped_df["time_spent"] = preped_df.time_spent.apply(lambda x: round(x/1000000, 2))

        return preped_df

    def prep_data_for_visits(self, visited_url: pd.DataFrame) -> pd.DataFrame:
        '''
            New columnm with data is "visit_count"        
        '''
       
        unique_domains = visited_url["domain"].unique()

        inter_df = visited_url[["id", "url", "domain", "visit_count"]]
        
        preped_df = pd.DataFrame(data=unique_domains, columns=["domain"])

        preped_df["visit_count"] = preped_df.domain.apply(lambda x: inter_df[inter_df.domain == x]["visit_count"].sum())

        return preped_df
        

    def prep_data_for_average_time_spent(self, visited_url: pd.DataFrame, visit: pd.DataFrame) -> pd.DataFrame:
        '''
            Window in considered to be time spent in one url.
            New columnm with data is "average_time_spent"
        '''
        unique_domains = visited_url["domain"].unique()

        inter_df = visited_url[["id", "url", "domain"]]

        inter_df["time_spent"] = inter_df.id.apply(lambda x: visit[visit.url == x]['visit_duration'].values[0])
        
        preped_df = pd.DataFrame(data=unique_domains, columns=["domain"])
        
        preped_df["average_time_spent"] = preped_df.domain.apply(lambda x: inter_df[inter_df.domain == x]["time_spent"].mean())

        preped_df["average_time_spent"] = preped_df.average_time_spent.apply(lambda x: round(x/1000000, 2))

        return preped_df
    
    def pred_data_for_to_ip(self, visited_url: pd.DataFrame) -> pd.DataFrame:
        '''
            New columnm with data is "visit_count"
        '''
        inter_df = visited_url[["id", "url", "domain", "visit_count"]]

        preped_df = pd.DataFrame()

        preped_df["domain"] = inter_df.domain.apply(lambda x: x if self.is_ip(x) else pd.NA)

        preped_df = preped_df.dropna()

        unique_domains = preped_df["domain"].unique()

        preped_df = pd.DataFrame(data=unique_domains, columns=["domain"])

        preped_df["visit_count"] = preped_df.domain.apply(lambda x: inter_df[inter_df.domain == x]["visit_count"].sum())

        return preped_df
        

    def parse_domain(self, url: str) -> str:
        text = url.split("/")
        text = text[2]

        www_split = text.split(".")

        domain = ""
        for i in www_split:
            if i != "www":
                domain = domain + i + "."
        domain = domain[0: -1]
        return domain
    
    def add_domain_collumn(self, visited_url: pd.DataFrame) -> pd.DataFrame:

        visited_url['domain'] = visited_url.url.apply(lambda x: self.parse_domain(x))

        return visited_url
    
    def is_ip(self, url: str) -> bool:

        parts = url.split(".")

        if len(parts) > 3:
            return True
        else:
            return False
        
    def group_to_top(self, top_of: int, data: pd.DataFrame, column_to_order: str) -> pd.DataFrame:
        tmp_df = pd.DataFrame()

        # top values
        tmp_df = data.nlargest(top_of, column_to_order)

        # grouping other values under label "other"
        data = data.sort_values(by=column_to_order, ascending=False).tail(len(data) - top_of)

        sum = data[column_to_order].sum()

        new_row = pd.DataFrame([["Other", data[column_to_order].sum()]], columns=tmp_df.columns)
        tmp_df = pd.concat([tmp_df, new_row], ignore_index=True)

        return tmp_df
