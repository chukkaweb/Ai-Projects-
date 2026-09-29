"""
Talk to Your Data - Chat Interface
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from core.sql_generator import SQLGenerator
from core.db import db_manager
from ui.talk_to_data_theme import talk_to_data_theme
from visualization.chart_generator import ChartGenerator
from security.guardrails import (
    detect_prompt_injection,
    is_on_topic,
    mask_pii
)


def render_talk_to_data():
    """Render the Talk to Your Data chat interface."""
    talk_to_data_theme()

    # Header
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">Ask your data</h1>
        <p class="hero-subtitle">
            Convert natural language into SQL, inspect the generated query, and download result sets without leaving the workspace.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Check if database has tables
    try:
        table_names = db_manager.get_table_names()
        
        # Filter out SQLite system tables
        table_names = [t for t in table_names if not t.startswith('sqlite_')]
        
        if not table_names:
            st.warning("No tables found in database. Generate data first in the Data Generation tab.")
            
            # Option to clear database
            if st.button("Clear database", help="Remove all old tables"):
                try:
                    db_manager.truncate_all_tables()
                    st.success("Database cleared.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing database: {e}")
            return
        
        # Show available tables with row counts and clear option
        col1, col2 = st.columns([5, 1])
        with col1:
            with st.expander("Available tables", expanded=False):
                for table in table_names:
                    try:
                        row_count = len(db_manager.get_table_data(table, limit=10000))
                        st.write(f"• `{table}` ({row_count} rows)")
                    except:
                        st.write(f"• `{table}`")
        
        with col2:
            if st.button("Clear all", help="Remove all tables from database"):
                try:
                    from sqlalchemy import text
                    # Drop all tables
                    with db_manager.engine.begin() as conn:
                        for table in table_names:
                            try:
                                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
                            except:
                                pass
                    st.success("All tables cleared.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            
    except ConnectionError as e:
        st.error(f"Database connection error: {e}")
        st.info("💡 Please ensure the database is accessible. You can still use the 'Data Generation' tab.")
        return
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return
    
    # Chat history display
    st.markdown("---")
    
    # Show existing conversation
    if st.session_state.chat_history:
     for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            render_user_message(message)
        elif message["role"] == "assistant":
            render_assistant_message(message, i)
        
    
 # 1. No more st.form! Use a standard container.
    with st.container():
        # Text input tied to a key and a callback function
        st.text_input(
            "Ask a question about your data:",
            placeholder="💬 e.g., Show me all users created in the last month",
            label_visibility="collapsed",
            key="widget_user_input",
            on_change=process_chat_submission  # Runs instantly when user presses 'Enter'
        )
        
        # Action row for manual clicking
        col1, col2, col3 = st.columns([5, 1, 1])
        with col2:
            # Clicking Send triggers the exact same logic manually
            if st.button("🚀 Send", use_container_width=True, type="primary"):
                st.rerun()
        with col3:
            if st.button("🗑️ Clear chat", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state["widget_user_input"] = ""
                st.rerun()

def render_user_message(message):
    """Render a user message in chat."""
    st.markdown(f"""
    <div class="user-message">
        <div class="user-message-label">You</div>
        <div class="user-message-text">{message['content']}</div>
        <div class="message-time">{message.get('timestamp', '')}</div>
    </div>
    """, unsafe_allow_html=True)


def render_assistant_message(message, index):
    """Render an assistant message with SQL, data, and charts."""
    # Assistant header
    st.markdown(f"""
    <div class="assistant-message-label">Assistant</div>
    """, unsafe_allow_html=True)
    
    # SQL Query
    if "sql" in message and message["sql"]:
        st.markdown("**Generated SQL:**")
        st.code(message["sql"], language="sql")
    
    # Results
    if "data" in message and message["data"] is not None:
        df = message["data"]
        chart = None
        
        if not df.empty:
            # Summary
            st.markdown(f"**Results:** Found {len(df)} row(s)")
            
            # Data table
            st.dataframe(df, use_container_width=True, height=min(len(df) * 35 + 38, 400))

            # Generate chart
            chart = ChartGenerator.create_chart(df)

        if chart:
            st.subheader("Visualization")
            st.pyplot(chart)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"query_results_{index}.csv",
                mime="text/csv",
                key=f"download_{index}"
            )
        else:
            st.info("No results found for this query.")
    
    # Error message
    if "error" in message and message["error"]:
        st.error(message["error"])
    
    # Timestamp
    st.markdown(f"<div class='message-time'>{message.get('timestamp', '')}</div>", unsafe_allow_html=True)
    st.markdown("---")


def handle_user_message(user_input: str):
    """Handle user message and generate response."""

    # Guardrails  
    if detect_prompt_injection(user_input):
        st.error("Unsafe instructions detected.")
        return

    if not is_on_topic(user_input):
        st.warning("Please ask questions related to your data.")
        return

    user_input = mask_pii(user_input)
    

    # Add user message to chat
    user_message = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%I:%M %p")
    }
    st.session_state.chat_history.append(user_message)
    
    # Generate response
    try:
        with st.spinner("Thinking..."):
            sql_generator = SQLGenerator()
            sql_query, results_df = sql_generator.generate_and_execute(user_input)
            
            # Add assistant response to chat
            assistant_message = {
                "role": "assistant",
                "sql": sql_query,
                "data": results_df,
                "timestamp": datetime.now().strftime("%I:%M %p")
            }
            st.session_state.chat_history.append(assistant_message)
            
    except Exception as e:
        # Add error response
        assistant_message = {
            "role": "assistant",
            "error": str(e),
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
        st.session_state.chat_history.append(assistant_message)

def process_chat_submission():
    """Callback function that processes the input immediately before rerun."""
    # Get the input text from session state
    user_input = st.session_state.get("widget_user_input", "").strip()
    
    if user_input:
        # Process the message
        handle_user_message(user_input)
        # Clear the input box value in session state so it's empty next time
        st.session_state["widget_user_input"] = ""