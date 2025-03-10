import streamlit as st
import openai

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
            "To begin, please tell me what type of news interests you the most (e.g., Tech, Sports, Politics, or Movies)."
        )
    })

# Conversation stages:
# 0 => Asking user about interest
# 1 => We have a valid profile, show recommendations
# 2 => Ask if user wants to refine or end
# -1 => Conversation ended
if "chat_stage" not in st.session_state:
    st.session_state["chat_stage"] = 0
if "chat_profile" not in st.session_state:
    st.session_state["chat_profile"] = None

# =====================================
# Dummy Recommendation Data
# =====================================
dummy_recommendations = {
    "Tech Enthusiast 💻": [
        ("AI Revolutionizes the World 🤖", "A breakthrough in AI is transforming technology."),
        ("The Future of Smartphones 📱", "Innovative designs set to change the mobile markets."),
        ("Quantum Computing Advances", "Exploring the next frontier in computing technology."),
    ],
    "Sports Fan ⚽": [
        ("Champions League Final 2025 🏆", "A match of the decade with unforgettable moments."),
        ("Record-Breaking Athletes", "Stories of athletes setting new records in 2025."),
        ("Olympic Dreams", "Rising stars preparing for the next Olympics."),
    ],
    "Political Enthusiast 🏛️": [
        ("Elections 2025: What You Need to Know 🗳️", "A detailed look at the upcoming elections."),
        ("Global Climate Policies", "How international measures tackle climate change."),
        ("Diplomatic Breakthroughs", "Historic agreements reshaping global politics."),
    ],
    "Movie Buff 🎬": [
        ("March 2025 Releases 🍿", "Highly anticipated films of the month you shouldn't miss."),
        ("Revival of the Classics", "Iconic films reimagined for a modern audience."),
        ("Indie Film Spotlight", "Breakthrough films from independent directors."),
    ],
}

def map_input_to_profile(user_input: str):
    text = user_input.lower()
    if "tech" in text or "computer" in text:
        return "Tech Enthusiast 💻"
    elif "sport" in text or "game" in text:
        return "Sports Fan ⚽"
    elif "politic" in text or "government" in text:
        return "Political Enthusiast 🏛️"
    elif "movie" in text or "film" in text:
        return "Movie Buff 🎬"
    else:
        return None

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
            background-color: #F8F3E9 !important; /* Egg white */
            font-family: 'Segoe UI', Arial, sans-serif;
            color: #333333;
        }
        .stApp {
            max-width: 1100px;
            margin: 0 auto;
            padding: 20px; /* Reduced padding for a cleaner layout */
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
            margin-top: 6px; /* Slightly reduced margin */
        }
        /* Control Section */
        .control-section {
            background-color: #FAFAFA;
            padding: 15px; /* Slightly reduced padding */
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
            margin-bottom: 20px; /* Less bottom spacing */
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

# If logo.jpg is in the same folder, remove "Application/" from src
st.markdown("""
    <div class="top-right-logo">
        <img src="logo.jpg" width="90">
    </div>
""", unsafe_allow_html=True)


# Title & Subtitle
st.markdown('<h1 class="main-title">SokoNews 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover personalized news recommendations using Microsoft technology ✨</p>', unsafe_allow_html=True)

# =========================
# Control Section (Profile)
# =========================
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

# =========================
# 4 TABS
# =========================
tabs = st.tabs(["Collaborative Filtering", "Content-Based", "Hybrid", "Chatbot Recommender"])

# TAB 1: Collaborative Filtering
with tabs[0]:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Collaborative Filtering ⚙️</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description-text">This method analyzes the behavior of users with similar interests to recommend relevant news articles.</p>', unsafe_allow_html=True)
    recs = dummy_recommendations.get(selected_profile, [])[:num_recommendations]
    if recs:
        for title, summary in recs:
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
    recs = dummy_recommendations.get(selected_profile, [])[:num_recommendations]
    if recs:
        for title, summary in recs:
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
    recs = dummy_recommendations.get(selected_profile, [])[:num_recommendations]
    if recs:
        for title, summary in recs:
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

    # Display conversation so far
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # If conversation ended
    if st.session_state["chat_stage"] == -1:
        st.markdown("**The conversation has ended.** You can refresh the page to start again.")
    else:
        user_input = st.chat_input("Type your message here and press Enter...")
        if user_input:
            # Append user message
            st.session_state["chat_history"].append({"role": "user", "content": user_input})

            # Stage-based logic
            if st.session_state["chat_stage"] == 0:
                profile = map_input_to_profile(user_input)
                if profile is None:
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": "I didn't quite understand that. Please mention Tech, Sports, Politics, or Movies."
                    })
                else:
                    st.session_state["chat_profile"] = profile
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": (
                            f"Great! You've chosen **{profile}**. Let me fetch some recommendations for you. "
                            "Would you like to see them now? (Type 'yes' or 'refine' or 'end')"
                        )
                    })
                    st.session_state["chat_stage"] = 1

            elif st.session_state["chat_stage"] == 1:
                lower_inp = user_input.lower()
                if "refine" in lower_inp:
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": "Okay, let's refine your interest. Please tell me again: Tech, Sports, Politics, or Movies?"
                    })
                    st.session_state["chat_stage"] = 0
                elif "end" in lower_inp:
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": "No problem! The conversation has ended. Have a great day!"
                    })
                    st.session_state["chat_stage"] = -1
                elif "yes" in lower_inp or "show" in lower_inp:
                    profile = st.session_state["chat_profile"]
                    recs = dummy_recommendations.get(profile, [])
                    if recs:
                        top_recs = recs[:3]
                        bullet_list = "\n".join([f"- [{title}](#)" for title, _ in top_recs])
                        explanation = (
                            f"Based on your interest in **{profile}**, here are a few articles:\n\n"
                            f"{bullet_list}\n\n"
                            "These recommendations are chosen because they cover the latest trends in your area."
                        )
                    else:
                        explanation = "Sorry, I don't have any recommendations for that profile at the moment."
                    st.session_state["chat_history"].append({"role": "assistant", "content": explanation})
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": "Would you like to refine your interest or end the conversation? (Type 'refine' or 'end')"
                    })
                    st.session_state["chat_stage"] = 2
                else:
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": "I didn't catch that. Please type 'yes', 'refine', or 'end'."
                    })

            elif st.session_state["chat_stage"] == 2:
                lower_inp = user_input.lower()
                if "refine" in lower_inp:
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": "Alright, let's refine your interest. Which topic do you prefer: Tech, Sports, Politics, or Movies?"
                    })
                    st.session_state["chat_stage"] = 0
                elif "end" in lower_inp:
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": "Thanks for chatting! The conversation has ended. Have a great day!"
                    })
                    st.session_state["chat_stage"] = -1
                else:
                    st.session_state["chat_history"].append({
                        "role": "assistant",
                        "content": "Please type 'refine' or 'end'."
                    })

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
