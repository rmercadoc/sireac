from pymusicFP.Classes.Measure import Measure


class Part:
    def __init__(self, mxml_part: dict):
        self.__src__: dict = mxml_part
        self.id: str = mxml_part['@id']
        self.measures: list[Measure] = self.init_measures(mxml_part['measure'])

    @staticmethod
    def init_measures(mxml_measures: dict or list[dict]) -> list[Measure]:
        if isinstance(mxml_measures, list):
            measures = []
            for xml_measure in mxml_measures:
                if 'attributes' not in xml_measure.keys() and mxml_measures.index(xml_measure) > 0:
                    xml_measure['attributes'] = mxml_measures[mxml_measures.index(xml_measure) - 1]['attributes']
                measures.append(Measure(xml_measure))
            return measures
        return [Measure(mxml_measures)]
