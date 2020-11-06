from pymusicFP import knowledgeBase as kb
from pymusicFP.profileProcessing import *
from pymusicFP.Classes import Key
from pymusicFP import config


class Chord:
    def __init__(self, notes: set, key: Key, context_key: Key = None):
        self.notes: set = notes
        self.chord_definition = self.init_chord_def()
        self.key = key
        self.context_key = context_key
        self.chroma_distances = self.get_chroma_distances()
        self.min_chroma_distances = self.get_min_chroma_distances()
        self.root_chroma = self.identify_chord_root()
        self.closest_chord_qualities, self.quality = self.identify_chord_quality()

    def init_chord_def(self):
        return [1 if x in self.notes else 0 for x in range(12)]

    def get_chroma_distances(self):
        chroma_distances = {}
        for chroma_chord_profiles in self.key.chord_profiles:
            chroma_distances[
                kb.NOTES[self.key.chord_profiles.index(chroma_chord_profiles)]
            ] = profiles_distance(self.chord_definition, chroma_chord_profiles)

        cdl = []
        for cd in chroma_distances.keys():
            for pd in chroma_distances[cd].keys():
                cdl.append([cd, pd, chroma_distances[cd][pd]])
        return cdl

    def get_min_chroma_distances(self):
        chroma_distances = self.get_chroma_distances()
        chroma_distances.sort(key=lambda x: x[2])
        return chroma_distances[:config.NEAR_CHORD_SAMPLE_SIZE]

    def identify_chord_root(self):
        near_base_chroma_freq = {}
        for e in self.min_chroma_distances:
            near_base_chroma_freq[e[0]] = 0

        for e in self.min_chroma_distances:
            near_base_chroma_freq[e[0]] += 1

        near_base_chroma_freq = [[x, y] for x, y in near_base_chroma_freq.items()]
        near_base_chroma_freq.sort(key=lambda x: x[1], reverse=True)

        near_base_chroma_freq_filtered = list(
            filter(lambda x: x[1] <= near_base_chroma_freq[0][1], near_base_chroma_freq)
        )
        # [print(x) for x in near_base_chroma_freq_filtered]

        if len(list(near_base_chroma_freq_filtered)) == 1:
            return kb.NOTES.index(list(near_base_chroma_freq_filtered)[0][0])

        for x in near_base_chroma_freq_filtered:
            if self.context_key is None:
                x[1] *= self.key.normalized_key_profile[kb.NOTES.index(x[0])]
            else:
                x[1] *= self.key.normalized_key_profile[kb.NOTES.index(x[0])] * \
                        self.context_key.normalized_key_profile[kb.NOTES.index(x[0])]

        # [print(x) for x in near_base_chroma_freq_filtered]

        near_base_chroma_freq_filtered.sort(key=lambda x: x[1], reverse=True)

        return kb.NOTES.index(near_base_chroma_freq_filtered[0][0])

    def identify_chord_quality(self):
        displaced_profiles = displace_profiles_by_key(self.root_chroma, kb.CHORD_PROFILES)
        distances = [[k, v] for k, v in profiles_distance(self.chord_definition, displaced_profiles).items()]
        distances.sort(key=lambda x: x[1])
        # [print('{:>15} | {:<23}'.format(kb.NOTES[self.root_chroma] + x[0], x[1])) for x in distances]
        min_distance = distances[0][1]
        closest_qualities = []
        [closest_qualities.append(x[0]) for x in distances if x[1] == min_distance]
        # print(closest_qualities)
        return closest_qualities, closest_qualities[0] if len(closest_qualities) == 1 else None

    def __repr__(self):
        return kb.NOTES[self.root_chroma] + self.quality
