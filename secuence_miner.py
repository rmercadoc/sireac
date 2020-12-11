from client_credentials import url as base_url
from http_request import http_request
from typing import Any
from printer import printer

_log_prefix = '[CSM] >'
_log_width = 80


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
        except ValueError as e:
            break
    return index_pos_list if len(index_pos_list) > 0 else []


def get_frequents(needles: list or set, haystack: list, min_sup: float = 0.2):
    frequent = []
    for needle in needles:
        count = 0
        for element in haystack:
            count += 1 if find(needle, element) else 0
        if (count / len(haystack)) >= min_sup:
            frequent.append([needle]) if not isinstance(needle, list) else frequent.append(needle)
    return frequent


def generate_valid_products(elements: list, length: int, valid_rules: list):
    valid = []
    p_list = []
    minor_len_rules = []
    for rule in valid_rules:
        if len(rule) == length - 1:
            for e in elements:
                test = [r for r in rule]
                test.append(e)
                p_list.append(test)

    for p in p_list:
        frequent_children = True
        for index in range(len(list(p))):
            if list(p)[index:index + (length - 1)] not in valid_rules:
                frequent_children = False
                break
        if frequent_children:
            valid.append(list(p))
    return valid


def generate_rules(params: dict, detailed_chords: bool = False, log_width: int = 80, verbose: bool = False):
    global _log_width
    _log_width = log_width
    progression_type = 'chord_progression_detail' if detailed_chords else 'chord_progression'
    if verbose:
        log(' CHORD SEQUENCE MINER (CSM) ', center='/')
        log('Gathering data from knowledge base ...')
        log(' -[ API CONSUMPTION ]- ', center='-')
    request, data = http_request(base_url, '/api/mir/search', 'POST', body=params, verbose=verbose,
                                 log_width=log_width)
    if verbose:
        log('RESPONSE STATUS 200 OK. GOT DATA') if request.getcode() == 200 else \
            exit(str(request.getcode()) + ' - CONNECTION ERROR')
        log(' -[ API CONSUMPTION END ]- ', center='-')
        log('Successfully gathered data from knowledge base!')

        log(' => RULE GENERATOR <= ', center='-')
    pieces = list(data)

    if len(pieces) == 0:
        return []

    chords = set()
    for piece in pieces:
        [chords.add(chord) for chord in piece[progression_type]]

    chord_progressions = [piece[progression_type] for piece in pieces]

    min_sup = (2 / len(pieces))

    frequent_rules = []
    frequent_chords = []
    for f in get_frequents(chords, chord_progressions, min_sup):
        if f not in frequent_rules:
            frequent_rules.append(f)
            frequent_chords.append(f[0])

    if verbose:
        log('{:3}|{:3}|{:<}'.format('l'.center(3), 'n'.center(3),
                                    'chord sequences'.center(log_width - 8 - len(_log_prefix))))
        log('{:3}|{:3}| {:<}'.format(1, len(frequent_rules), str(frequent_rules)))

    i = 1
    while True:
        i += 1
        new = []
        valid_permutations = generate_valid_products(frequent_chords, i, frequent_rules)
        for f in get_frequents(valid_permutations, chord_progressions, min_sup):
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
        log(' CSM END ', center='/')

    return frequent_rules
