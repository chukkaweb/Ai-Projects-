"""
Streamlit UI layout and navigation.
"""
import streamlit as st

def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Data assistant",
        page_icon="SD",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_sidebar():
    """
    Render sidebar navigation.
    
    Returns:
        Selected tab name
    """
    st.sidebar.title("Data assistant")
    
    # Radio buttons without label and with hidden label
    tab = st.sidebar.radio(
        "nav",  # Simple key
        ["Data Generation", "Talk to your Data"],
        label_visibility="hidden"  # Completely hide the label
    )  
    return tab
