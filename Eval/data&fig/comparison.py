import math
def process_data(filename):
    # read file
    all_cases = {}
    with open(filename) as infile:
        lines = infile.readlines()
        for line in lines:
            strs = line.split()
            all_cases[(int(strs[1]), int(strs[5]))] = float(strs[0])
    return all_cases

table = process_data("one_giant")

class realCase:
    def __init__(self, nvar, nltr, ncls, total_time, num_of_round):
        self.nvar = nvar
        self.nltr = nltr
        self.ncls = ncls
        self.total_time = total_time
        self.num_of_round = num_of_round

    def __repr__(self):
        res = ""
        res += "nvar:{}, ".format(self.nvar)
        res += "nltr:{}, ".format(self.nltr)
        res += "ncls:{}, ".format(self.ncls)
        res += "total:{}, ".format(self.total_time)
        res += "number_of_round:{}".format(self.num_of_round)
        return res

def data_process_r(filename):
    results = []
    with open(filename) as f:

        while (True):
            # Read a line.
            line = f.readline()
            # print(line)
            # When readline returns an empty string, the file is fully read.
            if len(line) == 0:
                print("::DONE::")
                break
            # When a newline is returned, the line is empty.
            if line == "finish generate\n":
                round = f.readline()
                nor = int(round.split()[1])
                skip = f.readline()
                total = f.readline()
                total_time = float(total.split()[2])
                instance = f.readline()
                nvar = int(instance.split()[0])
                nltr = int(instance.split()[2])
                ncls = int(instance.split()[4])
                skip = f.readline()
                tc = realCase(nvar, nltr, ncls, total_time, nor)
                results.append(tc)
    return results



result_real = data_process_r("real.result")
s = []

for tc in result_real:
    noc = tc.ncls
    nov = tc.nvar
    step_length = table[(nov, noc)]
    projected = step_length * (tc.num_of_round-1)
    s.append((tc.num_of_round, tc.total_time, projected, (tc.total_time- projected) / tc.total_time))
    print(tc.num_of_round, tc.nvar, tc.ncls, ":", (tc.total_time- projected) / tc.total_time)


s.sort(key = lambda x: x[0])
print(s)


