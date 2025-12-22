import streamlit as st
import pandas as pd
from recommender import hybrid_recommend, get_metadata
from youtubesearchpython import VideosSearch
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title='Aura Music AI', page_icon='🎶', layout='wide')

# --- MODERN FUTURISTIC CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #e0e0e0;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        transition: 0.3s ease;
    }
    .glass-card:hover {
        border: 1px solid #00d2ff;
        transform: translateY(-5px);
    }

    /* Modern Buttons */
    .stButton>button {
        background: rgba(0, 210, 255, 0.1);
        border: 1px solid #00d2ff;
        color: white;
        border-radius: 12px;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: #00d2ff;
        color: #0f0c29;
    }

    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(20px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- AI CONFIGURATION ---
# This version is secure for GitHub
if "GEMINI_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.sidebar.warning("⚠️ API Key not found in Streamlit Secrets.")

# --- POPUP VIDEO PLAYER (WhatsApp Style) ---
@st.dialog("Now Playing")
def play_video_popup(track_name, artist):
    st.write(f"### {track_name}")
    st.write(f"*{artist}*")
    with st.spinner("Fetching from YouTube..."):
        search = VideosSearch(f"{track_name} {artist}", limit=1)
        res = search.result()['result']
        if res:
            st.video(f"https://www.youtube.com/watch?v={res[0]['id']}")
        else:
            st.error("Could not find video.")

# --- APP LOGIC ---
if 'current_song_index' not in st.session_state:
    st.session_state['current_song_index'] = 1255 # Default song

def change_song(index):
    st.session_state['current_song_index'] = index

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.title("🛡️ Aura DJ Control")
    mode = st.radio("Discovery Mode", ["AI Mood Search", "Expert Filters", "Classic Hybrid"])
    
    st.divider()
    rec_count = st.slider("Result Depth", 1, 10, 3)
    
    pop_toggle = st.toggle("Prioritize Popular Songs", value=True)

# --- MAIN PAGE CONTENT ---
current_song = get_metadata(st.session_state['current_song_index'])

st.title("🎶 Aura Music Discovery")

# Hero Section
with st.container():
    st.markdown(f"""
    <div class="glass-card">
        <h2 style='margin:0;'>Now Exploring: {current_song['track_name']}</h2>
        <p style='color:#00d2ff;'>Artist: {current_song['track_artist']}</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("▶️ Play Preview (Popup)"):
        play_video_popup(current_song['track_name'], current_song['track_artist'])

# DISCOVERY MODES
if mode == "AI Mood Search":
    st.subheader("🤖 Describe your Vibe")
    user_input = st.text_input("How are you feeling?", placeholder="e.g. A melancholic rainy night in a jazz cafe")
    if st.button("Generate Aura"):
        # AI logic would process user_input here to filter your CSV
        st.info("AI is analyzing your sentiment to tune the recommendation engine...")

elif mode == "Expert Filters":
    st.subheader("🎚️ Manual Sonic Tuning")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Select Genre", ["Pop", "Rock", "R&B", "EDM", "Latin"])
        st.slider("Energy", 0.0, 1.0, 0.5)
    with col2:
        st.slider("Danceability", 0.0, 1.0, 0.5)
        st.slider("Tempo (BPM)", 60, 200, 120)

else:
    # CLASSIC HYBRID SYSTEM
    recommendations = hybrid_recommend(st.session_state['current_song_index'], rec_count, prioritisePopular=pop_toggle)
    
    for category, songs in recommendations.items():
        st.write(f"### {category.title()}")
        cols = st.columns(len(songs))
        for idx, song in enumerate(songs):
            with cols[idx]:
                st.markdown(f"""
                <div class="glass-card">
                    <b>{song['track_name']}</b><br>
                    <small>{song['track_artist']}</small>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Listen", key=f"btn_{category}_{idx}"):
                    play_video_popup(song['track_name'], song['track_artist'])
