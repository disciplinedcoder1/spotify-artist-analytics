import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
from spotify_utils import SpotifyClient

class SpotifyAnalyzer:
    def __init__(self, spotify_client: SpotifyClient):
        self.spotify_client = spotify_client
        self.audio_features_keys = [
            'danceability', 'energy', 'key', 'loudness', 'mode',
            'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'tempo', 'duration_ms'
        ]
    
    def get_artist_stats(self, artist_name: str) -> Dict[str, Any]:
        """Get comprehensive stats for an artist"""
        artist = self.spotify_client.search_artist(artist_name)
        if not artist:
            return {'error': f'Artist "{artist_name}" not found'}
        
        artist_info = self.spotify_client.get_artist_info(artist['id'])
        top_tracks = self.spotify_client.get_artist_top_tracks(artist['id'])
        
        if not top_tracks:
            return {'error': f'No tracks found for "{artist_name}"'}
        
        track_ids = [track['id'] for track in top_tracks]
        audio_features = self.spotify_client.get_multiple_tracks_audio_features(track_ids)
        
        stats = {
            'artist_name': artist['name'],
            'artist_id': artist['id'],
            'popularity': artist['popularity'],
            'followers': artist['followers']['total'],
            'genres': artist['genres'],
            'top_tracks': top_tracks,
            'audio_features': audio_features,
            'track_count': len(top_tracks),
            'avg_audio_features': self._calculate_avg_audio_features(audio_features)
        }
        
        return stats
    
    def _calculate_avg_audio_features(self, audio_features: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate average audio features from a list of tracks"""
        if not audio_features:
            return {}
        
        df = pd.DataFrame(audio_features)
        avg_features = {}
        
        for feature in self.audio_features_keys:
            if feature in df.columns:
                avg_features[feature] = df[feature].mean()
        
        return avg_features
    
    def compare_songs(self, song1_data: Dict[str, Any], song2_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two songs based on their audio features"""
        features1 = song1_data.get('audio_features', {})
        features2 = song2_data.get('audio_features', {})
        
        if not features1 or not features2:
            return {'error': 'Audio features not available for comparison'}
        
        comparison = {
            'song1': {
                'name': song1_data['name'],
                'artist': song1_data['artists'][0]['name'],
                'popularity': song1_data['popularity']
            },
            'song2': {
                'name': song2_data['name'],
                'artist': song2_data['artists'][0]['name'],
                'popularity': song2_data['popularity']
            },
            'feature_comparison': {},
            'similarity_score': 0.0
        }
        
        feature_diffs = []
        
        for feature in self.audio_features_keys:
            if feature in features1 and feature in features2:
                val1 = features1[feature]
                val2 = features2[feature]
                
                if feature == 'duration_ms':
                    diff = abs(val1 - val2) / max(val1, val2)
                elif feature in ['key', 'mode']:
                    diff = 0 if val1 == val2 else 1
                else:
                    diff = abs(val1 - val2)
                
                comparison['feature_comparison'][feature] = {
                    'song1': val1,
                    'song2': val2,
                    'difference': diff
                }
                
                feature_diffs.append(diff)
        
        if feature_diffs:
            comparison['similarity_score'] = 1 - (sum(feature_diffs) / len(feature_diffs))
        
        return comparison
    
    def compare_artist_to_top_songs(self, target_artist: str, comparison_artist: str) -> Dict[str, Any]:
        """Compare a song from target artist against top songs from comparison artist"""
        target_stats = self.get_artist_stats(target_artist)
        comparison_stats = self.get_artist_stats(comparison_artist)
        
        if 'error' in target_stats or 'error' in comparison_stats:
            return {'error': f'Could not fetch data for one or both artists'}
        
        target_top_song = target_stats['top_tracks'][0] if target_stats['top_tracks'] else None
        comparison_top_songs = comparison_stats['top_tracks'][:5]
        
        if not target_top_song or not comparison_top_songs:
            return {'error': 'Could not find songs for comparison'}
        
        target_audio_features = self.spotify_client.get_track_audio_features(target_top_song['id'])
        target_song_data = {
            'name': target_top_song['name'],
            'artists': target_top_song['artists'],
            'popularity': target_top_song['popularity'],
            'audio_features': target_audio_features
        }
        
        comparisons = []
        for comp_song in comparison_top_songs:
            comp_audio_features = self.spotify_client.get_track_audio_features(comp_song['id'])
            comp_song_data = {
                'name': comp_song['name'],
                'artists': comp_song['artists'],
                'popularity': comp_song['popularity'],
                'audio_features': comp_audio_features
            }
            
            comparison = self.compare_songs(target_song_data, comp_song_data)
            comparisons.append(comparison)
        
        comparisons.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)
        
        return {
            'target_artist': target_artist,
            'comparison_artist': comparison_artist,
            'target_song': target_song_data,
            'comparisons': comparisons,
            'most_similar': comparisons[0] if comparisons else None
        }
    
    def rank_songs_by_feature(self, songs: List[Dict[str, Any]], feature: str, ascending: bool = False) -> List[Dict[str, Any]]:
        """Rank songs by a specific audio feature"""
        songs_with_features = []
        
        for song in songs:
            audio_features = self.spotify_client.get_track_audio_features(song['id'])
            if audio_features and feature in audio_features:
                songs_with_features.append({
                    'song': song,
                    'feature_value': audio_features[feature]
                })
        
        songs_with_features.sort(key=lambda x: x['feature_value'], reverse=not ascending)
        return songs_with_features
    
    def get_feature_distribution(self, artist_name: str) -> Dict[str, Any]:
        """Get distribution of audio features for an artist's top tracks"""
        stats = self.get_artist_stats(artist_name)
        if 'error' in stats:
            return stats
        
        audio_features = stats['audio_features']
        if not audio_features:
            return {'error': 'No audio features available'}
        
        df = pd.DataFrame(audio_features)
        distribution = {}
        
        for feature in self.audio_features_keys:
            if feature in df.columns:
                distribution[feature] = {
                    'mean': df[feature].mean(),
                    'std': df[feature].std(),
                    'min': df[feature].min(),
                    'max': df[feature].max(),
                    'median': df[feature].median()
                }
        
        return {
            'artist': artist_name,
            'feature_distribution': distribution,
            'track_count': len(audio_features)
        }