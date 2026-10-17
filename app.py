import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Setlhoa Capital Allocation Platform (SCAP Tool)",
    page_icon="🪙",
    layout="wide"
)

# App Header
st.title("🪙 Setlhoa Capital Allocation Platform (SCAP Tool)")
st.caption("Operational Strategy & Financial Allocation Engine for Setlhoa Cash Solutions")
st.markdown("---")

# ---------------------------------------------------------
# 1. INPUTS: Gross Monthly Income
# ---------------------------------------------------------
col_inc, col_info = st.columns([1, 2])

with col_inc:
    gross_income = st.number_input(
        "Enter Monthly Gross Income (BWP / P):",
        min_value=0.0,
        value=10000.0,
        step=500.0,
        format="%.2f"
    )

# Determine Applicable Default Tier & Key Prefix based on Gross Income
if gross_income < 15000:
    tier_name = "Base Level Tier (Up to P10k / < P15k)"
    tier_key = "base"
    default_officer = 3500.0
    default_director_total = 1000.0
elif 15000 <= gross_income < 20000:
    tier_name = "Level 2 Tier (P15k Threshold)"
    tier_key = "l2"
    default_officer = 7000.0
    default_director_total = 2000.0
else:  # Gross Income >= P20,000
    tier_name = "Level 3 Tier (Cap Level - P20k+)"
    tier_key = "l3"
    default_officer = 10500.0
    default_director_total = 3000.0

with col_info:
    st.info(f"**Applied Operational Tier:** {tier_name}")

st.markdown("---")

# ---------------------------------------------------------
# 2. EXPENSE CHECKLIST & EDITABLE BREAKDOWN
# ---------------------------------------------------------
st.header("📋 Expense Breakdown & Monthly Checklist")
st.caption("Toggle items applicable for the month and adjust amounts if actual costs varied.")

# Create two columns for categorizing expenses
col_fixed, col_allowances = st.columns(2)

# --- Fixed Overhead Default Items ---
fixed_defaults = [
    {"id": "rent", "label": "Rent", "amount": 3500.0},
    {"id": "ads", "label": "Social Media Ads", "amount": 700.0},
    {"id": "canva", "label": "Canva Subscription", "amount": 210.0},
    {"id": "utilities", "label": "Utilities (Electricity & Water)", "amount": 300.0},
    {"id": "supplies", "label": "Office Supplies & Airtime/Internet", "amount": 200.0},
]

selected_expenses = {}

with col_fixed:
    st.subheader("1. Operating Overhead")
    for item in fixed_defaults:
        c_check, c_amount = st.columns([2, 1])
        with c_check:
            is_active = st.checkbox(item["label"], value=True, key=f"chk_{item['id']}")
        with c_amount:
            val = st.number_input(
                f"P ({item['label']})", 
                value=item["amount"], 
                step=50.0, 
                key=f"val_{item['id']}", 
                label_visibility="collapsed"
            )
        if is_active:
            selected_expenses[item["label"]] = val

# --- Allowance Default Items (Tied dynamically to tier_key) ---
with col_allowances:
    st.subheader("2. Compensation & Allowances")
    
    # Officer Allowance
    c_off_check, c_off_amount = st.columns([2, 1])
    with c_off_check:
        officer_active = st.checkbox("Officer Allowance", value=True, key=f"chk_officer_{tier_key}")
    with c_off_amount:
        officer_val = st.number_input(
            "Officer Allowance P", 
            value=default_officer, 
            step=500.0, 
            key=f"val_officer_{tier_key}", 
            label_visibility="collapsed"
        )
    if officer_active:
        selected_expenses["Officer Allowance"] = officer_val

    # Director Allowances Total
    c_dir_check, c_dir_amount = st.columns([2, 1])
    with c_dir_check:
        director_active = st.checkbox("Director Allowances Total", value=True, key=f"chk_director_{tier_key}")
    with c_dir_amount:
        director_val = st.number_input(
            "Director Allowance P", 
            value=default_director_total, 
            step=500.0, 
            key=f"val_director_{tier_key}", 
            label_visibility="collapsed"
        )
    if director_active:
        selected_expenses["Director Allowances Total"] = director_val

# Calculate Total Active OpEx
total_opex = sum(selected_expenses.values())

st.markdown("---")

# ---------------------------------------------------------
# 3. FINANCIAL SUMMARY & CALCULATIONS
# ---------------------------------------------------------
st.header("📊 Financial Summary & SCAP Distribution")

net_operating_income = gross_income - total_opex

# Metric summary cards
m1, m2, m3 = st.columns(3)
m1.metric("Gross Income", f"P{gross_income:,.2f}")
m2.metric("Total Active OpEx", f"P{total_opex:,.2f}")
m3.metric("Net Surplus / Profit", f"P{net_operating_income:,.2f}", 
          delta=f"{net_operating_income:,.2f}", 
          delta_color="normal" if net_operating_income >= 0 else "inverse")

st.markdown("#### **Income Allocation Breakdown**")

# Distribution Logic
if gross_income >= 30000 and net_operating_income >= 10000:
    st.success("🎉 **Distribution Trigger Met (Gross Income ≥ P30,000 & Net Surplus ≥ P10,000)**")
    
    dividend_pool = net_operating_income * 0.70
    retained_savings = net_operating_income * 0.30
    dir1_dividend = dividend_pool * 0.50
    dir2_dividend = dividend_pool * 0.50

    col_dist1, col_dist2 = st.columns(2)
    with col_dist1:
        st.markdown("##### **70% Dividends Pool:**")
        st.write(f"- **Director 1 (35%):** P{dir1_dividend:,.2f}")
        st.write(f"- **Director 2 (35%):** P{dir2_dividend:,.2f}")
        st.subheader(f"Total Dividends: P{dividend_pool:,.2f}")

    with col_dist2:
        st.markdown("##### **30% Reinvestment:**")
        st.write("- **Company Savings:** Retained for liquidity & expansion")
        st.subheader(f"Company Retained Capital: P{retained_savings:,.2f}")

else:
    if gross_income < 30000:
        st.info("ℹ️ **70/30 Profit Distribution Trigger Inactive:** Gross monthly income is under P30,000.")
    elif net_operating_income < 10000:
        st.warning("⚠️ **70/30 Profit Distribution Trigger Inactive:** Net surplus is less than P10,000 after OpEx.")

    st.write(f"**Retained Net Operating Surplus:** P{max(0.0, net_operating_income):,.2f}")
    st.caption("All surplus remains in company reserves until the P30,000 gross / P10,000 net surplus threshold is achieved.")
