from pymusicFP.pymusicFP import *
# from collections import Counter


def chord_detection(note_group: Chord, last_beat: bool = False):
    notes = note_group.notes
    key = note_group.key
    context_key = note_group.context_key
    # Define Notes in chord
    chord_definition = [1 if x in notes else 0 for x in range(12)]
    print('\tCHORD DEF:', chord_definition)

    # Calculate distances by chroma by chord type [12*12] -> return only the min_distance per chroma
    chroma_distances = {}
    for chroma_chord_profiles in key.chord_profiles:
        distances = profiles_distance(chord_definition, chroma_chord_profiles)
        min_distance = [
            list(distances.keys())[list(distances.values()).index(min(list(distances.values())))],
            min(list(distances.values()))
        ]
        chroma_distances[kb.NOTES[key.chord_profiles.index(chroma_chord_profiles)]] = min_distance

    # Sort the min distance per chroma to order from smaller to grater distance
    chroma_distances_sorted = []
    for chroma_key in chroma_distances:
        chroma_distances_sorted.append([chroma_key, chroma_distances[chroma_key][0], chroma_distances[chroma_key][1]])
    chroma_distances_sorted.sort(key=lambda x: x[2])

    # Pretty print chroma distances
    format_string = ' | {:5} | {:15} | {:20} |'
    print('\tLIST OF CLOSEST CHORD BY CHROMA')
    print('\t' + format_string.format('NOTE', 'CHORD', 'DISTANCE'))
    [print('\t' + format_string.format(x[0], x[1], x[2])) for x in chroma_distances_sorted]

    # Define minimum distance between chord and reference built chords
    min_distance = chroma_distances_sorted[0][-1]

    # Select chords
    chords = {}
    for chroma in chroma_distances:
        if chroma_distances[chroma][1] == min_distance:
            chords[chroma] = chroma_distances[chroma]
    print('\t'+str(chords))

    # Return None if selected more than one chord, distance difference between near chords not in tolerance range and
    # it's not the last beat
    if len(chords) > 1 and abs(chroma_distances_sorted[0][2] - chroma_distances_sorted[len(chords)][2]) < 0.1 \
            and not last_beat:
        return

    # Generate chord profile based on Overall Key and context key if existent
    if context_key is None:
        chord_profile = [chord_definition[i] * key.key_profile[i] for i in range(12)]
    else:
        chord_profile = [chord_definition[i] * key.key_profile[i] * context_key.key_profile[i] for i in range(12)]

    # Normalize chord profile
    normalized_chord_profile = [x / sum(chord_profile) for x in chord_profile]

    # Pretty print chord profiles
    format_string = '\t' + ' | {:5} | {:15} | {:27} |'
    print('\tCHORD PROFILE BY KEY AND CONTEXT KEY')
    print(format_string.format('NOTE', 'CHORD PROFILE:', 'NOMALIZED CHORD PROFILE:'))
    [print(format_string.format(kb.NOTES[i], chord_profile[i], normalized_chord_profile[i])) for i in range(len(kb.NOTES))]

    # Select base chroma for chord name
    base_chroma = kb.NOTES[normalized_chord_profile.index(max(normalized_chord_profile))]

    # Select chord
    print('\tBASE CHROMA', base_chroma)
    chosen_chord = None
    for chord in chords:
        if chord == base_chroma:
            chosen_chord = chord
            break

    # No chord chosen but last beat
    if last_beat and chosen_chord is None:
        print('LAST BEAT AND NONE CHOSEN', chosen_chord)
        return base_chroma

    # Build chosen chord name
    chosen_chord = chosen_chord + chords[chosen_chord][0] if chosen_chord is not None else None

    return chosen_chord


# def chord_detection_old(notes: list[int], key: Key, context_key: Key or None = None, last_beat: bool = False):
#     counter = Counter(notes)
#     print(counter)
#     chord_definition = [1 if x in notes else 0 for x in range(12)]
#     chroma_distances = {}
#     for chroma_chord_profiles in key.chord_profiles:
#         distances = profile_distance(chord_definition, chroma_chord_profiles)
#         min_distance = [
#             list(distances.keys())[list(distances.values()).index(min(list(distances.values())))],
#             min(list(distances.values()))
#         ]
#         chroma_distances[kb.NOTES[key.chord_profiles.index(chroma_chord_profiles)]] = min_distance
#
#     chroma_distances_values = list(chroma_distances.values())
#     chroma_distances_values.sort(key=lambda x: x[1])
#     min_distance = chroma_distances_values[0][1]
#
#     chords = {}
#     for chroma in chroma_distances:
#         if chroma_distances[chroma][1] == min_distance:
#             chords[chroma] = chroma_distances[chroma]
#
#     if len(chords) > 1 and abs(
#             chroma_distances_values[0][1] - chroma_distances_values[len(chords)][1]
#     ) < 0.1 and not last_beat:
#         print(chords)
#         [print(chroma_distances[x]) for x in chroma_distances]
#         return
#
#     if context_key is None:
#         chord_profile = [chord_definition[i] * key.key_profile[i] for i in range(12)]
#     else:
#         chord_profile = [chord_definition[i] * key.key_profile[i] * context_key.key_profile[i] for i in range(12)]
#     # chord_profile = chord_definition
#
#     normalized_chord_profile = [x / sum(chord_profile) for x in chord_profile]
#     print('\t', chord_definition, sep='')
#     print('\t', chord_profile, sep='')
#     print('\t', normalized_chord_profile, sep='')
#
#     base_chroma = kb.NOTES[normalized_chord_profile.index(max(normalized_chord_profile))]
#
#     print('\t', notes, sep='')
#
#     print('\tBASE CHROMA', base_chroma)
#     chosen_chord = None
#     for chord in chords:
#         if chord == base_chroma:
#             chosen_chord = chord
#             break
#
#     if last_beat and chosen_chord is None:
#         print('LAST BEAT AND NONE CHOSEN', chosen_chord)
#         return base_chroma
#
#     chosen_chord = chosen_chord + chords[chosen_chord][0] if chosen_chord is not None else None
#
#     return chosen_chord
