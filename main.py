import xmltodict
import json
from pymusicFP.pymusicFP import *

with open('sheetmusic/anger1.musicxml', 'r') as xml_file:
    data = json.loads(json.dumps(xmltodict.parse(xml_file.read())))

full_score = Score(data['score-partwise'])

full_score_measures = []
[[full_score_measures.append(measure) for measure in part.measures] for part in full_score.parts]

key = dominant_key(full_score_measures)
print(key)

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

        chord = Chord(beat_context, key)

        if chord.quality is None and len(measure_chords) > 0:
            [beat_context.append(note) for note in measure_chords[-1].notes]
            chord = Chord(beat_context, key)

        if chord.quality is None and not last_beat:
            extended_beat_context = beat_context
            continue
        elif chord.quality is None and last_beat:
            chord.quality = chord.closest_chord_qualities[0]

        extended_beat_context = None
        measure_chords.append(chord)

    chord_progression.append(measure_chords)

print('\nCHORD PROGRESSION PER MEASURE')
[print('{:3} | {:}'.format(chord_progression.index(x) + 1, x)) for x in chord_progression]
