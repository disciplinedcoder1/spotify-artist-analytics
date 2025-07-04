import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from typing import Dict, List, Optional, Any

load_dotenv()

class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not found in environment variables")
        
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def search_artist(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """Search for an artist by name and return the first result"""
        try:
            results = self.sp.search(q=artist_name, type='artist', limit=1)
            if results['artists']['items']:
                return results['artists']['items'][0]
            return None
        except Exception as e:
            print(f"Error searching for artist {artist_name}: {e}")
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
        """Get audio features for multiple tracks"""
        try:
            results = self.sp.audio_features(track_ids)
            return [feature for feature in results if feature is not None]
        except Exception as e:
            print(f"Error getting audio features for multiple tracks: {e}")
            return []
    
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