"""
Modern Data Generation Tab with Enhanced UI/UX.
Professional design with custom styling and improved user experience.
"""
import streamlit as st
import pandas as pd
import zipfile
import io
from core.data_generator import DataGenerator
from core.ddl_parser import SchemaParser
from security.guardrails import (
    detect_prompt_injection,
    mask_pii
)


# ============================================================================
# MAIN RENDER FUNCTION
# ============================================================================
def render_data_generation_tab():
    """
    Main function to render the modernized Data Generation tab.
    """
      
    # Initialize session state
    _initialize_session_state()
    
    # Hero Section
    _render_hero_section()
    
    # Section 1: File Upload
    _render_file_upload_section()
    
    # Section 2: Data Generation Configuration
    if st.session_state.parsed_schema:
        _render_data_generation_section()
    
    # Section 3: Generated Data Preview
    if st.session_state.generated_tables:
        _render_data_preview_section()
    
    # Section 4: Table Modification
    if st.session_state.generated_tables:
        _render_modification_section()
    
    # Section 5: Download Options
    if st.session_state.generated_tables:
        _render_download_section()


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
def _initialize_session_state():
    """Initialize all session state variables."""
    defaults = {
        "generated_tables": {},
        "parsed_schema": None,
        "ddl_content": None,
        "modification_preview": None,
        "modification_table_name": None
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


# ============================================================================
# UI RENDERING SECTIONS
# ============================================================================
def _render_hero_section():
    """Render hero banner with title and description."""
    st.markdown("""
    <div class="hero-banner">
        <h1 class="hero-title">Synthetic data generation</h1>
        <p class="hero-subtitle">
            Turn SQL schemas into realistic relational datasets, refine them with AI, and export clean CSV files from one focused workspace.
        </p>
    </div>
    """, unsafe_allow_html=True)


def _render_file_upload_section():
    """Render the file upload section."""
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">1</span>
        <span>Upload Database Schema</span>
    </div>
    """, unsafe_allow_html=True)
    
    # st.info("Upload a SQL DDL file containing CREATE TABLE statements.")
    
    uploaded_file = st.file_uploader(
        "Choose your DDL file",
        type=["sql", "ddl", "txt"],
        help="Supported formats: .sql, .ddl, .txt",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
     if uploaded_file.size > 10 * 1024 * 1024:
        st.error(
            "File size exceeds 10MB."
        )

        st.stop()
    
    # Parse and preview schema
    if uploaded_file is not None:
        ddl_content = uploaded_file.read().decode("utf-8")

        # This prevents someone uploading a huge file.
    #     if len(ddl_content) > 100000:
    #      st.error(
    #      "DDL schema too large."
    #    )
    #     st.stop()

        st.session_state.ddl_content = ddl_content
        parse_and_preview_schema(ddl_content)
    elif st.session_state.ddl_content:
        parse_and_preview_schema(st.session_state.ddl_content)


def _render_data_generation_section():
    """Render data generation configuration section."""
    
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">2</span>
        <span>Configure Data Generation</span>
    </div>
    """, unsafe_allow_html=True)
    
    # st.info("Define the volume, tone, and constraints for your synthetic dataset.")
    
    # Main configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        instructions = st.text_area(
            "Generation instructions",
            placeholder="Example: Use realistic Indian names, dates between 2020-2024, valid email formats...",
            help="Provide specific instructions to guide AI data generation",
            height=154
        )
    
    with col2:
        num_rows = st.number_input(
            "Rows per table",
            min_value=1,
            max_value=10000,
            value=10,
            step=10,
            help="Number of rows to generate per table"
        )
        
        # Batch processing indicator
        if num_rows > 30:
            st.caption("Batch processing enabled")

        temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=0.7,
                step=0.1,
                help="**Lower** (0.0-0.5): Focused & deterministic\n\n**Higher** (0.8-2.0): Creative & diverse"
            )
            
        # Visual indicator
        if temperature < 0.5:
            st.caption("Focused mode")
        elif temperature > 1.0:
            st.caption("Creative mode")
        else:
            st.caption("Balanced mode")
    
    # Advanced Settings
    # with st.expander("Advanced AI settings", expanded=False):
    #     st.markdown("**Fine-tune AI generation parameters**")
        
    #     col_adv1, col_adv2 = st.columns(2)
        
    #     with col_adv1:
    #         temperature = st.slider(
    #             "Temperature",
    #             min_value=0.0,
    #             max_value=2.0,
    #             value=0.7,
    #             step=0.1,
    #             help="**Lower** (0.0-0.5): Focused & deterministic\n\n**Higher** (0.8-2.0): Creative & diverse"
    #         )
            
    #         # Visual indicator
    #         if temperature < 0.5:
    #             st.caption("Focused mode")
    #         elif temperature > 1.0:
    #             st.caption("Creative mode")
    #         else:
    #             st.caption("Balanced mode")
        
    #     with col_adv2:
    #         max_tokens = st.number_input(
    #             "Max output tokens",
    #             min_value=100,
    #             max_value=8192,
    #             value=8192,
    #             step=100,
    #             help="Maximum tokens for generation. Higher = more data but increased costs"
    #         )
            
    #         # Token usage indicator
    #         token_percentage = (max_tokens / 8192) * 100
    #         st.caption(f"Using {token_percentage:.0f}% token capacity")
    
    # Info for large datasets
    if num_rows > 30:
        st.info(f"Generating **{num_rows}** rows in optimized batches for reliability.")
    
    # Generate button
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("Generate synthetic data", type="primary", use_container_width=True):
            generate_data_with_progress(instructions, num_rows, temperature)


