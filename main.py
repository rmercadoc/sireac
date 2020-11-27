from client_credentials import url as base_url
from http_request import http_request
from typing import Any
from itertools import product


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
    # n = sum([len(e) for e in haystack])  # / len(haystack)
    # print('n', n)
    for needle in needles:
        count = 0
        for element in haystack:
            # count += len(find(needle, element))
            count += 1 if find(needle, element) else 0
        # print('count', count)
        # if (count / n) > min_sup:
        if (count / len(haystack)) >= min_sup:
            frequent.append([needle]) if not isinstance(needle, list) else frequent.append(needle)
    # print('GET FREQUENTS |', '\n\t' + str(needles), '\n\t' + str(haystack), '\n\t' + str(frequent))
    return frequent


def generate_valid_products(elements: list, length: int, valid_rules: list):
    valid = []
    # p_list = list(product(elements, repeat=length))
    p_list = []
    minor_len_rules = []
    for rule in valid_rules:
        if len(rule) == length - 1:
            for e in elements:
                test = [r for r in rule]
                test.append(e)
                p_list.append(test)

    # print(p_list)
    for p in p_list:
        frequent_children = True
        for index in range(len(list(p))):
            if list(p)[index:index + (length - 1)] not in valid_rules:
                frequent_children = False
                break
        if frequent_children:
            valid.append(list(p))
    # print(valid)
    return valid


sentiments = ['anger', 'fear', 'love', 'joy', 'sadness', 'surprise']
min_sup = 0.17

for sentiment in sentiments:
    print('-'*50)
    print(sentiment.upper())
    print('\nREQUESTING DATA TO ' + base_url)
    request, data = http_request(base_url, '/api/mir/' + sentiment)
    print('GOT DATA\n') if request.getcode() == 200 else exit(str(request.getcode()) + ' - CONNECTION ERROR')
    pieces = list(data)

    if len(pieces) == 0:
        continue

    chords = set()
    for piece in pieces:
        [chords.add(chord) for chord in piece['chord_progression']]

    chord_progressions = [piece['chord_progression'] for piece in pieces]

    min_sup = (2 / len(pieces))

    frequent_rules = []
    frequent_chords = []
    for f in get_frequents(chords, chord_progressions, min_sup):
        if f not in frequent_rules:
            frequent_rules.append(f)
            frequent_chords.append(f[0])

    print(len(frequent_rules), frequent_rules)

    i = 1
    while True:
        i += 1
        print('i =', i)
        new = []
        valid_permutations = generate_valid_products(frequent_chords, i, frequent_rules)
        for f in get_frequents(valid_permutations, chord_progressions, min_sup):
            if f not in frequent_rules:
                frequent_rules.append(f)
                new.append(f)
        print(len(new), new)
        if not new:
            break

    print('FINAL n=' + str(len(frequent_rules)), ' |', frequent_rules)

    print('-' * 50)
