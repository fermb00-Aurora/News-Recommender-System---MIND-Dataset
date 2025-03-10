import streamlit as st
import openai

# -------------------------------
# Helper: Safe Rerun Function
# -------------------------------
def safe_rerun():
    """
    Forces a re-run of the app by reading and re-setting
    the existing query parameters. This avoids using any
    experimental_* methods that may be deprecated.
    """
    params = st.query_params  # st.query_params is a property
    st.set_query_params(**params)  # This triggers a rerun


# =====================================
# SET UP OPENAI API (via st.secrets)
# =====================================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Please add your OpenAI API key to the Streamlit advanced settings (st.secrets).")
    st.stop()
else:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# =====================================
# Initialize Chatbot Session Variables
# =====================================
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": (
            "Hello, I'm ChatNews 🤖! I'm here to help you get the best news recommendations. "
            "To start, what type of news interests you the most? (e.g., Tech, Sports, Politics, or Movies)"
        )
    })

if "chat_stage" not in st.session_state:
    st.session_state["chat_stage"] = 0  # 0: ask for interest; 1: provide recommendations
if "chat_profile" not in st.session_state:
    st.session_state["chat_profile"] = None

# Helper: Map user input to a profile
def map_input_to_profile(user_input: str):
    txt = user_input.lower()
    if "tech" in txt or "computer" in txt:
        return "Tech Enthusiast 💻"
    elif "sport" in txt or "game" in txt:
        return "Sports Fan ⚽"
    elif "politic" in txt or "government" in txt:
        return "Political Enthusiast 🏛️"
    elif "movie" in txt or "film" in txt:
        return "Movie Buff 🎬"
    else:
        return None

