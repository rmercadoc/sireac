from pymusicFP.Classes.Part import Part


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
        self.__src__: dict = musicxml_data
        self.parts: list[Part] = self.init_parts(musicxml_data['part'])

    @staticmethod
    def init_parts(mxml_parts: dict) -> list[Part]:
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
