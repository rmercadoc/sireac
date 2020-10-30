import knowledgeBase as kb
from MusicXMLParse import *


# Calculate the musicXML dominant key
def dominant_key(measures: [Measure]):
    # note frequency calculation
    note_count = []

    for i in range(12):
        note_count.append(0)

    for measure in measures:
        for note in measure.notes:
            try:
                # Extra weight for first and last note
                if (measures.index(measure) == 0 and measure.notes.index(note) == 0) \
                        or (measures.index(measure) == len(measures) - 1
                            and measure.notes.index(note) == len(measure.notes) - 1):
                    note_count[note.chroma] += int(note.duration) * 2
                # Minor extra weight for strong beat note (first note in measure)
                elif measure.notes.index(note) == 0:
                    note_count[note.chroma] += int(note.duration) + 1
                # Normal weight for normal beats
                else:
                    note_count[note.chroma] += int(note.duration)
            except KeyError:
                pass

    total = sum(note_count)
    frequencies = [count / total for count in note_count]

    # Generate normalized key profiles based on the piece's notes normalized frequency
    if len(frequencies) < 12:
        return Exception
    offset = frequencies.index(max(frequencies))
    profiles = {}
    if offset == 0:
        profiles = kb.NORMALIZED_PROFILES
    else:
        for profile in kb.NORMALIZED_PROFILES:
            displaced_profile = []

            for prefix in kb.NORMALIZED_PROFILES[profile][-offset:]:
                displaced_profile.append(prefix)
            for suffix in kb.NORMALIZED_PROFILES[profile][0:-offset]:
                displaced_profile.append(suffix)

            profiles[profile] = displaced_profile

    # Calculate euclidean distances between the piece's notes frequency and the key profiles
    distances = {}
    for profile in profiles:
        squared_dist = 0
        for index in range(len(profiles[profile])):
            squared_dist += (frequencies[index] - profiles[profile][index]) ** 2
        distances[profile] = squared_dist ** (1 / 2)

    key = kb.NOTES[frequencies.index(max(frequencies))]

    min_dist = min(distances.values())

    print(key, list(distances.keys())[list(distances.values()).index(min_dist)])
    return key, list(distances.keys())[list(distances.values()).index(min_dist)]
