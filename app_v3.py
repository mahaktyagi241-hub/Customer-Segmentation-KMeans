import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os
import time
from fpdf import FPDF
import streamlit.components.v1 as components
import textwrap

# Set page config to wide layout and set title and icon
st.set_page_config(
    page_title="Segment.AI // Enterprise Cohort Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to render HTML markdown without indentation issues
def st_html(html_str):
    st.markdown(textwrap.dedent(html_str), unsafe_allow_html=True)

# Inject custom CSS for premium Vercel/Stripe/Linear dark luxury aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;600;800&display=swap');

    /* Global styling overrides */
    .stApp {
        background: radial-gradient(circle at 50% -20%, rgba(168, 85, 247, 0.12) 0%, rgba(3, 7, 18, 0) 50%),
                    radial-gradient(circle at 10% 20%, rgba(6, 182, 212, 0.06) 0%, rgba(3, 7, 18, 0) 40%),
                    #030014 !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Hide standard Streamlit header and footer */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }

    /* Adjust page margins */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }

    /* Sidebar floating glass design */
    section[data-testid="stSidebar"] {
        background: rgba(8, 8, 16, 0.6) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    section[data-testid="stSidebar"] > div {
        background-color: transparent !important;
    }

    /* Input overrides to look premium and dark */
    input, select, textarea, [data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.02) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
    }
    div[data-baseweb="base-input"] {
        background-color: transparent !important;
        border: none !important;
    }
    input:focus {
        border-color: rgba(168, 85, 247, 0.5) !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.25) !important;
    }
    
    /* Number input widget wrap */
    div[data-testid="stNumberInput"] {
        background-color: transparent !important;
    }

    /* Glassmorphism Luxury Cards */
    .luxury-card {
        background: rgba(10, 10, 20, 0.45) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 24px !important;
        padding: 30px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        margin-bottom: 25px !important;
    }
    .luxury-card:hover {
        transform: translateY(-4px);
        border-color: rgba(168, 85, 247, 0.3) !important;
        box-shadow: 0 20px 50px rgba(124, 58, 237, 0.12), 0 0 30px rgba(6, 182, 212, 0.04) !important;
    }

    /* Gradient Border Card Wrapper */
    .gradient-border-card {
        position: relative;
        background: linear-gradient(135deg, #a855f7 0%, #3b82f6 50%, #06b6d4 100%);
        border-radius: 24px;
        padding: 1.5px; /* Border weight */
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6) !important;
        margin-bottom: 30px;
    }
    .gradient-border-card-inner {
        background: #050218;
        border-radius: 23.5px;
        padding: 35px;
        color: #ffffff;
    }

    /* Metric sub-cards in the AI report */
    .metric-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 18px;
        transition: all 0.3s ease;
        text-align: center;
    }
    .metric-card:hover {
        border-color: rgba(6, 182, 212, 0.25);
        background: rgba(6, 182, 212, 0.03);
    }

    /* Sidebar Primary Button (Active Item) */
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(6, 182, 212, 0.15) 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.15) !important;
        width: 100%;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    section[data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
        border-color: rgba(6, 182, 212, 0.5) !important;
        box-shadow: 0 4px 20px rgba(6, 182, 212, 0.2) !important;
    }

    /* Sidebar Secondary Button (Inactive Item) */
    section[data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #94a3b8 !important;
        border: 1px solid transparent !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        text-align: left !important;
        justify-content: flex-start !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        width: 100%;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    section[data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
        border-color: rgba(255, 255, 255, 0.05) !important;
        transform: translateX(4px);
    }

    /* Main Content Action Button (e.g. Predict button) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #a855f7 0%, #3b82f6 50%, #06b6d4 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 9999px !important; /* Pill shaped */
        padding: 16px 36px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.3), 0 0 40px rgba(6, 182, 212, 0.15) !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        letter-spacing: -0.5px !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        display: block;
        margin: 0 auto;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 30px rgba(168, 85, 247, 0.5), 0 0 50px rgba(6, 182, 212, 0.3) !important;
    }

    /* Secondary CTA / Download button styling */
    div.stButton > button[kind="secondary"], div.stDownloadButton > button {
        background: rgba(255, 255, 255, 0.02) !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 9999px !important; /* Pill shaped */
        padding: 14px 30px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    div.stButton > button[kind="secondary"]:hover, div.stDownloadButton > button:hover {
        background: rgba(255, 255, 255, 0.06) !important;
        border-color: rgba(255, 255, 255, 0.15) !important;
        transform: translateY(-2px);
    }

    /* Hero section classes */
    .hero-section {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.08) 0%, rgba(59, 130, 246, 0.05) 50%, rgba(6, 182, 212, 0.08) 100%) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 30px !important;
        padding: 80px 60px !important;
        margin-bottom: 40px !important;
        position: relative;
        overflow: hidden;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }
    
    .hero-section::after {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.12) 0%, rgba(0, 0, 0, 0) 70%);
        top: -100px;
        right: -50px;
        z-index: 0;
        pointer-events: none;
    }
    
    .hero-section::before {
        content: "";
        position: absolute;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.08) 0%, rgba(0, 0, 0, 0) 70%);
        bottom: -150px;
        left: -50px;
        z-index: 0;
        pointer-events: none;
    }
    
    .hero-tag {
        display: inline-block;
        padding: 6px 14px;
        background: linear-gradient(90deg, rgba(168, 85, 247, 0.15), rgba(6, 182, 212, 0.15));
        border: 1px solid rgba(168, 85, 247, 0.3);
        border-radius: 9999px;
        color: #c084fc;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 24px;
        text-transform: uppercase;
    }
    
    .hero-title {
        font-size: 58px !important;
        font-weight: 800 !important;
        line-height: 1.1 !important;
        background: linear-gradient(to right, #ffffff 20%, #c084fc 60%, #06b6d4 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 24px !important;
        letter-spacing: -2.5px !important;
    }
    
    .hero-subtitle {
        font-size: 18px;
        color: #94a3b8;
        max-width: 750px;
        line-height: 1.6;
        margin-bottom: 30px;
        font-weight: 400;
    }

    /* Animations styling */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .animated-card {
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    .delay-4 { animation-delay: 0.4s; }

    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    .floating-emoji {
        display: inline-block;
        animation: float 4s ease-in-out infinite;
        font-size: 2.5rem;
    }

    /* Loader Spinners */
    .spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(168, 85, 247, 0.1);
        border-radius: 50%;
        border-top-color: #a855f7;
        border-right-color: #06b6d4;
        animation: spin 1s linear infinite;
        margin: 0 auto;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.15);
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }

    /* Layout grids for responsiveness */
    .report-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-bottom: 30px;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        margin-bottom: 40px;
    }

    /* Responsive media queries */
    @media (max-width: 992px) {
        .report-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
    }
    @media (max-width: 768px) {
        .block-container {
            padding: 1.5rem !important;
        }
        .hero-title {
            font-size: 38px !important;
            letter-spacing: -1px !important;
        }
        .hero-subtitle {
            font-size: 15px !important;
        }
        .luxury-card {
            padding: 20px !important;
        }
        .feature-grid {
            grid-template-columns: 1fr !important;
        }
    }
    @media (max-width: 480px) {
        .report-grid {
            grid-template-columns: 1fr !important;
        }
    }

    /* Style st.container(border=True) to be glassmorphic and have premium SaaS styling */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(10, 10, 20, 0.4) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        padding: 24px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        margin-bottom: 20px !important;
        animation: fadeInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(168, 85, 247, 0.3) !important;
        box-shadow: 0 15px 40px rgba(124, 58, 237, 0.12), 0 0 20px rgba(6, 182, 212, 0.04) !important;
        transform: translateY(-2px);
    }

    /* Style streamlit metrics to look like SaaS analytics dashboards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        border-color: rgba(6, 182, 212, 0.2) !important;
    }
    div[data-testid="stMetricLabel"] > div {
        color: #94a3b8 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: #ffffff !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.45) !important;
    }

    /* Style streamlit progress bars to match the purple/cyan gradient */
    div[data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, #a855f7 0%, #06b6d4 100%) !important;
    }
    div[data-testid="stProgress"] > div > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 9999px !important;
    }

    /* Style the main report header h3 to look like premium gradient text */
    div[data-testid="stMarkdown"] h3 {
        background: linear-gradient(135deg, #ffffff 10%, #a855f7 50%, #06b6d4 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 34px !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
        margin-top: 0px !important;
        margin-bottom: 20px !important;
    }

    /* Section headings (h3) inside st.container(border=True) cards */
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stMarkdown"] h3 {
        background: none !important;
        -webkit-text-fill-color: initial !important;
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
        margin-top: 0px !important;
        margin-bottom: 12px !important;
    }

    /* Style the h4 header to look like a premium gradient badge */
    div[data-testid="stMarkdown"] h4 {
        display: inline-block !important;
        background: linear-gradient(90deg, rgba(168, 85, 247, 0.12), rgba(6, 182, 212, 0.12)) !important;
        border: 1px solid rgba(168, 85, 247, 0.35) !important;
        color: #c084fc !important;
        padding: 6px 16px !important;
        border-radius: 9999px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        margin-top: 0px !important;
        margin-bottom: 15px !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load model and scaler
@st.cache_resource
def load_models():
    model_path = os.path.join("models", "kmeans_model.pkl")
    scaler_path = os.path.join("models", "scaler.pkl")
    
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
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
    
    # Premium color map (matching luxury theme)
    color_map = {
        "Average Customers": "#a855f7",        # Purple
        "Premium Customers": "#3b82f6",        # Blue
        "High Potential Customers": "#06b6d4", # Cyan
        "Careful Customers": "#f59e0b",        # Amber/Orange
        "Budget Customers": "#ec4899"          # Pink
    }
else:
    raw_df = None

# Initialize session state for navigation
if 'page' not in st.session_state:
    st.session_state.page = "🏠 Home"

# Sidebar Custom Navigation Toggles (Linear-style Menu)
with st.sidebar:
    st_html("""
    <div style="text-align: center; padding: 25px 0 35px 0;">
        <h2 style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; background: linear-gradient(135deg, #a855f7 0%, #3b82f6 50%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1.5px; margin-bottom: 0px;">SEGMENT.AI</h2>
        <div style="color: #64748b; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">Cohort Analytics Engine</div>
    </div>
    """)
    
    nav_items = [
        {"icon": "🏠", "label": "Home", "full": "🏠 Home"},
        {"icon": "📈", "label": "Dashboard", "full": "📈 Dashboard"},
        {"icon": "🔮", "label": "Predict Customer", "full": "🔮 Predict Customer"},
        {"icon": "📖", "label": "About Project", "full": "📖 About Project"}
    ]
    
    for item in nav_items:
        is_active = st.session_state.page == item["full"]
        if st.button(
            f"{item['icon']}  {item['label']}", 
            key=f"nav_{item['label'].lower().replace(' ', '_')}", 
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = item["full"]
            st.rerun()

# ----------------- HOME PAGE -----------------
if st.session_state.page == "🏠 Home":
    # 2-Column Landing Hero
    hero_col1, hero_col2 = st.columns([5, 3])
    
    with hero_col1:
        st_html("""
        <div class="hero-section animated-card">
            <div class="hero-tag">Release 3.0</div>
            <h1 class="hero-title">Group, Target & Scale With Machine Learning</h1>
            <p class="hero-subtitle">
                Unlock customer lifetime value. Segment.AI identifies distinct buying cohorts within your retail demographics, driving high-impact targeted marketing campaigns.
            </p>
        </div>
        """)
        
        # Landing Page CTA Actions
        cta_col1, cta_col2, cta_col3 = st.columns([1.5, 1.5, 4])
        with cta_col1:
            if st.button("Launch Dashboard 📈", type="primary", use_container_width=True):
                st.session_state.page = "📈 Dashboard"
                st.rerun()
        with cta_col2:
            if st.button("Predict Customer 🔮", type="secondary", use_container_width=True):
                st.session_state.page = "🔮 Predict Customer"
                st.rerun()
                
    with hero_col2:
        # Lottie Animation Frame
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_fq74kvt0.json"
        lottie_frame = f"""
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <div style="display: flex; justify-content: center; align-items: center; height: 320px; overflow: hidden;">
            <lottie-player src="{lottie_url}" background="transparent" speed="1.2" style="width: 320px; height: 320px;" loop autoplay></lottie-player>
        </div>
        """
        components.html(lottie_frame, height=320)
        
    st.write(" ")
    
    # Metrics Row using native glassmorphic containers
    if raw_df is not None:
        st.write(" ")
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            with st.container(border=True):
                st.metric(label="Total Surveyed Base", value=f"{len(raw_df)} leads")
        with m_col2:
            with st.container(border=True):
                st.metric(label="Cohort Avg Income", value=f"${raw_df['Annual Income (k$)'].mean():.1f}k")
        with m_col3:
            with st.container(border=True):
                st.metric(label="Cohort Avg Spend Score", value=f"{raw_df['Spending Score (1-100)'].mean():.1f}/100")

    # Capabilities Suite (Features Grid using native containers)
    st.write(" ")
    st.markdown("### 🧠 Capabilities Suite")
    st.write("Unsupervised learning engine constructed for high-converting marketing setups.")
    st.write(" ")
    
    feat_col1, feat_col2 = st.columns(2)
    with feat_col1:
        with st.container(border=True):
            st.markdown("#### 🤖 Intelligent K-Means Model")
            st.write("Uses mathematically optimized cluster models to classify users based on spatial densities and centroids.")
        
        st.write(" ")
        
        with st.container(border=True):
            st.markdown("#### 🎯 Real-Time Cohort Predictors")
            st.write("Evaluate active retail leads instantly. Calculate exact centroid alignment scores and confidence indexes.")
            
    with feat_col2:
        with st.container(border=True):
            st.markdown("#### 📊 Interactive Data Overlays")
            st.write("Visual analytics dashboards displaying cluster ratios, box plots of age distributions, and demographics.")
            
        st.write(" ")
        
        with st.container(border=True):
            st.markdown("#### 📄 Enterprise PDF Exports")
            st.write("Export high-fidelity, customized marketing action summaries and customer report sheets automatically.")

# ----------------- DASHBOARD PAGE -----------------
elif st.session_state.page == "📈 Dashboard":
    st.markdown("### 📊 Interactive Segmentation Dashboard")
    st.write("Review statistical spreads, customer densities, and regional partitions mapped dynamically across cohorts.")
    
    if raw_df is None:
        st.markdown("""
        <div class="luxury-card animated-card" style="border-color: #f59e0b;">
            <h3 style="color: #f59e0b; margin-top: 0;">⚠️ Analytics Database Not Connected</h3>
            <p style="color: #94a3b8; margin: 0;">Please confirm that 'Mall_Customers.csv' is present in the workspace.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write(" ")
        
        # KPI Row
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        with kpi_col1:
            with st.container(border=True):
                st.metric(label="Database Volume", value=f"{len(raw_df)} leads")
        with kpi_col2:
            with st.container(border=True):
                st.metric(label="Active Cohorts", value="5 Clusters")
        with kpi_col3:
            with st.container(border=True):
                st.metric(label="Mean Income", value=f"${raw_df['Annual Income (k$)'].mean():.1f}k")
        with kpi_col4:
            with st.container(border=True):
                st.metric(label="Mean Spending Score", value=f"{raw_df['Spending Score (1-100)'].mean():.1f}/100")
                
        st.write(" ")
        
        # Dashboard Core Visual Panels (Side by Side)
        dash_col1, dash_col2 = st.columns([3, 2])
        
        with dash_col1:
            # Interactive Scatter Plot
            fig_scatter = px.scatter(
                raw_df,
                x="Annual Income (k$)",
                y="Spending Score (1-100)",
                color="Cluster Name",
                hover_data=["Age", "CustomerID"],
                color_discrete_map=color_map,
                labels={"Cluster Name": "Segment"},
                title=""
            )
            
            # Add centroids
            centroids_scaled = kmeans.cluster_centers_
            centroids_orig = scaler.inverse_transform(centroids_scaled)
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
                font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.25,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=11)
                ),
                margin=dict(t=20, b=20, l=10, r=10),
                height=520,
                xaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.05)",
                    zerolinecolor="rgba(255, 255, 255, 0.1)",
                    linecolor="rgba(255, 255, 255, 0.1)"
                ),
                yaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.05)",
                    zerolinecolor="rgba(255, 255, 255, 0.1)",
                    linecolor="rgba(255, 255, 255, 0.1)"
                )
            )
            fig_scatter.update_traces(
                marker=dict(size=9, opacity=0.75, line=dict(width=1, color="rgba(255, 255, 255, 0.15)")),
                selector=dict(mode='markers')
            )
            
            with st.container(border=True):
                st.markdown("### 📊 Cluster Density Mapping")
                st.write("Customer distribution and centroids in the Income vs Spending Score space.")
                st.plotly_chart(fig_scatter, use_container_width=True)
            
        with dash_col2:
            # Pie Chart
            counts = raw_df["Cluster Name"].value_counts().reset_index()
            counts.columns = ["Segment", "Count"]
            
            fig_pie = px.pie(
                counts,
                values="Count",
                names="Segment",
                color="Segment",
                color_discrete_map=color_map,
                hole=0.45
            )
            fig_pie.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.15,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10)
                ),
                margin=dict(t=20, b=20, l=10, r=10),
                height=470
            )
            
            with st.container(border=True):
                st.markdown("### 🍩 Volume Distribution Share")
                st.write("Relative proportion and overall volume weights of cohorts.")
                st.plotly_chart(fig_pie, use_container_width=True)
            
        st.write(" ")
        
        # Demographics and Distributions Row
        d_row_col1, d_row_col2 = st.columns(2)
        
        with d_row_col1:
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
                font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
                showlegend=False,
                margin=dict(t=20, b=20, l=10, r=10),
                xaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.05)",
                    linecolor="rgba(255, 255, 255, 0.1)"
                ),
                yaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.05)",
                    linecolor="rgba(255, 255, 255, 0.1)"
                ),
                height=380
            )
            
            with st.container(border=True):
                st.markdown("### 📈 Age Demographics Distributions")
                st.write("Demographic box ranges mapped to specific cluster tags.")
                st.plotly_chart(fig_box, use_container_width=True)
            
        with d_row_col2:
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
                font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
                showlegend=False,
                margin=dict(t=20, b=20, l=10, r=10),
                xaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.05)",
                    linecolor="rgba(255, 255, 255, 0.1)"
                ),
                yaxis=dict(
                    gridcolor="rgba(255, 255, 255, 0.05)",
                    linecolor="rgba(255, 255, 255, 0.1)"
                ),
                height=380
            )
            
            with st.container(border=True):
                st.markdown("### 📊 Direct Member Count")
                st.write("Direct member metrics count within the database.")
                st.plotly_chart(fig_bar, use_container_width=True)

# ----------------- PREDICT CUSTOMER PAGE -----------------
elif st.session_state.page == "🔮 Predict Customer":
    st.markdown("""
    <div class="animated-card" style="margin-bottom: 35px;">
        <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 38px; letter-spacing: -1.5px; margin-bottom: 8px;">Customer Segment Predictor</h1>
        <p style="color: #64748b; font-size: 15px; margin: 0;">Input age, income, and spending criteria to determine cluster metrics and export premium AI cohort reports.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if kmeans is None or scaler is None or raw_df is None:
        st.markdown("""
        <div class="luxury-card animated-card" style="border-color: #ef4444;">
            <h3 style="color: #ef4444; margin-top: 0;">⚠️ Models or Scaling Files Unreachable</h3>
            <p style="color: #94a3b8; margin: 0;">Please connect the required scikit-learn models to continue.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Cluster Profile Configurations
        cluster_details = {
            0: {
                "name": "Average Customers",
                "color": "#a855f7",
                "bg": "linear-gradient(135deg, #2b0c36 0%, #0c0211 100%)",
                "border": "#a855f7",
                "badge": "#a855f7",
                "text": "#f3e5f5",
                "characteristics": "Moderate income (~$55.3k), moderate spending (~49.5 score), middle-aged (~42.7 years old). Representing the stable core customer cohort.",
                "strategy": "Engage via standard loyalty programs, customer newsletters, and moderate discount incentives to maintain steady purchasing.",
                "recommendation": "Develop subscription models or points-based loyalty systems to incrementally increase transaction value.",
                "products": "Mid-range apparel, family value packs, reward card subscriptions, seasonal store promotions"
            },
            1: {
                "name": "Premium Customers",
                "color": "#3b82f6",
                "bg": "linear-gradient(135deg, #052244 0%, #010a16 100%)",
                "border": "#3b82f6",
                "badge": "#3b82f6",
                "text": "#e3f2fd",
                "characteristics": "High income (~$86.5k), high spending (~82.1 score), young adults (~32.7 years old). Loyal brand advocates with high LTV.",
                "strategy": "Provide exclusive VIP experiences, personal concierges, early access to new lines, and premium reward tiers.",
                "recommendation": "Maximize customer lifetime value (LTV) by upselling premium products. Avoid high discounts to protect brand prestige.",
                "products": "Designer clothing, luxury accessories, personal shopper services, exclusive brand releases, high-end electronics"
            },
            2: {
                "name": "High Potential Customers",
                "color": "#06b6d4",
                "bg": "linear-gradient(135deg, #022b25 0%, #000c0a 100%)",
                "border": "#06b6d4",
                "badge": "#06b6d4",
                "text": "#e0f2f1",
                "characteristics": "Low income (~$25.7k), high spending (~79.4 score), young (~25.3 years old). Trend-driven, active impulse shoppers.",
                "strategy": "Target with social media campaigns, limited-time flash sales, gamified rewards, and Buy Now Pay Later (BNPL) options.",
                "recommendation": "Drive volume sales or push lifestyle add-ons. Focus on high-margin fast fashion to capture youth spend.",
                "products": "Trendy fast-fashion, social-media popular items, flash deal bundles, cosmetic sets, casual sportswear"
            },
            3: {
                "name": "Careful Customers",
                "color": "#f59e0b",
                "bg": "linear-gradient(135deg, #3d2001 0%, #160b00 100%)",
                "border": "#f59e0b",
                "badge": "#f59e0b",
                "text": "#fff3e0",
                "characteristics": "High income (~$88.2k), low spending (~17.1 score), middle-aged (~41.1 years old). Conservative spenders with high purchasing power.",
                "strategy": "Highlight product quality, craftsmanship, warranties, family-centric bundle packages, and value-for-money propositions.",
                "recommendation": "Deploy feedback surveys to identify hesitation. Offer risk-free trials or satisfaction-guaranteed services.",
                "products": "High-durability goods, premium home appliances, extended warranties, bundle deals, classic footwear"
            },
            4: {
                "name": "Budget Customers",
                "color": "#ec4899",
                "bg": "linear-gradient(135deg, #3b031c 0%, #150009 100%)",
                "border": "#ec4899",
                "badge": "#ec4899",
                "text": "#fce4ec",
                "characteristics": "Low income (~$26.3k), low spending (~20.9 score), older (~45.2 years old). Highly price-sensitive shoppers focused on essentials.",
                "strategy": "Promote seasonal clearance sales, high-value discount coupons, BOGO deals, and everyday low-price guarantees.",
                "recommendation": "Minimize acquisition costs. Use clearance channels to optimize inventory turnover on essential basic goods.",
                "products": "Discounted basic essentials, clearance aisle items, BOGO utility wear, bulk value groceries"
            }
        }
        
        # User Inputs (Luxury Card)
        st.markdown("<div class='luxury-card animated-card'>", unsafe_allow_html=True)
        col_in_1, col_in_2, col_in_3 = st.columns(3)
        
        with col_in_1:
            age = st.number_input(
                "Customer Age",
                min_value=18,
                max_value=100,
                value=35,
                step=1,
                help="Age of the customer in years"
            )
        with col_in_2:
            annual_income = st.number_input(
                "Annual Income (k$)",
                min_value=1.0,
                max_value=250.0,
                value=60.0,
                step=1.0,
                help="Annual income of the customer in thousands of dollars"
            )
        with col_in_3:
            spending_score = st.number_input(
                "Spending Score (1-100)",
                min_value=1,
                max_value=100,
                value=50,
                step=1,
                help="Spending score index value (1 = low spending power, 100 = maximum)"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Trigger button
        if st.button("🔮 Predict Cohort Segment", type="primary", use_container_width=True):
            status_box = st.empty()
            with status_box.container():
                st.markdown("""
                <div style="text-align: center; padding: 40px 0;">
                    <div class="spinner"></div>
                    <p style="color: #a855f7; font-weight: 600; margin-top: 20px; font-size: 16px; letter-spacing: -0.5px; animation: pulse 1.5s infinite;">Consulting AI Cluster Models...</p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1.2)
            status_box.empty()
            
            # Format inputs as DataFrame
            input_df = pd.DataFrame(
                [[annual_income, spending_score]],
                columns=["Annual Income (k$)", "Spending Score (1-100)"]
            )
            
            # Transform and predict
            input_scaled = scaler.transform(input_df)
            pred_cluster = kmeans.predict(input_scaled)[0]
            details = cluster_details[pred_cluster]
            
            # Calculate K-Means distance-based Softmax Confidence Score
            centroids_scaled = kmeans.cluster_centers_
            distances = np.linalg.norm(centroids_scaled - input_scaled, axis=1)
            # Softmax on negative distances
            temp = 2.2
            exp_dists = np.exp(-distances * temp)
            probs = exp_dists / np.sum(exp_dists)
            confidence = float(probs[pred_cluster] * 100)
            
            # Clamp confidence to reasonable values
            if confidence > 99.9:
                confidence = 99.9
            elif confidence < 20.0:
                confidence = 20.0
                
            # Store in session state
            st.session_state['prediction'] = {
                'age': age,
                'annual_income': annual_income,
                'spending_score': spending_score,
                'cluster': int(pred_cluster),
                'details': details,
                'confidence': confidence
            }
        st.markdown("</div>", unsafe_allow_html=True) # End of inputs card
            
        # Display prediction results if they exist in session state
        if 'prediction' in st.session_state:
            pred = st.session_state['prediction']
            age_val = pred['age']
            income_val = pred['annual_income']
            score_val = pred['spending_score']
            cluster_val = pred['cluster']
            details_val = pred['details']
            confidence_val = pred['confidence']
            
            # Fetch cluster dataset information dynamically
            cluster_df = raw_df[raw_df["Cluster"] == cluster_val]
            cluster_size = len(cluster_df)
            cluster_avg_income = cluster_df["Annual Income (k$)"].mean()
            cluster_avg_spending = cluster_df["Spending Score (1-100)"].mean()
            cluster_avg_age = cluster_df["Age"].mean()
            
            st.write(" ")
            
            res_col1, res_col2 = st.columns([5, 4])
            
            with res_col1:
                # Premium gradient badge above the result (styled via global h4 CSS)
                st.markdown(f"#### 🔮 Cluster {cluster_val} • {details_val['name']}")
                
                # Main attractive heading
                st.markdown("### 🧠 AI Executive Analysis")
                
                # Confidence Progress Card
                with st.container(border=True):
                    col_conf1, col_conf2 = st.columns([3, 1])
                    with col_conf1:
                        st.markdown("**⚡ Centroid Proximity Match (Confidence)**")
                        st.progress(confidence_val / 100.0)
                    with col_conf2:
                        st.metric(label="Confidence Index", value=f"{confidence_val:.1f}%")
                
                # Comparative Baseline Parameters Card
                with st.container(border=True):
                    st.markdown("**📊 Cohort Baseline Parameters**")
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    with metric_col1:
                        st.metric(label="Cohort Size", value=f"{cluster_size}", delta=f"{cluster_size/len(raw_df)*100:.1f}% base")
                    with metric_col2:
                        st.metric(label="Avg Income", value=f"${cluster_avg_income:.1f}k")
                    with metric_col3:
                        st.metric(label="Avg Spend", value=f"{cluster_avg_spending:.1f}/100")
                    with metric_col4:
                        st.metric(label="Avg Age", value=f"{cluster_avg_age:.1f} yrs")
                
                # Characteristics Playbook Card
                with st.container(border=True):
                    st.markdown("### 📋 Cohort Characteristics")
                    st.write(details_val['characteristics'])
                
                # Marketing Strategy Card
                with st.container(border=True):
                    st.markdown("### 🎯 Marketing Playbook & Strategy")
                    st.write(details_val['strategy'])
                
                # Recommendations Card
                with st.container(border=True):
                    st.markdown("### 🚀 Tactical Recommendations")
                    st.write(details_val['recommendation'])
                
                # Target Products Card
                with st.container(border=True):
                    st.markdown("### 🛍️ Target Products")
                    st.write(details_val['products'])
                
            with res_col2:
                # PDF report download
                pdf_bytes = create_pdf_report(age_val, income_val, score_val, cluster_val, details_val)
                st.download_button(
                    label="📄 Export Executive Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"cohort_report_cluster_{cluster_val}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.write(" ")
                
                # Visual Indicator Plot
                fig_loc = go.Figure()
                
                # Plot background dots
                for name, color in color_map.items():
                    sub_df = raw_df[raw_df["Cluster Name"] == name]
                    fig_loc.add_trace(
                        go.Scatter(
                            x=sub_df["Annual Income (k$)"],
                            y=sub_df["Spending Score (1-100)"],
                            mode="markers",
                            marker=dict(color=color, size=6, opacity=0.35),
                            name=name,
                            showlegend=False
                        )
                    )
                
                # Plot predicted customer
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
                        name="Target Lead"
                    )
                )
                
                fig_loc.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Plus Jakarta Sans", color="#94a3b8"),
                    title=dict(text="Lead Coordinates in Spatial Clusters", font=dict(size=14, color="#ffffff", family="Plus Jakarta Sans")),
                    xaxis_title="Annual Income (k$)",
                    yaxis_title="Spending Score (1-100)",
                    margin=dict(t=40, b=10, l=10, r=10),
                    height=300,
                    xaxis=dict(
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        linecolor="rgba(255, 255, 255, 0.1)"
                    ),
                    yaxis=dict(
                        gridcolor="rgba(255, 255, 255, 0.05)",
                        linecolor="rgba(255, 255, 255, 0.1)"
                    )
                )
                st.plotly_chart(fig_loc, use_container_width=True)

# ----------------- ABOUT PAGE -----------------
elif st.session_state.page == "📖 About Project":
    st_html("""
    <div class="animated-card" style="margin-bottom: 35px;">
        <h1 style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 38px; letter-spacing: -1.5px; margin-bottom: 8px;">Theoretical Framework</h1>
        <p style="color: #64748b; font-size: 15px; margin: 0;">Understand the mathematical formulas, clustering limits, and standardizations backing the engine.</p>
    </div>
    """)
    
    st.markdown("<div class='luxury-card animated-card delay-1'>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #ffffff; font-family: 'Plus Jakarta Sans'; font-weight: 700; margin-top: 0; font-size: 20px;">🧮 K-Means Clustering Algorithmic Bounds</h3>
    <p style="color: #94a3b8; font-size: 14.5px; line-height: 1.6;">
        K-Means partitions data observations into $K$ distinct sets based on Euclidean distance, minimizing inertia or Within-Cluster Sum of Squares (WCSS).
    </p>
    """, unsafe_allow_html=True)
    st.latex(r"d(p, q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='luxury-card animated-card delay-2'>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #ffffff; font-family: 'Plus Jakarta Sans'; font-weight: 700; margin-top: 0; font-size: 20px;">⚖️ Standard Z-Score Scalers</h3>
    <p style="color: #94a3b8; font-size: 14.5px; line-height: 1.6;">
        Standardizing features prior to running distance calculations offsets scale variances across dimensions. Features are adjusted to have a mean of 0 and standard deviation of 1.
    </p>
    """, unsafe_allow_html=True)
    st.latex(r"z = \frac{x - \mu}{\sigma}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='luxury-card animated-card delay-3'>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #ffffff; font-family: 'Plus Jakarta Sans'; font-weight: 700; margin-top: 0; font-size: 20px;">💪 Heuristics: Elbow & WCSS Optimization</h3>
    <p style="color: #94a3b8; font-size: 14.5px; line-height: 1.6;">
        The Elbow method tracks WCSS curves across multiple dimensions of $K$, selecting the bend or elbow boundary ($K=5$) as the optimal cluster partition limit.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='luxury-card animated-card delay-4'>", unsafe_allow_html=True)
    st.markdown("""
    <h3 style="color: #ffffff; font-family: 'Plus Jakarta Sans'; font-weight: 700; margin-top: 0; font-size: 20px;">📈 Silhouette Cohesion Indices</h3>
    <p style="color: #94a3b8; font-size: 14.5px; line-height: 1.6;">
        Measures intra-cluster alignment score coefficients against neighboring boundaries on a [-1, 1] range to evaluate model clustering fit.
    </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- UNIVERSAL PREMIUM FOOTER -----------------
st.markdown("""
<footer style="margin-top: 80px; padding: 40px 0; border-top: 1px solid rgba(255, 255, 255, 0.05); text-align: center;">
    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 15px; flex-wrap: wrap;">
        <span style="color: #64748b; font-size: 13px; font-weight: 500;">SEGMENT.AI © 2026</span>
        <span style="color: rgba(255, 255, 255, 0.1);">|</span>
        <span style="color: #64748b; font-size: 13px; font-weight: 500;">Enterprise Grade Cohort Intelligence</span>
        <span style="color: rgba(255, 255, 255, 0.1);">|</span>
        <span style="color: #64748b; font-size: 13px; font-weight: 500; background: linear-gradient(135deg, #a855f7 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Status: Online ⚡</span>
    </div>
    <p style="color: #475569; font-size: 11px; max-width: 600px; margin: 0 auto; line-height: 1.5; font-family: 'Plus Jakarta Sans', sans-serif;">
        Powered by Unsupervised Machine Learning. Built with Streamlit, Scikit-learn, and Plotly. Overriden with Custom Glassmorphism UI tokens.
    </p>
</footer>
""", unsafe_allow_html=True)
