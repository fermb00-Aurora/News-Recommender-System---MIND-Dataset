import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="SokoNews - News Recommender",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS for a readable dark theme
st.markdown("""
    <style>
        /* Overall Dark Background */
        body {
            background-color: #2E2E2E !important;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #EAEAEA;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header Section */
        .header-container {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px 0;
            border-bottom: 2px solid #00A4EF;
        }
        .main-title {
            color: #00A4EF;
            font-size: 2.8em;
            font-weight: 700;
            margin: 0;
        }
        .subtitle {
            color: #CCCCCC;
            font-size: 1.1em;
            font-weight: 400;
            margin-top: 5px;
        }
        
        /* Control Section */
        .control-section {
            background-color: #3A3A3A;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
            margin: 20px 0;
            display: flex;
            gap: 20px;
            align-items: center;
        }
        .control-label {
            color: #00A4EF;
            font-size: 1em;
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        /* Streamlit Widgets */
        .stSelectbox > div > div > div {
            background-color: #454545;
            border: 1px solid #00A4EF;
            border-radius: 5px;
            padding: 5px;
            font-size: 1em;
            color: #EAEAEA;
        }
        .stSlider > div > div > div > div {
            background-color: #00A4EF;
        }
        
        /* Tabs */
        .stTabs {
            margin-top: 20px;
        }
        .stTabs [role="tab"] {
            background-color: #3A3A3A;
            color: #00A4EF;
            border-radius: 10px 10px 0 0;
            padding: 12px 25px;
            font-weight: 500;
            font-size: 1em;
            transition: background-color 0.3s, color 0.3s;
        }
        .stTabs [role="tab"][aria-selected="true"] {
            background-color: #2E2E2E;
            color: #FF8C00;
            border-bottom: 3px solid #FF8C00;
        }
        .stTabs [role="tab"]:hover {
            background-color: #454545;
        }
        .tab-content {
            background-color: #3A3A3A;
            padding: 25px;
            border-radius: 0 10px 10px 10px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
        }
        
        /* Article Cards */
        .article-card {
            background-color: #454545;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #00A4EF;
        }
        .article-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.7);
        }
        .article-title {
            color: #00A4EF;
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .article-summary {
            color: #CCCCCC;
            font-size: 1em;
            line-height: 1.5;
        }
        .description-text {
            color: #CCCCCC;
            font-size: 1em;
            font-style: italic;
            margin-bottom: 25px;
            line-height: 1.6;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #CCCCCC;
            font-size: 0.9em;
            margin-top: 40px;
            padding: 20px 0;
            border-top: 1px solid #00A4EF;
        }
        .footer a {
            color: #00A4EF;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Header with logo and title
st.markdown('<div class="header-container">', unsafe_allow_html=True)
col1, col2 = st.columns([1, 5])
with col1:
    # Ensure logo.png is in the same folder as this app.py
    st.image("logo.png", width=80)
with col2:
    st.markdown('<h1 class="main-title">SokoNews</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover personalized news recommendations using Microsoft technology</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Control Section for user profile & number of recommendations
st.markdown('<div class="control-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown('<p class="control-label">User Profile</p>', unsafe_allow_html=True)
    user_profiles = ["Tech Enthusiast", "Sports Fan", "Political Enthusiast", "Movie Buff"]
    selected_profile = st.selectbox(
        "Select a profile",  # Non-empty label for accessibility
        user_profiles,
        label_visibility="collapsed",
        help="Choose a profile to personalize your recommendations."
    )
with col2:
    st.markdown('<p class="control-label">Number of Recommendations</p>', unsafe_allow_html=True)
    num_recommendations = st.slider(
        "Number of Recommendations",  # Non-empty label for accessibility
        1, 20, 5,
        label_visibility="collapsed",
        help="Adjust how many news articles you wish to see."
    )
with col3:
    st.markdown('<p class="control-label">Refresh</p>', unsafe_allow_html=True)
    if st.button("Refresh"):
        st.info("Page refreshed!")  # Button click triggers a rerun automatically

st.markdown('</div>', unsafe_allow_html=True)

# Dummy data for recommendations
collab_recommendations = {
    "Tech Enthusiast": [
        ("AI Revolutionizes the World", "A breakthrough in artificial intelligence is changing how we interact with technology."),
        ("The Future of Smartphones", "Innovations set to transform the mobile market in 2025 and beyond."),
    ],
    "Sports Fan": [
        ("Champions League Final 2025", "A recap of the match of the decade with key moments and analysis."),
        ("Record-Breaking Athletes", "Inspiring stories of athletes making history in 2025."),
    ],
    "Political Enthusiast": [
        ("Elections 2025: What You Need to Know", "An in-depth analysis of the candidates and their key proposals."),
        ("Global Climate Policies", "New measures to tackle climate change on an international scale."),
    ],
    "Movie Buff": [
        ("March 2025 Releases", "The most anticipated movies of the month that you shouldn't miss."),
        ("Revival of the Classics", "Remakes bringing back iconic stories with a modern twist."),
    ],
}

content_based_recommendations = {
    "Tech Enthusiast": [
        ("Latest Gadgets of 2025", "The newest portable tech making waves in the market."),
        ("Cloud Impact", "How cloud computing is transforming modern business operations."),
    ],
    "Sports Fan": [
        ("Tech in Sports", "How data and analytics are changing the game."),
        ("Training Innovations", "Gadgets that help athletes enhance their performance."),
    ],
    "Political Enthusiast": [
        ("Digital Politics", "How social media is influencing global political decisions."),
        ("Post-Pandemic Economy", "New economic strategies in a recovering world."),
    ],
    "Movie Buff": [
        ("Directors to Watch", "Emerging talents reshaping the cinematic landscape."),
        ("Streaming Impact", "How platforms are changing the way we experience movies."),
    ],
}

hybrid_recommendations = {
    "Tech Enthusiast": [
        ("AI Ethics Debate", "Exploring the ethical implications of artificial intelligence."),
        ("Trends in Technology 2025", "What to expect in the world of tech this year."),
    ],
    "Sports Fan": [
        ("Tech in Football", "Innovations changing the modern game."),
        ("Marathon Highlights", "Not-to-miss events for passionate runners."),
    ],
    "Political Enthusiast": [
        ("Data in Elections", "The role of data and AI in modern campaigns."),
        ("Sustainable Future", "Global agreements paving the way for a greener world."),
    ],
    "Movie Buff": [
        ("Cinema and Technology", "How AI is creating immersive movie experiences."),
        ("Film Festival 2025", "Upcoming events for independent and mainstream films."),
    ],
}

def get_recommendations(profile, recommender_type):
    if recommender_type == "Collaborative Filtering":
        return collab_recommendations.get(profile, [])[:num_recommendations]
    elif recommender_type == "Content-Based":
        return content_based_recommendations.get(profile, [])[:num_recommendations]
    elif recommender_type == "Hybrid":
        return hybrid_recommendations.get(profile, [])[:num_recommendations]
    return []

# Create tabs for each recommendation method
tab1, tab2, tab3 = st.tabs(["Collaborative Filtering", "Content-Based", "Hybrid"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Collaborative Filtering</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method analyzes the behavior of users with similar interests to recommend relevant news articles.</p>', unsafe_allow_html=True)
    recommendations = get_recommendations(selected_profile, "Collaborative Filtering")
    if recommendations:
        for title, summary in recommendations:
            st.markdown(f"""
                <div class="article-card">
                    <h3 class="article-title">{title}</h3>
                    <p class="article-summary">{summary}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p class="description-text">No recommendations available for this profile at the moment.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Content-Based</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method recommends news based on the content of articles you have previously read, identifying patterns in your preferences.</p>', unsafe_allow_html=True)
    recommendations = get_recommendations(selected_profile, "Content-Based")
    if recommendations:
        for title, summary in recommendations:
            st.markdown(f"""
                <div class="article-card">
                    <h3 class="article-title">{title}</h3>
                    <p class="article-summary">{summary}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p class="description-text">No recommendations available for this profile at the moment.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Hybrid</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method combines collaborative filtering and content-based approaches to offer more precise recommendations.</p>', unsafe_allow_html=True)
    recommendations = get_recommendations(selected_profile, "Hybrid")
    if recommendations:
        for title, summary in recommendations:
            st.markdown(f"""
                <div class="article-card">
                    <h3 class="article-title">{title}</h3>
                    <p class="article-summary">{summary}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p class="description-text">No recommendations available for this profile at the moment.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2025 SokoNews - Developed for Microsoft Capstone Project</p>
        <p>Explore the MIND dataset <a href="https://www.kaggle.com/datasets/arashnic/mind-news-dataset" target="_blank">here</a>.</p>
    </div>
""", unsafe_allow_html=True)
