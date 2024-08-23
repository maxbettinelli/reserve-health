#rtoken analysis

import pandas as pd
import streamlit as st

# Convert the string data into a pandas DataFrame
# Get the absolute path to the project root

# Construct the full path to the CSV file
csv_path = 'slippage_rtoken_check.csv'

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

# from data_processing.rtoken_safety.rtoken_analysis import rtoken_slippage, styled_legend_df

import pandas as pd
import altair as alt
st.markdown("# RToken Price Depth")
st.markdown("---")

st.sidebar.markdown("# RToken Price Depth")
st.sidebar.markdown("---")

# Display the styled DataFrame in Streamlit
# Path to the image file
image_path = 'rtoken_liquidity_aug22.png'

# Display the image in Streamlit
st.subheader("DEX Liquidity per RToken")
st.image(image_path, caption='RToken Liquidity - August 22', use_column_width=True)

# Define the highlighting function for "Difference" column
def highlight_difference(val):
    if val > 0:
        return 'background-color: rgba(0, 255, 0, 0.1)'  # Green for positive
    else:
        return 'background-color: rgba(255, 0, 0, 0.1)'  # Red for negative

# Define the highlighting function for "Last Week" and "This Week" columns
# def highlight_amount(val):
#     if val > 2500000:
#         return 'background-color: rgba(0, 255, 0, .2)'  # Green
#     if val > 2000000:
#         return 'background-color: rgba(0, 255, 0, 0.1)'  # Green
#     elif val > 1000000:
#         return 'background-color: rgba(255, 255, 0, 0.1)'  # Yellow
#     elif val > 100000:
#         return 'background-color: rgba(255, 165, 0, 0.1)'  # Orange
#     elif val > 1000 or val < 101:
#         return 'background-color: rgba(255, 0, 0, 0.1)'  # Red
#     else:
#         return 'background-color: rgba(255, 255, 0, 0.1)'  # 100k-999k


# Apply the highlighting functions
styled_df = rtoken_slippage.style.applymap(highlight_difference, subset=['Difference %']) 
#                               \.applymap(highlight_amount, subset=['Last Week', 'This Week']) \
                                 
st.subheader("Weekly Change in DEX Liquidity: \n How much can I sell in a single clip before .5% Price Impact?")
st.dataframe(styled_df, use_container_width=True)

# st.dataframe(styled_legend_df, use_container_width=True)