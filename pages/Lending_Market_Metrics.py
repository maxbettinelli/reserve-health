# data_transformations.py
import pandas as pd

# Function to process the data and return a DataFrame
def process_liquidation_data(response):
    # Create a dictionary for the renaming
    rename_dict = {
        '0x3f4d007982a480dd99052c05d811cf6838ce61b2a2be8dc52fca107f783d1f15': 'ETH+/eUSD',
        '0x461da96754b33fec844fc5e5718bf24298a2c832d8216c5ffd17a5230548f01f': 'WBTC/eUSD',
        '0x6029eea874791e01e2f3ce361f2e08839cd18b1e26eea6243fa3e43fe8f6fa23': 'wstETH/eUSD',
        '0x9ec52d7195bafeba7137fa4d707a0f674a04a6d658c9066bcdbebc6d81eb0011': 'ETH+/WETH',
        '0xf9ed1dba3b6ba1ede10e2115a9554e9c52091c9f1b1af21f9e0fecc855ee74bf': 'bsdETH/eUSD (Base)',
        '0x3a5bdf0be8d820c1303654b078b14f8fc6d715efaeca56cec150b934bdcbff31': 'hyUSD/eUSD (Base)',
        '0xb5d424e4af49244b074790f1f2dc9c20df948ce291fc6bcc6b59149ecf91196d': 'cbETH/eUSD (Base)',
        '0xce89aeb081d719cd35cb1aafb31239c4dfd9c017b2fec26fc2e9a443461e9aea': 'wstETH/eUSD (Base)'
    }

    # Transform the response into a pandas DataFrame
    items = response['transactions']['items']
    df = pd.json_normalize(items)

    # Sort the DataFrame by blockNumber in descending order
    df = df.sort_values(by='blockNumber', ascending=True)

    # Create a new column 'total_liquidations'
    df['total_liquidations'] = df.groupby('data.market.uniqueKey')['data.seizedAssetsUsd'].cumsum()

    # Apply the renaming to the 'data.market.uniqueKey' column
    df['data.market.uniqueKey'] = df['data.market.uniqueKey'].map(rename_dict).fillna(df['data.market.uniqueKey'])

    # Select relevant columns and rename them
    df_selected = df[['blockNumber', 'type', 'user.address', 'data.market.uniqueKey', 'data.seizedAssetsUsd', 'hash', 'total_liquidations']]
    df_selected.columns = ['blockNumber', 'type', 'user', 'market', 'seizedAssetsUsd', 'hash', 'liquidations_total']

    return df_selected

# Function to get the ending totals by market
def get_ending_totals(df_selected):
    ending_totals_df = df_selected.groupby('market').agg({
        'liquidations_total': 'last'
    }).reset_index()

    # Sort the DataFrame by 'liquidations_total' in descending order
    ending_totals_df = ending_totals_df.sort_values(by='liquidations_total', ascending=False)

    return ending_totals_df