def _render_data_preview_section():
    """Render generated data preview section with metrics."""
    
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">3</span>
        <span>Generated Data Preview</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Table selector
    table_names = list(st.session_state.generated_tables.keys())
    selected_table = st.selectbox(
        "Select table to view",
        table_names,
        label_visibility="collapsed"
    )
    
    if selected_table:
        df = st.session_state.generated_tables[selected_table]
        
        # Display dataframe
        st.dataframe(df, use_container_width=True, height=400)


def _render_modification_section():
    """Render table modification section with preview."""
    
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">4</span>
        <span>Modify Table Data</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Use AI to modify existing data: add rows, update values, or transform a table.")
    
    # Table selection
    mod_table = st.selectbox(
        "Select table to modify",
        list(st.session_state.generated_tables.keys()),
        key="modify_table_select"
    )
    
    # Modification instruction
    modification_instruction = st.text_area(
        "Modification instructions",
        placeholder="Examples:\n• Add 20 more employees with senior positions\n• Increase all salaries by 15%\n• Update emails to company domain\n• Add records for Q4 2024",
        key="modify_instruction",
        height=120
    )
    
    # Action buttons
    col_mod1, col_mod2 = st.columns(2)
    
    with col_mod1:
        if st.button("Preview changes", key="preview_btn", use_container_width=True):
            preview_modification(mod_table, modification_instruction)
    
    with col_mod2:
        if st.button("Apply changes", key="modify_btn", type="primary", use_container_width=True):
            apply_modification(mod_table)
    
    # Show modification preview
    if (st.session_state.modification_preview is not None and 
        st.session_state.modification_table_name == mod_table):
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Preview of changes")
        st.warning(f"Review modified `{mod_table}` table below. Click **Apply changes** to confirm.")
        
        st.dataframe(st.session_state.modification_preview, use_container_width=True, height=350)
        
        # Preview metrics
        col_prev1, col_prev2 = st.columns(2)
        with col_prev1:
            st.info(f"Preview: **{len(st.session_state.modification_preview)}** rows")
        with col_prev2:
            original_count = len(st.session_state.generated_tables.get(mod_table, []))
            preview_count = len(st.session_state.modification_preview)
            diff = preview_count - original_count
            
            if diff > 0:
                st.success(f"**+{diff}** rows added")
            elif diff < 0:
                st.error(f"**{abs(diff)}** rows removed")
            else:
                st.info("Values modified")


