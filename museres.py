import getopt
import sys
import json
import pymusicFP.knowledgeBase as kb
from pymusicFP.profileProcessing import displace_profiles_by_key
from secuence_miner import generate_rules
from pymusicFP.pymusicFP import mir
from printer import printer
from datetime import datetime
from itertools import combinations

_log_prefix = '>'
_log_width = 80

_detail = False


class Recommendation:

    def __init__(self, recommended_chords: list[str], mir: dict = None):
        self._mir = mir
        self._recommended_chords = recommended_chords

    @property
    def chords(self):
        if self._mir:
            return [RecommendedChord(chord, self._mir['dominant_key']) for chord in self._recommended_chords]
        else:
            return [RecommendedChord(chord) for chord in self._recommended_chords]

    @property
    def __dict__(self):
        if self._mir:
            return {
                'detected_dominant_key': self._mir['dominant_key'],
                'chord_recommendations': [x.__dict__ for x in self.chords]
            }
        else:
            return {
                'chord_recommendations': [x.__dict__ for x in self.chords]
            }

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__dict__)


class RecommendedChord:

    def __init__(self, chord_degree: str, dominant_key: str = None):
        self._dominant_key = dominant_key
        self.key = dominant_key.split(' ')[0] if dominant_key else ''
        if dominant_key:
            self.scale = dominant_key.split(' ')[1] if len(dominant_key.split(' ')) > 1 else ''
        self._chord_degree = chord_degree.split(' ')[0]
        self._chord_quality = chord_degree.split(' ')[1] if len(chord_degree.split(' ')) > 1 else ''

    @property
    def key_index(self):
        if self._dominant_key:
            return kb.NOTES.index(self.key)
        else:
            return

    @property
    def name(self):
        if self._dominant_key:
            displaced_degrees = displace_profiles_by_key(self.key_index, kb.SCALE_DEGREES)
            return kb.NOTES[displaced_degrees.index(self._chord_degree)] + self._chord_quality
        else:
            return

    @property
    def degree(self):
        return self._chord_degree + ' ' + self._chord_quality if self._chord_quality else self._chord_degree

    @property
    def __dict__(self):
        if _detail:
            if self._dominant_key:
                return {
                    'degree': self.degree,
                    'name': self.name
                }
            return {'degree': self.degree}
        return self._chord_degree

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__dict__)


def log(*args, center: str = None):
    printer(*args, prefix=_log_prefix, width=_log_width, center=center)


