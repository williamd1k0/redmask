#!/usr/bin/sh
python ../redmask.py source.png palette.png --step 10 -o test-mask.png
python ../redmask.py test-mask.png gb-pocket.gpl --step 10 --apply -o test-gb-pocket.png
