import streamlit as st
import pandas as pd
import google.generativeai as genai
from recommender import hybrid_recommend, get_metadata
from youtubesearchpython import VideosSearch

# --- PAGE CONFIG ---
st.set_page_config(page_title='Aura Music AI', page_icon='🎶', layout='wide')

# --- HIGH VISIBILITY NEON DESIGN ---
st.markdown("""
    <style>
    /* Main Background - High Contrast */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 2px solid #00D4FF;
    }
    /* Song Cards */
    .song-card {
        background: #1C2128;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #30363D;
        margin-bottom: 10px;
        text-align: center;
    }
    .song-card:hover {
        border-color: #00D4FF;
    }
    /* Text Colors */
    h1, h2, h3 { color: #00D4FF !important; }
    p { color: #C9D1D9 !important; }
    
    /* Button Styling */
    .stButton>button {
        background-color: #00D4FF !important;
        color: #0E1117 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AI SETUP ---
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.sidebar.error("🔑 API Key Missing in Secrets")

# --- APP LOGIC ---
if 'current_song_index' not in st.session_state:
    st.session_state['current_song_index'] = 1255

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Aura DJ Control")
    # Using checkbox instead of toggle for older version compatibility
    pop_toggle = st.checkbox("Prioritize Popular Songs", value=True)
    st.markdown("---")
    count = st.select_slider("Recommendation Depth", options=[3, 5, 7, 10], value=3)

# --- MAIN CONTENT ---
current_song = get_metadata(st.session_state['current_song_index'])

st.title("🎶 Aura Music Discovery")

# Hero Section
st.markdown(f"""
<div class="song-card">
    <h2 style='margin:0;'>NOW EXPLORING</h2>
    <h1 style='margin:10px 0;'>{current_song['track_name']}</h1>
    <h3 style='color:#8B949E !important;'>Artist: {current_song['track_artist']}</h3>
</div>
""", unsafe_allow_html=True)

# Video Player
with st.expander("▶️ CLICK TO WATCH VIDEO", expanded=False):
    with st.spinner("Fetching YouTube Video..."):
        search = VideosSearch(f"{current_song['track_name']} {current_song['track_artist']}", limit=1)
        res = search.result()['result']
        if res:
            st.video(f"https://www.youtube.com/watch?v={res[0]['id']}")
        else:
            st.error("Video not found.")

st.markdown("---")

# RECOMMENDATIONS
st.header("🎯 AI Generated Playlists")
recommendations = hybrid_recommend(st.session_state['current_song_index'], res_count, prioritisePopular=pop_pref)
 
for category, songs in recommendations.items():
    if songs: # Only show category if songs exist
        st.subheader(f"✨ {category.upper()}")
        
        # We process in rows of 3 to prevent "last columns block" layout errors
        for i in range(0, len(songs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(songs):
                    song = songs[i+j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="song-card" style="padding: 15px; border-color: #30363D;">
                            <div class="song-title" style="font-size: 16px;">{song['track_name']}</div>
                            <div class="song-artist" style="font-size: 14px;">{song['track_artist']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        # Navigation Button
                        if st.button("Explore This", key=f"btn_{category}_{i+j}"):
                            st.session_state['current_song_index'] = song['index']
                            # Using experimental_rerun for older version compatibility
                            try:
                                st.rerun()
                            except:
                                st.experimental_rerun()
 
