from database.user_request import get_data_from_sql
import datetime as dt
from main_interact.plot_data import plot_data
from main_interact.prediction_data import analyze_data
from main_interact.top_stock_data import top_stocks
from main_interact.prediction_data_LZ import analyze_data_Lorentzian


start_dt = dt.datetime(2024, 8, 6)
end_dt =dt.datetime(2024, 8, 26)

time_points = {"start": start_dt, "end": end_dt}

needed_data = get_data_from_sql(start_dt, end_dt)

# plot_data("MSFT", needed_data, **time_points)

# prediction = analyze_data(needed_data, time_points)

# top_stocks(start_dt, end_dt)

analyze_data_Lorentzian(needed_data, time_points)

