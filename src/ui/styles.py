"""
Matrix-themed styling system for Song Analytics Dashboard
"""

import streamlit as st

# Matrix color palette
COLORS = {
    # Matrix greens
    'matrix_green': '#00FF41',
    'matrix_dark_green': '#008F11',
    'matrix_bright': '#39FF14',
    'matrix_dim': '#003300',
    
    # Matrix blacks and grays
    'matrix_black': '#000000',
    'matrix_dark': '#0a0a0a',
    'matrix_gray': '#1a1a1a',
    'matrix_light_gray': '#2a2a2a',
    
    # Accent colors
    'matrix_red': '#FF0000',
    'matrix_blue': '#0066FF',
    'matrix_white': '#FFFFFF',
    'matrix_cyan': '#00FFFF'
}

def load_css():
    """Load Matrix-themed CSS styling"""
    css = f"""
    <style>
    /* Import Matrix-style fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Courier+Prime:wght@400;700&display=swap');
    
    /* Global Matrix Theme */
    .main {{
        background: {COLORS['matrix_black']};
        color: {COLORS['matrix_green']};
        font-family: 'Courier Prime', monospace;
        padding: 0;
    }}
    
    /* Matrix Rain Effect Background */
    .matrix-bg {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: {COLORS['matrix_black']};
        background-image: 
            radial-gradient(2px 2px at 20px 30px, {COLORS['matrix_dim']}, transparent),
            radial-gradient(2px 2px at 40px 70px, {COLORS['matrix_dim']}, transparent),
            radial-gradient(1px 1px at 90px 40px, {COLORS['matrix_dim']}, transparent),
            radial-gradient(1px 1px at 130px 80px, {COLORS['matrix_dim']}, transparent),
            radial-gradient(2px 2px at 160px 30px, {COLORS['matrix_dim']}, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: matrixScroll 20s linear infinite;
    }}
    
    @keyframes matrixScroll {{
        0% {{ background-position: 0 0; }}
        100% {{ background-position: 0 100px; }}
    }}
    
    /* Matrix Header */
    .matrix-header {{
        background: linear-gradient(135deg, {COLORS['matrix_black']} 0%, {COLORS['matrix_dark']} 50%, {COLORS['matrix_black']} 100%);
        border: 2px solid {COLORS['matrix_green']};
        border-radius: 0;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 
            0 0 20px {COLORS['matrix_green']},
            inset 0 0 20px rgba(0, 255, 65, 0.1);
        animation: matrixPulse 3s ease-in-out infinite;
    }}
    
    @keyframes matrixPulse {{
        0%, 100% {{ box-shadow: 0 0 20px {COLORS['matrix_green']}, inset 0 0 20px rgba(0, 255, 65, 0.1); }}
        50% {{ box-shadow: 0 0 40px {COLORS['matrix_bright']}, inset 0 0 30px rgba(0, 255, 65, 0.2); }}
    }}
    
    .matrix-header h1 {{
        color: {COLORS['matrix_bright']};
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 2.8rem;
        margin: 0;
        text-shadow: 0 0 10px {COLORS['matrix_green']};
        letter-spacing: 3px;
    }}
    
    .matrix-header p {{
        color: {COLORS['matrix_green']};
        font-size: 1.1rem;
        margin: 1rem 0 0 0;
        font-family: 'Courier Prime', monospace;
        text-shadow: 0 0 5px {COLORS['matrix_green']};
    }}
    
    /* Matrix Track Cards */
    .matrix-track {{
        background: linear-gradient(135deg, {COLORS['matrix_dark']} 0%, {COLORS['matrix_black']} 100%);
        border: 1px solid {COLORS['matrix_green']};
        margin: 1rem 0;
        padding: 1.5rem;
        position: relative;
        transition: all 0.3s ease;
        font-family: 'Courier Prime', monospace;
    }}
    
    .matrix-track:hover {{
        border-color: {COLORS['matrix_bright']};
        box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        transform: translateX(5px);
    }}
    
    .matrix-track::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: {COLORS['matrix_green']};
        animation: matrixScan 2s linear infinite;
    }}
    
    @keyframes matrixScan {{
        0% {{ background: {COLORS['matrix_green']}; }}
        50% {{ background: {COLORS['matrix_bright']}; }}
        100% {{ background: {COLORS['matrix_green']}; }}
    }}
    
    /* Matrix MOON Track Highlight */
    .matrix-moon {{
        border: 2px solid {COLORS['matrix_cyan']};
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, {COLORS['matrix_black']} 100%);
        animation: moonMatrix 1.5s ease-in-out infinite alternate;
    }}
    
    @keyframes moonMatrix {{
        0% {{ box-shadow: 0 0 15px rgba(0, 255, 255, 0.3); }}
        100% {{ box-shadow: 0 0 30px rgba(0, 255, 255, 0.6); }}
    }}
    
    .matrix-moon::before {{
        background: {COLORS['matrix_cyan']};
    }}
    
    /* Matrix Metrics */
    .matrix-metric {{
        background: {COLORS['matrix_black']};
        border: 1px solid {COLORS['matrix_green']};
        padding: 1.5rem;
        text-align: center;
        position: relative;
        transition: all 0.3s ease;
    }}
    
    .matrix-metric:hover {{
        border-color: {COLORS['matrix_bright']};
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
    }}
    
    .matrix-metric-value {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {COLORS['matrix_bright']};
        font-family: 'Orbitron', monospace;
        text-shadow: 0 0 10px {COLORS['matrix_green']};
    }}
    
    .matrix-metric-label {{
        font-size: 0.9rem;
        color: {COLORS['matrix_green']};
        margin-top: 0.5rem;
        font-family: 'Courier Prime', monospace;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Matrix Progress Bars */
    .matrix-progress {{
        background: {COLORS['matrix_dark']};
        height: 6px;
        margin: 0.5rem 0;
        position: relative;
        overflow: hidden;
    }}
    
    .matrix-progress-bar {{
        height: 100%;
        background: linear-gradient(90deg, {COLORS['matrix_green']} 0%, {COLORS['matrix_bright']} 100%);
        position: relative;
        animation: matrixFlow 2s ease-in-out infinite;
    }}
    
    @keyframes matrixFlow {{
        0% {{ box-shadow: 0 0 5px {COLORS['matrix_green']}; }}
        50% {{ box-shadow: 0 0 15px {COLORS['matrix_bright']}; }}
        100% {{ box-shadow: 0 0 5px {COLORS['matrix_green']}; }}
    }}
    
    /* Matrix Text Styles */
    .matrix-title {{
        color: {COLORS['matrix_bright']};
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1.4rem;
        text-shadow: 0 0 8px {COLORS['matrix_green']};
        margin-bottom: 0.5rem;
    }}
    
    .matrix-subtitle {{
        color: {COLORS['matrix_green']};
        font-family: 'Courier Prime', monospace;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }}
    
    .matrix-data {{
        color: {COLORS['matrix_green']};
        font-family: 'Courier Prime', monospace;
        font-size: 0.85rem;
        line-height: 1.4;
    }}
    
    .matrix-highlight {{
        color: {COLORS['matrix_bright']};
        text-shadow: 0 0 5px {COLORS['matrix_green']};
    }}
    
    /* Matrix Artist Cards */
    .matrix-artist {{
        background: linear-gradient(135deg, {COLORS['matrix_dark']} 0%, {COLORS['matrix_black']} 100%);
        border: 1px solid {COLORS['matrix_green']};
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        transition: all 0.3s ease;
    }}
    
    .matrix-artist:hover {{
        border-color: {COLORS['matrix_bright']};
        box-shadow: 0 0 25px rgba(0, 255, 65, 0.2);
        transform: scale(1.02);
    }}
    
    .matrix-artist-name {{
        color: {COLORS['matrix_bright']};
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 8px {COLORS['matrix_green']};
    }}
    
    /* Matrix Welcome Screen */
    .matrix-welcome {{
        background: linear-gradient(135deg, {COLORS['matrix_black']} 0%, {COLORS['matrix_dark']} 50%, {COLORS['matrix_black']} 100%);
        border: 2px solid {COLORS['matrix_green']};
        padding: 3rem;
        margin: 2rem 0;
        text-align: center;
        position: relative;
        animation: matrixWelcome 4s ease-in-out infinite;
    }}
    
    @keyframes matrixWelcome {{
        0%, 100% {{ box-shadow: 0 0 30px rgba(0, 255, 65, 0.2); }}
        50% {{ box-shadow: 0 0 50px rgba(0, 255, 65, 0.4); }}
    }}
    
    .matrix-welcome h2 {{
        color: {COLORS['matrix_bright']};
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: 2.2rem;
        margin-bottom: 1rem;
        text-shadow: 0 0 15px {COLORS['matrix_green']};
        letter-spacing: 2px;
    }}
    
    .matrix-welcome p {{
        color: {COLORS['matrix_green']};
        font-family: 'Courier Prime', monospace;
        font-size: 1rem;
        line-height: 1.6;
        margin: 1rem 0;
    }}
    
    .matrix-welcome ul {{
        color: {COLORS['matrix_green']};
        font-family: 'Courier Prime', monospace;
        text-align: left;
        max-width: 400px;
        margin: 2rem auto;
    }}
    
    .matrix-welcome li {{
        margin: 0.5rem 0;
        position: relative;
        padding-left: 20px;
    }}
    
    .matrix-welcome li::before {{
        content: '>';
        position: absolute;
        left: 0;
        color: {COLORS['matrix_bright']};
        font-weight: bold;
    }}
    
    /* Remove Streamlit Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{visibility: hidden;}}
    
    /* Matrix Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {COLORS['matrix_black']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {COLORS['matrix_green']};
        border-radius: 0;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['matrix_bright']};
        box-shadow: 0 0 5px {COLORS['matrix_green']};
    }}
    
    /* Override Streamlit Styling */
    .stSelectbox > div > div {{
        background: {COLORS['matrix_black']};
        border: 1px solid {COLORS['matrix_green']};
        color: {COLORS['matrix_green']};
    }}
    
    .stTextInput > div > div > input {{
        background: {COLORS['matrix_black']};
        border: 1px solid {COLORS['matrix_green']};
        color: {COLORS['matrix_green']};
        font-family: 'Courier Prime', monospace;
    }}
    
    .stButton > button {{
        background: {COLORS['matrix_black']};
        border: 2px solid {COLORS['matrix_green']};
        color: {COLORS['matrix_green']};
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background: {COLORS['matrix_green']};
        color: {COLORS['matrix_black']};
        box-shadow: 0 0 15px {COLORS['matrix_green']};
    }}
    
    /* Matrix Data Grid */
    .matrix-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }}
    
    .matrix-cell {{
        background: {COLORS['matrix_black']};
        border: 1px solid {COLORS['matrix_green']};
        padding: 1rem;
        font-family: 'Courier Prime', monospace;
        transition: all 0.3s ease;
    }}
    
    .matrix-cell:hover {{
        border-color: {COLORS['matrix_bright']};
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    }}
    
    .matrix-cell-label {{
        color: {COLORS['matrix_green']};
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }}
    
    .matrix-cell-value {{
        color: {COLORS['matrix_bright']};
        font-size: 1.2rem;
        font-weight: bold;
        text-shadow: 0 0 5px {COLORS['matrix_green']};
    }}
    </style>
    
    <div class="matrix-bg"></div>
    """
    st.markdown(css, unsafe_allow_html=True)

