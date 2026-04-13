# 🎵 Music Recommender Simulation

## Project Summary

In this project, you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user's "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real-world AI recommenders

This simulation builds a content-based music recommender that scores songs against a user's taste profile using five audio features: energy, acousticness, mood, genre, and valence. Each feature contributes a weighted proximity score so the system can explain exactly why each song was recommended. The project explores how real platforms like Spotify translate measurable audio properties into personalized listening experiences.

---

## How The System Works

Real-world recommenders like Spotify combine two signals: what millions of other users with similar taste have listened to (collaborative filtering), and the actual audio properties of each song such as tempo, energy, and mood (content-based filtering). This simulation focuses entirely on the content-based side. Rather than learning from a crowd, it scores each song by measuring how closely its audio features match a single user's stated preferences. The system prioritizes **listening intent over genre loyalty** — a user who wants something calm should get calm songs regardless of genre, because energy and mood define the immediate experience far more than a style label does. Every score is a weighted sum of five proximity signals, which makes the reasoning transparent and each recommendation fully explainable.

### Song Features

Each `Song` object stores the following attributes:

| Field | Type | What it represents |
|---|---|---|
| `id` | int | Unique identifier |
| `title` | str | Song name |
| `artist` | str | Artist name |
| `genre` | str | Musical style (e.g. pop, lofi, rock, ambient) |
| `mood` | str | Emotional label (e.g. happy, chill, intense, moody) |
| `energy` | float 0–1 | Overall intensity and activity level |
| `tempo_bpm` | float | Speed of the beat in beats per minute |
| `valence` | float 0–1 | Musical positivity — high = happy, low = sad |
| `danceability` | float 0–1 | How suited the track is for dancing |
| `acousticness` | float 0–1 | Organic/acoustic (1.0) vs. electronic/produced (0.0) |

### UserProfile Features

Each `UserProfile` object stores the following preferences:

| Field | Type | What it represents |
|---|---|---|
| `favorite_genre` | str | Preferred musical style — used as a soft bonus, not a hard filter |
| `favorite_mood` | str | The emotional tone the user is seeking right now |
| `target_energy` | float 0–1 | Desired intensity level — the single strongest matching signal |
| `likes_acoustic` | bool | Whether the user prefers organic/acoustic sound over electronic production |
| `target_valence` | float 0–1 | Desired emotional tone — derived from mood if not supplied explicitly |

---

### Algorithm Recipe

Each song is scored out of **10 points** across five components. The final ranked list is produced by sorting all scores descending and returning the top `k`.

#### Scoring Formula

```
score = energy_pts + acoustic_pts + mood_pts + genre_pts + valence_pts
```

#### Component Rules

**1. Energy Proximity — max 3.5 pts**
```
energy_pts = (1 - abs(song.energy - user.target_energy)) * 3.5
```
Rewards songs whose intensity level is close to what the user wants right now.
A song exactly matching the target scores the full 3.5. A song 0.5 away scores 1.75.

**2. Acoustic Texture — max 2.5 pts**
```
if user.likes_acoustic:
    acoustic_pts = song.acousticness * 2.5
else:
    acoustic_pts = (1 - song.acousticness) * 2.5
```
Rewards organic/acoustic sound when the user prefers it, or electronic/produced sound when they don't.

**3. Mood Match — max 2.0 pts (binary)**
```
mood_pts = 2.0 if song.mood == user.favorite_mood else 0.0
```
Full points for an exact match, nothing otherwise. Mood is weighted above genre because it defines the user's current listening intent, not just their general taste.

**4. Genre Match — max 1.0 pt (binary)**
```
genre_pts = 1.0 if song.genre == user.favorite_genre else 0.0
```
A soft style bonus. Kept at 1.0 so cross-genre songs that match on energy and mood can still surface in the top results.

**5. Valence Proximity — max 1.0 pt**
```
valence_pts = (1 - abs(song.valence - user.target_valence)) * 1.0
```
Fine-tunes emotional tone. If no explicit `target_valence` is given, it is derived from `favorite_mood` (e.g. "happy" → 0.80, "melancholic" → 0.30).

#### Weight Rationale

| Component | Max pts | Why this weight |
|---|---|---|
| Energy proximity | 3.5 | Widest meaningful spread in the dataset (0.18–0.97); defines listening context most directly |
| Acoustic texture | 2.5 | Near-independent of energy; captures production aesthetic as a second strong axis |
| Mood match | 2.0 | Current listening intent — wrong mood makes a recommendation feel wrong regardless of genre |
| Genre match | 1.0 | Soft bonus only; cross-genre discoveries should still be possible |
| Valence proximity | 1.0 | Emotional tone tiebreaker; partially overlaps with mood so weighted lower |