def main(argv):
    start_time = datetime.now()
    global _log_width
    global _detail
    score = None
    score_mi = None
    sentiments = {}
    progression_type = 'chord_progression'
    verbose = False
    recommendations_amount = 3
    try:
        opts, args = getopt.getopt(argv, 'hs:w:dvn:', ['help', 'score=', 'n=', 'width=', 'anger=', 'fear=',
                                                      'joy=', 'love=', 'sadness=', 'surprise='])
    except getopt.GetoptError:
        print('museres.py -s <path-to-score> --anger= --fear= --joy= --love= --sadness= --surprise=')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            log('museres.py -s <path-to-score> '
                '--anger=(1-5) --fear=(1-5) --joy=(1-5) --love=(1-5) --sadness=(1-5) --surprise=(1-5)')
            sys.exit()
        elif opt == '-d':
            _detail = True
            progression_type = 'chord_progression_detail'
        elif opt == '-v':
            verbose = True
        elif opt in ('-s', '--score'):
            try:
                if arg.split('.')[-1] != 'musicxml':
                    raise ValueError
                open(arg, 'r')
            except OSError:
                print('\tERROR: Invalid score file path', arg)
                sys.exit()
            except ValueError:
                print('\tERROR:\tInvalid score file format', arg)
                print('\t\tFile format must be .musicxml')
                sys.exit()
            score = arg
        elif opt in ('-n', '--n'):
            try:
                if int(arg) > 10:
                    raise ValueError('Max amount of recommendations is 10')
                elif int(arg) <= 0:
                    raise ValueError('Min amount of recommendations is 1')
                recommendations_amount = int(arg)
            except ValueError as e:
                print('\tERROR:\t', e)
                sys.exit()
        elif opt in ('-w', '--width'):
            if int(arg) > _log_width:
                _log_width = int(arg)
        elif opt in ('--anger', '--fear', '--joy', '--love', '--sadness', '--surprise'):
            if not 1 <= int(arg) <= 5:
                print('\tERROR:\tInvalid value for', opt + '.')
                print('\t\tValue', arg, 'is out of range.', '\'' + opt + '\'', 'must be in range [1-5].')
                exit()
            sentiments[opt.replace('-', '')] = arg

    if verbose:
        print('-' * _log_width)
        print('888b     d888 888     888  .d8888b.  8888888888 8888888b.  8888888888 .d8888b.  ')
        print('8888b   d8888 888     888 d88P  Y88b 888        888   Y88b 888       d88P  Y88b ')
        print('88888b.d88888 888     888 Y88b.      888        888    888 888       Y88b.      ')
        print('888Y88888P888 888     888  "Y888b.   8888888    888   d88P 8888888    "Y888b.   ')
        print('888 Y888P 888 888     888     "Y88b. 888        8888888P"  888           "Y88b. ')
        print('888  Y8P  888 888     888       "888 888        888 T88b   888             "888 ')
        print('888   "   888 Y88b. .d88P Y88b  d88P 888        888  T88b  888       Y88b  d88P ')
        print('888       888  "Y88888P"   "Y8888P"  8888888888 888   T88b 8888888888 "Y8888P"  ')
        print('\n', 'MUSIC SENTIMENT BASED CHORD RECOMMENDER SYSTEM'.center(75), '\n')
        log('[START]:', start_time)
        log('INPUT:')
        if score and len(score) > (_log_width - 33):
            log('\tscore file:\t\t', score[:int(_log_width*0.25)] + '...' + score[-int(_log_width*0.25):])
        else:
            log('\tscore file:\t', score)

        if len(sentiments.keys()) > 1:
            log('\tsearch:\t\t {')
            for k, v in sentiments.items():
                log('\t\t\t {:>10}: {:<}'.format(k, v))
            log('\t\t\t }')
        else:
            log('\tsearch:\t\t\t', sentiments)
        log('\tchord detail:\t\t', _detail)
        log('\trecommendations amount:\t', recommendations_amount, '\n')

    recommendations = []

    search_list = [sentiments]

    if score:
        if verbose:
            log('Analyzing score, retrieving music information...')
        score_mi = mir(score, log_width=_log_width, verbose=verbose)
        if verbose:
            log('Music information retrieved from score.')

    while len(recommendations) < recommendations_amount:
        rules = []
        if verbose:
            log('Generating chord sequence association rules...')
        for search in search_list:
            [rules.append(r) for r in generate_rules(search, progression_type, log_width=_log_width, verbose=verbose)]
        if verbose:
            log('Found', len(rules), 'chord sequence rules.')

        if len(rules) > 0:
            if verbose:
                log('Sorting rules ...')
            rules.sort(key=lambda x: (x.confidence, x.support, x.lift), reverse=True)
            if verbose:
                log('Sorted rules!')

            if score:
                progression = score_mi[progression_type]
                for rule in rules:
                    if len(rule) > 1:
                        if rule[:-1] == progression[-(len(rule)-1):] or progression == rule[:-1]:
                            if rule[-1] not in recommendations:
                                recommendations.append(rule[-1])
                    if len(recommendations) >= recommendations_amount:
                        break

                if len(recommendations) < recommendations_amount:
                    for rule in rules:
                        if rule[0] not in recommendations:
                            recommendations.append(rule[0])
                        if len(recommendations) >= recommendations_amount:
                            break
            else:
                for rule in rules:
                    if rule[0] not in recommendations:
                        recommendations.append(rule[0])
                    if len(recommendations) >= recommendations_amount:
                        break

        if len(recommendations) < recommendations_amount:
            if verbose:
                log('Dividing search parameters ...')
            new_search_list = []
            for keys in list(combinations(sentiments.keys(), len(search_list[0].keys()) - 1)):
                search_dict = {}
                for key in keys:
                    search_dict[key] = sentiments[key]
                new_search_list.append(search_dict)
            search_list = new_search_list
            if verbose:
                log('Divided original search in sub-searches:')
                [log(s) for s in search_list]

    if not score:
        recommendations = Recommendation(recommendations)
    else:
        recommendations = Recommendation(recommendations, mir=score_mi)

    if verbose:
        log(' RECOMMENDATIONS ', center='-')
        for recommendation in recommendations.chords:
            log('{:>8} - {:<8}'.format(recommendation.degree, recommendation.name), center=' ')
    else:
        print(json.dumps(recommendations.__dict__))

    end_time = datetime.now()
    if verbose:
        log(center='-')
        log('[END]', end_time)
        log('[EXECUTION-TIME]', end_time - start_time)


if __name__ == '__main__':
    main(sys.argv[1:])