def create_matrix_header(title, subtitle=""):
    """Create Matrix-themed header"""
    return f"""
    <div class="matrix-header">
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """

def create_matrix_metric(value, label, icon=""):
    """Create Matrix-themed metric card"""
    return f"""
    <div class="matrix-metric">
        <div class="matrix-metric-value">{icon} {value}</div>
        <div class="matrix-metric-label">{label}</div>
    </div>
    """

def display_matrix_track_card(track, rank):
    """Display Matrix-themed track card with audio feature expander"""
    import streamlit as st

    is_moon = track.get('is_moon_track', False)
    moon_prefix = "[MOON] " if is_moon else f"[{rank:02d}] "

    # Format data
    duration = track.get('duration_formatted', 'Unknown')
    popularity = track.get('popularity', 0)
    album = track.get('album_name', 'Unknown')
    year = track.get('release_year', 'Unknown')

    # Create container with Matrix styling
    container_class = "matrix-track-container matrix-track-moon" if is_moon else "matrix-track-container"
    
    with st.container():
        st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
        
        # Title
        st.markdown(f'<div class="matrix-track-title">{moon_prefix}{track["name"]}</div>', unsafe_allow_html=True)
        
        # Subtitle  
        st.markdown(f'<div class="matrix-track-subtitle">Album: {album} ({year})</div>', unsafe_allow_html=True)
        
        # Main data grid
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            **POPULARITY**  
            `{popularity}/100`  
            *{track.get('popularity_category', 'Unknown')}*
            """)
            
        with col2:
            st.markdown(f"""
            **DURATION**  
            `{duration}`  
            *{track.get('duration_category', 'Unknown')}*
            """)
            
        with col3:
            st.markdown(f"""
            **ALBUM TYPE**  
            `{track.get('album_type', 'Unknown').title()}`  
            *Track {track.get('track_number', '?')} of {track.get('album_total_tracks', '?')}*
            """)
            
        with col4:
            explicit = "Yes" if track.get('explicit', False) else "No"
            preview = "Available" if track.get('preview_url') else "None"
            st.markdown(f"""
            **CONTENT**  
            `Explicit: {explicit}`  
            *Preview: {preview}*
            """)

        # Expander for Audio Features
        with st.expander("AUDIO FEATURES ANALYSIS"):
            audio_features_grid = st.columns(3)
            
            features_to_display = {
                'danceability': 'Danceability',
                'energy': 'Energy',
                'valence': 'Valence (Positivity)',
                'acousticness': 'Acousticness',
                'instrumentalness': 'Instrumentalness',
                'speechiness': 'Speechiness'
            }
            
            for i, (key, label) in enumerate(features_to_display.items()):
                with audio_features_grid[i % 3]:
                    value = track.get(key)
                    if value is not None:
                        st.metric(label=label, value=f"{value:.2f}")
                    else:
                        st.metric(label=label, value="N/A")
        
        st.markdown('</div>', unsafe_allow_html=True)

def create_matrix_welcome():
    """Create Matrix-themed welcome screen"""
    return """
    <div class="matrix-welcome">
        <h2>SONG ANALYTICS MATRIX</h2>
        <p>Access the digital music database</p>
        <ul>
            <li>Track popularity analysis</li>
            <li>Duration pattern recognition</li>
            <li>Release timeline mapping</li>
            <li>MOON track identification</li>
            <li>Artist catalog scanning</li>
            <li>Real-time data visualization</li>
        </ul>
        <p class="matrix-highlight">Initialize search protocol →</p>
    </div>
    """

def create_matrix_artist_card(artist, has_moon=False):
    """Create Matrix-themed artist selection card"""
    moon_indicator = "[MOON DETECTED]" if has_moon else "[STANDARD]"
    
    return f"""
    <div class="matrix-artist">
        <div class="matrix-artist-name">{moon_indicator} {artist['name']}</div>
        <div class="matrix-data">
            Followers: <span class="matrix-highlight">{artist.get('followers', 0):,}</span><br>
            Popularity: <span class="matrix-highlight">{artist.get('popularity', 0)}/100</span><br>
            ID: <span style="font-size: 0.7rem;">{artist['id'][:16]}...</span>
        </div>
        {f'<div class="matrix-data matrix-highlight">🌙 MOON tracks available</div>' if has_moon else ''}
    </div>
    """