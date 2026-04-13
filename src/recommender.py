"""
Music Recommender Simulation
Content-based filtering using genre, mood, energy, valence, and danceability.
"""

import csv
import os


def load_songs(filepath: str) -> list[dict]:
    """Load songs from a CSV file, converting numeric fields to floats."""
    songs = []
    numeric_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in numeric_fields:
                if field in row:
                    row[field] = float(row[field])
            if "tempo_bpm" in row:
                row["tempo_bpm"] = int(row["tempo_bpm"])
            songs.append(row)
    return songs


def score_song(user_prefs: dict, song: dict) -> tuple[float, list[str]]:
    """
    Score a single song against user preferences.

    Scoring rules:
      +2.0  genre match
      +1.0  mood match
      +1.0  energy similarity  (1 - |song_energy - target_energy|)
      +0.5  valence similarity (1 - |song_valence - target_valence|)
      +0.5  danceability similarity

    Returns a (score, reasons) tuple so the caller can explain the result.
    """
    score = 0.0
    reasons = []

    # Genre match
    if song.get("genre", "").lower() == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match
    if song.get("mood", "").lower() == user_prefs.get("favorite_mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity (0-1 scale; closer = higher reward, max +1.0)
    if "target_energy" in user_prefs and "energy" in song:
        energy_sim = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
        score += energy_sim
        reasons.append(f"energy similarity (+{energy_sim:.2f})")

    # Valence similarity (max +0.5)
    if "target_valence" in user_prefs and "valence" in song:
        valence_sim = (1.0 - abs(song["valence"] - user_prefs["target_valence"])) * 0.5
        score += valence_sim
        reasons.append(f"valence similarity (+{valence_sim:.2f})")

    # Danceability similarity (max +0.5)
    if "target_danceability" in user_prefs and "danceability" in song:
        dance_sim = (1.0 - abs(song["danceability"] - user_prefs["target_danceability"])) * 0.5
        score += dance_sim
        reasons.append(f"danceability similarity (+{dance_sim:.2f})")

    return score, reasons


def recommend_songs(user_prefs: dict, songs: list[dict], k: int = 5) -> list[dict]:
    """
    Rank all songs by score and return the top-k results.

    Uses sorted() (non-destructive) so the original song list is preserved.
    Each result dict includes 'score' and 'reasons' keys alongside song data.
    """
    scored = []
    for song in songs:
        s, reasons = score_song(user_prefs, song)
        result = dict(song)
        result["score"] = round(s, 3)
        result["reasons"] = reasons
        scored.append(result)

    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
    return ranked[:k]
