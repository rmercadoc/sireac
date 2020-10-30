import knowledgeBase as kb
import pprint


class Measure:

    def __init__(self, xml_measure: dict):
        print('created measure')
        pprint.pprint(xml_measure)
        self.notes = []


# Calculate the music)xml dominant key
def dominant_key(measures: [dict]):
    # note frequency calculation
    note_count = []

    for i in range(12):
        note_count.append(0)

    for measure in measures:
        for note in measure['note']:
            try:
                note_index = kb.NOTES.index(note['pitch']['step']) if 'alter' not in note['pitch'].keys() \
                    else kb.NOTES.index(note['pitch']['step']) + int(note['pitch']['alter'])
                # Extra weight for first and last note
                if (measures.index(measure) == 0 and measure['note'].index(note) == 0) \
                        or (measures.index(measure) == len(measures) - 1
                            and measure['note'].index(note) == len(measure['note']) - 1):
                    note_count[note_index] += int(note['duration']) * 2
                # Minor extra weight for strong beat note (first note in measure)
                elif measure['note'].index(note) == 0:
                    note_count[note_index] += int(note['duration']) + 1
                # Normal weight for normal beats
                else:
                    note_count[note_index] += int(note['duration'])
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
