import streamlit as st
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import your Streamlit page
import pages.RToken_Price_Depth as rtpd

# Run the Streamlit app
if __name__ == "__main__":
    rtpd.main()  # Assuming your Streamlit app logic is in a function called main()