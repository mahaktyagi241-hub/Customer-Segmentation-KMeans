import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
from fpdf import FPDF

# Set page config to wide layout and set title and icon
st.set_page_config(
    page_title="Customer Segmentation AI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for premium look and card container styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* Global fonts and overrides */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(26, 8, 50, 0.18) 0%, rgba(3, 6, 22, 0.18) 90%), #09090b !important;
        color: #ececec !important;
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Enforce dark text inputs, select boxes, number inputs */
    input, select, textarea {
        background-color: rgba(20, 20, 25, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* Gradient headers */
    .main-title {
        font-size: 44px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a1a1aa 50%, #71717a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        font-family: 'Outfit', sans-serif;
        letter-spacing: -2px;
    }
    
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        border-left: 4px solid #7c3aed;
        padding-left: 14px;
        margin-top: 36px;
        margin-bottom: 20px;
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.5px;
    }
    
    /* Styled container cards with Glassmorphism and Hover Animations */
    .insight-card {
        background: rgba(20, 20, 25, 0.6) !important;
        backdrop-filter: blur(12px) saturate(180%);
        -webkit-backdrop-filter: blur(12px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, box-shadow 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .insight-card:hover {
        transform: translateY(-4px) scale(1.01);
        border-color: rgba(6, 182, 212, 0.4) !important; /* cyan glow */
        box-shadow: 0 12px 30px 0 rgba(6, 182, 212, 0.2) !important;
    }
    
    .metric-value {
        font-size: 38px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #ffffff 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        font-size: 13.5px;
        font-weight: 600;
        color: #a1a1aa;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Dark theme glassmorphic prediction card styling */
    .prediction-card {
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 25px;
        backdrop-filter: blur(12px) saturate(180%);
        -webkit-backdrop-filter: blur(12px) saturate(180%);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    .segment-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 11px;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .segment-title {
        font-size: 32px;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 18px;
        letter-spacing: -0.8px;
    }
    
    .section-header {
        font-size: 16px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 8px;
        padding-bottom: 4px;
    }
    
    .section-content {
        font-size: 14.5px;
        line-height: 1.6;
        margin-bottom: 14px;
    }

    /* Sidebar custom design */
    section[data-testid="stSidebar"] {
        background-color: #030303 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    section[data-testid="stSidebar"] div[class*="stRadio"] label {
        color: #a1a1aa !important;
        font-weight: 500 !important;
        font-size: 15px !important;
        padding: 6px 12px !important;
        border-radius: 8px !important;
        transition: background-color 0.2s ease, color 0.2s ease !important;
    }
    
    section[data-testid="stSidebar"] div[class*="stRadio"] label:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        margin-bottom: 20px !important;
    }
    
    /* Sleek custom buttons styling */
    div.stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #06b6d4 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.3) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(6, 182, 212, 0.4) !important;
    }
    
    div.stButton > button:active {
        transform: translateY(0);
    }
    
    div.stDownloadButton > button {
        background-color: transparent !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: background-color 0.2s ease, border-color 0.2s ease, transform 0.1s ease !important;
    }
    
    div.stDownloadButton > button:hover {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-1px);
    }
    
    /* Hero section container */
    .hero-section {
        background: linear-gradient(135deg, rgba(21, 9, 42, 0.4) 0%, rgba(3, 10, 28, 0.4) 100%) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 20px !important;
        padding: 56px 40px;
        margin-bottom: 36px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .hero-section::before {
        content: "";
        position: absolute;
        top: -30%;
        right: -30%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.15) 0%, rgba(0,0,0,0) 70%);
        pointer-events: none;
    }
    
    .hero-section::after {
        content: "";
        position: absolute;
        bottom: -30%;
        left: -30%;
        width: 350px;
        height: 350px;
        background: radial-gradient(circle, rgba(124, 58, 237, 0.15) 0%, rgba(0,0,0,0) 70%);
        pointer-events: none;
    }
    
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #a1a1aa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 12px;
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 18px;
        color: #a1a1aa;
        max-width: 850px;
        line-height: 1.6;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load model and scaler
@st.cache_resource
def load_models():
    model_path = os.path.join("models", "kmeans_model.pkl")
    scaler_path = os.path.join("models", "scaler.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        st.error("Error: Trained model or scaler not found. Please ensure 'models/kmeans_model.pkl' and 'models/scaler.pkl' exist.")
        return None, None
        
    kmeans = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return kmeans, scaler

# Load models
kmeans, scaler = load_models()

# Helper function to load and cluster dataset
@st.cache_data
def load_data():
    if not os.path.exists("Mall_Customers.csv"):
        st.error("Error: Mall_Customers.csv not found.")
        return None
        
    df = pd.read_csv("Mall_Customers.csv")
    return df

# Load original data
raw_df = load_data()

# Helper function to generate PDF report
def create_pdf_report(age, annual_income, spending_score, cluster_num, details):
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Hex to RGB helper
    hex_color = details["color"].lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # ---------------- HEADER ----------------
    pdf.set_fill_color(31, 119, 180) # Primary Theme Color (Deep Blue)
    pdf.rect(0, 0, 210, 40, "F")
    
    pdf.set_font("helvetica", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(12)
    pdf.cell(w=0, h=10, text="CUSTOMER SEGMENTATION REPORT", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(w=0, h=5, text="Strategic Marketing & Business Intelligence Profile", new_x="LMARGIN", new_y="NEXT", align="C")
    
    pdf.set_y(48)
    
    # ---------------- CUSTOMER METRICS ----------------
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(w=0, h=10, text="1. Input Customer Profile", new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(220, 220, 220)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    # Table of metrics
    pdf.set_font("helvetica", "B", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.set_fill_color(245, 245, 245)
    
    pdf.cell(w=63, h=8, text="  Age", border=1, fill=True)
    pdf.cell(w=63, h=8, text="  Annual Income", border=1, fill=True)
    pdf.cell(w=64, h=8, text="  Spending Score (1-100)", border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(w=63, h=10, text=f"  {age} years old", border=1)
    pdf.cell(w=63, h=10, text=f"  ${annual_income:.1f}k", border=1)
    pdf.cell(w=64, h=10, text=f"  {spending_score}/100", border=1, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    
    # ---------------- SEGMENT PREDICTION ----------------
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(w=0, h=10, text="2. Segment Partition Details", new_x="LMARGIN", new_y="NEXT")
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    # Prediction header badge
    pdf.set_fill_color(r, g, b)
    pdf.rect(10, pdf.get_y(), 190, 14, "F")
    
    pdf.set_font("helvetica", "B", 13)
    pdf.set_text_color(255, 255, 255)
    pdf.set_y(pdf.get_y() + 2)
    pdf.cell(w=0, h=10, text=f"  {details['name']} (Cluster {cluster_num})", new_x="LMARGIN", new_y="NEXT", align="L")
    pdf.ln(6)
    
    # Section details
    def render_section(title, content_str):
        pdf.set_font("helvetica", "B", 11)
        pdf.set_text_color(r, g, b)
        pdf.cell(w=0, h=8, text=title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(w=0, h=5, text=content_str)
        pdf.ln(3)
        
    render_section("Business Description", details["characteristics"])
    render_section("Marketing Strategy", details["strategy"])
    render_section("Business Recommendation", details["recommendation"])
    render_section("Recommended Products", details["products"])
    
    # ---------------- FOOTER DISCLAIMER ----------------
    pdf.set_y(-25)
    pdf.set_draw_color(220, 220, 220)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    pdf.set_font("helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(w=0, h=4, text="Disclaimer: This analysis report is generated by the Customer Segmentation AI application using a pre-trained K-Means clustering algorithm. Business suggestions are automatic recommendations based on historical cohort characteristics.", align="C")
    
    return bytes(pdf.output())

# Process data if models and data loaded successfully
if kmeans is not None and scaler is not None and raw_df is not None:
    # Scale and predict clusters for dashboard
    X = raw_df[["Annual Income (k$)", "Spending Score (1-100)"]]
    X_scaled = scaler.transform(X)
    raw_df["Cluster"] = kmeans.predict(X_scaled)
    
    # Map cluster names
    cluster_names = {
        0: "Average Customers",
        1: "Premium Customers",
        2: "High Potential Customers",
        3: "Careful Customers",
        4: "Budget Customers"
    }
    raw_df["Cluster Name"] = raw_df["Cluster"].map(cluster_names)
    
    # Custom color palette for consistency across plots
    color_map = {
        "Average Customers": "#9C27B0",        # Purple
        "Premium Customers": "#2196F3",        # Blue
        "High Potential Customers": "#009688", # Teal
        "Careful Customers": "#FF9800",        # Orange
        "Budget Customers": "#E91E63"          # Pink
    }
else:
    raw_df = None

# Sidebar Navigation
st.sidebar.markdown("### 📊 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Home", "📈 Dashboard", "🔮 Predict Customer", "📖 About Project"]
)

# ----------------- HOME PAGE -----------------
if page == "🏠 Home":
    st.markdown("""<div class="hero-section">
<h1 class="hero-title">Customer Segmentation AI Portal</h1>
<p class="hero-subtitle">Leverage unsupervised machine learning to group retail customers into distinct cohorts based on purchasing patterns, enabling precise and data-driven marketing campaigns.</p>
</div>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("<div class='section-title'>Project Overview</div>", unsafe_allow_html=True)
        st.markdown("""
        Understanding customer behavior is a vital key to business growth. This project uses **Unsupervised Machine Learning (K-Means Clustering)** to group mall customers by their **Annual Income** and **Spending Score**. 
        
        Using the segmented data, marketing teams can design highly targeted promotions (e.g., VIP rewards for high-value spenders, budget deals for price-sensitive groups) instead of using a one-size-fits-all approach.
        """)
        
        st.markdown("<div class='section-title'>Technologies Used</div>", unsafe_allow_html=True)
        st.markdown("""
        - **Python 3.13 / 3.14** - Core programming environment
        - **Scikit-learn** - Model development (K-Means, StandardScaler)
        - **Pandas & NumPy** - Data engineering and statistics
        - **Plotly Express & Graph Objects** - Interactive visualizations
        - **Joblib** - Model serialization & persistence
        - **Streamlit** - Interactive dashboard development
        """)
        
    with col2:
        if raw_df is not None:
            st.markdown("<div class='section-title'>Dataset Summary</div>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='insight-card'>
                <div class='metric-value'>{len(raw_df)}</div>
                <div class='metric-label'>Total Customers Surveyed</div>
            </div>
            <div class='insight-card'>
                <div class='metric-value'>${raw_df['Annual Income (k$)'].mean():.1f}k</div>
                <div class='metric-label'>Average Annual Income</div>
            </div>
            <div class='insight-card'>
                <div class='metric-value'>{raw_df['Spending Score (1-100)'].mean():.1f}</div>
                <div class='metric-label'>Average Spending Score (1-100)</div>
            </div>
            """, unsafe_allow_html=True)

# ----------------- DASHBOARD PAGE -----------------
elif page == "📈 Dashboard":
    st.markdown("<h1 class='main-title'>Interactive Segmentation Dashboard</h1>", unsafe_allow_html=True)
    st.write("Explore the statistical distributions, demographics, and spatial partitions of the customer clusters.")
    
    if raw_df is None:
        st.warning("Please ensure the models are trained and the dataset is present.")
    else:
        # Create tabs
        tab1, tab2 = st.columns([3, 2])
        
        with tab1:
            st.markdown("<h4 style='text-align: center; color: #ffffff;'>Cluster Distribution (Income vs Spending Space)</h4>", unsafe_allow_html=True)
            
            # Interactive Scatter Plot
            fig_scatter = px.scatter(
                raw_df,
                x="Annual Income (k$)",
                y="Spending Score (1-100)",
                color="Cluster Name",
                hover_data=["Age", "CustomerID"],
                color_discrete_map=color_map,
                labels={"Cluster Name": "Customer Segment"},
                title=""
            )
            
            # Inverse scale centroids to original scale
            centroids_scaled = kmeans.cluster_centers_
            centroids_orig = scaler.inverse_transform(centroids_scaled)
            
            # Add centroids to plot
            fig_scatter.add_trace(
                go.Scatter(
                    x=centroids_orig[:, 0],
                    y=centroids_orig[:, 1],
                    mode="markers",
                    marker=dict(
                        color="red",
                        size=15,
                        symbol="x",
                        line=dict(width=2, color="white")
                    ),
                    name="Cluster Centroids"
                )
            )
            
            fig_scatter.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(t=10, b=10, l=10, r=10),
                height=500
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with tab2:
            st.markdown("<h4 style='text-align: center; color: #ffffff;'>Cluster Volume Share</h4>", unsafe_allow_html=True)
            
            # Pie Chart
            counts = raw_df["Cluster Name"].value_counts().reset_index()
            counts.columns = ["Segment", "Count"]
            
            fig_pie = px.pie(
                counts,
                values="Count",
                names="Segment",
                color="Segment",
                color_discrete_map=color_map,
                hole=0.4
            )
            fig_pie.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1
                ),
                margin=dict(t=10, b=10, l=10, r=10),
                height=450
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("<div class='section-title'>Age Demographics of Clusters</div>", unsafe_allow_html=True)
            fig_box = px.box(
                raw_df,
                x="Cluster Name",
                y="Age",
                color="Cluster Name",
                color_discrete_map=color_map,
                labels={"Cluster Name": "Segment"}
            )
            fig_box.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
        with col_right:
            st.markdown("<div class='section-title'>Total Customers per Segment</div>", unsafe_allow_html=True)
            fig_bar = px.bar(
                counts,
                x="Segment",
                y="Count",
                color="Segment",
                color_discrete_map=color_map,
                text="Count"
            )
            fig_bar.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                height=350
            )
            st.plotly_chart(fig_bar, use_container_width=True)

# ----------------- PREDICT CUSTOMER PAGE -----------------
elif page == "🔮 Predict Customer":
    st.markdown("<h1 class='main-title'>Customer Segment Predictor</h1>", unsafe_allow_html=True)
    st.write("Input a single customer's details below to predict their segment and download strategic recommendations.")
    
    if kmeans is None or scaler is None:
        st.warning("Please ensure model and scaler files are loaded.")
    else:
        # Define cluster profiles
        cluster_details = {
            0: {
                "name": "Average Customers",
                "color": "#9C27B0",
                "bg": "linear-gradient(135deg, #2b0c36 0%, #0c0211 100%)",
                "border": "#9C27B0",
                "badge": "#9C27B0",
                "text": "#f3e5f5",
                "characteristics": "Moderate income (~$55.3k), moderate spending (~49.5 score), middle-aged (~42.7 years old). Representing the stable core customer cohort.",
                "strategy": "Engage via standard loyalty programs, customer newsletters, and moderate discount incentives to maintain steady purchasing.",
                "recommendation": "Develop subscription models or points-based loyalty systems to incrementally increase transaction value.",
                "products": "Mid-range apparel, family value packs, reward card subscriptions, seasonal store promotions"
            },
            1: {
                "name": "Premium Customers",
                "color": "#2196F3",
                "bg": "linear-gradient(135deg, #052244 0%, #010a16 100%)",
                "border": "#2196F3",
                "badge": "#2196F3",
                "text": "#e3f2fd",
                "characteristics": "High income (~$86.5k), high spending (~82.1 score), young adults (~32.7 years old). Loyal brand advocates with high LTV.",
                "strategy": "Provide exclusive VIP experiences, personal concierges, early access to new lines, and premium reward tiers.",
                "recommendation": "Maximize customer lifetime value (LTV) by upselling premium products. Avoid high discounts to protect brand prestige.",
                "products": "Designer clothing, luxury accessories, personal shopper services, exclusive brand releases, high-end electronics"
            },
            2: {
                "name": "High Potential Customers",
                "color": "#009688",
                "bg": "linear-gradient(135deg, #022b25 0%, #000c0a 100%)",
                "border": "#009688",
                "badge": "#009688",
                "text": "#e0f2f1",
                "characteristics": "Low income (~$25.7k), high spending (~79.4 score), young (~25.3 years old). Trend-driven, active impulse shoppers.",
                "strategy": "Target with social media campaigns, limited-time flash sales, gamified rewards, and Buy Now Pay Later (BNPL) options.",
                "recommendation": "Drive volume sales or push lifestyle add-ons. Focus on high-margin fast fashion to capture youth spend.",
                "products": "Trendy fast-fashion, social-media popular items, flash deal bundles, cosmetic sets, casual sportswear"
            },
            3: {
                "name": "Careful Customers",
                "color": "#FF9800",
                "bg": "linear-gradient(135deg, #3d2001 0%, #160b00 100%)",
                "border": "#FF9800",
                "badge": "#FF9800",
                "text": "#fff3e0",
                "characteristics": "High income (~$88.2k), low spending (~17.1 score), middle-aged (~41.1 years old). Conservative spenders with high purchasing power.",
                "strategy": "Highlight product quality, craftsmanship, warranties, family-centric bundle packages, and value-for-money propositions.",
                "recommendation": "Deploy feedback surveys to identify hesitation. Offer risk-free trials or satisfaction-guaranteed services.",
                "products": "High-durability goods, premium home appliances, extended warranties, bundle deals, classic footwear"
            },
            4: {
                "name": "Budget Customers",
                "color": "#E91E63",
                "bg": "linear-gradient(135deg, #3b031c 0%, #150009 100%)",
                "border": "#E91E63",
                "badge": "#E91E63",
                "text": "#fce4ec",
                "characteristics": "Low income (~$26.3k), low spending (~20.9 score), older (~45.2 years old). Highly price-sensitive shoppers focused on essentials.",
                "strategy": "Promote seasonal clearance sales, high-value discount coupons, BOGO deals, and everyday low-price guarantees.",
                "recommendation": "Minimize acquisition costs. Use clearance channels to optimize inventory turnover on essential basic goods.",
                "products": "Discounted basic essentials, clearance aisle items, BOGO utility wear, bulk value groceries"
            }
        }
        
        # User input form
        col_in_1, col_in_2, col_in_3 = st.columns(3)
        
        with col_in_1:
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=35,
                step=1,
                help="Age of the customer in years (typically between 18 and 100)"
            )
            
        with col_in_2:
            annual_income = st.number_input(
                "Annual Income (k$)",
                min_value=1.0,
                max_value=250.0,
                value=60.0,
                step=1.0,
                help="Annual income of the customer in thousands of dollars (e.g. 60.0 = $60,000)"
            )
            
        with col_in_3:
            spending_score = st.number_input(
                "Spending Score (1-100)",
                min_value=1,
                max_value=100,
                value=50,
                step=1,
                help="Purchasing power/spending index score assigned by the mall system (1 = lowest, 100 = highest)"
            )
            
        if st.button("🔮 Predict Segment", use_container_width=True):
            # Format inputs as DataFrame to preserve features name warning-free
            input_df = pd.DataFrame(
                [[annual_income, spending_score]],
                columns=["Annual Income (k$)", "Spending Score (1-100)"]
            )
            
            # Apply scaling using saved scaler
            input_scaled = scaler.transform(input_df)
            
            # Predict using saved KMeans model
            pred_cluster = kmeans.predict(input_scaled)[0]
            
            # Fetch cluster details
            details = cluster_details[pred_cluster]
            
            # Store in session state
            st.session_state['prediction'] = {
                'age': age,
                'annual_income': annual_income,
                'spending_score': spending_score,
                'cluster': int(pred_cluster),
                'details': details
            }
            
        # Display prediction results if they exist in session state
        if 'prediction' in st.session_state:
            pred = st.session_state['prediction']
            age_val = pred['age']
            income_val = pred['annual_income']
            score_val = pred['spending_score']
            cluster_val = pred['cluster']
            details_val = pred['details']
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            col_res_1, col_res_2 = st.columns([5, 4])
            
            with col_res_1:
                # Beautiful Colored Result Card
                st.markdown(f"""<div class='prediction-card' style='background: {details_val["bg"]}; border: 1px solid {details_val["border"]}50; color: {details_val["text"]};'>
<div class='segment-badge' style='background-color: {details_val["badge"]}22; color: {details_val["border"]}; border: 1px solid {details_val["border"]}50;'>Cluster {cluster_val}</div>
<div class='segment-title' style='color: {details_val["border"]};'>{details_val["name"]}</div>
<div class='section-header' style='color: {details_val["border"]}; border-bottom: 1px solid {details_val["border"]}30;'>📋 Business Description</div>
<div class='section-content'>{details_val["characteristics"]}</div>
<div class='section-header' style='color: {details_val["border"]}; border-bottom: 1px solid {details_val["border"]}30;'>🎯 Marketing Strategy</div>
<div class='section-content'>{details_val["strategy"]}</div>
<div class='section-header' style='color: {details_val["border"]}; border-bottom: 1px solid {details_val["border"]}30;'>🚀 Recommended Products</div>
<div class='section-content'>{details_val["products"]}</div>
</div>""", unsafe_allow_html=True)
                
            with col_res_2:
                # Metric Cards for selected values
                st.markdown("<h4 style='color: #ffffff; margin-top: 0;'>Profile Parameters</h4>", unsafe_allow_html=True)
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Age", f"{age_val} yrs")
                with col_m2:
                    st.metric("Income", f"${income_val:.1f}k")
                with col_m3:
                    st.metric("Spending Score", f"{score_val}/100")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Download Button
                pdf_bytes = create_pdf_report(age_val, income_val, score_val, cluster_val, details_val)
                st.download_button(
                    label="📄 Download Prediction Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"customer_report_cluster_{cluster_val}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Visual Indicator of Location
                fig_loc = go.Figure()
                
                # Plot the background raw customer points (small/transparent)
                if raw_df is not None:
                    for name, color in color_map.items():
                        sub_df = raw_df[raw_df["Cluster Name"] == name]
                        fig_loc.add_trace(
                            go.Scatter(
                                x=sub_df["Annual Income (k$)"],
                                y=sub_df["Spending Score (1-100)"],
                                mode="markers",
                                marker=dict(color=color, size=6, opacity=0.3),
                                name=name,
                                showlegend=False
                            )
                        )
                
                # Plot predicted point (large/pulsing)
                fig_loc.add_trace(
                    go.Scatter(
                        x=[income_val],
                        y=[score_val],
                        mode="markers",
                        marker=dict(
                            color=details_val["color"],
                            size=18,
                            line=dict(width=3, color="white"),
                            symbol="star"
                        ),
                        name="Predicted Customer"
                    )
                )
                
                fig_loc.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    title="Customer Location in Feature Space",
                    xaxis_title="Annual Income (k$)",
                    yaxis_title="Spending Score (1-100)",
                    margin=dict(t=40, b=10, l=10, r=10),
                    height=280
                )
                st.plotly_chart(fig_loc, use_container_width=True)

# ----------------- ABOUT PAGE -----------------
elif page == "📖 About Project":
    st.markdown("<h1 class='main-title'>Theoretical Framework</h1>", unsafe_allow_html=True)
    st.write("Understand the mathematical and engineering foundations supporting this customer segmentation system.")
    
    st.markdown("<div class='section-title'>1. K-Means Clustering</div>", unsafe_allow_html=True)
    st.markdown("""
    **K-Means** is a distance-based, unsupervised machine learning algorithm. It groups data points into $K$ distinct clusters based on their feature similarity.
    
    - **How it works:**
      1. Initializes $K$ cluster centers (centroids) randomly.
      2. Assigns each customer to the nearest centroid using **Euclidean Distance**:
         $$d(p, q) = \\sqrt{\\sum_{i=1}^{n} (p_i - q_i)^2}$$
      3. Recalculates the centroids by taking the average (mean) of all points assigned to that cluster.
      4. Repeats steps 2 and 3 until the centroids no longer shift (convergence).
    """)
    
    st.markdown("<div class='section-title'>2. Feature Scaling</div>", unsafe_allow_html=True)
    st.markdown("""
    **Standardization (StandardScaler)** is crucial before running K-Means.
    
    - **Why it matters:** K-Means relies on distance calculations. If one feature has a much larger range (e.g., Annual Income ranging up to 137k) compared to another (e.g., Age ranging up to 70), the feature with the larger scale will dominate the distance calculations, skewing clusters.
    - **Formula:** It transforms features to have a mean of 0 and a standard deviation of 1:
      $$z = \\frac{x - \\mu}{\\sigma}$$
      where $\\mu$ is the mean and $\\sigma$ is the standard deviation.
    """)
    
    st.markdown("<div class='section-title'>3. Elbow Method</div>", unsafe_allow_html=True)
    st.markdown("""
    The **Within-Cluster Sum of Squares (WCSS)** measures the compactness of the clusters (the distance between points and their centroid).
    
    - **The heuristic:** As we increase $K$, WCSS will naturally decrease. The "Elbow" represents the point where adding another cluster does not give a significantly better fit, appearing as a bend in the graph. In our dataset, this bend occurred clearly at **$K = 5$**.
    """)
    
    st.markdown("<div class='section-title'>4. Silhouette Score</div>", unsafe_allow_html=True)
    st.markdown("""
    The **Silhouette Score** measures how similar a customer is to their own cluster (cohesion) compared to other clusters (separation).
    
    - **Range:** It ranges from -1 to +1, where a high value indicates that the customer is well matched to their own cluster and poorly matched to neighboring clusters. We used it alongside the Elbow method to mathematically validate that $K = 5$ represents the optimal cluster partition.
    """)
    
    st.markdown("<div class='section-title'>5. PCA (Principal Component Analysis)</div>", unsafe_allow_html=True)
    st.markdown("""
    **PCA** is a linear dimensionality reduction method.
    
    - **How it works:** It rotates the feature space to project data points along the directions of maximum variance (Principal Components). 
    - **Utility:** In high-dimensional spaces (3+ features), PCA simplifies the features to a 2D or 3D coordinate system so data scientists can visualize clusters. In this project, PCA was implemented to demonstrate how high-dimensional spaces are compressed and visualised.
    """)
