class Attributes:
    def __init__(self, xml_attr: dict):
        self.__src__: dict = xml_attr
        self.key: int = int(xml_attr['key']['fifths'])
        self.numerator: int = int(xml_attr['time']['beats'])
        self.denominator: int = int(xml_attr['time']['beat-type'])
        self.staves: list[dict] = [xml_attr['clef']] if not isinstance(xml_attr['clef'], list) else xml_attr['clef']
