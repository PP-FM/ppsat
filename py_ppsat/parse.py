filename = "verif_test/genos.haps.5.cnf"

with open(filename, "r") as infile:
    first_line = infile.readline().split()
    nvar = int(first_line[2])
    ncls = int(first_line[3])
    for i in range(0, ncls):
        line = infile.readline().split()
        for var_raw in line[:-1]:
            pass