def process_market_data(response):
    target_unique_keys = {
        "0x3f4d007982a480dd99052c05d811cf6838ce61b2a2be8dc52fca107f783d1f15",
        "0x461da96754b33fec844fc5e5718bf24298a2c832d8216c5ffd17a5230548f01f",
        "0x6029eea874791e01e2f3ce361f2e08839cd18b1e26eea6243fa3e43fe8f6fa23",
        "0x9ec52d7195bafeba7137fa4d707a0f674a04a6d658c9066bcdbebc6d81eb0011",
        "0xf9ed1dba3b6ba1ede10e2115a9554e9c52091c9f1b1af21f9e0fecc855ee74bf",
        "0x3a5bdf0be8d820c1303654b078b14f8fc6d715efaeca56cec150b934bdcbff31",
        "0xb5d424e4af49244b074790f1f2dc9c20df948ce291fc6bcc6b59149ecf91196d",
        "0xce89aeb081d719cd35cb1aafb31239c4dfd9c017b2fec26fc2e9a443461e9aea"
    }

    market_chain_mapping = {
        "0x3f4d007982a480dd99052c05d811cf6838ce61b2a2be8dc52fca107f783d1f15": "Mainnet",
        "0x461da96754b33fec844fc5e5718bf24298a2c832d8216c5ffd17a5230548f01f": "Mainnet",
        "0x6029eea874791e01e2f3ce361f2e08839cd18b1e26eea6243fa3e43fe8f6fa23": "Mainnet",
        "0x9ec52d7195bafeba7137fa4d707a0f674a04a6d658c9066bcdbebc6d81eb0011": "Mainnet",
        "0xf9ed1dba3b6ba1ede10e2115a9554e9c52091c9f1b1af21f9e0fecc855ee74bf": "Base",
        "0x3a5bdf0be8d820c1303654b078b14f8fc6d715efaeca56cec150b934bdcbff31": "Base",
        "0xb5d424e4af49244b074790f1f2dc9c20df948ce291fc6bcc6b59149ecf91196d": "Base",
        "0xce89aeb081d719cd35cb1aafb31239c4dfd9c017b2fec26fc2e9a443461e9aea": "Base"
    }

    extracted_data_list = []
    for data in response['markets']['items']:
        if data["uniqueKey"] in target_unique_keys:
            market_name = f"{data['collateralAsset']['symbol']}/{data['loanAsset']['symbol']}"
            chain = market_chain_mapping[data["uniqueKey"]]

            extracted_data = {
                "marketName": market_name,
                "lltv": float(data["lltv"])/ 10 ** 18,
                "utilization": round(data["state"]["utilization"], 4),
                "supplyAssetsUsd": round(data["state"]["supplyAssetsUsd"]),
                "borrowAssetsUsd": round(data["state"]["borrowAssetsUsd"]),
                "Idle Funds": round(data["state"]["supplyAssetsUsd"] - data["state"]["borrowAssetsUsd"]),
                "supplyApy": data["state"]["supplyApy"],
                "borrowApy": data["state"]["borrowApy"],
                "chain": chain
            }
            extracted_data_list.append(extracted_data)

    df = pd.DataFrame(extracted_data_list)
    df.sort_values(by='chain', ascending=False, inplace=True)
    
    return df

