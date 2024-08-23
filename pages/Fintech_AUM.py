import streamlit as st
from data_processing.dune_queries.fintech_aum_call import fintech_aum_query_result, ugly_cash_total, sentz_total, ugly_cash_weekly_change_total, sentz_weekly_change_total
import altair as alt

st.markdown("# FinTech AUM") 
st.markdown("---")

st.sidebar.markdown("# FinTech AUM")  
st.sidebar.markdown("---")

st.markdown("<br><br>", unsafe_allow_html=True)  # Adds two lines of space

# Create an Altair bar chart with horizontal x-axis labels
chart = alt.Chart(fintech_aum_query_result).mark_bar().encode(
    x=alt.X('wallet_group', title='FinTech Partner', axis=alt.Axis(labelAngle=0)),  # Set labelAngle to 0 for horizontal labels
    y=alt.Y('current_balance', title='eUSD Balance'),
    color='wallet_group',
    tooltip=['network', 'weekly_change'] # deleted 'wallet_group', 
).properties(
    width=600,
    height=400
)
# Assuming sentz_total, sentz_weekly_change_total, ugly_cash_total, ugly_cash_weekly_change_total are defined

# Round the totals and weekly changes to the nearest whole number
sentz_total_rounded = round(sentz_total)
sentz_weekly_change_total_rounded = round(sentz_weekly_change_total)
ugly_cash_total_rounded = round(ugly_cash_total)
ugly_cash_weekly_change_total_rounded = round(ugly_cash_weekly_change_total)

# Format the numbers with a dollar sign and commas (no decimals)
sentz_total_formatted = f"${sentz_total_rounded:,}"
sentz_weekly_change_total_formatted = f"${sentz_weekly_change_total_rounded:,}"
ugly_cash_total_formatted = f"${ugly_cash_total_rounded:,}"
ugly_cash_weekly_change_total_formatted = f"${ugly_cash_weekly_change_total_rounded:,}"

# Determine the color based on whether the weekly change is positive, negative, or zero
def determine_color(value):
    if value > 0:
        return "green"
    elif value < 0:
        return "red"
    else:
        return "white"  # Normal color for zero

sentz_color = determine_color(sentz_weekly_change_total_rounded)
ugly_cash_color = determine_color(ugly_cash_weekly_change_total_rounded)

# Create two columns
col1, col2 = st.columns(2)

# Display Sentz Holdings in the first column
with col1:
    st.markdown(f"### Sentz Balance: \n ## {sentz_total_formatted} eUSD")
    st.markdown(f'<span style="color:{sentz_color};">Weekly Change: {sentz_weekly_change_total_formatted} eUSD</span>', unsafe_allow_html=True)

# Display Ugly Cash Holdings in the second column
with col2:
    st.markdown(f"### Ugly Cash Balance: \n ## {ugly_cash_total_formatted} eUSD")
    st.markdown(f'Weekly Change: <span style="color:{ugly_cash_color};">{ugly_cash_weekly_change_total_formatted} eUSD</span>', unsafe_allow_html=True)


st.markdown("<br><br>", unsafe_allow_html=True)  # Adds two lines of space



# Display the chart in Streamlit
st.altair_chart(chart)

if st.checkbox('View detailed FinTech Data', value=True):
    fintech_aum_query_result
