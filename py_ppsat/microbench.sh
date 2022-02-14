for nvar in 10 50 100 1000
  do
    for ncls in 100 500 1000 5000 10000
      do
        for nltr in 3
        do
            python3 microbenchmark.py $nvar $ncls $nltr $1
            sleep 1
          done
        done
    done