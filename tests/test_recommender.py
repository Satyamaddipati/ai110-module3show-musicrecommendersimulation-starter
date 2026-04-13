"""Tests for the music recommender scoring and ranking logic."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from src.recommender import load_songs, score_song, recommend_songs

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")

# ── Fixtures ──────────────────────────────────────────────────────────────────

POP_HAPPY_USER = {
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.80,
    "target_valence": 0.80,
    "target_danceability": 0.80,
}

CHILL_USER = {
    "favorite_genre": "lofi",
    "favorite_mood": "calm",
    "target_energy": 0.15,
    "target_valence": 0.40,
    "target_danceability": 0.40,
}

SAMPLE_SONG_MATCH = {
    "title": "Test Bop",
    "artist": "Test Artist",
    "genre": "pop",
    "mood": "happy",
    "energy": 0.80,
    "valence": 0.80,
    "danceability": 0.80,
    "acousticness": 0.05,
    "tempo_bpm": 120,
}

SAMPLE_SONG_NO_MATCH = {
    "title": "Serene Space",
    "artist": "Test Artist",
    "genre": "ambient",
    "mood": "calm",
    "energy": 0.10,
    "valence": 0.35,
    "danceability": 0.20,
    "acousticness": 0.95,
    "tempo_bpm": 60,
}

# ── Tests ─────────────────────────────────────────────────────────────────────

def test_load_songs_count():
    songs = load_songs(DATA_PATH)
    assert len(songs) == 20, f"Expected 20 songs, got {len(songs)}"


def test_load_songs_numeric_fields():
    songs = load_songs(DATA_PATH)
    for song in songs:
        assert isinstance(song["energy"], float)
        assert isinstance(song["valence"], float)
        assert isinstance(song["tempo_bpm"], int)


def test_score_perfect_match():
    score, reasons = score_song(POP_HAPPY_USER, SAMPLE_SONG_MATCH)
    assert score > 4.0, "A perfect genre+mood+energy match should score above 4.0"
    assert any("genre match" in r for r in reasons)
    assert any("mood match" in r for r in reasons)


def test_score_no_match_lower_than_match():
    score_match, _ = score_song(POP_HAPPY_USER, SAMPLE_SONG_MATCH)
    score_no_match, _ = score_song(POP_HAPPY_USER, SAMPLE_SONG_NO_MATCH)
    assert score_match > score_no_match


def test_score_returns_reasons_list():
    _, reasons = score_song(POP_HAPPY_USER, SAMPLE_SONG_MATCH)
    assert isinstance(reasons, list)
    assert len(reasons) > 0


def test_recommend_songs_returns_k():
    songs = load_songs(DATA_PATH)
    recs = recommend_songs(POP_HAPPY_USER, songs, k=5)
    assert len(recs) == 5


def test_recommend_songs_sorted_descending():
    songs = load_songs(DATA_PATH)
    recs = recommend_songs(POP_HAPPY_USER, songs, k=10)
    scores = [r["score"] for r in recs]
    assert scores == sorted(scores, reverse=True)


def test_recommend_chill_profile_low_energy():
    songs = load_songs(DATA_PATH)
    recs = recommend_songs(CHILL_USER, songs, k=5)
    # Top picks should all have energy below 0.5 (chill profile)
    for r in recs[:3]:
        assert r["energy"] <= 0.5, f"Expected low energy for chill profile, got {r['title']} ({r['energy']})"


def test_original_songs_list_not_mutated():
    songs = load_songs(DATA_PATH)
    original_length = len(songs)
    recommend_songs(POP_HAPPY_USER, songs, k=5)
    assert len(songs) == original_length
    assert "score" not in songs[0]  # sorted() shouldn't mutate originals
