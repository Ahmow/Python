import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Ahmet.user_request import get_data_from_sql
import datetime as dt
from Ahmet.plot_data import plot_data

start_dt = dt.datetime(2025, 3, 3)
end_dt =dt.datetime(2025, 3, 23)

time_points = {"start": start_dt, "end": end_dt}

needed_data = get_data_from_sql(start_dt, end_dt)


plot_data("MSFT", needed_data, **time_points)

# prediction = analyze_data(needed_data, time_points)