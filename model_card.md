# 🎧 Model Card — VibeTune 1.0

## 1. Model Name

**VibeTune 1.0**

---

## 2. Intended Use

VibeTune suggests 3–5 songs from a small catalog based on a user's preferred genre, mood, energy, valence, and danceability. It is designed for classroom exploration of how content-based recommendation works. It is **not** intended for real production use, real users, or any monetized music product.

**Not intended for:**
- Personalized recommendations for real streaming users
- Replacing human curation or editorial playlists
- Any domain outside of academic/educational exploration

---

## 3. How It Works (Short Explanation)

When you give VibeTune a taste profile—say, you love high-energy pop that makes you happy—it goes through every song in the catalog and gives each one a score. A genre match earns 2 points, a mood match earns 1 point, and then it awards partial points based on how close the song's energy, positivity (valence), and danceability are to your target numbers. The closer the match, the higher the points. After scoring every song, it sorts the list and hands you the top 5. Every recommendation comes with a plain-English explanation of why it was chosen.

---

## 4. Data

- **20 songs** in `data/songs.csv` (10 original starter songs + 10 added for diversity)
- Features per song: title, artist, genre, mood, energy (0–1), tempo_bpm, valence (0–1), danceability (0–1), acousticness (0–1)
- Genres represented: pop, rock, metal, lofi, ambient, jazz, indie, hiphop, country
- Moods represented: happy, calm, angry, sad, melancholic, dark, epic, confident, motivated, nostalgic
- Whose taste this reflects: mostly Western mainstream music from roughly 2000–2023; under-represents non-English music, classical, and regional genres

---

## 5. Strengths

- **Transparent**: every recommendation comes with a reason list, so the user can see exactly why a song was chosen
- **Fast and simple**: no model training needed; runs instantly on any machine
- **Genre-diverse enough**: 9 genres means most basic taste profiles find some meaningful matches
- **Correct direction for energy**: low-energy profiles consistently get acoustic/ambient songs; high-energy profiles get pop/hiphop/metal—the system moves the right way

---

## 6. Limitations and Bias

**Genre dominance.** The genre weight (2.0) is twice as large as the mood weight (1.0) and far larger than any numerical similarity score (max 1.0). This means a song that perfectly matches your energy and mood but belongs to a different genre will almost always rank below a genre-matched song with mediocre similarity scores.

**Dataset imbalance creates filter bubbles.** Pop accounts for 7 of 20 songs (~35%). Pop-loving users get a rich, well-differentiated top-5. Lofi users get only one genre match in the whole catalog, so their second and third picks are driven entirely by energy/mood similarity with no genre bonus—the system effectively collapses their options.

**Mood labels are subjective.** "Epic" vs. "motivated" vs. "confident" are fuzzy human calls. Two annotators labeling the same catalog would produce different rankings for the same user profile.

**No diversity control.** The recommender always picks the closest matches. In a real product, you'd want some variety; here, similar songs cluster at the top and a user might get five nearly-identical-sounding tracks.

**Cold-start-like problem.** If a user prefers "country" or "jazz," the catalog is too small to surface a meaningful ranked list—at most 1–2 genre matches exist.

---

## 7. Evaluation

Three user profiles were tested:

| Profile | Top Result | Felt Right? |
|---|---|---|
| High-Energy Pop | Blinding Lights (4.93) | ✅ Yes — upbeat, danceable, pop |
| Chill Lofi / Ambient | Lofi Study Beats (4.88) | ✅ Yes — only lofi song wins |
| Deep Intense Rock | Numb — Linkin Park (3.75) | ⚠️ Partially — Linkin Park is alt-rock, not "deep intense rock" |

**Surprise finding:** Enter Sandman (Metallica) scored only 4th for the "Deep Intense Rock" profile despite being the closest match to the intended vibe. Because the genre label is "metal" (not "rock"), it missed the +2.0 genre bonus. This shows that coarse genre labels are a meaningful limitation.

**Weight experiment:** When mentally doubling the energy weight, Enter Sandman would have ranked 2nd (energy gap of only 0.05), which intuitively felt more accurate. This suggests energy should carry more weight—or genre labels should be more granular (e.g., "hard rock" vs. "indie rock").

No numeric accuracy metric was computed; evaluation was qualitative, comparing top-5 outputs to personal music intuition.

---

## 8. Future Work

1. **Normalize genre labels** into a hierarchy (e.g., metal → hard rock → rock) so related genres share partial credit instead of getting zero for a non-exact match
2. **Add diversity re-ranking** after scoring to ensure recommendations span at least 3 different genres, preventing the filter bubble from collapsing into one style
3. **Collaborative signals** — even a simple "users who liked X also liked Y" lookup using a co-listen matrix would dramatically improve recommendation quality for edge-case genres

---

## 9. Personal Reflection

The biggest learning moment came when Enter Sandman ranked fourth for the "Deep Intense Rock" profile. I had intuitively expected it to win—it's the heaviest song in the catalog—but the genre string "metal" vs. "rock" cost it 2 full points. That gap made me realize how much the *representation of data* determines the outcome of an algorithm. The scoring math was working exactly as designed; the problem was that my categories didn't match my intuitions.

Using AI tools (GitHub Copilot pattern, mapped here to this design exercise) helped me quickly iterate on the scoring weights and think through edge cases I hadn't considered, like what happens when no song matches a niche genre. But I had to double-check whether the energy similarity formula should use absolute difference or squared difference—the AI initially suggested squared, which would have over-penalized moderate mismatches. Catching that required me to actually think about what the formula means, not just accept the output.

What surprised me most is that a system this simple—100 lines of Python, no ML, no embeddings—can still produce outputs that *feel* like recommendations. That's because the underlying pattern (match attributes, rank by score) is genuinely how early recommendation systems worked. Real Spotify is infinitely more complex, but the core loop is recognizable. Where human judgment still matters most is in choosing what features to measure, how to weight them, and what "good" even means—none of that can come from the algorithm itself.
