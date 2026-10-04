import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# 1. Page Configuration
st.set_page_config(
    page_title="Executive Churn Dashboard", 
    page_icon="⚡", 
    layout="wide"
)

# Custom Styling for Professional Look
st.markdown("""
    <style>
    .metric-card {
        background-color: #1e222d;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00adb5;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Database Connection
@st.cache_data
def load_data():
    engine = create_engine('postgresql://postgres@localhost:5432/ecommerce_db')
    return pd.read_sql("SELECT * FROM customer_churn_predictions", engine)

df = load_data()

# 3. Sidebar Filtering & Options
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("Filter predictions & analyze churn segments.")

risk_filter = st.sidebar.multiselect(
    "Select Churn Status:",
    options=df['Is_Churned'].unique(),
    default=df['Is_Churned'].unique(),
    format_func=lambda x: "Churned" if x == 1 else "Retained"
)

filtered_df = df[df['Is_Churned'].isin(risk_filter)]

# 4. Header Section
st.title("⚡ E-Commerce Customer Churn & RFM Analytics")
st.caption("Real-Time Prediction Pipeline connected directly to PostgreSQL database")

st.markdown("---")

# 5. KPI Metrics Cards
col1, col2, col3, col4 = st.columns(4)

total_cust = len(filtered_df)
churned_cust = filtered_df['Is_Churned'].sum() if 'Is_Churned' in filtered_df.columns else 0
retained_cust = total_cust - churned_cust
churn_rate = (churned_cust / total_cust * 100) if total_cust > 0 else 0

col1.metric("Total Customers Evaluated", f"{total_cust:,}")
col2.metric("Retained Customers", f"{retained_cust:,}", delta="Safe Segment", delta_color="normal")
col3.metric("Churned Customers", f"{churned_cust:,}", delta="At-Risk Segment", delta_color="inverse")
col4.metric("Predicted Churn Rate", f"{churn_rate:.1f}%")

st.markdown("---")

# 6. Tabbed Analytics Area
tab1, tab2, tab3 = st.tabs(["📊 Visual Analytics", "⚠️ High Risk Alert", "📋 Full Dataset"])

with tab1:
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Customer Distribution Ratio")
        fig_pie = px.pie(
            filtered_df, 
            names='Is_Churned', 
            hole=0.4,
            color='Is_Churned',
            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
            title="Churned (1) vs Retained (0)"
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.subheader("RFM Scatter Analysis")
        if 'Recency' in filtered_df.columns and 'Monetary' in filtered_df.columns:
            fig_scatter = px.scatter(
                filtered_df, 
                x='Recency', 
                y='Monetary', 
                color='Is_Churned',
                size='Frequency' if 'Frequency' in filtered_df.columns else None,
                color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
                title="Recency vs Monetary (Size = Frequency)"
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.subheader("🚨 Top High-Risk Customers Requiring Re-engagement")
    if 'Is_Churned' in filtered_df.columns:
        high_risk = filtered_df[filtered_df['Is_Churned'] == 1].head(15)
        st.write("Customers with highest churn probability:")
        st.dataframe(high_risk, use_container_width=True)

with tab3:
    st.subheader("Database Table Preview")
    st.dataframe(filtered_df, use_container_width=True, height=450)


    