---

### Expected Biases

No scoring system is neutral. These are the known trade-offs built into this design:

- **Mood and genre are binary — partial matches score zero.** A user who wants "chill" music gets no credit for a "relaxed" song even though those moods are nearly identical. This can exclude songs that feel right but use a slightly different label.
- **Genre match rewards exact labels only.** A pop fan will get zero genre points for an indie pop or synth-pop song, even though those genres strongly overlap. The system might surface a pop song with the wrong mood over a near-pop song with the right mood.
- **`likes_acoustic` is a binary switch, not a spectrum.** A user who enjoys lightly produced acoustic-adjacent music (acousticness ~0.5) gets the same signal whether they set the flag true or false. Songs in the middle of the acoustic range are effectively invisible to this feature.
- **Energy dominates at 35%.** In a 25-song catalog, high-energy songs will reliably outrank everything else for a high-energy user, even if those songs fail on mood, genre, and valence. The sheer weight of the energy component can override three other signals.
- **No tempo signal.** `tempo_bpm` exists in every song but is unused in scoring. A user who wants background study music at ~70 BPM could receive a high-energy pop track at 132 BPM if its other features align — the BPM mismatch goes unpenalized.
- **Small catalog amplifies all biases.** With only 25 songs, a single miscalibrated weight can have an outsized effect. In a real 50-million-song catalog, extreme weights self-correct because there are always enough candidates at every point in the feature space.

---

## CLI Verification
![CLI output](image.png)

## Stress Test with Diverse Profiles
![CLI output](edgeCase1.png)
![CLI output](edgeCase2.png)
![CLI output](edgeCase3.png)
![CLI output](edgeCase4.png)

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

What was your biggest learning moment during this project?

The biggest learning moment came from running the edge-case profiles and watching the system fail in ways that were completely logical but still felt wrong. When I gave it a "High Energy but Sad" profile, it recommended upbeat electronic tracks because energy (3.5 pts) mathematically overpowered the melancholic mood signal. The code was doing exactly what I told it to do; it was my weight decisions that were wrong for that use case. That was the moment I understood that building a recommender is not really about writing code. It is about assumptions, and every assumption has consequences for someone.

The dataset size was the second big lesson. With 91% of genres having only one song, the genre feature made almost no meaningful difference. I had spent time carefully weighing genre versus mood, but in practice, the genre component was nearly pointless because the data supporting it were too thin. The algorithm can only be as good as what you feed it.

How did using AI tools help you, and when did you need to double-check them?

AI tools helped at every stage where I needed to quickly translate an idea into working code: loading the CSV, structuring the scoring function, and formatting the terminal output. They were also useful for explaining concepts like why `sorted()` is safer than `.sort()` for functions that should not modify their inputs.

Where I had to slow down and verify: the suggested scoring weights. An early draft gave genre greater weight than mood, which sounded reasonable in the abstract but produced incorrect results the moment I tested it. Gym Hero (pop, intense) ranked above Rooftop Lights (indie pop, happy) for a user who wanted happy music. I had to reason through the actual numbers myself to catch that. The AI gave me a starting point, but deciding which feature deserved more weight required testing real profiles and thinking about what a correct result actually looked like.

What surprised you about how simple algorithms can still "feel" like recommendations?

The most surprising thing was how convincing the output felt, even though the system had no real understanding of music. When Library Rain scored 9.65/10 for the chill lo-fi listener, it genuinely felt like a good recommendation, not because the system knew anything about lo-fi aesthetics or late-night study sessions, but because five numbers happened to align. That felt slightly unsettling once I thought about it. A real Spotify recommendation carries a sense of meaning — this app knows me. But VibeRecommender is just measuring distances between numbers. The feeling of a good recommendation comes entirely from the output matching intuition, not from any understanding inside the system. It made me more doubtful of the confidence in the real apps project.

What would you try next if you were to extend this project?

The first thing I would change is genre and mood matching. Instead of all-or-nothing binary scoring, I would build a small similarity table so that "metal" scores partial credit against a "rock" preference, and "ambient" scores partial credit against "lofi." That one change would make the bottom four results far more meaningful for niche listeners.

Second, I would expand the dataset to at least five songs per genre and mood. Right now, the data is the bottleneck, not the algorithm. The scoring logic is sound, but it has almost nothing to work with for most genres. With a richer dataset, I could also add a diversity rule so the top five never return what feels like five versions of the same song.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section; treat it like an explanation to a non-programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
