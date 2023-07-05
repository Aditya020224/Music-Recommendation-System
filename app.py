import streamlit as st
from recommender import hybrid_recommend, get_metadata
from youtubesearchpython import VideosSearch

dataset_url = 'https://www.kaggle.com/datasets/imuhammad/audio-features-and-lyrics-of-spotify-songs'

st.set_page_config(
    page_title='Customizable Music Recommendation System', 
    page_icon='🎶',
    menu_items={
        'Get Help': None,
        'Report a bug': 'https://github.com/N-Shar-ma/Customizable-Music-Recommendation-System/issues',
        'About': f"### Project made as part of Microsoft Engage'22!\n#### Music Data sourced from [Kaggle]({dataset_url})"
    }
)

st.title('Customizable Music Recommendation System')



# Persistent app state managment

def change_song(index):
    st.session_state['current_song_index'] = index

if 'current_song_index' not in st.session_state:
    change_song(1255)



# Sidebar with customizing options

st.sidebar.title('Choose:')

option1 = 'Keep up with what\'s trending'
option2 = 'Discover hidden gems'
mode = st.sidebar.selectbox('Your mode of recommendations', (option1, option2))
if(mode == option1):
    prioritisePopular = True
else:
    prioritisePopular = False

recommendations_count = st.sidebar.slider('Upto how many of each kind of recommendations would you like '
'(lesser means more accurate but more means more variety!)', min_value=1, max_value=10, value=3)

st.sidebar.write('Which kinds of recommendations you\'d like') # options added later below when adding songs



# Main Content:


# Showing current song

current_song = get_metadata(st.session_state['current_song_index'])

st.write(f'## {current_song["track_name"]} - {current_song["track_artist"]}')

youtube_search = VideosSearch(f'## {current_song["track_name"]} - {current_song["track_artist"]}', limit = 1)
youtube_id = youtube_search.result()['result'][0]['id'] # getting youtube link
thumbnail_url = youtube_search.result()['result'][0]['thumbnails'][0]['url'] # getting youtube thumbnail

st.write(f'[![YouTube thumbnail]({thumbnail_url})](https://www.youtube.com/watch?v={youtube_id})')
st.write(f'[Hear on YouTube](https://www.youtube.com/watch?v={youtube_id})')

with st.expander('Show lyrics'):
    st.write(current_song['lyrics'])


# Retreiving and showing recommendations as per user's choices

recommendations = hybrid_recommend(st.session_state['current_song_index'], recommendations_count, prioritisePopular=prioritisePopular)

for recommendation_type, songs in recommendations.items():
    if not st.sidebar.checkbox(recommendation_type, value=True):
        continue
    if(len(songs) == 0): # do not show a recommendation type if it has no songs
        continue
    st.write(f'#### {recommendation_type.title()}')
    with st.container():
        for song in songs:
            st.write(f'- {song["track_name"]} - {song["track_artist"]}')
            st.button("listen", key=str(song['index'])+recommendation_type, on_click=change_song, args=(song['index'],))