# gql_queries.py
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Function to execute the GraphQL query and return the data
def fetch_liquidation_data():
    # Define the GraphQL query
    query = gql("""
    query {
      transactions(
        where: {
          marketUniqueKey_in: [
            "0x3f4d007982a480dd99052c05d811cf6838ce61b2a2be8dc52fca107f783d1f15"
            "0x461da96754b33fec844fc5e5718bf24298a2c832d8216c5ffd17a5230548f01f"
            "0x6029eea874791e01e2f3ce361f2e08839cd18b1e26eea6243fa3e43fe8f6fa23"
            "0xf9ed1dba3b6ba1ede10e2115a9554e9c52091c9f1b1af21f9e0fecc855ee74bf"
            "0x3a5bdf0be8d820c1303654b078b14f8fc6d715efaeca56cec150b934bdcbff31"
            "0xb5d424e4af49244b074790f1f2dc9c20df948ce291fc6bcc6b59149ecf91196d"
            "0xce89aeb081d719cd35cb1aafb31239c4dfd9c017b2fec26fc2e9a443461e9aea"
          ]
          type_in: [MarketLiquidation]
        }
      ) {
        items {
          blockNumber
          hash
          type
          user {
            address
          }
          data {
            ... on MarketLiquidationTransactionData {
              seizedAssets
              repaidAssets
              seizedAssetsUsd
              repaidAssetsUsd
              badDebtAssetsUsd
              liquidator
              market {
                uniqueKey
              }
            }
          }
        }
      }
    }
    """)

    # Set up the client
    transport = RequestsHTTPTransport(
        url="https://blue-api.morpho.org/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Execute the query
    response = client.execute(query)
    return response


def fetch_market_data():
    query = gql("""
    query {
      markets(first: 1000) {
        items {
          uniqueKey
          lltv
          oracleAddress
          irmAddress
          loanAsset {
            address
            symbol
            decimals
          }
          collateralAsset {
            address
            symbol
            decimals
          }
          state {
            borrowApy
            borrowAssets
            borrowAssetsUsd
            supplyApy
            supplyAssets
            supplyAssetsUsd
            fee
            utilization
          }
        }
      }
    }
    """)

    # Set up the client
    transport = RequestsHTTPTransport(
        url="https://blue-api.morpho.org/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Execute the query
    response = client.execute(query)
    return response


# Liquidation_info.py

#from data_processing.morpho_setup.gql_queries import fetch_liquidation_data, fetch_market_data
#from data_processing.morpho_setup.data_transformations import process_liquidation_data, process_market_data
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


#rtoken_analysis


import pandas as pd
import streamlit as st

# Convert the string data into a pandas DataFrame
# Get the absolute path to the project root

# Construct the full path to the CSV file
csv_path = 'data_processing\\aug22_data\\slippage_rtoken_check.csv'

# Read the CSV file
rtoken_slippage = pd.read_csv(csv_path)
rtoken_slippage = rtoken_slippage.round(2)
rtoken_slippage = rtoken_slippage.rename(columns={"Difference": "Difference %"})
rtoken_slippage[['Last Week', 'This Week', 'Difference %']] = rtoken_slippage[['Last Week', 'This Week', 'Difference %']].astype(int)

# Define a function to format numbers with a dollar sign and commas
def format_currency(val):
    return f"${val:,}"

# Apply the formatting function to the 'Last Week' and 'This Week' columns
rtoken_slippage[['Last Week', 'This Week']] = rtoken_slippage[['Last Week', 'This Week']].applymap(format_currency)

# Display the DataFrame
print(rtoken_slippage)


# Create a DataFrame with the legend values
legend_data = {
    "Legend": [
        "Better Liquidity WoW",
        "Worse Liquidity WoW",
        "$2,500,000+",
        "$2,000,000 - $2,500,000",
        "$1,000,000 - $2,000,000",
        "$100,000 - $1,000,000",
        "$0 - $100,000"

    ]
}

legend_df = pd.DataFrame(legend_data)

# Define the function to apply the background color
def apply_legend_colors(val):
    if "2,500,000+" in val:
        return 'background-color: rgba(0, 255, 0, .2)'  # Green
    if "2,000,000 - $2,500,000" in val:
        return 'background-color: rgba(0, 255, 0, 0.1)'  # Green
    elif "1,000,000 - $2,000,000" in val:
        return 'background-color: rgba(255, 255, 0, 0.1)'  # Yellow
    elif "100,000 - $1,000,000" in val:
        return 'background-color: rgba(255, 165, 0, 0.1)'  # Orange
    elif "0 - $100,000" in val:
        return 'background-color: rgba(255, 0, 0, 0.1)'  # Red
    elif "Better Liquidity WoW" in val:
        return 'background-color: rgba(0, 255, 0, 0.1)'  # Green
    elif "Worse Liquidity WoW" in val:
        return 'background-color: rgba(255, 0, 0, 0.1)'  # Red
    else:
        return ''

# Apply the color to the "Range" column in the legend DataFrame
styled_legend_df = legend_df.style.applymap(apply_legend_colors, subset=['Legend'])

#
#
#
# Rtoken Growth Score


# Create the DataFrame with the provided data
data = {
    "RToken": ["ETH+", "bsdETH", "hyUSD (Base)", "eUSD (ETH)", "USD3 (ETH)", "KNOX (Arb)"],
    "8/22": [0.56, 2.01, 3.40, 3.60, 5.86, 7.22],
    "8/16": [0.50, 1.92, 3.26, 3.08, 5.93, 6.38]
}

df = pd.DataFrame(data)

# Define a function to highlight values under 1 with red, with alpha of .1
def highlight_values(val):
    if val < 1:
        return 'background-color: rgba(255, 0, 0, 0.1)'  # Red with alpha of .1
    return ''

# Apply the highlighting to the DataFrame
styled_df = df.style.applymap(highlight_values, subset=["8/22", "8/16"])



# Three files above

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

#from data_processing.morpho_setup.gql_queries import fetch_liquidation_data, fetch_market_data
#from data_processing.morpho_setup.data_transformations import process_liquidation_data, process_market_data
#from data_processing.morpho_setup.liquidation_info import plot_liquidations, df_liquidations, df_market

st.markdown("# Lending Market Metrics")  
st.markdown("---")

st.sidebar.markdown("# Lending Market Metrics")
st.sidebar.markdown("---")

morpho_monday = 'data_processing\\aug22_data\\morpho_8.18.png'
morpho_thursday = 'data_processing\\aug22_data\\morpho_8.22.png'

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


