import streamlit as st
from data_processing.rtoken_safety.rtoken_analysis import rtoken_slippage, styled_legend_df
import pandas as pd
import altair as alt
st.markdown("# RToken Price Depth")
st.markdown("---")

st.sidebar.markdown("# RToken Price Depth")
st.sidebar.markdown("---")

# Display the styled DataFrame in Streamlit
# Path to the image file
image_path = 'aug22_data\\rtoken_liquidity_aug22.png'

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