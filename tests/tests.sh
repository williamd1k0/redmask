#!/usr/bin/sh
cd ..
python -m redmask -v tests/source.png tests/palette.png --step 10 -o tests/test-mask.png
python -m redmask -v tests/test-mask.png tests/gb-pocket.gpl --step 10 --apply -o tests/test-gb-pocket.png
