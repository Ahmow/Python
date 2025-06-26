# data_df hat die ganze Info über Open, Close, High, Low, Volume, Tag
import time
import matplotlib.pyplot as plt


def plot_data(symbol, data_df, **time_points):
    start_point = time_points["start"]
    end_point = time_points["end"]
    
    data_df.plot(kind="scatter", x="date", y="open")
    plt.show()