def _render_download_section():
    """Render download section with export options."""

    st.markdown("""
    <div class="section-header">
        <span class="section-badge">5</span>
        <span>Download & Export</span>
    </div>
    """, unsafe_allow_html=True)
    
    # st.info("Export generated data as CSV files.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Individual table")
        selected_download_table = st.selectbox(
            "Select table",
            list(st.session_state.generated_tables.keys()),
            key="download_table_select",
            label_visibility="collapsed"
        )
        
        if selected_download_table:
            df = st.session_state.generated_tables[selected_download_table]
            csv = df.to_csv(index=False)
            
            st.download_button(
                label=f"Download `{selected_download_table}.csv`",
                data=csv,
                file_name=f"{selected_download_table}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.caption(f"{len(df)} rows x {len(df.columns)} columns")
    
    with col2:
        st.markdown("#### All tables")
        st.markdown("Get all tables in a ZIP file")
        
        if st.button("Prepare ZIP export", use_container_width=True):
            download_all_tables_zip()
        
        table_count = len(st.session_state.generated_tables)
        st.caption(f"{table_count} table(s) ready")


# ============================================================================
# BUSINESS LOGIC FUNCTIONS
# ============================================================================
def parse_and_preview_schema(ddl_content: str):
    """Parse DDL and display schema preview."""
    try:
        parser = SchemaParser()
        schema = parser.parse_ddl(ddl_content)
        if len(schema) > 7:
           st.error(
            "Maximum 7 tables supported."
           )
           return
        st.session_state.parsed_schema = schema
        
        if schema:
            st.success(f"Schema parsed successfully. Found **{len(schema)}** table(s).")

            # ====== Uncomment below code if we want to see the schema details =====
            # with st.expander("View schema details", expanded=True):
            #     for idx, (table_name, table_info) in enumerate(schema.items(), 1):
            #         st.markdown(f"**{idx}. Table: `{table_name}`**")
                    
            #         columns = table_info.get("columns", [])
            #         col_names = [col["name"] for col in columns]
                    
            #         col_schema1, col_schema2 = st.columns([2, 1])
                    
            #         with col_schema1:
            #             st.write(f"**Columns ({len(col_names)}):** {', '.join(col_names)}")
                    
            #         with col_schema2:
            #             if table_info.get("primary_keys"):
            #                 st.write(f"**PK:** {', '.join(table_info['primary_keys'])}")
                    
            #         if table_info.get("foreign_keys"):
            #             fk_info = [
            #                 f"`{fk['column']}` → `{fk['references_table']}.{fk['references_column']}`"
            #                 for fk in table_info["foreign_keys"]
            #             ]
            #             st.write(f"**FK:** {', '.join(fk_info)}")
                    
            #         if idx < len(schema):
            #             st.markdown("---")
        else:
            st.warning("No tables found in DDL. Please check your schema file.")
    
    except Exception as e:
        st.error(f"Error parsing schema: {str(e)}")


def generate_data_with_progress(instructions: str, num_rows: int, temperature: float = 0.7, max_tokens: int = 8192):
    """Generate synthetic data."""
    try:
        if not st.session_state.ddl_content:
            st.error("Please upload a DDL schema file first.")
            return
        
        with st.spinner("Generating synthetic data..."):
            generator = DataGenerator(temperature=temperature, max_tokens=max_tokens)
            if detect_prompt_injection(instructions):
             st.error(
                "Unsafe instructions detected."
             )
             return

            instructions = mask_pii(instructions)
         
            dataframes = generator.generate_data(
                ddl_content=st.session_state.ddl_content,
                instructions=instructions or "Generate realistic data",
                num_rows=num_rows,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            st.session_state.generated_tables = dataframes
            st.success(f"Successfully generated data for {len(dataframes)} table(s).")
            st.rerun()
    
    except Exception as e:
        st.error(f"Error generating data: {str(e)}")


def preview_modification(table_name: str, modification_instruction: str):
    """Generate preview of modified table data."""
    try:
        if not modification_instruction:
            st.warning("Please provide modification instructions.")
            return
        
        if table_name not in st.session_state.generated_tables:
            st.error(f"Table `{table_name}` not found.")
            return
        
        with st.spinner(f"Generating preview for `{table_name}`..."):
            current_df = st.session_state.generated_tables[table_name]
            current_data = current_df.to_dict('records')
            
            schema_info = st.session_state.parsed_schema.get(table_name, {})
            
            from llm.gemini_client import GeminiClient
            gemini_client = GeminiClient()
            modified_data = gemini_client.modify_table_data(
                table_name=table_name,
                current_data=current_data,
                modification_instruction=modification_instruction,
                schema=schema_info
            )
            
            modified_df = pd.DataFrame(modified_data)
            
            st.session_state.modification_preview = modified_df
            st.session_state.modification_table_name = table_name
            
            st.success("Preview generated. Review changes below.")
            st.rerun()
    
    except Exception as e:
        st.error(f"Error generating preview: {str(e)}")


def apply_modification(table_name: str):
    """Apply previewed modification to table."""
    try:
        if st.session_state.modification_preview is None:
            st.warning("Please generate a preview first.")
            return
        
        if st.session_state.modification_table_name != table_name:
            st.warning(f"Preview is for `{st.session_state.modification_table_name}`, not `{table_name}`.")
            return
        
        with st.spinner(f"Applying changes to `{table_name}`..."):
            st.session_state.generated_tables[table_name] = st.session_state.modification_preview.copy()
            
            from core.db import db_manager
            db_manager.insert_dataframe(
                table_name,
                st.session_state.modification_preview,
                if_exists="replace"
            )
            
            st.session_state.modification_preview = None
            st.session_state.modification_table_name = None
            
            st.success(f"Successfully modified `{table_name}`.")
            st.rerun()
    
    except Exception as e:
        st.error(f"Error applying modification: {str(e)}")


def download_all_tables_zip():
    """Create and download ZIP with all tables."""
    try:
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for table_name, df in st.session_state.generated_tables.items():
                csv_data = df.to_csv(index=False)
                zip_file.writestr(f"{table_name}.csv", csv_data)
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="Download ZIP file",
            data=zip_buffer.getvalue(),
            file_name="synthetic_data_all_tables.zip",
            mime="application/zip",
            key="download_zip_btn",
            use_container_width=True
        )
        
        st.success(f"ZIP ready with {len(st.session_state.generated_tables)} table(s).")
    
    except Exception as e:
        st.error(f"Error creating ZIP: {str(e)}")