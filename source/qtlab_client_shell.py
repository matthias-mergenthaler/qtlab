import os
import sys

def insert_in_file_list(entries, entry, ignore_list):
    adddir, addname = entry
    if os.path.splitext(addname)[1] != ".py":
        return

    for start in ignore_list:
        if addname.startswith(start):
            return

    index = 0
    for (dir, name) in entries:
        if name[0] > addname[0] or (name[0] == addname[0] and name[1] > addname[1]):
            entries.insert(index, entry)
            break
        index += 1

    if index == len(entries):
        entries.append(entry)

def get_shell_files(path, ignore_list):
    ret = []

    entries = os.listdir(path)
    for i in entries:
        if len(i) > 0 and i[0] == '.':
            continue

        if os.path.isdir(i):
            subret = get_shell_files(path + '/' + i)
            for j in subret:
                insert_in_file_list(ret, j, ignore_list)
        else:
            insert_in_file_list(ret, (path, i), ignore_list)

    return ret


if __name__ == '__main__':
    print 'Starting QT Lab environment...'

    sys.path.append('%s/source/' % os.getcwd())

    _vars = {}
    _vars['ignorelist'] = []
    _vars['i'] = 1
    while _vars['i'] < len(sys.argv):
        if sys.argv[_vars['i']] == '-i':
            i += 1
            _vars['ignorelist'].append(sys.argv[_vars['i']])
        _vars['i'] += 1

    _vars['filelist'] = get_shell_files('shell', _vars['ignorelist'])
    for (_vars['dir'], _vars['name']) in _vars['filelist']:
        _vars['filename'] = '%s/%s' % (_vars['dir'], _vars['name'])
        print 'Executing %s...' % (_vars['filename'])
        execfile(_vars['filename'])
