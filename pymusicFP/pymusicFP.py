from pymusicFP.Classes.Score import Score
from pymusicFP.Classes.Part import Part
from pymusicFP.Classes.Measure import Measure
from pymusicFP.Classes.Note import Note
from pymusicFP.Classes.Attributes import Attributes
from pymusicFP.Classes.Chord import Chord
from pymusicFP.Classes.Key import Key
from pymusicFP import knowledgeBase as kb

from pymusicFP.profileProcessing import *


# Calculate the musicXML dominant key
def dominant_key(measures: [Measure]) -> Key:
    # note frequency calculation
    note_count = []

    for i in range(12):
        note_count.append(0)

    for measure in measures:
        for note in measure.notes:
            try:
                if not note.rest:
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

    frequencies = [count / sum(note_count) for count in note_count]

    # Generate normalized key profiles based on the piece's notes normalized frequency
    if len(frequencies) != 12:
        raise Exception
    offset = frequencies.index(max(frequencies))
    profiles = displace_profiles_by_key(offset, kb.NORMALIZED_PROFILES)

    # Calculate euclidean distances between the piece's notes frequency and the key profiles
    distances = profiles_distance(frequencies, profiles)

    key = Key(
        frequencies.index(max(frequencies)),
        list(distances.keys())[list(distances.values()).index(min(distances.values()))]
    )

    return key

