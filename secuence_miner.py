from client_credentials import url as base_url
from http_request import http_request
from typing import Any
from printer import printer

_log_prefix = '[CSM] >'
_log_width = 80
_dataset = None


class Rule:

    def __init__(self, rule: list or str, rule_list):
        self._name = str(rule).replace('[', '').replace(']', '').replace(',', '').replace('\'', '')
        self._chord_list = rule if isinstance(rule, list) else [rule]
        self._rule_list = rule_list
        global _dataset
        self._dataset = _dataset

    @property
    def n(self):
        count = 0
        for rule in self._rule_list:
            count += 1 if find(self._chord_list, rule) else 0
        return count

    @property
    def support(self):
        return self.n / len(self._dataset)

    @property
    def confidence(self):
        return self.n / len(self._rule_list)

    @property
    def lift(self):
        rule_count = 0
        for rule in self._dataset:
            rule_count += 1 if find(self._chord_list, rule) else 0
        return (self.n * len(self._dataset)) / (len(self._rule_list) * rule_count)

    def __eq__(self, other):
        if isinstance(other, list):
            return self._chord_list == other
        else:
            return self._name == other

    def __ne__(self, other):
        return not self == other

    def __contains__(self, item):
        return item in self._chord_list

    def __iter__(self):
        return iter(self._chord_list)

    def __len__(self):
        return len(self._chord_list)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self._chord_list).replace('[', '').replace(']', '').replace(',', '').replace('\'', '')

    def __format__(self, format_spec):
        return format(str(self), format_spec)


def log(*args, center: str = None):
    printer(*args, prefix=_log_prefix, width=_log_width, center=center)


def find(needle: Any, haystack: list):
    if not isinstance(needle, list):
        needle = [needle]
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            index_pos = haystack.index(needle[0], index_pos)
            if haystack[index_pos:index_pos + len(needle)] == needle:
                index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError:
            break
    return index_pos_list


def get_frequents(needles: list or set, min_sup: float = 0.2):
    frequent = []
    for needle in needles:
        if needle.support >= min_sup:
            frequent.append(needle)
    return frequent


def generate_valid_products(elements: list, length: int, valid_rules: list):
    valid = []
    p_list = []
    for rule in valid_rules:
        if len(rule) == length - 1:
            for e in elements:
                test = [r for r in rule]
                test.append(e)
                p_list.append(test)

    for p in p_list:
        frequent_children = True
        for index in range(len(p)):
            if p[index:index + (length - 1)] not in valid_rules:
                frequent_children = False
                break
        if frequent_children:
            valid.append(p)
    return valid


def generate_rules(params: dict, detailed_chords: bool = False, log_width: int = 80, verbose: bool = False):
    global _log_width
    _log_width = log_width
    progression_type = 'chord_progression_detail' if detailed_chords else 'chord_progression'
    if verbose:
        log(' CHORD SEQUENCE MINER (CSM) ', center='/')
        log('Gathering data from knowledge base (KB) ...')
        log(' -[ API CONSUMPTION ]- ', center='-')

    global _dataset
    if not _dataset:
        if verbose:
            log('GET all data from KB ...')
        request, data = http_request(base_url, '/api/mir/search', 'POST', body={}, verbose=verbose,
                                     log_width=log_width)
        _dataset = [piece[progression_type] for piece in list(data)]
        if verbose:
            log('RESPONSE STATUS 200 OK. GOT DATA') if request.getcode() == 200 else \
                exit(str(request.getcode()) + ' - CONNECTION ERROR')

    if verbose:
        log('GET filtered data by search parameters from KB ...')
    request, data = http_request(base_url, '/api/mir/search', 'POST', body=params, verbose=verbose,
                                 log_width=log_width)
    if verbose:
        log('RESPONSE STATUS 200 OK. GOT DATA') if request.getcode() == 200 else \
            exit(str(request.getcode()) + ' - CONNECTION ERROR')
        log(' -[ API CONSUMPTION END ]- ', center='-')
        log('Successfully gathered data from knowledge base!')

        log(' => RULE GENERATOR <= ', center='-')
    filtered_pieces = list(data)

    if len(filtered_pieces) == 0:
        return []

    chord_progressions = [piece[progression_type] for piece in filtered_pieces]

    chords = set()
    for piece in filtered_pieces:
        [chords.add(chord) for chord in piece[progression_type]]

    min_sup = (2 / len(filtered_pieces))
    if verbose:
        log('Minimum support:', min_sup)

    frequent_rules = []
    frequent_chords = []
    for f in get_frequents([Rule(chord, chord_progressions) for chord in chords], min_sup):
        if f not in frequent_rules:
            frequent_rules.append(f)
            frequent_chords.append(str(f))

    if verbose:
        log(frequent_rules)
        log(frequent_chords)
        log('{:3}|{:3}|{:<}'.format('l'.center(3), 'n'.center(3),
                                    'chord sequences'.center(log_width - 8 - len(_log_prefix))))
        log('{:3}|{:3}| {:<}'.format(1, len(frequent_rules), str(frequent_rules)))

    i = 1
    while True:
        i += 1
        new = []
        valid_permutations = generate_valid_products(frequent_chords, i, frequent_rules)
        valid_rules = [Rule(p, chord_progressions) for p in valid_permutations]
        for f in get_frequents(valid_rules, min_sup):
            if f not in frequent_rules:
                frequent_rules.append(f)
                new.append(f)
        if not new:
            break
        if verbose:
            log('{:3}|{:3}| {:<}'.format(i, len(new), str(new)))

    if verbose:
        log('{:>3}|{:3}|'.format('T', len(frequent_rules)))
        log(' => END OF RULE GENERATION <= ', center='-')
        log(' * Rule List * ', center=' ')
        log('{:^30s} | {:^10s} | {:^10s} | {:^10s}'.format('RULE', 'SUPPORT', 'CONFIDENCE', 'LIFT'))
        frequent_rules.sort(key = lambda x: (x.confidence, x.support, x.lift), reverse=True)
        for rule in frequent_rules:
            log('{:30s} | {:10.4f} | {:10.4f} | {:10.4f}'.format(rule, rule.support, rule.confidence, rule.lift))
        log(' CSM END ', center='/')

    return frequent_rules
