def printer(*args, prefix: str or list = '>', width: int = None, center: str = None):
    final_str = ''
    for arg in args:
        final_str += str(arg) + ' '
    final_str = final_str[:-1]
    str_list = final_str.split('\n')
    for line in str_list:
        if center:
            line = line.center(width - len(prefix) - 1, center)
        if width:
            line_width = width
            if '\t' in final_str:
                line_width = line_width - (7 * final_str.count('\t'))
            if len(line) > (line_width - len(prefix)):
                line = line[:line_width - len(prefix) - 5] + ' ...'
        if prefix:
            if isinstance(prefix, list):
                print('> ' + str(prefix)[1:-1].replace(' ', '').replace(',', ' > ').replace('\'', '') + ' >', line)
            elif prefix != '>':
                print('> ' + prefix + ' >', line)
            else:
                print(prefix, line)
        else:
            print(line)


def prepare_log(_log_width: int = 80, log_width: int = 80,
                _log_prefix: str or list = None,  log_prefix: str or list = None):
    _log_width = log_width
    if log_prefix:
        if isinstance(log_prefix, list):
            _log_prefix = [x for x in log_prefix].append(_log_prefix)
        else:
            _log_prefix = [log_prefix, _log_prefix]
    return _log_width, _log_prefix
