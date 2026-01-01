import streamlit as st
import pickle

# Load data
games = pickle.load(open('games_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Initialize History in Session State if it doesn't exist
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("🎮 Personalized Steam Matchmaker")

# Sidebar: Search History
st.sidebar.header("Your Recent Searches")
for h_game in st.session_state.history[-5:]: # Show last 5
    st.sidebar.write(f"• {h_game}")

# Main Search
selected_game = st.selectbox("Search for a game:", games['title'].values)

if st.button('Recommend'):
    # Add to history
    if selected_game not in st.session_state.history:
        st.session_state.history.append(selected_game)
    
    # Logic to show recommendations (as done before)
    idx = games[games['title'] == selected_game].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    
    st.subheader(f"Because you liked {selected_game}:")
    cols = st.columns(5)
    for i in range(1, 6):
        with cols[i-1]:
            game_data = games.iloc[distances[i][0]]
            st.image(f"https://cdn.akamai.steamstatic.com/steam/apps/{game_data.app_id}/header.jpg")
            st.write(game_data.title)

# FEATURE: Recommendations based on ALL previous searches
if st.session_state.history:
    st.divider()
    st.subheader("Recommended based on your history")
    
    # Pick a random game from history to "Feature"
    import random
    featured_base = random.choice(st.session_state.history)
    st.caption(f"Inspired by your interest in {featured_base}")
    
    f_idx = games[games['title'] == featured_base].index[0]
    f_distances = sorted(list(enumerate(similarity[f_idx])), reverse=True, key=lambda x: x[1])
    
    f_cols = st.columns(5)
    for i in range(6, 11): # Show different games than the primary search
        with f_cols[i-6]:
            f_game = games.iloc[f_distances[i][0]]
            st.image(f"https://cdn.akamai.steamstatic.com/steam/apps/{f_game.app_id}/header.jpg")
            st.write(f_game.title)