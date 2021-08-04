from pymusicFP.profileProcessing import *
import pymusicFP.knowledgeBase as kb


class Key:
    def __init__(self, chroma: int or str, scale: str):
        self.chroma: int = chroma if isinstance(chroma, int) else kb.NOTES.index(chroma)
        self.note: str = self.get_note()
        self.scale: str = scale if isinstance(scale, str) and scale in kb.SCALE_PROFILES.keys() else None
        self.scale_notes: set = self.get_scale_notes()
        self.key_profile: list[float] = self.get_key_profile()
        self.normalized_key_profile: list[float] = self.get_normalized_key_profile()
        self.chord_definitions: list[dict] = self.get_chord_definitions()
        self.chord_profiles: list[dict] = self.get_chord_profiles()
        self.scale_degrees: list[str] = self.init_scale_degrees()

    def __repr__(self) -> str:
        return self.note + ' ' + self.scale

    def get_note(self) -> str:
        return kb.NOTES[self.chroma]

    def get_key_profile(self) -> list:
        return displace_profiles_by_key(self.chroma, {self.scale: kb.SCALE_PROFILES[self.scale]})[self.scale]

    def get_normalized_key_profile(self) -> list:
        return [count / sum(self.key_profile) for count in self.key_profile]

    def get_scale_notes(self):
        notes = set()
        for x in range(12):
            if displace_profiles_by_key(self.chroma, kb.SCALE_NOTES)[self.scale][x] == 1:
                notes.add(x)
        return notes

    def init_scale_degrees(self):
        return displace_profiles_by_key(self.chroma, kb.SCALE_DEGREES)

    def get_chord_definitions(self) -> list:
        chord_profiles = []

        for chroma in range(len(kb.NOTES)):
            chroma_chord_profiles = displace_profiles_by_key(chroma, kb.CHORD_PROFILES)
            chroma_chord_profiles_by_key = {}

            for chroma_chord_profile in chroma_chord_profiles:
                chroma_chord_profile_by_key = []

                for x in range(12):
                    if chroma_chord_profiles[chroma_chord_profile][x] == 1:
                        if x not in self.scale_notes:
                            chroma_chord_profiles[chroma_chord_profile][x] = -1

                for note in range(12):
                    chroma_chord_profile_by_key.append(
                        chroma_chord_profiles[chroma_chord_profile][note] #* self.key_profile[note]
                    )

                chroma_chord_profiles_by_key[chroma_chord_profile] = chroma_chord_profile_by_key
            chord_profiles.append(chroma_chord_profiles_by_key)

        # pprint
        # format_string = '{:50} | '
        # header = '| '
        # for k in kb.CHORD_PROFILES.keys():
        #     header += format_string.format(k)
        # print(header)
        # for chroma in chord_profiles:
        #     body = '| '
        #     x = [str(chroma[i]) for i in chroma.keys()]
        #     for y in x:
        #         body += format_string.format(y)
        #
        #     print(body)

        return chord_profiles

    def get_chord_profiles(self) -> list:
        chord_profiles = []
        for chroma in self.chord_definitions:
            normalized_chroma = {}
            for chord_profile in chroma.keys():
                normalized_chroma[chord_profile] = [
                    chroma[chord_profile][i] * self.normalized_key_profile[i] for i in
                    range(len(self.normalized_key_profile))
                ]
            chord_profiles.append(normalized_chroma)

        # pprint
        # format_string = '{:110} | '
        # header = '| '
        # for k in kb.CHORD_PROFILES.keys():
        #     header += format_string.format(k)
        # print(header)
        # for chroma in chord_profiles:
        #     body = '| '
        #     x = [str(chroma[i]) for i in chroma.keys()]
        #     for y in x:
        #         body += format_string.format(y)
        #
        #     print(body)

        return chord_profiles
