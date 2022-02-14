basedir=~/Code/ppsat/py_ppsat/genos2sat/benchmarks
for genotype in n1 n2 n3 n4 n5 n6 n7 n8; do
    for fullfilename in $basedir/$genotype/*.cnf; do
        filename=$(basename $fullfilename)
        casenum=$(echo $filename | sed 's/genos.haps.\(.*\).cnf/\1/')
#        for h in det rand wrand; do
#            # echo $n $num $h
#            python3 ppsat.py $fullfilename $genotype $casenum $h
#        done
         ./build/kissat $fullfilename > result
        # echo $genotype $casenum KISSAT
         python3 parse.py result $genotype $casenum KISSAT
    done
done