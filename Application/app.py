import streamlit as st
import openai
import pandas as pd
from Models.categorical_frequency_model import categorical_frequency_model

# =====================================
# SET UP OPENAI API (via st.secrets)
# =====================================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Please add your OpenAI API key to the Streamlit advanced settings (st.secrets).")
    st.stop()
else:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# -----------------------------------
# PAGE CONFIG & GLOBAL STYLING
# -----------------------------------
st.set_page_config(
    page_title="SokoNews - News Recommender",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        /* Overall Egg White Background & Font */
        body {
            background-color: #F8F3E9 !important;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #333333;
        }
        .stApp {
            max-width: 1100px;
            margin: 0 auto;
            padding: 20px;
        }
        /* Top-right Logo */
        .top-right-logo {
            position: absolute;
            top: 15px;
            right: 15px;
            z-index: 1000;
        }
        /* Title and Subtitle */
        .main-title {
            color: #0078D4;
            font-size: 2.4em;
            font-weight: 700;
            margin: 0;
        }
        .subtitle {
            color: #555555;
            font-size: 1.05em;
            font-weight: 400;
            margin-top: 6px;
        }
        /* Control Section */
        .control-section {
            background-color: #FAFAFA;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #E0E0E0;
            margin-bottom: 20px;
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .control-label {
            color: #0078D4;
            font-size: 1em;
            font-weight: 500;
            margin-bottom: 5px;
        }
        /* Tabs */
        .stTabs {
            margin-bottom: 20px;
        }
        .stTabs [role="tab"] {
            background-color: #F0F0F0;
            color: #0078D4;
            border-radius: 10px 10px 0 0;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 1em;
            transition: background-color 0.3s, color 0.3s;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #FFFFFF;
            color: #F25022;
            border-bottom: 3px solid #F25022;
        }
        .stTabs [role="tab"]:hover {
            background-color: #E8E8E8;
        }
        .tab-content {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
            margin-bottom: 20px;
        }
        /* Article Cards */
        .article-card {
            background-color: #E6F7FF;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #0078D4;
        }
        .article-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        }
        .article-title {
            color: #0078D4;
            font-size: 1.15em;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .article-summary {
            color: #333333;
            font-size: 0.95em;
            line-height: 1.5;
        }
        .description-text {
            color: #666666;
            font-size: 0.95em;
            font-style: italic;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        /* Footer */
        .footer {
            text-align: center;
            color: #666666;
            font-size: 0.85em;
            margin-top: 30px;
            padding: 15px 0;
            border-top: 1px solid #E0E0E0;
        }
        .footer a {
            color: #0078D4;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="top-right-logo">
        <img src="logo.jpg" style="width: 90px; height: auto; object-fit: contain;">
    </div>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">SokoNews 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover personalized news recommendations using Microsoft technology ✨</p>', unsafe_allow_html=True)

# ---------------------------
# Control Section
# ---------------------------
st.markdown('<div class="control-section">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    user_id = st.text_input("Enter your User ID", value="U13740", help="Type your user ID from the behaviors dataset.")
with col2:
    num_recommendations = st.slider("Number of Recommendations", 1, 20, 5, help="Adjust how many articles to retrieve.")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Create tabs
# ---------------------------
tabs = st.tabs(["Frequency_Categorical Recommender", "Content-Based", "Hybrid", "Chatbot Recommender"])

# TAB 1: Frequency_Categorical Recommender
with tabs[0]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Frequency_Categorical Recommender</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method finds your most-read category and recommends unseen articles in that category.</p>', unsafe_allow_html=True)

    # Call the frequency-based model
    recommendations_df, explanation = frequency_categorical_recommender(user_id, num_recommendations)

    if recommendations_df is not None:
        st.markdown(f"### {explanation}")
        for idx, row in recommendations_df.iterrows():
            url = row.get("url", "#")
            st.markdown(f"- [{row['title']}]({url})")
    else:
        st.markdown(f"**{explanation}**")
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: Content-Based (placeholder / dummy)
with tabs[1]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Content-Based 📄</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method recommends news based on the content of articles you have previously read. (Placeholder)</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: Hybrid (placeholder / dummy)
with tabs[2]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Hybrid 🔀</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method combines collaborative filtering and content-based approaches. (Placeholder)</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: Chatbot Recommender (placeholder / dummy)
with tabs[3]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Chatbot Recommender 🤖</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">Interact with our chatbot for personalized recommendations. (Placeholder)</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown("""
    <div class="footer">
        <p>© 2025 SokoNews - Developed for Microsoft Capstone Project</p>
        <p>Explore the <a href="https://msnews.github.io/" target="_blank">MIND dataset</a> 📊</p>
    </div>
""", unsafe_allow_html=True)
