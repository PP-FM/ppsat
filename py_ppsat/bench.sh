#1!/usr/bin/sh

# NOTE: download data then specify its path in "basedir".
basedir=genos2sat/benchmarks
for genotype in n3r3 n3r4 n3r5 n6r6 n6r8 n6r10; do
    for fullfilename in $basedir/$genotype/*.cnf; do
        filename=$(basename $fullfilename)
        casenum=$(echo $filename | sed 's/genos.haps.\(.*\).cnf/\1/')
        for h in det rand wrand; do
            # echo $n $num $h
            python3 ppsat.py $fullfilename $genotype $casenum $h
        done
    done
done
