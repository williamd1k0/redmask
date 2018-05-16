"""
MIT License

Copyright (c) 2018 William Tumeo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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
        return {'name': line[len(PARAM_NAME):].strip()}
    elif line.startswith(PARAM_COLUMNS):
        return {'columns': line[len(PARAM_COLUMNS):].strip()}
    raise Exception('Wrong param')

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
    params = {
        'header': HEADER,
        'comments': [],
        'colors': [],
        'names': []
    }
    params_count = 0
    for n, line in enumerate(lines):
        line = line.strip()
        if n == 0:
            if not check_header:
                raise Exception("Header won't match.")
        elif params_count < PARAMS_COUNT:
            params_count += 1
            params.update(check_params(line))
        elif is_comment(line):
            params['comments'].append(line)
        else:
            color = get_color(line)
            if color is not None:
                params['colors'].append(color[0])
                params['names'].append(color[1])
    return params

def load_file(path):
    with open(path, 'r') as gpl:
        pal = load_lines(gpl.readlines())
    return pal


if __name__ == '__main__':
    import sys
    pal = load_file(sys.argv[-1])
    print(pal)
