from data_processing.morpho_setup.gql_queries import fetch_liquidation_data, fetch_market_data
from data_processing.morpho_setup.data_transformations import process_liquidation_data, process_market_data
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Fetch and process liquidation data
response_liquidations = fetch_liquidation_data()
df_liquidations = process_liquidation_data(response_liquidations)

# Fetch and process market data
market_response = fetch_market_data()
df_market = process_market_data(market_response)

# Define a function to plot liquidations by market using Plotly
def plot_liquidations(df):
    ending_totals_df = df.groupby('market').agg({'liquidations_total': 'last'}).reset_index()
    fig = px.bar(
        ending_totals_df, 
        x='market', 
        y='liquidations_total', 
        title='All-Time Liquidations by Market',
        labels={'liquidations_total': 'Total Liquidations (USD)'}
    )
    st.plotly_chart(fig)


# Define a function to plot borrow, supply, and utilization with Matplotlib
def plot_market_data_matplotlib(df):
    # Sort the DataFrame to group Mainnet and Base markets together
    df_sorted = df.sort_values(by='chain', ascending=False).reset_index(drop=True)

    # Set up the figure and axes for the plot
    fig, ax1 = plt.subplots(figsize=(12, 8))
    fig.suptitle('Morpho RToken Markets: Supply & Borrow Info', fontsize=16)

    # Bar plot: supplyAssetsUsd and borrowAssetsUsd by market
    width = 0.25  # Width of the bars

    # Define positions for each bar
    ind = range(len(df_sorted))  # The x locations for the groups

    # Iterate over each market and adjust opacity based on the chain
    for i in ind:
        if df_sorted['chain'][i] == 'Base':
            supply_alpha = 0.35
            borrow_alpha = 0.35
        else:
            supply_alpha = 1.0
            borrow_alpha = 1.0

        # Plot supply and borrow bars with adjusted opacity for Base markets
        ax1.bar(i, df_sorted['supplyAssetsUsd'][i], width, color='blue', alpha=supply_alpha)
        ax1.bar(i + width, df_sorted['borrowAssetsUsd'][i], width, color='red', alpha=borrow_alpha)

    # Add labels and legend for the bar plot
    ax1.set_xlabel('Market')
    ax1.set_ylabel('Assets (USD)')
    ax1.set_xticks([i + width for i in ind])
    ax1.set_xticklabels(df_sorted['marketName'], ha='right')

    # Add APY and Utilization info as text below the x-axis
    for i, market in enumerate(df_sorted['marketName']):
        supply_apy_text = f"{df_sorted['supplyApy'][i]:.2%}"
        borrow_apy_text = f"{df_sorted['borrowApy'][i]:.2%}"
        utilization_text = f"{df_sorted['utilization'][i] * 100:.2f}%"
        
        # Supply APY in blue
        ax1.text(i + width / 2, -max(df_sorted['supplyAssetsUsd']) * 0.1, supply_apy_text,
                ha='center', va='top', fontsize=10, color='blue')
        
        # Borrow APY in red
        ax1.text(i + width / 2, -max(df_sorted['supplyAssetsUsd']) * 0.15, borrow_apy_text,
                ha='center', va='top', fontsize=10, color='red')
        
        # Utilization in black
        ax1.text(i + width / 2, -max(df_sorted['supplyAssetsUsd']) * 0.2, utilization_text,
                ha='center', va='top', fontsize=10, color='black')

    # Create custom legend entries for Mainnet and Base
    mainnet_supply_patch = plt.Line2D([0], [0], color='blue', lw=4, alpha=1.0, label='Supply Assets (USD) - Mainnet')
    mainnet_borrow_patch = plt.Line2D([0], [0], color='red', lw=4, alpha=1.0, label='Borrow Assets (USD) - Mainnet')

    base_supply_patch = plt.Line2D([0], [0], color='blue', lw=4, alpha=0.35, label='Supply Assets (USD) - Base')
    base_borrow_patch = plt.Line2D([0], [0], color='red', lw=4, alpha=0.35, label='Borrow Assets (USD) - Base')

    # Add the custom legend to the plot
    ax1.legend(handles=[mainnet_supply_patch, mainnet_borrow_patch, base_supply_patch, base_borrow_patch], loc='upper left')

    # Adjust layout to make room for APY text
    plt.tight_layout(rect=[0, 0.1, 1, 0.95])

    # Display the plot in Streamlit
    st.pyplot(fig)


