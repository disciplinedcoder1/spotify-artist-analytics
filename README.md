# Spotify Artist Analytics

> **Status: Work in progress.** Core artist search, catalog, and comparison features work end-to-end, but this is not a finished product. See [Known limitations](#known-limitations) and [Roadmap](#roadmap--planned-features) below before relying on it for anything real.

A Streamlit app for exploring artist catalogs and comparing songs/artists using live Spotify data.

## Features (working today)

- **Live artist search** — type-ahead search bar with debounced, ranked suggestions as you type (no need to hit Enter)
- **Artist catalog view** — popularity, followers, genre count, and top genre at a glance, plus tabs for recent releases, most popular tracks, and tracks sorted by danceability/energy
- **Individual song comparison** — compare two songs head-to-head on audio features, with a radar chart breakdown
- **Artist feature distribution** — average audio features (danceability, energy, valence, etc.) across an artist's top tracks
- **Multi-artist comparison** — add several artists to a comparison cart and chart popularity/followers side by side

## Setup

1. **Create and activate a virtual environment**
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Add Spotify API credentials** — create a `.env` file in the project root:
   ```
   SPOTIPY_CLIENT_ID=your_client_id
   SPOTIPY_CLIENT_SECRET=your_client_secret
   ```
   Get these from the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).

4. **Run the app**
   ```
   streamlit run src/app.py
   ```

## Project structure

```
src/
  app.py          # Streamlit UI and page flow
  api/            # Spotify + ReccoBeats API clients
  core/           # Analysis/business logic
  ui/             # Styling helpers
tests/            # Test suite
scripts/          # Diagnostic/dev scripts
```

## Known limitations

- **Spotify API access is restricted for non-Premium developer accounts.** Spotify now requires the account behind the app's API credentials to have an active Premium subscription for search access. Without it, search will show a "Spotify Premium required" notice instead of results.
- Some audio features may fall back to sample data when API permissions are limited, rather than always reflecting live Spotify data.
- The test suite in `tests/test_app.py` has stale references to functions from an earlier version of the app and needs to be rewritten against the current codebase.

## Roadmap / planned features

Major pieces that are **not** built yet:

- **Playlist matching/discovery** — matching artists or songs to relevant playlists
- **Promotional content generation** — ad copy / content assistance for artist promotion (the project's original intent, per its `spotify_promo2025` roots)
- **Full ReccoBeats audio-feature integration** — replacing the sample-data fallback with consistent live data
- **User-authenticated Spotify login (OAuth)** — the app currently only uses app-level Client Credentials auth; there's no way to save comparisons, access a personal library, or act on a user's behalf
- **Real historical trend tracking** — tracking how an artist's popularity/followers change over time (previous UI iterations showed fabricated trend numbers; this would replace that with real data)
- **A working, up-to-date test suite**
