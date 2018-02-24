#!/bin/bash
# print categories of each snapshot
FILES=(2008-07 2008-11 2009-03 2009-07 2009-11 2010-03 2010-07 2010-11 2011-03 2011-07 2011-11 2012-03 2012-07 2012-11)

touch ./Stats/categories.txt

for F in ${FILES[@]}; do
    echo $F >> ./Stats/categories.txt
    python3 try_print.py -f ${F}.partition >> ./Stats/categories.txt
done