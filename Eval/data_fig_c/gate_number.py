import np as np
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class TestCase:
    def __init__(self, nvar, nltr, ncls, unit_time, guess_time, propagation_time, backtrack_time, check_time, total_time, num_of_gate):
        self.nvar = nvar
        self.nltr = nltr
        self.ncls = ncls
        self.unit_time = unit_time
        self.guess_time = guess_time
        self.propagation_time = propagation_time
        self.backtrack_time = backtrack_time
        self.check_time = check_time
        self.total_time = total_time
        self.num_of_gate = num_of_gate

    def __repr__(self):
        res = ""
        res += "nvar:{}, ".format(self.nvar)
        res += "nltr:{}, ".format(self.nltr)
        res += "ncls:{}, ".format(self.ncls)
        res += "unit_time:{}, ".format(self.unit_time)
        res += "guess_time:{}, ".format(self.guess_time)
        res += "propagation_time:{}, ".format(self.propagation_time)
        res += "backtrack_time:{}, ".format(self.backtrack_time)
        res += "check_time:{}".format(self.check_time)
        res += "number_of_gate:{}".format(self.num_of_gate)
        return res

def data_process(filename):
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
                unit = f.readline()
                unit_time = float(unit.split()[2])
                guess = f.readline()
                guess_time = float(guess.split()[1])
                mux = f.readline()
                mux_time = float(mux.split()[1])
                check = f.readline()
                check_time = float(check.split()[1])
                backtrack = f.readline()
                backtrack_time = float(backtrack.split()[1])
                propagation = f.readline()
                propagation_time = float(propagation.split()[1])
                total = f.readline()
                total_time = float(total.split()[2])
                instance = f.readline()
                nvar = int(instance.split()[0])
                nltr = int(instance.split()[2])
                ncls = int(instance.split()[4])
                gate = f.readline()
                number_of_gate = int(gate.split()[0])


                tc = TestCase(nvar, nltr, ncls, unit_time, guess_time, propagation_time, backtrack_time, check_time,
                              total_time, number_of_gate)
                results.append(tc)
    return results


results_d = data_process("result_det")
results_r = data_process("result")
results_w_r = data_process("result_w_r")

fig, ax = plt.subplots()
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')
num_gate_d = [tc.num_of_gate for tc in results_d  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 100  and tc.nltr == 3) ]
num_gate_r = [tc.num_of_gate for tc in results_r  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 100  and tc.nltr == 3)]
num_gate_w_r = [tc.num_of_gate for tc in results_w_r  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 100  and tc.nltr == 3)]

table_data=[
    ["DLIS"]+ num_gate_d,
    ["r"] + num_gate_r,
   ["w"]+ num_gate_w_r
]


# df = pd.DataFrame(["DLIS", num_gate_d], ["RAND", num_gate_r], ["Weighted RAND", num_gate_w_r])
table = ax.table(cellText= table_data, loc='center')
table.set_fontsize(14)
table.scale(1,4)
ax.axis('off')
fig.tight_layout()
plt.show()


