#!/bin/bash

for i in $(ls TE_ids)
    do 
        echo Sorting $i
        mv TE_ids/$i TE_ids/$( basename $i )
        echo Sorting $i DONE
done
