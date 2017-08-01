"""
MIT License

Copyright (c) 2017 William Tumeo

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

import os
from random import randrange
from argparse import ArgumentParser
from PIL import Image
from gpl import load_file as load_gpl


def load_image(path):
    return Image.open(path).convert('RGBA')

def load_palette(path):
    if path.endswith('.gpl'):
        gpl = load_gpl(path)
        return tuple(color + (255,) for color in gpl['colors'])
    else:
        img = load_image(path)
        pixels = img.load()
        return tuple(pixels[x, 0] for x in range(img.size[0]))


def process_pixel(red, normalized=False, random=''):
    if normalized:
        return red, red, red, 255
    if 'g' in random or 'b' in random:
        color = (red,)
        color += (randrange(0, 255),) if 'g' in random else (0,)
        color += (randrange(0, 255),) if 'b' in random else (0,)
        color += (255,)
        return color
    return red, 0, 0, 255

def generate_mask(img, pal, step, normalized=False, random=''):
    mask = img.copy()
    pixels = mask.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixels[x, y] in pal:
                pixels[x, y] = process_pixel(
                    pal.index(pixels[x, y])*step,
                    normalized, random
                )
            elif pixels[x, y][3] == 0:
                print('INFO: Ignoring transparent pixel')
            else:
                print('WARN: Wrong color/palette ', pixels[x, y])
    return mask

def apply_palette(mask, pal, step):
    img = mask.copy()
    pixels = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            pixels[x, y] = pal[pixels[x, y][0]//step]
    return img

def parse_output(input_, output_=None, term='0'):
    if output_ is None:
        base = os.path.basename(input_)
        output_ = os.path.join(
            os.path.dirname(os.path.abspath(input_)),
            '{1}-{0}{2}'.format(term, *os.path.splitext(base))
        )
    return output_

def main(args):
    if not args.apply:
        print('Generating mask...')
        img = load_image(args.input)
        pal = load_palette(args.palette)
        mask = generate_mask(
            img, pal, abs(args.step),
            args.normalized, args.random
        )
        mask.save(parse_output(args.input, args.output, 'mask'))
    else:
        print('Applying palette...')
        mask = load_image(args.input)
        pal = load_palette(args.palette)
        img = apply_palette(mask, pal, abs(args.step))
        img.save(parse_output(args.input, args.output, 'new'))
    print('Done')


if __name__ == '__main__':
    arg_parse = ArgumentParser('redmask')
    arg_parse.add_argument('input', type=str, metavar='<source.png>', help='input image')
    arg_parse.add_argument('palette', type=str, metavar='<pal.png|gpl>', help='palette image')
    arg_parse.add_argument('-o', '--output', type=str, metavar='<output.png>', help='output image')
    arg_parse.add_argument('-s', '--step', type=int, metavar='<color-step=1>', default=1, help='mask color step')
    arg_parse.add_argument('-r', '--random', type=str, metavar='<random=g|b|gb>', default='', help='use random values for green and/or blue')
    arg_parse.add_argument('-n', '--normalized', action='store_true', default=False, help='set same value for red, green and blue')
    arg_parse.add_argument('-a', '--apply', action='store_true', default=False, help='apply palette to a mask')
    args = arg_parse.parse_args()

    main(args)
