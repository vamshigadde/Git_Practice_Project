import streamlit as st
from config.config import SUPPORTED_COINS
from backend.processing import run_pipeline
from security.inventory import get_initial_inventory

# Page Configuration
st.set_page_config(page_title="Crypto Pipeline Demo", page_icon="🪙", layout="wide")

# Theme state initialization (defaults to Light mode)
if "theme" not in st.session_state:
    st.session_state.theme = "light"

is_dark = st.session_state.theme == "dark"

# Dynamic CSS styling based on active theme
bg_color = "#0F172A" if is_dark else "#F8FAFC"
text_color = "#F8FAFC" if is_dark else "#0F172A"
sub_text_color = "#94A3B8" if is_dark else "#64748B"
card_bg = "#1E293B" if is_dark else "#FFFFFF"
card_border = "#334155" if is_dark else "#E2E8F0"
status_app_bg = "#064E3B" if is_dark else "#DCFCE7"
status_app_text = "#A7F3D0" if is_dark else "#166534"
status_app_border = "#059669" if is_dark else "#BBF7D0"
status_rej_bg = "#7F1D1D" if is_dark else "#FEE2E2"
status_rej_text = "#FCA5A5" if is_dark else "#991B1B"
status_rej_border = "#DC2626" if is_dark else "#FCA5A5"

st.markdown(f"""
<style>
    /* Global Page Styling */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
        transition: background-color 0.3s ease, color 0.3s ease;
    }}
    
    .main-header {{
        font-size: 2.2rem;
        font-weight: 700;
        color: {text_color};
        margin-bottom: 0.2rem;
    }}
    
    .sub-header {{
        font-size: 1rem;
        color: {sub_text_color};
        margin-bottom: 1.5rem;
    }}
    
    /* Metrics Card Styling */
    .metric-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }}

    [data-testid="stMetric"] {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 10px !important;
        padding: 0.85rem 1rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, {"0.2" if is_dark else "0.04"}) !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: {text_color} !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {sub_text_color} !important;
    }}
    
    /* Form Container */
    [data-testid="stForm"] {{
        background-color: {card_bg} !important;
        border: 1px solid {card_border} !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, {"0.3" if is_dark else "0.05"}) !important;
    }}

    /* Form Inputs Styling */
    [data-baseweb="input"], [data-baseweb="select"] {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
    }}
    
    /* Status Badges */
    .status-approved {{
        background-color: {status_app_bg};
        color: {status_app_text};
        border: 1px solid {status_app_border};
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }}
    
    .status-rejected {{
        background-color: {status_rej_bg};
        color: {status_rej_text};
        border: 1px solid {status_rej_border};
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }}
    
    /* Dynamic Headers and Text Colors */
    h1, h2, h3, h4, h5, h6, label, p, span {{
        color: {text_color} !important;
    }}
    
    hr {{
        border-color: {card_border} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Inventory
if "inventory" not in st.session_state:
    st.session_state.inventory = get_initial_inventory()

# UI Layout Header with Top-Right Mode Selector Button
col_header, col_theme = st.columns([3.5, 1.2])

with col_header:
    st.markdown("<div class='main-header'>⚡ Crypto Transaction Pipeline</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Git Branching & Integration Practice Application</div>", unsafe_allow_html=True)

with col_theme:
    st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
    mode_label = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
    if st.button(mode_label, key="theme_toggle_btn", use_container_width=True, help="Click to switch between Light and Dark theme"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

col_input, col_output = st.columns([1, 1.2])

with col_input:
    st.subheader("📥 Transaction Entry")
    with st.form("tx_form"):
        coin = st.selectbox("Select Asset / Coin", options=SUPPORTED_COINS, index=0)
        quantity = st.number_input("Quantity", min_value=0.0, value=2.0, step=0.1)
        price = st.number_input("Unit Price ($)", min_value=0.0, value=60000.0, step=100.0)
        side = st.radio("Transaction Side", options=["BUY", "SELL"], horizontal=True)
        
        submitted = st.form_submit_button("Process Transaction", use_container_width=True)

with col_output:
    st.subheader("📊 Execution Results")
    
    if submitted:
        # Run backend processing pipeline
        result = run_pipeline(
            coin=coin,
            quantity=quantity,
            price=price,
            side=side,
            current_inventory=st.session_state.inventory
        )
        
        tx = result["transaction"]
        val = tx["validation"]

        # Update persistent session inventory if transaction approved
        if val["is_valid"]:
            st.session_state.inventory = result["new_inventory"]

        # Display Validation Badge
        st.markdown("#### Validation Status")
        if val["is_valid"]:
            st.markdown(f"<div class='status-approved'>✅ Status: {val['status']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='status-rejected'>❌ Status: {val['status']}</div>", unsafe_allow_html=True)
            for err in val["errors"]:
                st.error(f"• {err}")

        st.markdown("---")

        # Display Key Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Coin", tx["coin"])
        m2.metric("Side", tx["side"])
        m3.metric("Quantity", f"{tx['quantity']}")
        m4.metric("Total Value", tx["formatted_value"])

    else:
        st.info("Fill out the transaction form and click **Process Transaction** to see pipeline execution.")

st.markdown("---")

# Portfolio / Inventory Holdings Section
st.subheader("🔒 Security Holdings Inventory")
inv_cols = st.columns(len(st.session_state.inventory))
for i, (asset, amount) in enumerate(st.session_state.inventory.items()):
    inv_cols[i].metric(label=f"Holdings ({asset})", value=f"{amount:,.2f}")

