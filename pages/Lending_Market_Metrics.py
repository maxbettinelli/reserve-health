

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from data_processing.morpho_setup.gql_queries import fetch_liquidation_data, fetch_market_data
from data_processing.morpho_setup.data_transformations import process_liquidation_data, process_market_data
from data_processing.morpho_setup.liquidation_info import plot_liquidations, df_liquidations, df_market

st.markdown("# Lending Market Metrics")  
st.markdown("---")

st.sidebar.markdown("# Lending Market Metrics")
st.sidebar.markdown("---")

morpho_monday = 'aug22_data\\morpho_8.18.png'
morpho_thursday = 'aug22_data\\morpho_8.22.png'

st.image(morpho_monday, caption='Morpho Markets: Aug 16th', use_column_width=True)
st.image(morpho_thursday, caption='Morpho Markets: Aug 22nd', use_column_width=True)
# Sidebar: Download market data as CSV
st.download_button(
    label="Download Morpho Size Data CSV",
    data=df_market.to_csv(index=False),
    file_name='morpho_market_data.csv',
    mime='text/csv'
)

# Morpho Liquidations Section
st.subheader("Morpho Liquidations Data")

if st.checkbox('View in depth Liquidation Information'):
    # Plot total liquidations by market
    plot_liquidations(df_liquidations)


    # Dropdown to select a market
    selected_market = st.sidebar.selectbox(
        "Select a Market to View Liquidations",
        options=df_liquidations['market'].unique()
    )

    # Filter the DataFrame based on the selected market
    filtered_df = df_liquidations[df_liquidations['market'] == selected_market]

    # Create a side-by-side layout for market selection and liquidation count


    len_liquidations = len(filtered_df)
    st.subheader(f"{len_liquidations} All-Time Liquidation(s) for {selected_market}")
    st.dataframe(filtered_df)


