from pymusicFP.Classes.Score import Score
from pymusicFP.Classes.Part import Part
from pymusicFP.Classes.Measure import Measure
from pymusicFP.Classes.Note import Note
from pymusicFP.Classes.Attributes import Attributes
from pymusicFP.Classes.Chord import Chord
from pymusicFP.Classes.Key import Key
from pymusicFP import knowledgeBase as kb

from pymusicFP.profileProcessing import *

import json
import xmltodict


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
                    if (measures.index(measure) == 0) or (measures.index(measure) == len(measures) - 1):
                        if note.first:
                            note_count[note.chroma] += int(note.duration) * 6 if note.octave < 4 else int(note.duration)
                        else:
                            note_count[note.chroma] += int(note.duration)
                    # Normal weight for normal beats
                    else:
                        # Minor extra weight for strong beat note (first note in measure)
                        note_count[note.chroma] += int(note.duration) + 1 if note.first else int(note.duration)

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


def mir(file: str):
    bar_size = 100
    print('-' * bar_size, '\n', 'FILE:', file)
    with open(file, 'r') as xml_file:
        data = json.loads(json.dumps(xmltodict.parse(xml_file.read())))

    full_score = Score(data['score-partwise'])

    full_score_measures = []
    [[full_score_measures.append(measure) for measure in part.measures] for part in full_score.parts]

    key = dominant_key(full_score_measures)
    print('\tKEY + SCALE:', '\n\t\t', key)

    chord_progression_per_beat = []
    chord_progression = []

    # print('\n\tCONTEXT KEYS BY MEASURE')
    for index in range(len(full_score_measures)):
        # Define harmonic context (measure)
        measure = full_score_measures[index]
        beat_length = measure.duration / measure.attributes.numerator

        # get measure notes by beats
        beats_notes = [[] for beat in range(measure.attributes.numerator)]

        for staff in measure.attributes.staves:
            time = 0
            for note_index in range(len(measure.notes)):
                note = measure.notes[note_index]
                if time >= measure.duration:
                    break
                if note.staff == staff['@number']:
                    start_beat = int(time // beat_length)
                    offset = int(note.duration // beat_length)
                    for beat in range(offset) if offset > 0 else range(1):
                        beats_notes[start_beat + beat].append(note) if not note.rest else None
                    try:
                        time += note.duration if not measure.notes[note_index + 1].chord else 0
                    except IndexError:
                        time += note.duration

        # Get chord per beat or extended beat context
        measure_chords = []

        extended_beat_context = None
        for beat_index in range(len(beats_notes)):
            beat_notes = beats_notes[beat_index]
            last_beat = beat_index == len(beats_notes) - 1

            if extended_beat_context is None:
                beat_context = [note for note in beat_notes]
            else:
                beat_context = extended_beat_context
                [beat_context.append(note) for note in beat_notes]

            for note in beat_context:
                if beat_index == 0:
                    note.duration += 1

            if not beat_context:
                continue

            chord = Chord(beat_context, key)

            if chord.quality is None and len(measure_chords) > 0:
                [beat_context.append(note) for note in measure_chords[-1]]
                chord = Chord(beat_context, key)

            if chord.quality is None and not last_beat:
                extended_beat_context = beat_context
                continue
            elif chord.quality is None and last_beat:
                chord.quality = chord.closest_chord_qualities[0]

            extended_beat_context = None
            measure_chords.append(chord)

        # measure chord prune
        pruned_chords = [measure_chords[0]]

        for i in range(1, len(measure_chords)):
            if measure_chords[i] != pruned_chords[-1]:
                pruned_chords.append(measure_chords[i])
            else:
                [pruned_chords[-1].append(x) for x in measure_chords[i]]

        chord_progression_per_beat.append(pruned_chords)
        [chord_progression.append(str(chord)) for chord in pruned_chords]

    print('\tCHORD PROGRESSION:')
    # [print('\t\t{:3} | {:}'.format(i+1, chord_progression_per_beat[i]))
    # for i in range(len(chord_progression_per_beat))]
    print('\t', chord_progression)
    print('-' * bar_size, '\n')
    return {
        'name': file.split("/")[-1].replace('.musicxml', ''),
        'dominant_key': str(key),
        'chord_progression': chord_progression
    }
