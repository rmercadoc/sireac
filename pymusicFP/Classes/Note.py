from pymusicFP import knowledgeBase as kb


class Note:
    def __init__(self, xml_note: dict, first: bool = False, last: bool = False):
        self.__src__: dict = xml_note
        self.chroma: int = self.init_chroma(xml_note['pitch']) if 'pitch' in xml_note.keys() else None
        self.octave: int = int(xml_note['pitch']['octave']) if 'pitch' in xml_note.keys() else None
        self.duration: int = int(xml_note['duration'])
        self.staff: str = xml_note['staff']
        self.rest: bool = 'rest' in xml_note.keys()
        self.chord: bool = 'chord' in xml_note.keys()
        self.name: str = self.init_name(xml_note['pitch']) if 'pitch' in xml_note.keys() else 'Rest'
        self.first = first
        self.last = last

    @staticmethod
    def init_chroma(xml_pitch: dict) -> int:
        chroma = kb.NOTES.index(xml_pitch['step'])
        chroma += int(xml_pitch['alter']) if 'alter' in xml_pitch.keys() else 0
        chroma -= 12 if chroma > 11 else 0
        chroma += 12 if chroma < 0 else 0
        return chroma

    @staticmethod
    def init_name(xml_pitch: dict) -> str:
        name = str(kb.NOTES[kb.NOTES.index(xml_pitch['step'])])
        if 'alter' in xml_pitch.keys():
            alt = int(xml_pitch['alter'])
            for alteration in range(abs(alt)):
                name += '#' if alt > 0 else 'b'
        return name

    def __str__(self):
        string = ''
        if self.rest:
            string += 'rest'
        else:
            string += self.name + ' (' + str(self.chroma) + ') O' + str(self.octave)
        string += ' D' + str(self.duration) + ' S' + self.staff
        return string

    def __repr__(self):
        return self.__str__()
