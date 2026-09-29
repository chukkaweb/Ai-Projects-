"""Custom CSS for light mode chat interface."""

import streamlit as st

def talk_to_data_theme():
   # Custom CSS to keep the modern, friendly design
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] input {
        background-color: #f8f9fa !important;
        color: #212529 !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #4a90e2 !important;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
    }
    div.stButton > button {
        border-radius: 12px !important;
        padding: 6px 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)