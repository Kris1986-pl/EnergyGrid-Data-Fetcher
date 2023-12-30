import plotly.express as px
from datetime import datetime
from fecher import DataFetcherFactory

# Example usage:
date = datetime.now()
data_fetcher_factory = DataFetcherFactory()

try:
    # Create a Day-Ahead data fetcher
    pse_5_fetcher = data_fetcher_factory.create_data_fetcher("Day-Ahead", date)
    df = pse_5_fetcher.fetch_data()
except ValueError as ve:
    # Handle other ValueErrors
    print(f"Error: {ve}")

# Create chart
fig = px.scatter(df, x="hour", y="price", title=str(date))

# Display chart
fig.show()
