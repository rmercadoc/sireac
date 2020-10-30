import knowledgeBase as kb


class Note:
    def __init__(self, xml_note):
        self.__src__ = xml_note
        self.chroma = self.init_chroma(xml_note['pitch'])
        self.octave = xml_note['pitch']['octave']
        self.duration = xml_note['duration']
        self.staff = xml_note['staff']

    @staticmethod
    def init_chroma(xml_pitch):
        chroma = kb.NOTES.index(xml_pitch['step'])
        chroma += int(xml_pitch['alter']) if 'alter' in xml_pitch.keys() else 0
        return chroma


class Attributes:
    def __init__(self, xml_attr):
        self.__src__ = xml_attr
        self.key = xml_attr['key']['fifths']
        self.numerator = xml_attr['time']['beats']
        self.denominator = xml_attr['time']['beat-type']
        self.staves = [xml_attr['clef']] if not isinstance(xml_attr['clef'], list) else xml_attr['clef']


class Measure:
    def __init__(self, xml_measure: dict):
        self.__src__ = xml_measure
        self.number = xml_measure['@number']
        self.attributes = self.init_attributes(xml_measure)
        self.notes = self.init_notes(xml_measure['note'])
        self.duration = xml_measure['backup']['duration']

    @staticmethod
    def init_attributes(xml_measure):
        if 'attributes' in xml_measure.keys():
            return Attributes(xml_measure['attributes'])
        return

    @staticmethod
    def init_notes(xml_notes):
        if isinstance(xml_notes, list):
            notes = []
            for note in xml_notes:
                notes.append(Note(note))
            return notes
        return Note(xml_notes)


class Part:
    def __init__(self, mxml_part):
        self.__src__ = mxml_part
        self.id = mxml_part['@id']
        self.measures = self.init_measures(mxml_part['measure'])

    @staticmethod
    def init_measures(mxml_measures):
        if isinstance(mxml_measures, list):
            measures = []
            for xml_measure in mxml_measures:
                if 'attributes' not in xml_measure.keys() and mxml_measures.index(xml_measure) > 0:
                    xml_measure['attributes'] = mxml_measures[mxml_measures.index(xml_measure) - 1]['attributes']
                measures.append(Measure(xml_measure))
            return measures
        return Measure(mxml_measures)


class Score:
    """
    A class to represent a MusicXML Score.

    Attributes
    ----------
    __src__: dict
        source MusicXMl parsed to a python dict
    parts : list[Part]
        List of parts that build up the score
    """
    def __init__(self, musicxml_data: dict):
        """
        Constructs all the necessary attributes for the Score object from a MusicXMl file parsed to a python dict.

        Parameters
        ----------
            musicxml_data : dict
                MusicXMl file parsed to a python dict
        """
        self.__src__ = musicxml_data
        self.parts = self.init_parts(musicxml_data['part'])

    @staticmethod
    def init_parts(mxml_parts) -> list[Part]:
        """
        Initiates the Parts Objects from MusicXML data parsed in a python dict.

        Parameters
        ----------
        mxml_parts : dict
            MusicXMl parts data parsed to a python dict

        Returns
        -------
        list[Part]
        """
        if isinstance(mxml_parts, list):
            parts = []
            for part in mxml_parts:
                parts.append(Part(part))
            return parts
        return [Part(mxml_parts)]
