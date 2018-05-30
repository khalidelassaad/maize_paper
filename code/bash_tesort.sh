#!/bin/bash

for i in $(ls TE_ids)
    do 
        echo Sorting $i
        python3 te_sort.py TE_ids/$i
        echo Sorting $i DONE
done
