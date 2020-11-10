from pymusicFP import knowledgeBase as kb
from pymusicFP.profileProcessing import *
from pymusicFP.Classes import Key, Note
from pymusicFP import config


class Chord:
    def __init__(self, notes: list[Note], key: Key):
        self.notes: list = notes
        self.notes_set: set = self.init_notes_set()
        self.identity_vector = self.init_chord_def()
        self.key = key
        self.chroma_distances = self.get_chroma_distances()
        self.min_chroma_distances = self.get_min_chroma_distances()
        self.root_chroma = self.identify_chord_root()
        self.closest_chord_qualities, self.quality = self.identify_chord_quality()
        self.scale_degree = key.scale_degrees[self.root_chroma]

    def init_chord_def(self):
        return [1 if x in self.notes_set else 0 for x in range(12)]

    def init_notes_set(self):
        return {x.chroma for x in self.notes}

    def get_chroma_distances(self):
        chroma_distances = {}
        for chroma_chord_profiles in self.key.chord_profiles:
            chroma_distances[
                kb.NOTES[self.key.chord_profiles.index(chroma_chord_profiles)]
            ] = profiles_distance(self.identity_vector, chroma_chord_profiles)

        cdl = []
        for chroma in chroma_distances.keys():
            for quality in chroma_distances[chroma].keys():
                cdl.append([chroma, quality, chroma_distances[chroma][quality]])
        return cdl

    def get_min_chroma_distances(self):
        chroma_distances = self.chroma_distances
        chroma_distances.sort(key=lambda x: x[2])
        return chroma_distances[:config.NEAR_CHORD_SAMPLE_SIZE]

    def identify_chord_root(self):

        notes_freq = [0 for i in range(12)]
        for note in self.notes:
            notes_freq[note.chroma] += note.duration
        total_notes = sum(notes_freq)
        notes_freq = [notes_freq[i] / total_notes for i in range(len(notes_freq))]
        # print('NOTES FREQ:', notes_freq)

        # print(self.min_chroma_distances)

        near_chroma_freq = [0 for i in range(12)]
        for e in self.min_chroma_distances:
            near_chroma_freq[kb.NOTES.index(e[0])] += 1
        # print(near_chroma_freq)
        total_near_chroma = sum(near_chroma_freq)
        near_chroma_freq = [near_chroma_freq[i] / total_near_chroma for i in range(len(near_chroma_freq))]
        near_chroma_freq = [near_chroma_freq[i] * notes_freq[i] for i in range(12)]
        # print(near_chroma_freq)

        # Count near chords root frequencies
        near_base_chroma_freq = {}
        for e in self.min_chroma_distances:
            if near_chroma_freq[kb.NOTES.index(e[0])] == max(near_chroma_freq):
                near_base_chroma_freq[e[0]] = near_chroma_freq[kb.NOTES.index(e[0])]

        # print(near_base_chroma_freq)
        # format frequencies to list and sort form greater to smaller
        near_base_chroma_freq = [[x, y] for x, y in near_base_chroma_freq.items()]
        near_base_chroma_freq.sort(key=lambda x: x[1], reverse=True)

        if len(list(near_base_chroma_freq)) == 1:
            return kb.NOTES.index(list(near_base_chroma_freq)[0][0])

        for x in near_base_chroma_freq:
            x[1] *= self.key.normalized_key_profile[kb.NOTES.index(x[0])]

        # [print(x) for x in near_base_chroma_freq]

        near_base_chroma_freq.sort(key=lambda x: x[1], reverse=True)

        return kb.NOTES.index(near_base_chroma_freq[0][0])

    def identify_chord_quality(self):
        displaced_profiles = displace_profiles_by_key(self.root_chroma, kb.CHORD_PROFILES)
        distances = [[k, v] for k, v in profiles_distance(self.identity_vector, displaced_profiles).items()]
        distances.sort(key=lambda x: x[1])
        # [print('{:>15} | {:<23}'.format(kb.NOTES[self.root_chroma] + x[0], x[1])) for x in distances]
        min_distance = distances[0][1]
        closest_qualities = []
        [closest_qualities.append(x[0]) for x in distances if x[1] == min_distance]
        # print(closest_qualities)
        return closest_qualities, closest_qualities[0] if len(closest_qualities) == 1 else None

    def __repr__(self):
        return self.scale_degree + ' (' + kb.NOTES[self.root_chroma] + self.quality + ')'
