"""
Main Streamlit application entry point.
"""

import streamlit as st
from ui.layout import setup_page, render_sidebar
from views.data_generation import render_data_generation_tab
from views.talk_to_data import render_talk_to_data
from ui.theme import inject_modern_theme


def main():
    """Main application function."""
    setup_page()
    
    # Render sidebar and get selected tab
    selected_tab = render_sidebar()
    
    # Render selected tab content
    if selected_tab == "Data Generation":
        render_data_generation_tab()
    elif selected_tab == "Talk to your Data":
        render_talk_to_data()
    
    # Injected last so it overrides older per-tab styling.
    inject_modern_theme()


if __name__ == "__main__":
    main()
