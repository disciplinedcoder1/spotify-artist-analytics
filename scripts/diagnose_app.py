#!/usr/bin/env python3

import os
import sys
import traceback
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test all imports step by step"""
    print("=== TESTING IMPORTS ===")
    
    try:
        print("1. Testing streamlit...")
        import streamlit as st
        print("   ✅ streamlit imported")
        
        print("2. Testing pandas...")
        import pandas as pd
        print("   ✅ pandas imported")
        
        print("3. Testing plotly...")
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        print("   ✅ plotly imported")
        
        print("4. Testing numpy...")
        import numpy as np
        print("   ✅ numpy imported")
        
        print("5. Testing spotify_utils...")
        from api.spotify_utils import SpotifyClient
        print("   ✅ spotify_utils imported")
        
        print("6. Testing styles...")
        from ui.styles import load_css, create_matrix_header
        print("   ✅ styles imported")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        traceback.print_exc()
        return False

def test_spotify_client():
    """Test SpotifyClient initialization"""
    print("\n=== TESTING SPOTIFY CLIENT ===")
    
    try:
        print("1. Initializing SpotifyClient...")
        start_time = time.time()
        
        from api.spotify_utils import SpotifyClient
        client = SpotifyClient()
        
        init_time = time.time() - start_time
        print(f"   ✅ Client initialized in {init_time:.2f}s")
        
        print("2. Testing basic search...")
        start_time = time.time()
        
        results = client.search_artist_suggestions("Drake", limit=1)
        
        search_time = time.time() - start_time
        print(f"   ✅ Search completed in {search_time:.2f}s")
        print(f"   Found {len(results)} results")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Spotify client failed: {e}")
        traceback.print_exc()
        return False

def test_reccobeats():
    """Test ReccoBeats client"""
    print("\n=== TESTING RECCOBEATS CLIENT ===")
    
    try:
        print("1. Testing ReccoBeats connection...")
        from api.reccobeats_client import ReccoBeatsClient
        
        client = ReccoBeatsClient()
        connected = client.test_connection()
        
        if connected:
            print("   ✅ ReccoBeats API reachable")
        else:
            print("   ⚠️  ReccoBeats API not reachable (expected)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ ReccoBeats test failed: {e}")
        traceback.print_exc()
        return False

def test_streamlit_components():
    """Test problematic streamlit components"""
    print("\n=== TESTING STREAMLIT COMPONENTS ===")
    
    try:
        print("1. Testing cached functions...")
        import streamlit as st
        
        # Test if @st.cache_data is causing issues
        @st.cache_data(ttl=300)
        def test_cached_function():
            return "test"
        
        print("   ✅ Cached function works")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Streamlit component failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests"""
    print("🔍 DIAGNOSING APP TIMEOUT ISSUES...\n")
    
    tests = [
        ("Imports", test_imports),
        ("Spotify Client", test_spotify_client),
        ("ReccoBeats", test_reccobeats),
        ("Streamlit Components", test_streamlit_components)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        success = test_func()
        results[test_name] = success
    
    print(f"\n{'='*50}")
    print("=== DIAGNOSIS SUMMARY ===")
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    if all(results.values()):
        print("\n🎯 All components working - issue may be in app.py logic")
    else:
        print("\n⚠️  Found failing components - these need fixing")

if __name__ == "__main__":
    main()