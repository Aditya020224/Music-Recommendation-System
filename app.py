import streamlit as st
from recommender import hybrid_recommend, get_metadata
from youtubesearchpython import VideosSearch

dataset_url = 'https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs'

st.set_page_config(
    page_title='Music Recommendation System', 
    page_icon='🎶',
    menu_items={
        'Get Help': None,
        'Report a bug': 'https://github.com/Aditya020224/Music-Recommendation-System/issues' 
    }
)

st.title('Music Recommendation System')



def change_song(index):
    st.session_state['current_song_index'] = index

if 'current_song_index' not in st.session_state:
    change_song(1255)

st.markdown(
    """
    <style>
   
    /* Make the sidebar transparent */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05); /* Very slight white tint */
        backdrop-filter: blur(10px); /* Optional: adds a glass effect */
    }
 
    /* Optional: Change text colors to match your theme */
    .stMarkdown, p, h1, h2, h3 {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title('Select :')

option1 = 'Trending'
option2 = 'Hidden songs'
mode = st.sidebar.selectbox('Your recommendation Modes', (option1, option2))
if(mode == option1):
    prioritisePopular = True
else:
    prioritisePopular = False

recommendations_count = st.sidebar.slider('How many delightful recommendations of each kind would you prefer to receive '
'(lesser means more accurate but more means more variety!)', min_value=1, max_value=10, value=3)

st.sidebar.write('What types of recommendations would you prefer')




current_song = get_metadata(st.session_state['current_song_index'])

st.write(f'## {current_song["track_name"]} - {current_song["track_artist"]}')

youtube_search = VideosSearch(f'## {current_song["track_name"]} - {current_song["track_artist"]}', limit = 1)
youtube_id = youtube_search.result()['result'][0]['id']
thumbnail_url = youtube_search.result()['result'][0]['thumbnails'][0]['url']

st.write(f'[![YouTube thumbnail]({thumbnail_url})](https://www.youtube.com/watch?v={youtube_id})')
st.write(f'[Hear on YouTube](https://www.youtube.com/watch?v={youtube_id})')

with st.expander('Show lyrics'):
    st.write(current_song['lyrics'])



recommendations = hybrid_recommend(st.session_state['current_song_index'], recommendations_count, prioritisePopular=prioritisePopular)

for recommendation_type, songs in recommendations.items():
    if not st.sidebar.checkbox(recommendation_type, value=True):
        continue
    if(len(songs) == 0): 
        continue
    st.write(f'#### {recommendation_type.title()}')
    with st.container():
        for song in songs:
            st.write(f'- {song["track_name"]} - {song["track_artist"]}')
            st.button("listen", key=str(song['index'])+recommendation_type, on_click=change_song, args=(song['index'],))
