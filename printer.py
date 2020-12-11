def printer(*args, prefix: str = '>', width: int = None, center: str = None):
    final_str = ''
    for arg in args:
        final_str += str(arg) + ' '
    str_list = final_str.split('\n')
    for line in str_list:
        if center:
            line = line.center(width - len(prefix) - 1, center)
        if width:
            if len(line) > width:
                line = line[:width - len(prefix) - 5] + ' ...'
        print(prefix, line)
