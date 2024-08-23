
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





#Rtoken_analysis file above





import streamlit as st
#from data_processing.rtoken_safety.rtoken_analysis import styled_df
todays_date = 'Data: August 22nd'
st.markdown("# RToken Safety")
st.markdown("---")

st.sidebar.markdown("# RToken Safety")
st.sidebar.markdown("---")


image_path_1 = 'rs_collateral_check_8.22.png'
image_path_2 = 'rs_currentbasket_8.22.png'
image_path_3 = 'rs_stader_10percent.png'



# Create two columns with a 2:1 ratio
col1, col2 = st.columns([2, 1])

# Display the styled DataFrame in the left column
with col1:
    st.markdown('What portion of an RToken can we redeem?')
    st.dataframe(styled_df, use_container_width=True)

# Display the explanation in the right column
with col2:
    st.markdown("---")

    st.markdown("""
    **Legend:**
    - **0 - 1**: Bad
    - **1+**: Good
    - **2+**: Great
    - Higher: 🚀 
    """) 

if st.checkbox('Formula Details'):


    # Display the formula using LaTeX in Streamlit
    st.latex(r'''
    \text = \min \left( \frac{\text{Idle\_Lending\_Market\_Liquidity}_1}{\text{Collateral\_in\_RToken}_1}, \frac{\text{Available\_DEX\_Liquidity}_2}{\text{Collateral\_in\_RToken}_2}, \dots, \frac{\text{Available\_Liquidity}_n}{\text{Collateral\_in\_RToken}_n} \right)
    ''')

st.markdown("---")

if st.checkbox('View ETH+ Basket Sims', value=True):
    st.subheader('Collateral Liquidity on DEXs')
    st.image(image_path_1, caption=todays_date, use_column_width=True)

    st.subheader('Cuurent ETH+ Basket Liquidity')
    st.image(image_path_2, caption=todays_date, use_column_width=True)

    st.subheader('ETH+ Proposal Liquidity')    
    st.image(image_path_3, caption=todays_date, use_column_width=True)