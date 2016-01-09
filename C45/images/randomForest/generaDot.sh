#!/bin/bash

for f in *.dot; do
    dot -Tpng $f -o ${f%.*}.png
done


