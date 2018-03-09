#!/bin/bash
# Compares every pair of consecutive partitions
FILES=(2008-07 2008-11 2009-03 2009-07 2009-11 2010-03 2010-07 2010-11 2011-03 2011-07 2011-11 2012-03 2012-07 2012-11)

for i in `seq 0 12`; do
    echo "From ${FILES[$i]} to ${FILES[$((i + 1))]}"
    echo "-----------------------------------------"
    echo "-----------------------------------------"
    python3 compare.py -f1 ${FILES[$i]}.partition -f2 ${FILES[$((i + 1))]}.partition
    echo
done
