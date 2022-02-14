the DIMACS CNF file was created by
```
bash-4.3$ ./genos2sat -r 20 -n 10 -s -i verif_test/genos.haps.5
```
and the output given to a MiniSAT variant available online at https://msoos.github.io/cryptominisat_web/

the output was put into the `.sat` file, which can be verified with
```
bash-4.3$ cat verif_test/genos.haps.5.sat | ./haploverif -n 10 -r 20 verif_test/genos.haps.5
```