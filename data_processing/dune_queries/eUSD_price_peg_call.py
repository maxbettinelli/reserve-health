from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
# import other needed packages
import pandas as pd
import streamlit as st

# Default value to use before the query result is fetched or if the query fails
default_eusd_price_peg_aum_query_result = pd.DataFrame({
    'timeperiod': ['day'],  # Example data
    'value': [1000]  # Replace with realistic default values
})

# Function to run the Dune query, cached to avoid redundant requests
@st.cache_data(show_spinner=True)
def fetch_eusd_price_peg_aum_query_result():
    dune = DuneClient(
        api_key="I7PEvvXEBi3IQvCWiklnIsoUO42nZGu7",
        base_url="https://api.dune.com",
        request_timeout=300
    )

    query = QueryBase(
        query_id=3950965,
        params=[
            QueryParameter.text_type(name="timeperiod", value="day"),
        ],
    )

    try:
        query_result = dune.run_query_dataframe(
            query=query,
            ping_frequency=10
        )
    except Exception as e:
        # If the query fails, return the default value
        st.error(f"Failed to fetch data: {e}")
        query_result = default_eusd_price_peg_aum_query_result
    
    return query_result

# Fetch the query result, either from cache or by querying Dune
eusd_price_peg_aum_query_result = fetch_eusd_price_peg_aum_query_result()
