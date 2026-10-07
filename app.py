import streamlit as st
from config.config import SUPPORTED_COINS
from backend.processing import run_pipeline
from security.inventory import get_initial_inventory

# Page Configuration
st.set_page_config(page_title="Crypto Pipeline Demo", page_icon="🪙", layout="wide")

# Custom CSS for rich visual styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .status-approved {
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .status-rejected {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Inventory
if "inventory" not in st.session_state:
    st.session_state.inventory = get_initial_inventory()

# UI Layout
st.markdown("<div class='main-header'>⚡ Crypto Transaction Pipeline</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Git Branching & Integration Practice Application</div>", unsafe_allow_html=True)

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
