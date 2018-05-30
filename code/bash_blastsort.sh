#!/bin/bash

for i in $(ls ../blast/outfiles/maizegenome_*)
    do 
        echo Sorting $i
        python3 blast_sort.py $i $( basename $i )
        echo Sorting $i DONE
done
