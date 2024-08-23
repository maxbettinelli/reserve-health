import streamlit as st

# Set up the main title for the homepage
st.title("Health Metrics Dashboard")
st.subheader('Reserve Protocol')


st.markdown("---")

# Create three columns
col1, col2, col3 = st.columns(3)

# Define a function to create a blue button-like link with high alpha (transparency)
def blue_button_link(text, url):
    return f'<a href="{url}" target="_blank" class="button-link">{text}</a>'

# Apply custom CSS for the button styling with high alpha
st.markdown("""
    <style>
    .button-link {
        display: inline-block;
        padding: 0.5em 1em;
        margin: 0.5em;
        text-decoration: none;
        color: rgba(255, 255, 255, 0.1);  /* White text with high alpha */
        background-color: rgba(0, 123, 255, 0.15);  /* Blue background with high alpha */
        border-radius: 4px;
        text-align: center;
        width: 100%;
    }
    .button-link:hover {
        background-color: rgba(0, 86, 179, 0.5);  /* Darker blue on hover with high alpha */
    }
    </style>
    """, unsafe_allow_html=True)

# Button in the first column
with col1:
    st.subheader("Reserve")
    st.markdown(blue_button_link("Register", "https://app.reserve.org/"), unsafe_allow_html=True)
    st.markdown(blue_button_link("ETH+", "https://app.reserve.org/ethereum/token/0xe72b141df173b999ae7c1adcbf60cc9833ce56a8/overview"), unsafe_allow_html=True)
    st.markdown(blue_button_link("eUSD", "https://app.reserve.org/ethereum/token/0xa0d69e286b938e21cbf7e51d71f6a4c8918f482f/overview"), unsafe_allow_html=True)


# Button in the second column
with col2:
    st.subheader("Lending")
    st.markdown(blue_button_link("Morpho Borrow", "https://app.morpho.org/borrow?network=mainnet&morphoPrice=0.65"), unsafe_allow_html=True)
    st.markdown(blue_button_link("Morpho Earn", "https://app.morpho.org/?network=mainnet&morphoPrice=0.65"), unsafe_allow_html=True)
    st.markdown(blue_button_link("Ionic", "https://app.ionic.money/market?chain=8453&pool=0"), unsafe_allow_html=True)


# Button in the third column
with col3:
    st.subheader("DEXs")
    st.markdown(blue_button_link("Curve", "https://curve.fi/#/ethereum/pools"), unsafe_allow_html=True)
    st.markdown(blue_button_link("Uniswap", "https://app.uniswap.org/pool"), unsafe_allow_html=True)
    st.markdown(blue_button_link("Aerodrome", "https://aerodrome.finance/liquidity"), unsafe_allow_html=True)
