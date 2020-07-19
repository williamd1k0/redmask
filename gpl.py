"""
Meteor License

2020 - William Tumeo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to no conditions.

The above author notice and this permission notice can be included in all
copies or substantial portions of the Software, but only if you so desire.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

HEADER = 'GIMP Palette'
PARAM_NAME = 'Name:'
PARAM_COLUMNS = 'Columns:'
PARAMS_COUNT = 2
COMMENT = '#'

def check_header(line):
    return line == HEADER

def check_params(line):
    if line.startswith(PARAM_NAME):
        return {'name': line.split(':')[1].strip()}
    elif line.startswith(PARAM_COLUMNS):
        return {'columns': line.split(':')[1].strip()}
    return None

def is_comment(line):
    return line.startswith(COMMENT)

def get_color(line):
    line = line.replace('\t', ' ')
    color_name = [c for c in line.split(' ') if c != ""]
    if len(color_name) >= 4:
        color = tuple(int(value) for value in color_name[:3])
        return color, ' '.join(color_name[3:])
    return None

def load_lines(lines):
    data = {
        'name': '',
        'columns': 4,
        'comments': [],
        'colors': [],
        'names': []
    }
    params_check = False
    for n, line in enumerate(lines):
        line = line.strip()
        if n == 0:
            if not check_header(line):
                raise Exception("Header won't match.")
            continue
        if is_comment(line):
            data['comments'].append(line['#' in line:].strip())
            continue
        elif not params_check:
            p = check_params(line)
            if not p is None:
                data.update(p)
                continue
            else:
                params_check = True
        color = get_color(line)
        if not color is None:
            data['colors'].append(color[0])
            data['names'].append(color[1])
    return data

def load_file(path):
    with open(path, 'r') as gpl:
        pal = load_lines(gpl.readlines())
    return pal


if __name__ == '__main__':
    import sys
    pal = load_file(sys.argv[-1])
    print('Name:', pal['name'])
    print('Columns:', pal['columns'])
    for name, color in zip(pal['names'], pal['colors']):
        print(name, *color)
