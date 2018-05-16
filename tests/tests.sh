#!/bin/bash
python ../redmask.py source.png palette.png --step 10
python ../redmask.py source-mask.png gb-pocket.gpl --step 10 --apply
