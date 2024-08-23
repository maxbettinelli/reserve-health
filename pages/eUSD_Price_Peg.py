import pandas as pd

# Convert the string data into a pandas DataFrame
csv_path = 'https://raw.githubusercontent.com/maxbettinelli/reserve-health/master/aug22_data/eusd_pricepeg.csv'
eusd_pricepeg_df = pd.read_csv(csv_path)

# # Convert the 'hour' column to datetime
eusd_pricepeg_df['hour'] = pd.to_datetime(eusd_pricepeg_df['hour'])

# # Set the 'hour' column as the index
eusd_pricepeg_df.set_index('hour', inplace=True)

# # Resample the data by month and calculate the mean for each network
monthly_avg_df = eusd_pricepeg_df.resample('M').mean()

# # Rename the columns to match the desired output
monthly_avg_df.columns = ['Mainnet', 'Base', 'Arbitrum']

# # Convert the index to month names
monthly_avg_df.index = monthly_avg_df.index.strftime('%B')
# # Display the DataFrame


# Calculate the average for each column
average_row = monthly_avg_df.mean().to_frame().T

# Rename the index of the average row to "Average"
average_row.index = ['Average']

# Append the average row to the DataFrame
monthly_avg_df_with_avg = pd.concat([monthly_avg_df, average_row])
monthly_avg_df_with_avg.index.name = "Date"

print(monthly_avg_df_with_avg)

# Above is the pricepeg file 

import streamlit as st
# from data_processing.dune_queries.eUSD_price_peg_call import eusd_price_peg_aum_query_result
# from data_processing.pricepeg_data_manipulation.data_transformation import monthly_avg_df_with_avg
import pandas as pd
import altair as alt
st.markdown("# eUSD Price Peg") 
st.markdown("---")

st.sidebar.markdown("# eUSD Price Peg")
st.sidebar.markdown("---")

# Path to your CSV file
csv_path = 'https://raw.githubusercontent.com/maxbettinelli/reserve-health/master/aug22_data/eusd_pricepeg.csv'

# Load the CSV file into a DataFrame
eusd_price_peg_aum_query_result = pd.read_csv(csv_path)

# Melt the DataFrame to a long format
df_long = eusd_price_peg_aum_query_result.melt(
    id_vars='hour', 
    value_vars=['avg_price_ethereum', 'avg_price_base', 'avg_price_arbitrum'],
    var_name='network', 
    value_name='avg_price'
)

# Rename the 'network' values for better readability
df_long['network'] = df_long['network'].replace({
    'avg_price_ethereum': 'ETH',
    'avg_price_base': 'Base',
    'avg_price_arbitrum': 'Arbitrum'
})

# Define custom colors for the networks
network_colors = alt.Scale(domain=['ETH', 'Base', 'Arbitrum'],
                            range=['#bf8700', '#0078bf', '#00af50'])  # Gold for ETH, Blue for Base, Green for Arbitrum

# Define a brush selection for the y-axis
brush = alt.selection_interval(bind='scales', encodings=['y'])

# Create Altair chart with draggable y-axis
chart = alt.Chart(df_long).mark_line().encode(
    x='hour:T',
    y=alt.Y('avg_price:Q', scale=alt.Scale(domain=[0.985, 1.015]), title='Average Price'),
    color=alt.Color('network:N', scale=network_colors, legend=alt.Legend(title="Network")),
).properties(
    width=800,
    height=400
).add_selection(
    brush  # Add the brush selection for interactive y-axis scaling
).interactive()

# Center the chart using Streamlit's built-in layout options
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.altair_chart(chart)
st.markdown("</div>", unsafe_allow_html=True)


# Define a function to apply conditional formatting
def highlight_outliers(val):
    if 0.999 <= val <= 1.001:
        color = 'background-color: rgba(0, 255, 0, 0.1)'  # Green with alpha
    elif 0.998 <= val <= 1.002:
        color = 'background-color: rgba(255, 255, 0, 0.1)'  # Yellow with alpha
    elif 0.995 <= val <= 1.005:
        color = 'background-color: rgba(255, 165, 0, 0.1)'  # Orange with alpha
    elif 0.990 <= val <= 1.010:
        color = 'background-color: rgba(255, 0, 0, 0.1)'  # Red with alpha
    else:
        color = ''
    return color

col1, col2 = st.columns([2, 1])  # 2:1 ratio means 66% and 34%


with col1:
        
    # Apply the conditional formatting and set column widths
    styled_df = monthly_avg_df_with_avg.style.applymap(highlight_outliers)

    # Display the styled DataFrame in Streamlit
    st.dataframe(styled_df, use_container_width=True)



def highlight_legend(val):
    if val == '0.999 - 1.001':
        color = 'background-color: rgba(0, 255, 0, 0.1)'  # Green with alpha
    elif val == '0.998 - 1.002':
        color = 'background-color: rgba(255, 255, 0, 0.1)'  # Yellow with alpha
    elif val == '0.995 - 1.005':
        color = 'background-color: rgba(255, 165, 0, 0.1)'  # Orange with alpha
    elif val == '0.990 - 1.010':
        color = 'background-color: rgba(255, 0, 0, 0.1)'  # Red with alpha
    else:
        color = ''
    return color

with col2:
    legend_data = {
        "Legend": [
            "0.999 - 1.001",
            "0.998 - 1.002",
            "0.995 - 1.005",
            "0.990 - 1.010"
        ]
    }
    legend_df = pd.DataFrame(legend_data)
    legend_df = legend_df.style.applymap(highlight_legend)
    legend_df

# '''

# if st.checkbox('Live Query: 3 minute Loadtime'):
#         # Melt the DataFrame to a long format
#     df_long = eusd_price_peg_aum_query_result.melt(
#         id_vars='hour', 
#         value_vars=['avg_price_ethereum', 'avg_price_base', 'avg_price_arbitrum'],
#         var_name='network', 
#         value_name='avg_price'
#     )

#     # Rename the 'network' values for better readability
#     df_long['network'] = df_long['network'].replace({
#         'avg_price_ethereum': 'ETH',
#         'avg_price_base': 'Base',
#         'avg_price_arbitrum': 'Arbitrum'
#     })

#     # Define custom colors for the networks
#     network_colors = alt.Scale(domain=['ETH', 'Base', 'Arbitrum'],
#                             range=['#bf8700', '#0078bf', '#00af50'])  # Gold for ETH, Blue for Base, Green for Arbitrum

#     # Define a brush selection for the y-axis
#     brush = alt.selection_interval(bind='scales', encodings=['y'])

#     # Create Altair chart with draggable y-axis
#     chart = alt.Chart(df_long).mark_line().encode(
#         x='hour:T',
#         y=alt.Y('avg_price:Q', scale=alt.Scale(domain=[0.99, 1.01]), title='Average Price'),
#         color=alt.Color('network:N', scale=network_colors, legend=alt.Legend(title="Network")),
#     ).properties(
#         width=800,
#         height=400
#     ).add_selection(
#         brush  # Add the brush selection for interactive y-axis scaling
#     ).interactive()

#     # Center the chart using Streamlit's built-in layout options
#     st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
#     st.altair_chart(chart)
#     st.markdown("</div>", unsafe_allow_html=True)

#     st.dataframe(eusd_price_peg_aum_query_result)
    
# '''