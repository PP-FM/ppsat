import matplotlib.pyplot as plt
import matplotlib as mpl
import  numpy as np
import  math

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
        self.num_of_gate = num_of_gate;

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
        res += "number_of_gate:{}".format(self.num_of_gategate)
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

def init_plotting(fig_width = 8, fig_height = 0):
    golden_mean = (math.sqrt(5)-1.0)/2.0    # Aesthetic ratio
    if fig_height == 0:
        fig_height = fig_width*golden_mean # height in inches
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] =[fig_width,fig_height]
    # plt.rcParams['font.size'] = font
    #plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Times'
    plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.5*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']

results_det = data_process("result_det")
results_rand = data_process("result")
results_wrand = data_process("result_w_r")

labels = ["100 clauses", "1000 clauses", "5000 clauses", "10000 clauses"]
ncls_axis = [100,1000, 5000, 10000]



mpl.style.use("default")
width = 0.15       # the width of the bars: can also be len(x) sequence
init_plotting()
fig, ax = plt.subplots(figsize=(30, 12))

bi_time_axis_det = [tc.guess_time for tc in results_det if tc.nvar == 100 and tc.ncls in ncls_axis and tc.nltr == 3]

bi_time_axis_rand = [tc.guess_time for tc in results_rand if tc.nvar == 100 and tc.ncls in ncls_axis and tc.nltr == 3]

bi_time_axis_wrand = [tc.guess_time for tc in results_wrand if tc.nvar == 100 and tc.ncls in ncls_axis and tc.nltr == 3]

x = np.arange(len(labels))
x = x /1.25

ax.bar(x -  width -0.05, bi_time_axis_det, width, label='DLIS', edgecolor='black', color = 'pink')
ax.bar(x,  bi_time_axis_rand, width, label='RAND', hatch = '\\', edgecolor='black',color = 'bisque')
ax.bar(x + width +0.05,  bi_time_axis_wrand, width, label='Weighted-RAND', hatch ='/' , edgecolor='black', color = 'lightskyblue')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize = 60)
# ax.set_yticks(fontsize = 60)

plt.yticks(fontsize = 60)


ax.set_ylabel ('Time (s)',  fontsize = 60)
ax.legend(loc='upper left', fontsize = 60)
fig.savefig('./figs_new/heuristics.pdf', bbox_inches='tight', dpi=200)

plt.show()

