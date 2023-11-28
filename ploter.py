
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from analyzer import Analyzer


class Ploter:

    def __init__(self, analyzer: Analyzer) -> None:
        self.analyzer = analyzer

    def get_data_for_plots(self):

        visited_url = self.analyzer.visited_url
        visits = self.analyzer.visits

        time_spent_data = self.analyzer.prep_data_for_time_spent(visited_url, visits)
        time_spent_data = self.analyzer.group_to_top(4, time_spent_data, "time_spent")

        visits_data = self.analyzer.prep_data_for_visits(visited_url)
        visits_data = self.analyzer.group_to_top(4, visits_data, "visit_count")

        avarage_time_spent_data = self.analyzer.prep_data_for_average_time_spent(visited_url, visits)
        avarage_time_spent_data = self.analyzer.group_to_top(4, avarage_time_spent_data, "avarage_time_spent")

        return time_spent_data, visits_data, avarage_time_spent_data


    def plot(self, plot_name: str):

        fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize = (12 , 10))

        time_spent_data, visits_data, avarage_time_spent_data = self.get_data_for_plots()

        y = time_spent_data.time_spent.values
        x = time_spent_data.domain.values

        # Time spent diagram
        ax1.bar(x, y)

        ax1.set_ylabel('Time')
        ax1.set_title('Time spent')

        ax1.set_xticks(ticks = np.arange(len(x)), labels = x, rotation="vertical")

        # Visits diagram
        y = visits_data.visit_count.values
        x = visits_data.domain.values

        ax2.bar(x, y)

        ax2.set_ylabel('Visits Count')
        ax2.set_title('Visits made')

        ax2.set_xticks(ticks = np.arange(len(x)), labels = x, rotation="vertical")

        # Avarage time spent diagram
        y = avarage_time_spent_data.avarage_time_spent.values
        x = avarage_time_spent_data.domain.values

        ax3.bar(x, y)

        ax3.set_ylabel('Avarage time')
        ax3.set_title('Avarage time spent')

        ax3.set_xticks(ticks = np.arange(len(x)), labels = x, rotation="vertical")

        plt.subplots_adjust(bottom=0.24)

        plt.savefig("diagrams.png")

        # plt.show()