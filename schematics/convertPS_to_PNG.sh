#!/bin/bash

f=$1
b="${f%.*}"
echo "$b"

gs -dSAFER -r900 -dEPSCrop -sDEVICE=pnggray -dDownScaleFactor=4 -o "$b".png "$f" && convert -negate "$b".png "$b".png
