# Note's names
NOTES = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

# Key profiles | David Temperley's Bayesian Approach to Key-Finding
SCALE_PROFILES = {
    'Major (Ionian)':   [5, 2, 3.5, 2, 4.5, 4, 2, 4.5, 2, 3.5, 1.5, 4],
    'Dorian':           [5, 2, 3.5, 4.5, 2, 4, 2, 4.5, 2, 3.5, 4, 1.5],
    'Phrygian':         [5, 3.5, 2, 4.5, 2, 4, 2, 4.5, 3.5, 2, 4, 1.5],
    'Lydian':           [5, 2, 3.5, 2, 4.5, 2, 4, 4.5, 2, 3.5, 1.5, 4],
    'Mixolydian':       [5, 2, 3.5, 2, 4.5, 4, 2, 4.5, 2, 3.5, 4, 1.5],
    'Minor (Aeolian)':  [5, 2, 3.5, 4.5, 2, 4, 2, 4.5, 3.5, 2, 4, 1.5],
    'Minor Harmonic':   [5, 2, 3.5, 4.5, 2, 4, 2, 4.5, 3.5, 2, 1.5, 4],
    'Locrian':          [5, 3.5, 2, 4.5, 2, 4, 4.5, 2, 3.5, 2, 4, 1.5]
}

# Key profiles with normalized (averaged) [0-1] values
NORMALIZED_PROFILES = {}
for profile in SCALE_PROFILES:
    total = sum(SCALE_PROFILES[profile])
    NORMALIZED_PROFILES[profile] = [x / sum(SCALE_PROFILES[profile]) for x in SCALE_PROFILES[profile]]
