#!/usr/bin/env python3
"""
Test the song-focused analytics dashboard
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api.spotify_utils import SpotifyClient

def test_song_focused_data():
    """Test that we can get detailed song data"""
    print("🎵 Testing Song-Focused Data Retrieval")
    print("=" * 50)
    
    client = SpotifyClient()
    target_id = "7cq88S2khvWL82FS68th1q"  # Ahmir with MOON
    
    try:
        # Get artist info
        artist_info = client.get_artist_info(target_id)
        print(f"✅ Artist: {artist_info['name']}")
        
        # Get top tracks
        top_tracks = client.get_artist_top_tracks(target_id)
        print(f"✅ Found {len(top_tracks)} tracks")
        
        # Test detailed track analysis
        print(f"\n🎼 Detailed Track Analysis:")
        print("-" * 50)
        
        detailed_tracks = []
        for i, track in enumerate(top_tracks[:3], 1):
            print(f"\n#{i} {track['name']}")
            
            # Available metrics
            metrics = {
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'duration_formatted': f"{track['duration_ms']//60000}:{(track['duration_ms']//1000)%60:02d}",
                'explicit': track.get('explicit', False),
                'preview_url': track.get('preview_url') is not None,
                'album_name': track.get('album', {}).get('name', 'Unknown'),
                'album_type': track.get('album', {}).get('album_type', 'Unknown'),
                'release_date': track.get('album', {}).get('release_date', 'Unknown'),
                'track_number': track.get('track_number', 0),
                'total_tracks': track.get('album', {}).get('total_tracks', 0),
                'is_moon': 'moon' in track['name'].lower(),
            }
            
            # Display metrics
            for key, value in metrics.items():
                if key == 'is_moon' and value:
                    print(f"   🌙 {key}: {value} ⭐ MOON TRACK FOUND! ⭐")
                else:
                    print(f"   📊 {key}: {value}")
            
            detailed_tracks.append(metrics)
        
        # Summary statistics
        print(f"\n📊 SUMMARY STATISTICS:")
        print("-" * 50)
        avg_popularity = sum(t['popularity'] for t in detailed_tracks) / len(detailed_tracks)
        avg_duration = sum(t['duration_ms'] for t in detailed_tracks) / len(detailed_tracks)
        explicit_count = sum(1 for t in detailed_tracks if t['explicit'])
        moon_count = sum(1 for t in detailed_tracks if t['is_moon'])
        
        print(f"✅ Average Popularity: {avg_popularity:.1f}/100")
        print(f"✅ Average Duration: {avg_duration//60000:.0f}:{((avg_duration//1000)%60):02.0f}")
        print(f"✅ Explicit Tracks: {explicit_count}/{len(detailed_tracks)}")
        print(f"✅ MOON Tracks: {moon_count}/{len(detailed_tracks)}")
        
        # Test categorization functions
        print(f"\n🏷️ CATEGORIZATION TESTS:")
        print("-" * 50)
        for i, track in enumerate(top_tracks[:3], 1):
            duration_cat = get_duration_category(track['duration_ms'])
            popularity_cat = get_popularity_category(track['popularity'])
            track_name = track['name'][:20] if len(track['name']) > 20 else track['name']
            print(f"   {track_name:.<20} Duration: {duration_cat}, Popularity: {popularity_cat}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def get_duration_category(duration_ms: int) -> str:
    """Test duration categorization"""
    minutes = duration_ms / 60000
    if minutes < 2:
        return "Short"
    elif minutes < 3:
        return "Medium"
    elif minutes < 4:
        return "Standard"
    elif minutes < 5:
        return "Long"
    else:
        return "Extended"

def get_popularity_category(popularity: int) -> str:
    """Test popularity categorization"""
    if popularity >= 70:
        return "🔥 Viral"
    elif popularity >= 50:
        return "📈 Popular"
    elif popularity >= 30:
        return "👍 Moderate"
    elif popularity >= 10:
        return "📊 Emerging"
    else:
        return "🎯 Underground"

def test_app_components():
    """Test app components work"""
    print(f"\n🧪 Testing App Components")
    print("=" * 50)
    
    try:
        # Test imports
        from app import get_duration_category, get_popularity_category, extract_year
        from ui.styles import create_matrix_metric, create_matrix_header, COLORS
        
        print("✅ All imports successful")
        
        # Test helper functions
        duration_cat = get_duration_category(180000)  # 3 minutes
        print(f"✅ Duration categorization: {duration_cat}")
        
        popularity_cat = get_popularity_category(25)
        print(f"✅ Popularity categorization: {popularity_cat}")
        
        year = extract_year("2023-05-15")
        print(f"✅ Year extraction: {year}")
        
        # Test styling components
        metric_html = create_matrix_metric("42", "Test Metric", "[*]")
        print(f"✅ Matrix metric created: {len(metric_html)} chars")
        
        header_html = create_matrix_header("Test Header", "Test Subtitle")
        print(f"✅ Matrix header created: {len(header_html)} chars")
        
        print(f"✅ Colors available: {len(COLORS)} colors")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Song-Focused Analytics Dashboard - Test Suite")
    print("=" * 60)
    
    # Run tests
    data_test = test_song_focused_data()
    component_test = test_app_components()
    
    # Summary
    tests_passed = sum([data_test, component_test])
    total_tests = 2
    
    print("\n" + "=" * 60)
    print(f"📊 TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n🚀 Ready to run song-focused app:")
        print("   streamlit run app.py")
        print("\n✨ Features available:")
        print("   • Detailed track metrics for each song")
        print("   • Popularity, duration, album info")
        print("   • Track categorization and analysis")
        print("   • Interactive filtering and sorting")
        print("   • MOON track detection and highlighting")
        print("   • Visual analytics charts")
    else:
        print("❌ Some tests failed. Please fix issues before running the app.")
    
    print("\n💡 This app shows ACTUAL song metrics that are available!")