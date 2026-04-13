"""
Entry point for the Music Recommender Simulation.
Run with:  python -m src.main
"""

import os
from src.recommender import load_songs, recommend_songs

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


# ── User profiles ────────────────────────────────────────────────────────────

PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "target_valence": 0.80,
        "target_danceability": 0.80,
    },
    "Chill Lofi / Ambient": {
        "favorite_genre": "lofi",
        "favorite_mood": "calm",
        "target_energy": 0.15,
        "target_valence": 0.40,
        "target_danceability": 0.40,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "angry",
        "target_energy": 0.85,
        "target_valence": 0.25,
        "target_danceability": 0.50,
    },
}


def print_recommendations(profile_name: str, recs: list[dict]) -> None:
    print(f"\n{'='*60}")
    print(f"  🎧  Profile: {profile_name}")
    print(f"{'='*60}")
    for i, song in enumerate(recs, 1):
        print(f"\n  {i}. {song['title']} — {song['artist']}")
        print(f"     Genre: {song['genre']}  |  Mood: {song['mood']}  |  Energy: {song['energy']}")
        print(f"     Score: {song['score']}")
        print(f"     Why:   {', '.join(song['reasons'])}")
    print()


def main():
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}")

    for profile_name, prefs in PROFILES.items():
        recs = recommend_songs(prefs, songs, k=5)
        print_recommendations(profile_name, recs)


if __name__ == "__main__":
    main()
