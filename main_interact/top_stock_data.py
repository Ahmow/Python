import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np


def top_stocks(start_dt, end_dt):
    # Define the list of stocks
    stocks = ["AAPL", "MSFT"]
    # Define the time window for trend calculation
    window = 30  
    # Function to calculate the slope of the closing price trend
    # def calculate_slope(stock):
    #     try:
    #         # Fetch historical stock data
    #         df = yf.download(stock, period="5d", interval="60m", progress=False)
    #         # Ensure there are enough data points
    #         if len(df) < window:
    #             return None  # Skip stocks with insufficient data
    #         # Prepare data for linear regression (last `window` days)
    #         X = np.arange(window).reshape(-1, 1)  # Days as independent variable
    #         y = df['Close'].iloc[-window:].values.reshape(-1, 1)  # Closing prices
    #         # Fit linear regression model
    #         model = LinearRegression().fit(X, y)
    #         slope = model.coef_[0][0]  # Extract slope
    #         return slope
        
    #     except Exception as e:
    #         print(f"Error processing {stock}: {e}")
    #         return None
    # # Store results in a DataFrame
    # stock_slopes = [(stock, calculate_slope(stock)) for stock in stocks]
    # df = pd.DataFrame(stock_slopes, columns=["Stock", "Slope"]).dropna()  # Remove None values
    # # Filter and sort stocks
    # df_up = df[df["Slope"] &gt; 0].sort_values(by="Slope", ascending=False)  # Only positive slopes
    # df_down = df[df["Slope"] &lt; 0].sort_values(by="Slope", ascending=True)  # Only negative slopes
    # # Get top 10 uptrend stocks
    # top_10_stocks = df_up.head(1)["Stock"].tolist()
    # # Get bottom 10 downtrend stocks
    # bottom_10_stocks = df_down.head(1)["Stock"].tolist()
    # # Display results
    # print("Top 10 Trending Stocks (Uptrend):", top_10_stocks)
    # print("Bottom 10 Trending Stocks (Downtrend):", bottom_10_stocks)