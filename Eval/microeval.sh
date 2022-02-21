for nvar in 10 50 100 1000
do
    for ncls in 100 500 1000 5000 10000
    do
        for nltr in 3
        do
            ./microtest 1 12345 $nvar $ncls $nltr 1 >/dev/null 2>/dev/null &
            ./microtest 2 12345 $nvar $ncls $nltr 1

            sleep 1
            echo "##########################"
        done
    done
done