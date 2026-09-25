import os
import spotipy
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv, find_dotenv
from typing import Dict, List, Optional, Any
from .reccobeats_client import ReccoBeatsClient

load_dotenv(find_dotenv())


class SpotifyPremiumRequiredError(Exception):
    """Raised when Spotify rejects a request because the developer account
    behind SPOTIPY_CLIENT_ID/SPOTIPY_CLIENT_SECRET needs an active Premium
    subscription for this endpoint."""
    pass


def _is_premium_required(e: Exception) -> bool:
    return (
        isinstance(e, SpotifyException)
        and e.http_status == 403
        and 'premium subscription required' in (e.msg or '').lower()
    )


class SpotifyClient:
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.client_id = client_id or os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIPY_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not found in environment variables")
        
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Initialize ReccoBeats client for audio features (lazy loading)
        self.reccobeats = None

        # In-memory cache for live-typing suggestions, keyed by (query, limit)
        self._suggestion_cache: Dict[tuple, List[Dict[str, Any]]] = {}

    def search_artist_suggestions(self, artist_name: str, limit: int = 8) -> List[Dict[str, Any]]:
        """Search for artists by name and return full artist data, ranked by relevance to the query."""
        if not artist_name or not artist_name.strip():
            return []

        query = artist_name.strip()
        cache_key = (query.lower(), limit)
        if cache_key in self._suggestion_cache:
            return self._suggestion_cache[cache_key]

        try:
            # Plain query (no field filter) matches Spotify's own fuzzy/partial
            # matching much better than a strict `artist:` filter, which was
            # causing real artists to come back empty for partial names.
            results = self.sp.search(q=query, type='artist', limit=limit)
            artists = results.get('artists', {}).get('items', [])

            query_lower = query.lower()

            def relevance(artist: Dict[str, Any]) -> tuple:
                name_lower = artist.get('name', '').lower()
                popularity = artist.get('popularity', 0)
                if name_lower == query_lower:
                    tier = 0
                elif name_lower.startswith(query_lower):
                    tier = 1
                elif query_lower in name_lower:
                    tier = 2
                else:
                    tier = 3
                return (tier, -popularity)

            seen_ids = set()
            suggestions = []
            for artist in sorted(artists, key=relevance):
                artist_id = artist.get('id')
                if artist_id and artist_id not in seen_ids:
                    suggestions.append(artist)
                    seen_ids.add(artist_id)

            self._suggestion_cache[cache_key] = suggestions
            return suggestions

        except SpotifyException as e:
            if _is_premium_required(e):
                raise SpotifyPremiumRequiredError(
                    "Spotify search requires the developer account behind this app's "
                    "API credentials to have an active Premium subscription."
                ) from e
            print(f"Search error for '{artist_name}': {e}")
            return []
        except Exception as e:
            # Log error but don't crash the UI
            print(f"Search error for '{artist_name}': {e}")
            return []
    
    def search_artist(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """Search for a single artist by name and return the first result"""
        if not artist_name or len(artist_name.strip()) < 2:
            return None
        
        try:
            # Clean input
            query = artist_name.strip()
            results = self.sp.search(q=query, type='artist', limit=1)
            artists = results.get('artists', {}).get('items', [])
            
            if artists:
                return artists[0]
            return None
            
        except Exception as e:
            print(f"Search error for '{artist_name}': {e}")
            return None
    
    def get_artist_info(self, artist_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about an artist"""
        try:
            return self.sp.artist(artist_id)
        except Exception as e:
            print(f"Error getting artist info for {artist_id}: {e}")
            return None
    
    def get_artist_top_tracks(self, artist_id: str, country: str = 'US') -> List[Dict[str, Any]]:
        """Get top tracks for an artist"""
        try:
            results = self.sp.artist_top_tracks(artist_id, country=country)
            return results['tracks']
        except Exception as e:
            print(f"Error getting top tracks for artist {artist_id}: {e}")
            return []
    
    def get_track_audio_features(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Get audio features for a specific track"""
        try:
            return self.sp.audio_features(track_id)[0]
        except Exception as e:
            print(f"Error getting audio features for track {track_id}: {e}")
            return None
    
    def get_multiple_tracks_audio_features(self, track_ids: List[str]) -> List[Dict[str, Any]]:
        """Get audio features using ReccoBeats API"""
        print(f"🎵 Fetching audio features for {len(track_ids)} tracks via ReccoBeats...")
        
        # Initialize ReccoBeats client on first use (lazy loading)
        if self.reccobeats is None:
            print("🔧 Initializing ReccoBeats client...")
            self.reccobeats = ReccoBeatsClient()
        
        # Try ReccoBeats first
        recco_features = self.reccobeats.get_multiple_tracks_audio_features(track_ids)
        
        if recco_features:
            print(f"✅ ReccoBeats returned {len(recco_features)} audio features")
            return recco_features
        else:
            print("⚠️  ReccoBeats unavailable, using enhanced Spotify data...")
            # Fallback: return enhanced Spotify track data as "audio features"
            return self._create_enhanced_spotify_features(track_ids)
    
    def _create_enhanced_spotify_features(self, track_ids: List[str]) -> List[Dict[str, Any]]:
        """Create enhanced features using available Spotify data"""
        features = []
        
        for track_id in track_ids:
            try:
                # Get track details from Spotify
                track = self.sp.track(track_id)
                
                # Create pseudo-audio features from available Spotify data
                enhanced_features = {
                    'id': track_id,
                    'name': track['name'],
                    'popularity': track['popularity'],
                    'duration_ms': track['duration_ms'],
                    'explicit': track['explicit'],
                    'track_number': track['track_number'],
                    # Estimate audio features based on available data
                    'energy': min(track['popularity'] / 100.0, 1.0),  # Higher popularity = higher energy
                    'danceability': 0.5 + (track['popularity'] / 200.0),  # Moderate baseline
                    'valence': track['popularity'] / 100.0,  # Popular songs tend to be happier
                    'tempo': 120.0,  # Default BPM
                    'loudness': -10.0,  # Default loudness
                    'speechiness': 0.1,  # Default low speechiness
                    'acousticness': 0.3,  # Default moderate acousticness
                    'instrumentalness': 0.1,  # Default low instrumentalness
                    'liveness': 0.2,  # Default low liveness
                    'key': 5,  # Default key
                    'mode': 1,  # Major mode
                    'time_signature': 4,  # 4/4 time
                    '_source': 'spotify_enhanced'  # Mark as estimated
                }
                features.append(enhanced_features)
                
            except Exception as e:
                print(f"Error getting enhanced features for {track_id}: {e}")
                continue
        
        return features
    
    def search_track(self, track_name: str, artist_name: str = None) -> Optional[Dict[str, Any]]:
        """Search for a specific track, optionally by artist"""
        try:
            query = track_name
            if artist_name:
                query = f"track:{track_name} artist:{artist_name}"
            
            results = self.sp.search(q=query, type='track', limit=1)
            if results['tracks']['items']:
                return results['tracks']['items'][0]
            return None
        except Exception as e:
            print(f"Error searching for track {track_name}: {e}")
            return None
    
    def get_artist_albums(self, artist_id: str, album_type: str = 'album', limit: int = 20) -> List[Dict[str, Any]]:
        """Get albums for an artist"""
        try:
            results = self.sp.artist_albums(artist_id, album_type=album_type, limit=limit)
            return results['items']
        except Exception as e:
            print(f"Error getting albums for artist {artist_id}: {e}")
            return []
    
    def get_track_info(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a track"""
        try:
            return self.sp.track(track_id)
        except Exception as e:
            print(f"Error getting track info for {track_id}: {e}")
            return None