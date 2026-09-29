"""Shared modern visual theme for the Streamlit app."""

import streamlit as st


def inject_modern_theme():
    """Inject final CSS overrides after page content is rendered."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --bg: #f7f8fc;
            --bg-soft: #eef0f7;
            --surface: #ffffff;
            --surface-2: #fafbff;
            --ink: #0f172a;
            --ink-2: #1e293b;
            --muted: #64748b;
            --muted-2: #94a3b8;
            --line: #e6e8f0;
            --line-soft: #eef1f7;

            --brand: #6366f1;
            --brand-2: #8b5cf6;
            --brand-strong: #4f46e5;
            --brand-soft: #eef0ff;
            --brand-ring: rgba(99, 102, 241, 0.18);

            --success: #10b981;
            --success-soft: #ecfdf5;
            --info: #0ea5e9;
            --info-soft: #eff8ff;
            --warning: #f59e0b;
            --warning-soft: #fffbeb;
            --danger: #ef4444;
            --danger-soft: #fef2f2;

            --radius-sm: 10px;
            --radius: 14px;
            --radius-lg: 18px;

            --shadow-xs: 0 1px 2px rgba(15, 23, 42, 0.04);
            --shadow-sm: 0 2px 6px rgba(15, 23, 42, 0.05);
            --shadow: 0 8px 24px rgba(15, 23, 42, 0.06), 0 2px 6px rgba(15, 23, 42, 0.04);
            --shadow-lg: 0 18px 40px rgba(15, 23, 42, 0.10), 0 6px 14px rgba(15, 23, 42, 0.05);
        }

        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(1200px 600px at 80% -10%, rgba(139, 92, 246, 0.08), transparent 60%),
                radial-gradient(900px 500px at -10% 10%, rgba(99, 102, 241, 0.08), transparent 60%),
                var(--bg) !important;
            color: var(--ink) !important;
            font-family: 'Inter', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        [data-testid="stHeader"] {
            background: rgba(247, 248, 252, 0.72) !important;
            border-bottom: 1px solid rgba(230, 232, 240, 0.6) !important;
            backdrop-filter: saturate(150%) blur(14px);
            -webkit-backdrop-filter: saturate(150%) blur(14px);
        }

        .main .block-container {
            max-width: 1200px !important;
            padding: 2.2rem 2.4rem 4rem !important;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--ink) !important;
            letter-spacing: -0.01em !important;
            font-weight: 700 !important;
        }
        h1 { font-weight: 800 !important; letter-spacing: -0.02em !important; }

        p, span, div, label, li {
            color: var(--ink-2) !important;
        }
        small, .stCaption { color: var(--muted) !important; }

        a, a:visited { color: var(--brand) !important; text-decoration: none !important; }
        a:hover { color: var(--brand-strong) !important; text-decoration: underline !important; }

        hr {
            margin: 1.8rem 0 !important;
            border: 0 !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--line), transparent) !important;
        }

        /* ===== Sidebar (light, modern) ===== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f6f7fc 100%) !important;
            border-right: 1px solid var(--line) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            padding: 1.4rem 1.1rem !important;
            background: transparent !important;
        }
        [data-testid="stSidebar"] h1 {
            color: var(--ink) !important;
            font-size: 1.35rem !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
            margin-bottom: 0.25rem !important;
        }
        [data-testid="stSidebar"] h3 {
            color: var(--brand) !important;
            font-size: 0.72rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.12em !important;
            margin-top: 0.3rem !important;
        }
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] li {
            color: var(--muted) !important;
        }
        [data-testid="stSidebar"] .stMarkdown p {
            color: var(--muted) !important;
            line-height: 1.55 !important;
            font-size: 0.9rem !important;
        }
        [data-testid="stSidebar"] hr {
            background: var(--line) !important;
            margin: 1.2rem 0 !important;
            height: 1px !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] {
            gap: 0.4rem !important;
            display: grid !important;
        }
        [data-testid="stSidebar"] [role="radiogroup"] > label {
            min-height: 44px !important;
            padding: 0.7rem 0.85rem !important;
            border-radius: var(--radius-sm) !important;
            border: 1px solid transparent !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            color: var(--ink-2) !important;
            font-weight: 500 !important;
            transition: background-color 160ms ease, border-color 160ms ease, transform 160ms ease !important;
        }
        [data-testid="stSidebar"] [role="radiogroup"] > label:hover {
            background: var(--brand-soft) !important;
            border-color: transparent !important;
            transform: none !important;
        }
        [data-testid="stSidebar"] [role="radiogroup"] > label[aria-checked="true"] {
            background: linear-gradient(135deg, rgba(99,102,241,0.10), rgba(139,92,246,0.10)) !important;
            border-color: rgba(99, 102, 241, 0.35) !important;
            color: var(--brand-strong) !important;
            box-shadow: inset 3px 0 0 var(--brand) !important;
        }
        [data-testid="stSidebar"] [role="radiogroup"] > label[aria-checked="true"] * {
            color: var(--brand-strong) !important;
            font-weight: 600 !important;
        }
        [data-testid="stSidebar"] [data-baseweb="radio"] {
            border: 2px solid var(--muted-2) !important;
            background: #fff !important;
        }
        [data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"] {
            border-color: var(--brand) !important;
        }
        [data-testid="stSidebar"] [data-baseweb="radio"][aria-checked="true"] > div {
            background: var(--brand) !important;
        }

        /* ===== Hero banner ===== */
        .hero-banner {
            position: relative !important;
            overflow: hidden !important;
            background:
                radial-gradient(800px 300px at 100% 0%, rgba(139, 92, 246, 0.18), transparent 60%),
                radial-gradient(700px 280px at 0% 100%, rgba(99, 102, 241, 0.16), transparent 60%),
                linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%) !important;
            border: 1px solid var(--line) !important;
            border-radius: var(--radius-lg) !important;
            box-shadow: var(--shadow) !important;
            padding: 2.4rem 2.5rem !important;
            margin: 0 0 2rem !important;
        }
        .hero-banner::before {
            content: "" !important;
            position: absolute !important;
            inset: 0 auto 0 0 !important;
            width: 4px !important;
            background: linear-gradient(180deg, var(--brand), var(--brand-2)) !important;
            border-radius: 4px 0 0 4px !important;
        }
        .hero-title {
            color: var(--ink) !important;
            font-size: clamp(2rem, 3.6vw, 2.9rem) !important;
            line-height: 1.08 !important;
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            margin: 0 !important;
            max-width: 880px !important;
            background: linear-gradient(135deg, #0f172a 0%, #4338ca 60%, #7c3aed 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        .hero-subtitle {
            color: var(--muted) !important;
            font-size: 1.05rem !important;
            line-height: 1.65 !important;
            margin: 0.9rem 0 0 !important;
            max-width: 740px !important;
            font-weight: 400 !important;
        }

        /* ===== Section header ===== */
        .section-header {
            display: flex !important;
            align-items: center !important;
            gap: 0.75rem !important;
            padding: 0 !important;
            margin: 2rem 0 1.1rem !important;
            border: 0 !important;
            color: var(--ink) !important;
            font-size: 1.18rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
        }
        .section-header span:last-child { color: var(--ink) !important; }
        .section-badge {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 30px !important;
            height: 30px !important;
            border-radius: 9px !important;
            background: linear-gradient(135deg, var(--brand), var(--brand-2)) !important;
            color: #ffffff !important;
            font-size: 0.85rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 10px var(--brand-ring) !important;
            border: 0 !important;
        }

        /* ===== Alerts ===== */
        [data-testid="stAlert"] {
            border-radius: var(--radius) !important;
            border: 1px solid var(--line) !important;
            box-shadow: var(--shadow-xs) !important;
            padding: 0.9rem 1rem !important;
        }
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] div,
        [data-testid="stAlert"] span { color: var(--ink-2) !important; }

        .stInfo, div[data-baseweb="notification"][kind="info"] {
            background: var(--info-soft) !important;
            border-color: #cfe9ff !important;
            border-left: 3px solid var(--info) !important;
        }
        .stSuccess, div[data-baseweb="notification"][kind="success"] {
            background: var(--success-soft) !important;
            border-color: #bdf0d6 !important;
            border-left: 3px solid var(--success) !important;
        }
        .stWarning, div[data-baseweb="notification"][kind="warning"] {
            background: var(--warning-soft) !important;
            border-color: #fde6a2 !important;
            border-left: 3px solid var(--warning) !important;
        }
        .stError, div[data-baseweb="notification"][kind="error"] {
            background: var(--danger-soft) !important;
            border-color: #fbcbcb !important;
            border-left: 3px solid var(--danger) !important;
        }

        /* ===== File uploader ===== */
        [data-testid="stFileUploader"] section,
        [data-testid="stFileUploadDropzone"],
        [data-testid="stFileUploaderDropzone"] {
            background: var(--surface) !important;
            border: 1.5px dashed #c7cde0 !important;
            border-radius: var(--radius) !important;
            padding: 2rem !important;
            transition: border-color 160ms ease, background-color 160ms ease !important;
            box-shadow: none !important;
        }
        [data-testid="stFileUploader"] section:hover,
        [data-testid="stFileUploadDropzone"]:hover,
        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: var(--brand) !important;
            background: var(--brand-soft) !important;
        }
        [data-testid="stFileUploader"] button,
        [data-testid="stFileUploadDropzone"] button,
        [data-testid="stFileUploaderDropzone"] button {
            background: linear-gradient(135deg, var(--brand), var(--brand-2)) !important;
            color: #ffffff !important;
            border: 0 !important;
            border-radius: var(--radius-sm) !important;
            box-shadow: 0 6px 14px var(--brand-ring) !important;
            font-weight: 600 !important;
            padding: 0.55rem 1.2rem !important;
        }
        [data-testid="stFileUploader"] button *,
        [data-testid="stFileUploadDropzone"] button *,
        [data-testid="stFileUploaderDropzone"] button * { color: #ffffff !important; }
        [data-testid="stFileUploader"] button:hover,
        [data-testid="stFileUploadDropzone"] button:hover,
        [data-testid="stFileUploaderDropzone"] button:hover {
            filter: brightness(1.05) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 10px 22px var(--brand-ring) !important;
        }
        [data-testid="stFileUploader"] small,
        [data-testid="stFileUploader"] p { color: var(--muted) !important; }
        [data-testid="stFileUploader"] svg,
        [data-testid="stFileUploadDropzone"] svg { color: var(--muted-2) !important; }

        /* ===== Inputs ===== */
        input, textarea,
        [data-baseweb="input"] > div,
        [data-baseweb="textarea"] textarea,
        [data-baseweb="select"] > div {
            background: var(--surface) !important;
            color: var(--ink) !important;
            border-color: var(--line) !important;
            border-radius: var(--radius-sm) !important;
            box-shadow: var(--shadow-xs) !important;
        }
        input:focus, textarea:focus,
        [data-baseweb="input"] > div:focus-within,
        [data-baseweb="textarea"] textarea:focus,
        [data-baseweb="select"] > div:focus-within {
            border-color: var(--brand) !important;
            box-shadow: 0 0 0 4px var(--brand-ring) !important;
        }
        ::placeholder { color: var(--muted-2) !important; opacity: 1 !important; }

        /* ===== Buttons ===== */
        .stButton > button,
        button[kind="secondary"] {
            border-radius: var(--radius-sm) !important;
            min-height: 42px !important;
            border: 1px solid #d6dbe8 !important;
            background: var(--surface) !important;
            color: var(--ink) !important;
            box-shadow: var(--shadow-sm) !important;
            font-weight: 600 !important;
            letter-spacing: 0 !important;
            padding: 0.5rem 1.2rem !important;
            transition: background-color 160ms ease, border-color 160ms ease, transform 160ms ease, box-shadow 160ms ease, color 160ms ease !important;
        }
        .stButton > button *,
        button[kind="secondary"] * { color: var(--ink) !important; }

        .stButton > button:hover,
        button[kind="secondary"]:hover {
            border-color: var(--brand) !important;
            background: var(--brand-soft) !important;
            color: var(--brand-strong) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 16px var(--brand-ring) !important;
        }
        .stButton > button:hover *,
        button[kind="secondary"]:hover * { color: var(--brand-strong) !important; }

        .stButton > button[kind="primary"],
        button[kind="primary"] {
            background: linear-gradient(135deg, var(--brand) 0%, var(--brand-2) 100%) !important;
            color: #ffffff !important;
            border: 0 !important;
            box-shadow: 0 8px 18px var(--brand-ring) !important;
        }
        .stButton > button[kind="primary"]:hover,
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, var(--brand-strong) 0%, #7c3aed 100%) !important;
            filter: brightness(1.04) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 12px 26px var(--brand-ring) !important;
            color: #ffffff !important;
            border: 0 !important;
        }
        .stButton > button[kind="primary"] *,
        button[kind="primary"] *,
        .stButton > button[kind="primary"]:hover *,
        button[kind="primary"]:hover * { color: #ffffff !important; }

        /* Download button — keep emerald gradient on hover too */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #059669, #10b981) !important;
            color: #ffffff !important;
            border: 0 !important;
            border-radius: var(--radius-sm) !important;
            min-height: 42px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.2rem !important;
            box-shadow: 0 8px 18px rgba(16, 185, 129, 0.22) !important;
            transition: background-color 160ms ease, transform 160ms ease, box-shadow 160ms ease !important;
        }
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #047857, #059669) !important;
            filter: brightness(1.04) !important;
            transform: translateY(-1px) !important;
            color: #ffffff !important;
            border: 0 !important;
            box-shadow: 0 12px 26px rgba(16, 185, 129, 0.30) !important;
        }
        .stDownloadButton > button *,
        .stDownloadButton > button:hover * { color: #ffffff !important; }

        /* Inline `code` inside any button: transparent chip so text stays readable on colored buttons */
        .stButton > button code,
        .stDownloadButton > button code,
        button[kind="primary"] code,
        button[kind="secondary"] code {
            background: rgba(255, 255, 255, 0.18) !important;
            color: inherit !important;
            border: 1px solid rgba(255, 255, 255, 0.28) !important;
            padding: 0.05rem 0.35rem !important;
        }
        .stButton > button:not([kind="primary"]) code,
        button[kind="secondary"] code {
            background: var(--brand-soft) !important;
            color: var(--brand-strong) !important;
            border: 1px solid #dfe2ff !important;
        }

        /* ===== Expanders ===== */
        [data-testid="stExpander"] {
            border: 1px solid var(--line) !important;
            border-radius: var(--radius) !important;
            background: var(--surface) !important;
            box-shadow: var(--shadow-xs) !important;
            overflow: hidden !important;
        }
        .streamlit-expanderHeader,
        [data-testid="stExpander"] summary {
            background: var(--surface) !important;
            color: var(--ink) !important;
            border: 0 !important;
            border-radius: 0 !important;
            font-weight: 600 !important;
            padding: 0.85rem 1.1rem !important;
        }
        .streamlit-expanderHeader:hover,
        [data-testid="stExpander"] summary:hover {
            background: var(--surface-2) !important;
        }
        [data-testid="stExpanderDetails"] {
            background: var(--surface) !important;
            border-top: 1px solid var(--line-soft) !important;
            padding: 1rem 1.1rem !important;
        }

        /* ===== Tables / dataframes ===== */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--line) !important;
            border-radius: var(--radius) !important;
            overflow: hidden !important;
            box-shadow: var(--shadow) !important;
            background: var(--surface) !important;
        }
        [data-testid="stDataFrame"] * { letter-spacing: 0 !important; }
        table, .dataframe { background: var(--surface) !important; }
        thead, th {
            background: var(--bg-soft) !important;
            color: var(--ink) !important;
            border-bottom: 1px solid var(--line) !important;
            font-weight: 600 !important;
        }
        tbody, td {
            background: var(--surface) !important;
            color: var(--ink-2) !important;
            border-color: var(--line-soft) !important;
        }
        tr:hover td { background: var(--surface-2) !important; }

        /* ===== Code ===== */
        pre, code {
            background: #0f172a !important;
            color: #e2e8f0 !important;
            border-radius: var(--radius-sm) !important;
            border: 1px solid #1e293b !important;
            font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace !important;
        }
        :not(pre) > code {
            background: var(--brand-soft) !important;
            color: var(--brand-strong) !important;
            border: 1px solid #dfe2ff !important;
            padding: 0.12rem 0.4rem !important;
            font-size: 0.88em !important;
        }

        /* ===== Forms ===== */
        [data-testid="stForm"] {
            background: var(--surface) !important;
            border: 1px solid var(--line) !important;
            border-radius: var(--radius) !important;
            box-shadow: var(--shadow) !important;
            padding: 1.2rem !important;
        }

        [data-testid="column"] { background: transparent !important; }
        [data-testid="stHorizontalBlock"] { gap: 1rem !important; }

        /* ===== Chat bubbles ===== */
        .user-message,
        .assistant-message {
            border-radius: var(--radius) !important;
            box-shadow: var(--shadow-sm) !important;
            padding: 1rem 1.25rem !important;
            margin: 0.9rem 0 !important;
        }
        .user-message {
            background: linear-gradient(135deg, var(--brand) 0%, var(--brand-2) 100%) !important;
            color: #ffffff !important;
            border: 0 !important;
            border-radius: 16px 16px 4px 16px !important;
            margin-left: 18% !important;
            box-shadow: 0 10px 24px var(--brand-ring) !important;
        }
        .user-message *,
        .user-message-label,
        .user-message-text { color: #ffffff !important; }
        .user-message-label { opacity: 0.85 !important; font-weight: 600 !important; font-size: 0.72rem !important; letter-spacing: 0.04em !important; text-transform: uppercase !important; }

        .assistant-message,
        .assistant-message-label {
            background: var(--surface) !important;
            color: var(--ink) !important;
        }
        .assistant-message {
            border: 1px solid var(--line) !important;
            border-radius: 16px 16px 16px 4px !important;
            margin-right: 18% !important;
        }
        .assistant-message-label {
            color: var(--brand) !important;
            font-weight: 700 !important;
            font-size: 0.72rem !important;
            letter-spacing: 0.04em !important;
            text-transform: uppercase !important;
            margin-bottom: 0.4rem !important;
        }

        /* ===== Sliders ===== */
        [data-testid="stSlider"] [role="slider"] {
            background: var(--brand) !important;
            border: 2px solid #ffffff !important;
            box-shadow: 0 0 0 3px var(--brand-ring) !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] > div {
            background: linear-gradient(90deg, var(--brand), var(--brand-2)) !important;
        }

        /* ===== Progress ===== */
        .stProgress > div > div,
        [data-testid="stProgress"] > div > div {
            background: linear-gradient(90deg, var(--brand), var(--brand-2)) !important;
            border-radius: 999px !important;
        }
        .stProgress > div {
            background: var(--line-soft) !important;
            border-radius: 999px !important;
        }

        /* ===== Metrics ===== */
        [data-testid="stMetricValue"] {
            color: var(--ink) !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; }

        /* ===== Icons ===== */
        svg { color: var(--brand) !important; fill: currentColor !important; }
        button svg { color: currentColor !important; }
        .stSuccess svg { color: var(--success) !important; }
        .stError svg { color: var(--danger) !important; }
        .stWarning svg { color: var(--warning) !important; }
        .stInfo svg { color: var(--info) !important; }

        /* ===== Scrollbars ===== */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-track { background: transparent !important; }
        ::-webkit-scrollbar-thumb {
            background: #cbd0de !important;
            border-radius: 999px;
            border: 2px solid transparent;
            background-clip: padding-box;
        }
        ::-webkit-scrollbar-thumb:hover { background: #a8aec3 !important; background-clip: padding-box; }

        /* ===== Misc ===== */
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 4px !important;
            background: var(--bg-soft) !important;
            padding: 6px !important;
            border-radius: var(--radius) !important;
        }
        [data-testid="stTabs"] [data-baseweb="tab"] {
            border-radius: var(--radius-sm) !important;
            color: var(--muted) !important;
            font-weight: 600 !important;
        }
        [data-testid="stTabs"] [aria-selected="true"] {
            background: var(--surface) !important;
            color: var(--brand-strong) !important;
            box-shadow: var(--shadow-xs) !important;
        }

        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input {
            border-radius: var(--radius) !important;
            background: var(--surface) !important;
        }

        @media (max-width: 768px) {
            .main .block-container { padding: 1.3rem 1rem 3rem !important; }
            .hero-banner { padding: 1.6rem 1.3rem !important; }
            .hero-title { font-size: 1.9rem !important; }
            .user-message { margin-left: 6% !important; }
            .assistant-message { margin-right: 6% !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )