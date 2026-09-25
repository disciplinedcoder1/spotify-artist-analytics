import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_searchbox import st_searchbox
from api.spotify_utils import SpotifyClient, SpotifyPremiumRequiredError
from core.analysis import SpotifyAnalyzer

def apply_premium_styling():
    """Apply a restrained, single-accent 2026 product aesthetic: flat surfaces,
    generous whitespace, one confident accent color, no glow/gradient noise."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --bg: #ffffff;
            --surface: #fafafa;
            --surface-hover: #f2f2f3;
            --border: rgba(11, 11, 12, 0.10);
            --border-strong: rgba(11, 11, 12, 0.20);
            --text: #0b0b0c;
            --text-muted: rgba(11, 11, 12, 0.58);
            --accent: #1DB954;
            --accent-strong: #169c46;
            --accent-on: #ffffff;
        }

        .main {
            background: var(--bg);
            color: var(--text);
            font-family: 'Inter', -apple-system, sans-serif;
        }

        .main .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1100px;
        }

        h1, h2, h3, h4, p, div, span, label { font-family: 'Inter', -apple-system, sans-serif; }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}

        /* Single-accent emphasis text (used sparingly, not on every header) */
        .startup-accent {
            color: var(--accent-strong);
            font-weight: 700;
        }

        /* Hero */
        .hero-section {
            padding: 1.5rem 0 2.5rem 0;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .hero-title {
            font-size: 2.25rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 0.5rem;
            color: var(--text);
        }

        .hero-subtitle {
            font-size: 1rem;
            color: var(--text-muted);
            font-weight: 400;
        }

        /* Flat surface card */
        .glass-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
        }

        /* Metric cards */
        .metric-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: left;
            transition: border-color 0.15s ease;
            height: 100%;
        }

        .metric-card:hover {
            border-color: var(--border-strong);
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 0.25rem;
            letter-spacing: -0.01em;
            overflow-wrap: break-word;
            line-height: 1.25;
        }

        .metric-label {
            font-size: 0.85rem;
            color: var(--text-muted);
        }

        /* Section titles */
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            letter-spacing: -0.01em;
        }

        .section-subtitle {
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
        }

        /* Streamlit element overrides */
        .stTextInput > div > div > input {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text);
            padding: 0.6rem 1rem;
            font-family: 'Inter', sans-serif;
        }

        .stTextInput > div > div > input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 1px var(--accent);
        }

        .stSelectbox > div > div > div {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text);
        }

        .stButton > button {
            background: var(--accent);
            border: none;
            border-radius: 8px;
            color: var(--accent-on);
            font-weight: 600;
            padding: 0.6rem 1.25rem;
            transition: background 0.15s ease;
            font-family: 'Inter', sans-serif;
        }

        .stButton > button:hover {
            background: var(--accent-strong);
            color: var(--accent-on);
        }

        .stTabs [data-baseweb="tab-list"] {
            background: transparent;
            border-bottom: 1px solid var(--border);
            gap: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 0;
            color: var(--text-muted);
            font-weight: 500;
            padding: 0.6rem 0.25rem;
            margin: 0 0.75rem 0 0;
        }

        .stTabs [aria-selected="true"] {
            background: transparent;
            color: var(--text);
            box-shadow: inset 0 -2px 0 var(--accent);
        }

        /* Chart styling */
        .js-plotly-plot {
            background: var(--surface) !important;
            border-radius: 12px;
            border: 1px solid var(--border);
        }
    </style>
    """, unsafe_allow_html=True)

def create_hero_section():
    """Create a clean, restrained hero header"""
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">
            <span class="startup-accent">Spotify</span> Artist Intelligence
        </h1>
        <p class="hero-subtitle">
            Live artist analytics and discovery, powered by the Spotify API
        </p>
    </div>
    """, unsafe_allow_html=True)

def create_artist_search_with_suggestions(spotify_client, key_suffix=""):
    """Create a live, type-ahead search component backed by the Spotify API"""
    st.markdown("""
    <div class="section-title">Discover Artists</div>
    <div class="section-subtitle">
        Search by name to explore an artist's catalog and analytics
    </div>
    """, unsafe_allow_html=True)

    def _search_artists(searchterm: str):
        if not searchterm or not searchterm.strip():
            return []

        try:
            suggestions = spotify_client.search_artist_suggestions(searchterm, limit=8)
        except SpotifyPremiumRequiredError:
            st.session_state['spotify_premium_blocked'] = True
            return []
        except Exception as e:
            st.session_state['spotify_premium_blocked'] = False
            st.error(f"Search error: {e}")
            return []

        st.session_state['spotify_premium_blocked'] = False
        options = []
        for artist in suggestions:
            followers = artist.get('followers', {}).get('total', 0)
            followers_text = f"{followers:,}" if followers else "N/A"
            genres_text = ", ".join(artist.get('genres', [])[:2]) if artist.get('genres') else "No genres"
            label = f"{artist['name']}  ·  {followers_text} followers  ·  {genres_text}"
            options.append((label, artist))
        return options

    selected_artist = st_searchbox(
        _search_artists,
        key=f"artist_searchbox_{key_suffix}",
        placeholder="Start typing artist name (e.g., Taylor Swift, Drake, Ariana Grande)",
        label="Search for an artist...",
        debounce=150,
        clear_on_submit=False,
    )

    if st.session_state.get('spotify_premium_blocked'):
        st.warning(
            "**Spotify Premium required on the developer account** — the API credentials "
            "powering this app need an active Spotify Premium subscription for search access. "
            "Ask the app owner to upgrade, or check the app's status in the "
            "[Spotify Developer Dashboard](https://developer.spotify.com/dashboard)."
        )

    return selected_artist

def create_premium_metrics_dashboard(artist_data):
    """Display key artist metrics in a compact card row"""
    st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{artist_data['popularity']}</div>
            <div class="metric-label">Popularity Score</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        followers_formatted = f"{artist_data['followers']['total']:,}" if artist_data['followers']['total'] > 0 else "N/A"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{followers_formatted}</div>
            <div class="metric-label">Followers</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        genres_count = len(artist_data['genres'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{genres_count}</div>
            <div class="metric-label">Genres</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        top_genre = artist_data['genres'][0].title() if artist_data.get('genres') else "—"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{top_genre}</div>
            <div class="metric-label">Top Genre</div>
        </div>
        """, unsafe_allow_html=True)

def display_artist_catalog(artist_data, spotify_client, analyzer):
    """Display comprehensive artist catalog with multiple views"""
    
    # Artist overview
    st.markdown(f"## {artist_data['name']}")

    # Premium metrics dashboard
    create_premium_metrics_dashboard(artist_data)

    # Get artist stats for detailed analysis
    try:
        with st.spinner("Analyzing artist catalog..."):
            artist_stats = analyzer.get_artist_stats(artist_data['name'])
    except Exception as e:
        st.error(f"Error loading artist data: {e}")
        st.info("This might be a temporary API issue. Try refreshing or selecting a different artist.")
        return

    if 'error' in artist_stats:
        st.error(f"Error loading artist data: {artist_stats['error']}")
        return

    # Track display options
    track_tabs = st.tabs(["Recent Tracks", "Most Popular", "By Danceability", "By Energy"])

    with track_tabs[0]:
        st.markdown("### Latest Releases")
        display_recent_tracks(artist_stats)

    with track_tabs[1]:
        st.markdown("### Top Tracks")
        display_popular_tracks(artist_stats)

    with track_tabs[2]:
        st.markdown("### Most Danceable Tracks")
        display_tracks_by_feature(artist_stats, "danceability", spotify_client)

    with track_tabs[3]:
        st.markdown("### High Energy Tracks")
        display_tracks_by_feature(artist_stats, "energy", spotify_client)

    # Add to comparison button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"Add {artist_data['name']} to Comparison", type="primary", use_container_width=True):
            if artist_data not in st.session_state.comparison_artists:
                st.session_state.comparison_artists.append(artist_data)
                st.success(f"Added **{artist_data['name']}** to comparison.")
            else:
                st.warning(f"**{artist_data['name']}** is already in comparison.")

def display_recent_tracks(artist_stats):
    """Display recent tracks"""
    if not artist_stats.get('top_tracks'):
        st.info("No tracks available for this artist.")
        return
    
    tracks_data = []
    for track in artist_stats['top_tracks'][:5]:
        release_date = track.get('album', {}).get('release_date', 'Unknown')
        tracks_data.append({
            'Track Name': track['name'],
            'Album': track['album']['name'],
            'Release Date': release_date,
            'Popularity': f"{track['popularity']}/100",
            'Duration': f"{track['duration_ms'] // 60000}:{(track['duration_ms'] % 60000) // 1000:02d}"
        })
    
    df = pd.DataFrame(tracks_data)
    st.dataframe(df, use_container_width=True)

def display_popular_tracks(artist_stats):
    """Display most popular tracks"""
    if not artist_stats.get('top_tracks'):
        st.info("No tracks available for this artist.")
        return
    
    # Sort by popularity
    sorted_tracks = sorted(artist_stats['top_tracks'], key=lambda x: x['popularity'], reverse=True)
    
    tracks_data = []
    for track in sorted_tracks[:5]:
        tracks_data.append({
            'Track Name': track['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Explicit': "Yes" if track['explicit'] else "No",
            'Preview': "Available" if track.get('preview_url') else "Unavailable"
        })
    
    df = pd.DataFrame(tracks_data)
    st.dataframe(df, use_container_width=True)

def display_tracks_by_feature(artist_stats, feature, spotify_client):
    """Display tracks sorted by a specific audio feature"""
    if not artist_stats.get('top_tracks'):
        st.info("No tracks available for this artist.")
        return
    
    # Get audio features for tracks
    track_ids = [track['id'] for track in artist_stats['top_tracks']]
    audio_features = spotify_client.get_multiple_tracks_audio_features(track_ids)
    
    if not audio_features:
        st.info("Audio features not available for this artist's tracks.")
        return
    
    # Combine track info with audio features
    tracks_with_features = []
    for i, track in enumerate(artist_stats['top_tracks']):
        if i < len(audio_features) and audio_features[i]:
            feature_value = audio_features[i].get(feature, 0)
            tracks_with_features.append({
                'Track Name': track['name'],
                'Album': track['album']['name'],
                f'{feature.capitalize()}': f"{feature_value:.3f}",
                'Popularity': track['popularity'],
                'feature_val': feature_value  # For sorting
            })
    
    # Sort by feature value
    tracks_with_features.sort(key=lambda x: x['feature_val'], reverse=True)
    
    # Remove the sorting column and display
    for track in tracks_with_features:
        del track['feature_val']
    
    df = pd.DataFrame(tracks_with_features[:5])
    st.dataframe(df, use_container_width=True)

def display_comparison_cart():
    """Show current comparison cart and comparison options"""
    if st.session_state.comparison_artists:
        st.markdown("### Artists in Comparison")

        for i, artist in enumerate(st.session_state.comparison_artists):
            col1, col2 = st.columns([4, 1])
            with col1:
                followers_text = f"{artist['followers']['total']:,}" if artist['followers']['total'] > 0 else "N/A"
                st.markdown(f"**{artist['name']}** ({followers_text} followers)")
            with col2:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.comparison_artists.pop(i)
                    st.rerun()

        if len(st.session_state.comparison_artists) >= 2:
            st.markdown("---")
            if st.button("Compare All Artists", type="primary", use_container_width=True):
                display_multi_artist_comparison()

def display_multi_artist_comparison():
    """Display comparison of multiple artists"""
    st.markdown("### Multi-Artist Comparison")
    
    artists = st.session_state.comparison_artists
    if len(artists) < 2:
        st.warning("Please add at least 2 artists to compare.")
        return
    
    # Create comparison data
    comparison_data = []
    for artist in artists:
        comparison_data.append({
            'Artist': artist['name'],
            'Popularity': artist['popularity'],
            'Followers': artist['followers']['total'],
            'Genres': len(artist['genres'])
        })
    
    df = pd.DataFrame(comparison_data)
    
    # Display comparison table
    st.dataframe(df, use_container_width=True)
    
    # Create comparison charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pop = px.bar(df, x='Artist', y='Popularity',
                        title="Popularity Comparison",
                        color_discrete_sequence=['#1DB954'])
        fig_pop.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#0b0b0c'
        )
        st.plotly_chart(fig_pop, use_container_width=True)

    with col2:
        fig_followers = px.bar(df, x='Artist', y='Followers',
                              title="Followers Comparison",
                              color_discrete_sequence=['#0b0b0c'])
        fig_followers.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#0b0b0c'
        )
        st.plotly_chart(fig_followers, use_container_width=True)

def lazy_load_spotify():
    """Lazy load Spotify client only when needed"""
    if 'spotify_client' not in st.session_state:
        try:
            spotify_client = SpotifyClient()
            analyzer = SpotifyAnalyzer(spotify_client)
            
            st.session_state.spotify_client = spotify_client
            st.session_state.analyzer = analyzer
            st.session_state.spotify_connected = True

            return True
        except Exception as e:
            st.session_state.spotify_connected = False
            st.error(f"Spotify connection error: {e}")
            st.info("Please check your Spotify API credentials in the .env file.")
            return False
    return st.session_state.get('spotify_connected', False)

def main():
    st.set_page_config(
        page_title="Spotify Artist Intelligence",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply premium styling immediately
    apply_premium_styling()
    
    # Create hero section
    create_hero_section()
    
    # Initialize session state
    if 'comparison_artists' not in st.session_state:
        st.session_state.comparison_artists = []
    if 'selected_artist' not in st.session_state:
        st.session_state.selected_artist = None

    try:
        if not lazy_load_spotify():
            return

        spotify_client = st.session_state.spotify_client
        analyzer = st.session_state.analyzer

        tab1, tab2, tab3 = st.tabs(["Artist Explorer", "Song Analysis", "Feature Distribution"])

        with tab1:
            # Artist Explorer - Premium version
            selected_artist = create_artist_search_with_suggestions(spotify_client, "main")

            if selected_artist:
                st.session_state.selected_artist = selected_artist
                display_artist_catalog(selected_artist, spotify_client, analyzer)

            # Show comparison cart if not empty
            if st.session_state.comparison_artists:
                st.markdown("---")
                display_comparison_cart()

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
                 title=f"Average Audio Features for {distribution['artist']}",
                 color_discrete_sequence=['#1DB954'])
    fig.update_layout(
        xaxis_tickangle=-45,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#0b0b0c'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df, use_container_width=True)

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
            line_color='#1DB954'
        ))

        fig.add_trace(go.Scatterpolar(
            r=song2_values,
            theta=feature_labels,
            fill='toself',
            name='Song 2',
            line_color='#6366F1'
        ))

        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 1],
                    gridcolor='rgba(11, 11, 12, 0.12)',
                    tickfont=dict(color='#0b0b0c')
                ),
                angularaxis=dict(
                    gridcolor='rgba(11, 11, 12, 0.12)',
                    tickfont=dict(color='#0b0b0c')
                )
            ),
            showlegend=True,
            title="Audio Features Comparison",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#0b0b0c'
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()