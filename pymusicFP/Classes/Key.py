from pymusicFP.profileProcessing import *
import pymusicFP.knowledgeBase as kb


class Key:
    def __init__(self, chroma: int or str, scale: str):
        self.chroma: int = chroma if isinstance(chroma, int) else kb.NOTES.index(chroma)
        self.note: str = self.get_note()
        self.scale: str = scale if isinstance(scale, str) and scale in kb.SCALE_PROFILES.keys() else None
        self.key_profile: list[float] = self.get_key_profile()
        self.normalized_key_profile: list[float] = self.get_normalized_key_profile()
        self.chord_definitions: list[dict] = self.get_chord_definitions()
        self.chord_profiles: list[dict] = self.get_chord_profiles()

    def __repr__(self) -> str:
        return self.note + ' ' + self.scale

    def get_note(self) -> str:
        return kb.NOTES[self.chroma]

    def get_key_profile(self) -> list:
        return displace_profiles_by_key(self.chroma, {self.scale: kb.SCALE_PROFILES[self.scale]})[self.scale]

    def get_normalized_key_profile(self) -> list:
        return [count / sum(self.key_profile) for count in self.key_profile]

    def get_chord_definitions(self) -> list:
        chord_profiles = []
        for chroma in range(len(kb.NOTES)):
            chroma_chord_profiles = displace_profiles_by_key(chroma, kb.CHORD_PROFILES)
            chroma_chord_profiles_by_key = {}
            for chroma_chord_profile in chroma_chord_profiles:
                chroma_chord_profile_by_key = []
                for note in range(len(chroma_chord_profiles[chroma_chord_profile])):
                    chroma_chord_profile_by_key.append(
                        chroma_chord_profiles[chroma_chord_profile][note] * self.key_profile[note]
                    )
                chroma_chord_profiles_by_key[chroma_chord_profile] = chroma_chord_profile_by_key
            chord_profiles.append(chroma_chord_profiles_by_key)

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
        return chord_profiles
