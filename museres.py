import getopt
import sys
from secuence_miner import generate_rules
from pymusicFP.pymusicFP import mir
from printer import printer
from datetime import datetime

_log_prefix = '>'
_log_width = 80


def log(*args, center: str = None):
    printer(*args, prefix=_log_prefix, width=_log_width, center=center)


def main(argv):
    start_time = datetime.now()
    global _log_width
    score = None
    sentiments = {}
    detail = False
    verbose = False
    try:
        opts, args = getopt.getopt(argv, 'hs:dv', ['help', 'score=', 'width=', 'anger=', 'fear=',
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
            detail = True
        elif opt == '-v':
            verbose = True
        elif opt == '--width':
            arg = int(arg)
            if arg > _log_width:
                _log_width = arg
        elif opt in ('-s', '--score'):
            try:
                open(arg, 'r')
            except OSError:
                print('\tERROR: Invalid score file path', arg)
                sys.exit()
            score = arg
        elif opt in ('--anger', '--fear', '--joy', '--love', '--sadness', '--surprise'):
            if not 1 <= int(arg) <= 5:
                print('\tERROR:\tInvalid value for', opt + '.')
                print('\t\tValue', arg, 'is out of range.', '\'' + opt + '\'', 'must be in range [1-5].')
                exit()
            sentiments[opt.replace('-', '')] = arg

    if verbose:
        print('[START]:', start_time)
        print('-'*_log_width)
        print('888b     d888 888     888  .d8888b.  8888888888 8888888b.  8888888888 .d8888b.  ')
        print('8888b   d8888 888     888 d88P  Y88b 888        888   Y88b 888       d88P  Y88b ')
        print('88888b.d88888 888     888 Y88b.      888        888    888 888       Y88b.      ')
        print('888Y88888P888 888     888  "Y888b.   8888888    888   d88P 8888888    "Y888b.   ')
        print('888 Y888P 888 888     888     "Y88b. 888        8888888P"  888           "Y88b. ')
        print('888  Y8P  888 888     888       "888 888        888 T88b   888             "888 ')
        print('888   "   888 Y88b. .d88P Y88b  d88P 888        888  T88b  888       Y88b  d88P ')
        print('888       888  "Y88888P"   "Y8888P"  8888888888 888   T88b 8888888888 "Y8888P"  ')
        print('\n', 'MUSIC SENTIMENT BASED CHORD RECOMMENDER SYSTEM'.center(75), '\n')
        print('INPUT:')
        if score and len(score) > (_log_width - 24):
            print('\tscore file:\t', score[:_log_width//0.225] + '...' + score[-(_log_width//2.35):])
        else:
            print('\tscore file:\t', score)

        if len(sentiments.keys()) > 1:
            print('\tsearch:\t\t {')
            for k, v in sentiments.items():
                print('\t\t\t {:>10}: {:<}'.format(k, v))
            print('\t\t\t }')
        else:
            print('\tsearch:\t\t', sentiments)
        print('\tchord detail:\t', detail, '\n')

    if verbose:
        log('Generating chord sequence association rules...')
    rules = generate_rules(sentiments, detail, log_width=_log_width, verbose=verbose)
    if verbose:
        log('Found', len(rules), 'chord sequence rules.')

    if score:
        if verbose:
            log('Analyzing score, retrieving music information...')
        score_mi = mir(score, log_width=_log_width, verbose=verbose)
        if verbose:
            log('Music information retrieved from score.')

    end_time = datetime.now()
    if verbose:
        print('-'*_log_width)
        print('[END]', end_time)
        print('[EXECUTION-TIME]', end_time - start_time)


if __name__ == '__main__':
    main(sys.argv[1:])
