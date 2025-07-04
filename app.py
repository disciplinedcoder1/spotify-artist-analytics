import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from spotify_utils import SpotifyClient
from analysis import SpotifyAnalyzer

def main():
    st.set_page_config(page_title="Spotify Artist Comparison", layout="wide")
    
    st.title("Spotify Artist & Song Comparison Tool")
    st.markdown("Compare artists, analyze songs, and discover musical similarities using Spotify data.")
    
    try:
        spotify_client = SpotifyClient()
        analyzer = SpotifyAnalyzer(spotify_client)
        
        tab1, tab2, tab3 = st.tabs(["Artist Comparison", "Song Analysis", "Feature Distribution"])
        
        with tab1:
            st.header("Compare Artists")
            
            col1, col2 = st.columns(2)
            
            with col1:
                target_artist = st.text_input("Target Artist", placeholder="e.g., Taylor Swift")
            
            with col2:
                comparison_artist = st.text_input("Comparison Artist", placeholder="e.g., Ariana Grande")
            
            if st.button("Compare Artists", type="primary"):
                if target_artist and comparison_artist:
                    with st.spinner("Analyzing artists..."):
                        comparison_result = analyzer.compare_artist_to_top_songs(target_artist, comparison_artist)
                        
                        if 'error' in comparison_result:
                            st.error(comparison_result['error'])
                        else:
                            display_artist_comparison(comparison_result)
                else:
                    st.warning("Please enter both artist names.")
        
        with tab2:
            st.header("Individual Song Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                song_artist = st.text_input("Artist Name", placeholder="e.g., The Beatles")
                song_name = st.text_input("Song Name", placeholder="e.g., Hey Jude")
            
            with col2:
                comp_song_artist = st.text_input("Compare with Artist", placeholder="e.g., Queen")
                comp_song_name = st.text_input("Compare with Song", placeholder="e.g., Bohemian Rhapsody")
            
            if st.button("Compare Songs", type="primary"):
                if all([song_artist, song_name, comp_song_artist, comp_song_name]):
                    with st.spinner("Analyzing songs..."):
                        song1 = spotify_client.search_track(song_name, song_artist)
                        song2 = spotify_client.search_track(comp_song_name, comp_song_artist)
                        
                        if song1 and song2:
                            song1_features = spotify_client.get_track_audio_features(song1['id'])
                            song2_features = spotify_client.get_track_audio_features(song2['id'])
                            
                            song1_data = {
                                'name': song1['name'],
                                'artists': song1['artists'],
                                'popularity': song1['popularity'],
                                'audio_features': song1_features
                            }
                            
                            song2_data = {
                                'name': song2['name'],
                                'artists': song2['artists'],
                                'popularity': song2['popularity'],
                                'audio_features': song2_features
                            }
                            
                            comparison = analyzer.compare_songs(song1_data, song2_data)
                            display_song_comparison(comparison)
                        else:
                            st.error("Could not find one or both songs. Please check the names and try again.")
                else:
                    st.warning("Please fill in all fields.")
        
        with tab3:
            st.header("Artist Feature Distribution")
            
            artist_for_distribution = st.text_input("Artist Name for Analysis", placeholder="e.g., Drake")
            
            if st.button("Analyze Features", type="primary"):
                if artist_for_distribution:
                    with st.spinner("Analyzing artist features..."):
                        distribution = analyzer.get_feature_distribution(artist_for_distribution)
                        
                        if 'error' in distribution:
                            st.error(distribution['error'])
                        else:
                            display_feature_distribution(distribution)
                else:
                    st.warning("Please enter an artist name.")
    
    except Exception as e:
        st.error(f"Error initializing Spotify client: {e}")
        st.info("Please check your Spotify API credentials in the .env file.")

def display_artist_comparison(comparison_result):
    """Display the results of artist comparison"""
    st.subheader(f"{comparison_result['target_artist']} vs {comparison_result['comparison_artist']}")
    
    target_song = comparison_result['target_song']
    st.write(f"**Target Song:** {target_song['name']} by {target_song['artists'][0]['name']}")
    st.write(f"**Popularity:** {target_song['popularity']}/100")
    
    st.subheader("Most Similar Songs")
    
    for i, comp in enumerate(comparison_result['comparisons'][:3]):
        if 'error' not in comp:
            with st.expander(f"#{i+1} - {comp['song2']['name']} (Similarity: {comp['similarity_score']:.2%})"):
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Song Details:**")
                    st.write(f"Artist: {comp['song2']['artist']}")
                    st.write(f"Popularity: {comp['song2']['popularity']}/100")
                
                with col2:
                    st.write("**Feature Comparison:**")
                    features_df = pd.DataFrame([
                        {'Feature': k, 'Target Song': v['song1'], 'Comparison Song': v['song2'], 'Difference': v['difference']}
                        for k, v in comp['feature_comparison'].items()
                        if k in ['danceability', 'energy', 'valence', 'acousticness']
                    ])
                    st.dataframe(features_df, use_container_width=True)
    
    create_similarity_chart(comparison_result['comparisons'])

def display_song_comparison(comparison):
    """Display the results of individual song comparison"""
    if 'error' in comparison:
        st.error(comparison['error'])
        return
    
    st.subheader("Song Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Song 1:**")
        st.write(f"Song: {comparison['song1']['name']}")
        st.write(f"Artist: {comparison['song1']['artist']}")
        st.write(f"Popularity: {comparison['song1']['popularity']}/100")
    
    with col2:
        st.write("**Song 2:**")
        st.write(f"Song: {comparison['song2']['name']}")
        st.write(f"Artist: {comparison['song2']['artist']}")
        st.write(f"Popularity: {comparison['song2']['popularity']}/100")
    
    st.metric("Overall Similarity", f"{comparison['similarity_score']:.2%}")
    
    create_feature_comparison_chart(comparison['feature_comparison'])

def display_feature_distribution(distribution):
    """Display feature distribution for an artist"""
    st.subheader(f"Feature Analysis for {distribution['artist']}")
    st.write(f"Based on {distribution['track_count']} top tracks")
    
    features_data = []
    for feature, stats in distribution['feature_distribution'].items():
        if feature in ['danceability', 'energy', 'valence', 'acousticness', 'speechiness', 'instrumentalness', 'liveness']:
            features_data.append({
                'Feature': feature.capitalize(),
                'Mean': stats['mean'],
                'Std Dev': stats['std'],
                'Min': stats['min'],
                'Max': stats['max']
            })
    
    df = pd.DataFrame(features_data)
    
    fig = px.bar(df, x='Feature', y='Mean', error_y='Std Dev',
                 title=f"Average Audio Features for {distribution['artist']}")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df, use_container_width=True)

