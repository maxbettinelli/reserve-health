import streamlit as st
from data_processing.rtoken_safety.rtoken_analysis import styled_df
todays_date = 'Data: August 22nd'
st.markdown("# RToken Safety")
st.markdown("---")

st.sidebar.markdown("# RToken Safety")
st.sidebar.markdown("---")


image_path_1 = 'C:\\Users\\betti\\reserve-projects\\health_metrics_v1\\aug22_data\\rs_collateral_check_8.22.png'
image_path_2 = 'C:\\Users\\betti\\reserve-projects\\health_metrics_v1\\aug22_data\\rs_currentbasket_8.22.png'
image_path_3 = 'C:\\Users\\betti\\reserve-projects\\health_metrics_v1\\aug22_data\\rs_stader_10percent.png'



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