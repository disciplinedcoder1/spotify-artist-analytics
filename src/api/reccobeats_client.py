import requests
from typing import Dict, List, Optional, Any
import time

class ReccoBeatsClient:
    """Client for ReccoBeats audio features API"""
    
    def __init__(self, base_url: str = "https://reccobeats.com"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Spotify-Analytics-App/1.0',
            'Accept': 'application/json'
        })
    
    def get_track_audio_features(self, track_id: str) -> Optional[Dict[str, Any]]:
        """Get audio features for a single track"""
        url = f"{self.base_url}/v1/track/{track_id}/audio-features"
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                print(f"Track {track_id} not found in ReccoBeats")
                return None
            elif response.status_code == 400:
                print(f"Bad request for track {track_id}")
                return None
            else:
                print(f"ReccoBeats API error {response.status_code} for track {track_id}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"Timeout getting audio features for track {track_id}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error for track {track_id}: {e}")
            return None
    
    def get_multiple_tracks_audio_features(self, track_ids: List[str]) -> List[Dict[str, Any]]:
        """Get audio features for multiple tracks"""
        results = []
        
        for track_id in track_ids:
            # Add small delay to be respectful to the API
            time.sleep(0.1)
            
            features = self.get_track_audio_features(track_id)
            if features:
                # Ensure the track ID is included in the response
                features['id'] = track_id
                results.append(features)
        
        return results
    
    def test_connection(self) -> bool:
        """Test if ReccoBeats API is accessible"""
        # Try a dummy request to see if the API is available
        url = f"{self.base_url}/v1/track/test/audio-features"
        
        try:
            response = self.session.get(url, timeout=5)
            # Any response (even 404) means the API is reachable
            return True
        except:
            return False