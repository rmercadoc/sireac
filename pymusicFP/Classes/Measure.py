from pymusicFP.Classes.Attributes import Attributes
from pymusicFP.Classes.Note import Note


class Measure:
    def __init__(self, xml_measure: dict):
        self.__src__: dict = xml_measure
        self.number: str = xml_measure['@number']
        self.attributes: Attributes = self.init_attributes(xml_measure)
        self.notes: list[Note] = self.init_notes(xml_measure['note'])
        self.duration: int = int(xml_measure['backup']['duration'])

    @staticmethod
    def init_attributes(xml_measure: dict) -> Attributes or None:
        if 'attributes' in xml_measure.keys():
            return Attributes(xml_measure['attributes'])
        return None

    @staticmethod
    def init_notes(xml_notes: list or dict) -> list[Note]:
        if isinstance(xml_notes, list):
            notes = []
            for note in xml_notes:
                staff_notes = list(filter(lambda x: x['staff'] == note['staff'], xml_notes))
                notes.append(Note(note)) if staff_notes.index(note) != 0 else notes.append(Note(note, True))
            return notes
        return [Note(xml_notes, True)]
