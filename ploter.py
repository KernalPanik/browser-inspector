
import pandas as pd
import matplotlib.pyplot as plt


class Ploter:

    def plot_column(self, data: pd.DataFrame, plot_name: str):

        fig, ax = plt.subplots()

        y = data.time_spent.values
        x = data.domain.values

        ax.bar(x, y)

        ax.set_ylabel('Time')
        ax.set_title('My plot')

        plt.xticks(rotation="vertical")
        plt.show()