def create_similarity_chart(comparisons):
    """Create a chart showing similarity scores"""
    if not comparisons:
        return
    
    similarity_data = []
    for comp in comparisons:
        if 'error' not in comp:
            similarity_data.append({
                'Song': comp['song2']['name'],
                'Artist': comp['song2']['artist'],
                'Similarity Score': comp['similarity_score']
            })
    
    if similarity_data:
        df = pd.DataFrame(similarity_data)
        fig = px.bar(df, x='Song', y='Similarity Score', 
                     title="Similarity Scores with Comparison Songs",
                     hover_data=['Artist'])
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

def create_feature_comparison_chart(feature_comparison):
    """Create a radar chart comparing audio features"""
    features = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness']
    
    song1_values = []
    song2_values = []
    feature_labels = []
    
    for feature in features:
        if feature in feature_comparison:
            song1_values.append(feature_comparison[feature]['song1'])
            song2_values.append(feature_comparison[feature]['song2'])
            feature_labels.append(feature.capitalize())
    
    if song1_values and song2_values:
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=song1_values,
            theta=feature_labels,
            fill='toself',
            name='Song 1',
            line_color='blue'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=song2_values,
            theta=feature_labels,
            fill='toself',
            name='Song 2',
            line_color='red'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            title="Audio Features Comparison"
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()