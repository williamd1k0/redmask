#!/usr/bin/env python
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

import os
from random import randrange
from argparse import ArgumentParser
from PIL import Image
from .gpl import load_file as load_gpl

VERBOSE = False

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
    wrong_colors = []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixels[x, y] in pal:
                pixels[x, y] = process_pixel(
                    pal.index(pixels[x, y])*step,
                    normalized, random
                )
            elif pixels[x, y][3] == 0:
                for i, color in enumerate(pal):
                    if color[3] == 0:
                        pixels[x, y] = process_pixel(
                            i*step,
                            normalized, random
                        )
                        break
                else:
                    if VERBOSE: print('INFO: Ignoring transparent pixel')
            elif not pixels[x, y] in wrong_colors:
                wrong_colors.append(pixels[x, y])
                if VERBOSE: print('WARN: Wrong color/palette ', pixels[x, y])
    return mask

def apply_palette(mask, pal, step, transparent=False):
    img = mask.copy()
    pixels = img.load()
    wrong_colors = []
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if not transparent and pixels[x, y][-1] != 255:
                if VERBOSE: print('INFO: Ignoring transparent pixel')
                continue
            try:
                pixels[x, y] = pal[pixels[x, y][0]//step]
            except IndexError:
                if not pixels[x, y] in wrong_colors:
                    wrong_colors.append(pixels[x, y])
                    if VERBOSE: print('WARN: Wrong color/palette ', pixels[x, y])
    return img

def generate_palette(img, transparent=False):
    pal = []
    pixels = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if not pixels[x, y] in pal:
                if transparent or pixels[x, y][3] == 255:
                    pal.append(pixels[x, y])
    if VERBOSE: print('%s colors' % len(pal))
    pal_img = Image.new('RGBA', (len(pal), 1))
    pixels = pal_img.load()
    for x in range(pal_img.size[0]):
        pixels[x, 0] = pal[x]
    return pal_img

def parse_output(input_, output_=None, term='0'):
    if output_ is None:
        base = os.path.basename(input_)
        output_ = os.path.join(
            os.path.dirname(os.path.abspath(input_)),
            '{1}-{0}{2}'.format(term, *os.path.splitext(base))
        )
    return output_

def main(args):
    if args.apply:
        if VERBOSE: print('Applying palette...')
        mask = load_image(args.input)
        pal = load_palette(args.palette)
        img = apply_palette(mask, pal, abs(args.step), args.transparent)
        img.save(parse_output(args.input, args.output, 'new'))
    elif args.generate_pal:
        if VERBOSE: print('Generating palette...')
        img = load_image(args.input)
        pal = generate_palette(img, args.transparent)
        pal.save(parse_output(args.palette+'.png', args.output, 'pal'))
    else:
        if VERBOSE: print('Generating mask...')
        img = load_image(args.input)
        pal = load_palette(args.palette)
        mask = generate_mask(
            img, pal, abs(args.step),
            args.normalized, args.random
        )
        mask.save(parse_output(args.input, args.output, 'mask'))
    if VERBOSE: print('Done')

def dist_main():
    parser = ArgumentParser('redmask')
    apply_or_gen = parser.add_mutually_exclusive_group()
    parser.add_argument('input', type=str, metavar='<source.png>', help='input image')
    parser.add_argument('palette', type=str, metavar='<pal.png|gpl>', help='palette image')
    parser.add_argument('-o', '--output', type=str, metavar='<output.png>', help='output image')
    parser.add_argument('-s', '--step', type=int, metavar='<color-step=1>', default=1, help='mask color step')
    parser.add_argument('-r', '--random', type=str, metavar='<random=g|b|gb>', default='', help='use random values for green and/or blue')
    parser.add_argument('-n', '--normalized', action='store_true', help='set same value for red, green and blue')
    parser.add_argument('-t', '--transparent', action='store_true', help='take transparent colors into account')
    apply_or_gen.add_argument('-a', '--apply', action='store_true', help='apply palette to a mask')
    apply_or_gen.add_argument('-g', '--generate-pal', action='store_true', help='generate palette input')
    parser.add_argument('-v', '--verbose', action='store_true', help='enable verbose output')
    args = parser.parse_args()

    global VERBOSE
    VERBOSE = args.verbose
    main(args)

if __name__ == '__main__':
    dist_main()