# Dummy recommendations
dummy_recommendations = {
    "Tech Enthusiast 💻": [
        ("AI Revolutionizes the World 🤖", "A breakthrough in AI is transforming technology."),
        ("The Future of Smartphones 📱", "Innovative designs set to change mobile markets."),
        ("Quantum Computing Advances", "Exploring the next frontier in computing.")
    ],
    "Sports Fan ⚽": [
        ("Champions League Final 2025 🏆", "An epic match with unforgettable moments."),
        ("Record-Breaking Athletes", "Stories of athletes setting new records."),
        ("Olympic Dreams", "Rising stars preparing for the Olympics.")
    ],
    "Political Enthusiast 🏛️": [
        ("Elections 2025: What You Need to Know 🗳️", "A detailed look at upcoming elections."),
        ("Global Climate Policies", "How international measures are tackling climate change."),
        ("Diplomatic Breakthroughs", "Historic agreements reshaping politics.")
    ],
    "Movie Buff 🎬": [
        ("March 2025 Releases 🍿", "Highly anticipated films of the month."),
        ("Revival of the Classics", "Iconic films reimagined for today."),
        ("Indie Film Spotlight", "Breakthrough films from independent directors.")
    ]
}

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
        /* Overall Light Background & Font */
        body {
            background-color: #FFFFFF !important;
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #333333;
        }
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        /* Top-right Logo */
        .top-right-logo {
            position: absolute;
            top: 10px;
            right: 10px;
            z-index: 1000;
        }
        /* Title and Subtitle */
        .main-title {
            color: #0078D4;
            font-size: 2.6em;
            font-weight: 700;
            margin: 0;
        }
        .subtitle {
            color: #666666;
            font-size: 1.1em;
            font-weight: 400;
            margin-top: 5px;
        }
        /* Control Section */
        .control-section {
            background-color: #FAFAFA;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E0E0E0;
            margin: 20px 0;
            display: flex;
            gap: 20px;
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
            margin-top: 20px;
        }
        .stTabs [role="tab"] {
            background-color: #F0F0F0;
            color: #0078D4;
            border-radius: 10px 10px 0 0;
            padding: 12px 25px;
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
            padding: 25px;
            border-radius: 0 10px 10px 10px;
            border: 1px solid #E0E0E0;
        }
        /* Article Cards */
        .article-card {
            background-color: #E6F7FF;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #0078D4;
        }
        .article-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }
        .article-title {
            color: #0078D4;
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .article-summary {
            color: #333333;
            font-size: 1em;
            line-height: 1.5;
        }
        .description-text {
            color: #666666;
            font-size: 1em;
            font-style: italic;
            margin-bottom: 25px;
            line-height: 1.6;
        }
        /* Footer */
        .footer {
            text-align: center;
            color: #666666;
            font-size: 0.9em;
            margin-top: 40px;
            padding: 20px 0;
            border-top: 1px solid #0078D4;
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

# Optional: top-right logo
st.markdown("""
    <div class="top-right-logo">
        <img src="logo.jpg" width="100">
    </div>
""", unsafe_allow_html=True)

# Title & Subtitle
st.markdown('<h1 class="main-title">SokoNews 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover personalized news recommendations using Microsoft technology ✨</p>', unsafe_allow_html=True)

# Control Section
st.markdown('<div class="control-section">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    st.markdown('<p class="control-label">User Profile</p>', unsafe_allow_html=True)
    user_profiles = ["Tech Enthusiast 💻", "Sports Fan ⚽", "Political Enthusiast 🏛️", "Movie Buff 🎬"]
    selected_profile = st.selectbox(
        "Select a profile",
        user_profiles,
        label_visibility="collapsed",
        help="Choose a profile to personalize your recommendations."
    )
with col2:
    st.markdown('<p class="control-label">Number of Recommendations</p>', unsafe_allow_html=True)
    num_recommendations = st.slider(
        "Number of Recommendations",
        1, 20, 5,
        label_visibility="collapsed",
        help="Adjust how many news articles you wish to see."
    )
with col3:
    st.markdown('<p class="control-label">Refresh</p>', unsafe_allow_html=True)
    if st.button("Refresh"):
        st.info("Page refreshed!")
st.markdown('</div>', unsafe_allow_html=True)

# Create four tabs: Collab, Content-Based, Hybrid, Chatbot
tabs = st.tabs(["Collaborative Filtering", "Content-Based", "Hybrid", "Chatbot Recommender"])

# TAB 1: Collaborative Filtering
with tabs[0]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Collaborative Filtering ⚙️</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method analyzes the behavior of users with similar interests to recommend relevant news articles.</p>', unsafe_allow_html=True)
    recommendations = dummy_recommendations.get(selected_profile, [])[:num_recommendations]
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

# TAB 2: Content-Based
with tabs[1]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Content-Based 📄</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method recommends news based on the content of articles you have previously read, identifying patterns in your preferences.</p>', unsafe_allow_html=True)
    recommendations = dummy_recommendations.get(selected_profile, [])[:num_recommendations]
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

# TAB 3: Hybrid
with tabs[2]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Hybrid 🔀</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method combines collaborative filtering and content-based approaches to offer more precise recommendations.</p>', unsafe_allow_html=True)
    recommendations = dummy_recommendations.get(selected_profile, [])[:num_recommendations]
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

# TAB 4: Chatbot Recommender
with tabs[3]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Chatbot Recommender 🤖</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">Interact with our chatbot to get personalized recommendations based on your interests.</p>', unsafe_allow_html=True)
    
    # Display existing chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Stage-based logic
    if st.session_state["chat_stage"] == 0:
        user_input = st.chat_input("What type of news interests you?")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            profile = map_input_to_profile(user_input)
            if profile is None:
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": "I didn't quite understand that. Please mention one of these topics: Tech, Sports, Politics, or Movies."
                })
            else:
                st.session_state["chat_profile"] = profile
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": f"Great! You've chosen **{profile}**. Based on that, I recommend the following articles:"
                })
                st.session_state["chat_stage"] = 1
            safe_rerun()

    elif st.session_state["chat_stage"] == 1:
        profile = st.session_state["chat_profile"]
        recs = dummy_recommendations.get(profile, [])
        if recs:
            rec_list = "\n".join([f"- [{title}](#)" for title, _ in recs[:3]])
            explanation = (
                f"Based on your interest in **{profile}**, here are some articles we recommend:\n\n"
                f"{rec_list}\n\n"
                "These recommendations were chosen because they cover the latest trends and insights in your area of interest."
            )
        else:
            explanation = "Sorry, no recommendations are available for your profile at the moment."
        
        st.session_state.chat_history.append({"role": "assistant", "content": explanation})
        with st.chat_message("assistant"):
            st.markdown(explanation)
        
        if st.button("Close Chat", key="close_chat_final"):
            st.session_state["chat_stage"] = -1
            safe_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown("""
    <div class="footer">
        <p>© 2025 SokoNews - Developed for Microsoft Capstone Project</p>
        <p>Explore the MIND dataset <a href="https://msnews.github.io/" target="_blank">here</a> 📊</p>
    </div>
""", unsafe_allow_html=True)
