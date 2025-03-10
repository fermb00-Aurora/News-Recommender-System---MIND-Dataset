import streamlit as st
import openai
import base64

# =====================================
# SET UP OPENAI API (Securely via st.secrets)
# =====================================
if "OPENAI_API_KEY" not in st.secrets:
    st.error("Please add your OpenAI API key to the Streamlit advanced settings (st.secrets).")
    st.stop()
else:
    openai.api_key = st.secrets["OPENAI_API_KEY"]

# =====================================
# Initialize Chatbot Session Variables
# =====================================
if "chat_visible" not in st.session_state:
    st.session_state["chat_visible"] = True
if "chat_stage" not in st.session_state:
    st.session_state["chat_stage"] = 0  # 0: Ask for news interest; 1: Provide recommendations; -1: Chat closed
if "chat_profile" not in st.session_state:
    st.session_state["chat_profile"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
    st.session_state.chat_history.append({
        "role": "assistant", 
        "content": "Hello, I'm ChatNews 🤖! I'm here to help you get the best news recommendations. To start, what type of news interests you the most? (e.g., Tech, Sports, Politics, or Movies)"
    })

# Helper function to map user input to a profile
def map_input_to_profile(user_input):
    user_input_lower = user_input.lower()
    if "tech" in user_input_lower or "computer" in user_input_lower:
        return "Tech Enthusiast 💻"
    elif "sport" in user_input_lower or "game" in user_input_lower:
        return "Sports Fan ⚽"
    elif "politic" in user_input_lower or "government" in user_input_lower:
        return "Political Enthusiast 🏛️"
    elif "movie" in user_input_lower or "film" in user_input_lower:
        return "Movie Buff 🎬"
    else:
        return None

# Dummy recommendations for chatbot explanation
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

# ===============================
# CHATBOT MODAL POPUP IMPLEMENTATION
# ===============================
if st.session_state.chat_visible and st.session_state.chat_stage != -1:
    st.markdown("""
        <style>
            .chat-modal {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                padding: 10px;
                z-index: 10000;
            }
            .chat-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #E0E0E0;
                padding-bottom: 5px;
                margin-bottom: 5px;
            }
            .chat-body {
                max-height: 200px;
                overflow-y: auto;
            }
        </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="chat-modal">', unsafe_allow_html=True)
        # Chat header with title and a close button
        col_header1, col_header2 = st.columns([3, 1])
        with col_header1:
            st.markdown("<strong>ChatBot 🤖</strong>", unsafe_allow_html=True)
        with col_header2:
            if st.button("X", key="close_chat"):
                st.session_state.chat_visible = False
                st.experimental_rerun()
        # Display conversation history using st.chat_message (Streamlit's chat functions)
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        # Sequential conversation logic:
        if st.session_state.chat_stage == 0:
            # Stage 0: Ask for user's news interest
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
                    st.session_state.chat_profile = profile
                    st.session_state.chat_history.append({
                        "role": "assistant", 
                        "content": f"Great! You've chosen **{profile}**. Based on that, I recommend the following articles:"
                    })
                    st.session_state.chat_stage = 1
                st.experimental_rerun()
        elif st.session_state.chat_stage == 1:
            # Stage 1: Provide recommendations and explanation
            profile = st.session_state.chat_profile
            recs = dummy_recommendations.get(profile, [])
            if recs:
                rec_list = "\n".join([f"- [{title}](#)" for title, _ in recs[:3]])
                explanation = (f"Based on your interest in **{profile}**, here are some articles we recommend:\n\n"
                               f"{rec_list}\n\n"
                               "These recommendations were chosen because they cover the latest trends and insights in your area of interest.")
            else:
                explanation = "Sorry, no recommendations are available for your profile at the moment."
            st.session_state.chat_history.append({"role": "assistant", "content": explanation})
            with st.chat_message("assistant"):
                st.markdown(explanation)
            if st.button("Close Chat", key="close_chat_final"):
                st.session_state.chat_stage = -1
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# REST OF THE SOKONEWS WEB APP CODE
# ===============================
# Custom CSS for a light, Microsoft-inspired UI with clean, clear colors
st.markdown("""
    <style>
        /* Overall Light Background */
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
        /* Widgets */
        .stSelectbox > div > div > div {
            background-color: #FFFFFF;
            border: 1px solid #0078D4;
            border-radius: 5px;
            padding: 5px;
            font-size: 1em;
            color: #333333;
        }
        .stSlider > div > div > div > div {
            background-color: #0078D4;
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
        /* Article Cards (Light Blue) */
        .article-card {
            background-color: #E6F7FF;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            border-left: 4px solid #0078D4;
        }
        .article-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
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

# Top-right logo (if desired)
st.markdown("""
    <div class="top-right-logo">
        <img src="logo.jpg" width="100">
    </div>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown('<h1 class="main-title">SokoNews 🚀</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover personalized news recommendations using Microsoft technology ✨</p>', unsafe_allow_html=True)

# Control Section for user profile & number of recommendations
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

# Extended dummy data for recommendations
collab_recommendations = {
    "Tech Enthusiast 💻": [
        ("AI Revolutionizes the World 🤖", "A breakthrough in artificial intelligence is changing how we interact with technology."),
        ("The Future of Smartphones 📱", "Innovations set to transform the mobile market in 2025 and beyond."),
        ("Quantum Computing Advances", "Exploring the next frontier in computing technology."),
        ("5G Connectivity Explored", "How 5G networks are revolutionizing communication.")
    ],
    "Sports Fan ⚽": [
        ("Champions League Final 2025 🏆", "A recap of the match of the decade with key moments and analysis."),
        ("Record-Breaking Athletes", "Inspiring stories of athletes making history in 2025."),
        ("Olympic Dreams", "How emerging talents are preparing for the next Olympics."),
        ("Sports Technology Trends", "Wearable devices and data analytics are shaping the future of sports.")
    ],
    "Political Enthusiast 🏛️": [
        ("Elections 2025: What You Need to Know 🗳️", "An in-depth analysis of the candidates and their key proposals."),
        ("Global Climate Policies", "New measures to tackle climate change on an international scale."),
        ("Diplomatic Breakthroughs", "Historic agreements reshaping international relations."),
        ("Economic Reforms", "The impact of new policies on the global economy.")
    ],
    "Movie Buff 🎬": [
        ("March 2025 Releases 🍿", "The most anticipated movies of the month that you shouldn't miss."),
        ("Revival of the Classics", "Remakes bringing back iconic stories with a modern twist."),
        ("Indie Film Spotlight", "A look at breakthrough films from independent directors."),
        ("Award Season Buzz", "Predictions and surprises from the upcoming awards season.")
    ]
}

content_based_recommendations = {
    "Tech Enthusiast 💻": [
        ("Latest Gadgets of 2025", "The newest portable tech making waves in the market."),
        ("Cloud Impact", "How cloud computing is transforming modern business operations."),
        ("Augmented Reality Trends", "Innovations in AR that are set to change our interaction with the world."),
        ("Robotics in Daily Life", "How robotics are making everyday tasks easier.")
    ],
    "Sports Fan ⚽": [
        ("Tech in Sports", "How data and analytics are changing the game."),
        ("Training Innovations", "Gadgets that help athletes enhance their performance."),
        ("Virtual Sports Arenas", "Exploring the rise of e-sports and virtual reality in sports."),
        ("Nutrition and Performance", "How dietary tech is revolutionizing athlete training.")
    ],
    "Political Enthusiast 🏛️": [
        ("Digital Politics", "How social media is influencing global political decisions."),
        ("Post-Pandemic Economy", "New economic strategies in a recovering world."),
        ("Cybersecurity in Governance", "Protecting national data in an increasingly digital world."),
        ("Policy Shifts Explained", "An analysis of emerging trends in international policies.")
    ],
    "Movie Buff 🎬": [
        ("Directors to Watch", "Emerging talents reshaping the cinematic landscape."),
        ("Streaming Impact", "How platforms are changing the way we experience movies."),
        ("Animation Innovations", "The latest trends in animated filmmaking."),
        ("Film Critic's Corner", "Reviews and insights from industry experts.")
    ]
}

hybrid_recommendations = {
    "Tech Enthusiast 💻": [
        ("AI Ethics Debate 🤔", "Exploring the ethical implications of artificial intelligence."),
        ("Trends in Technology 2025", "What to expect in the world of tech this year."),
        ("Blockchain Beyond Crypto", "Innovative applications of blockchain technology in business."),
        ("Sustainable Tech", "How green technology is shaping the future.")
    ],
    "Sports Fan ⚽": [
        ("Tech in Football", "Innovations changing the modern game."),
        ("Marathon Highlights", "Not-to-miss events for passionate runners."),
        ("Fan Engagement 2.0", "How technology is enhancing the spectator experience."),
        ("Virtual Training Camps", "The future of remote coaching and training sessions.")
    ],
    "Political Enthusiast 🏛️": [
        ("Data in Elections", "The role of data and AI in modern campaigns."),
        ("Sustainable Future", "Global agreements paving the way for a greener world."),
        ("Political Satire Online", "How digital media is reshaping political discourse."),
        ("Global Leadership Trends", "Exploring emerging leadership styles on the world stage.")
    ],
    "Movie Buff 🎬": [
        ("Cinema and Technology", "How AI is creating immersive movie experiences."),
        ("Film Festival 2025", "Upcoming events for independent and mainstream films."),
        ("Behind the Scenes", "A sneak peek into the making of blockbuster films."),
        ("Retro Reboots", "How classic films are being reimagined for a modern audience.")
    ]
}

def get_recommendations(profile, recommender_type):
    if recommender_type == "Collaborative Filtering":
        return collab_recommendations.get(profile, [])[:num_recommendations]
    elif recommender_type == "Content-Based":
        return content_based_recommendations.get(profile, [])[:num_recommendations]
    elif recommender_type == "Hybrid":
        return hybrid_recommendations.get(profile, [])[:num_recommendations]
    return []

# Tabs for each recommendation method
tab1, tab2, tab3 = st.tabs(["Collaborative Filtering", "Content-Based", "Hybrid"])

with tab1:
    st.markdown('<div class="tab-content">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Collaborative Filtering ⚙️</h2>', unsafe_allow_html=True)
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
    st.markdown('<h2 class="section-header">Content-Based 📄</h2>', unsafe_allow_html=True)
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
    st.markdown('<h2 class="section-header">Hybrid 🔀</h2>', unsafe_allow_html=True)
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
        <p>Explore the MIND dataset <a href="https://msnews.github.io/" target="_blank">here</a> 📊</p>
    </div>
""", unsafe_allow_html=True)
