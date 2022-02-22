for nvar in 100
do
    for ncls in  100
    do
        for nltr in 3
        do
            ./solver 1 12345 $nvar $ncls $nltr 1 >/dev/null 2>/dev/null &
            ./solver 2 12345 $nvar $ncls $nltr 1;
            sleep 1 ;
            echo "############ single step  ##############" ;
            ./solver 1 12345 $nvar $ncls $nltr 532 >/dev/null 2>/dev/null &
            ./solver 2 12345 $nvar $ncls $nltr 532 ;
            sleep 1 ;
            echo "############ 100 steps  ##############" ;
        done
    done
done