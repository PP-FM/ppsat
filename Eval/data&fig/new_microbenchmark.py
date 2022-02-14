import matplotlib.pyplot as plt
import math


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

def init_plotting(fig_width = 8, fig_height = 0, font=14):
    golden_mean = (math.sqrt(5)-1.0)/2.0    # Aesthetic ratio
    if fig_height == 0:
        fig_height = fig_width*golden_mean # height in inches
    plt.rcParams['text.usetex'] = True
    plt.rcParams['figure.figsize'] =[fig_width,fig_height]
    plt.rcParams['font.size'] = font
    #plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = 'Times'
    plt.rcParams['axes.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize'] = 1.5*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize'] = plt.rcParams['font.size']


init_plotting()
results_det = data_process("result_det")
results_rand = data_process("result")
results_wrand = data_process("result_w_r")

# fig, axs = plt.subplots(1, 4, sharey=True)
#

# f = plt.figure(figsize=(10,3))
# axs =[]
# axs[0] = f.add_subplot(121)
# axs[1] = f.add_subplot(122)
# axs[2] = f.add_subplot(123)
# axs[3] = f.add_subplot(124)

f, axs = plt.subplots(1,4, sharey= True, figsize = (15, 4))

# f.suptitle('Vertically stacked subplots')


nvar_axis = [10, 50, 100, 1000]

bi_time_axis_100 = [tc.unit_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.unit_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.unit_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.unit_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]
axs[0].plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
axs[0].plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1" )
axs[0].plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
axs[0].plot(nvar_axis, bi_time_axis_10000, '-*', label = "10000 clauses", color = "C3")
axs[0].set_xscale('log')
axs[0].set_yscale('log')
axs[0].set_title('(a) Unit Search', fontsize = 14)


bi_time_axis_100 = [tc.propagation_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.propagation_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.propagation_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.propagation_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]

axs[1].plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
axs[1].plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1" )
axs[1].plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
axs[1].plot(nvar_axis, bi_time_axis_10000, '-*', label = "10000 clauses", color = "C3")
axs[1].set_xscale('log')
axs[1].set_yscale('log')
axs[1].set_title('(b) Propagation', fontsize = 14)


bi_time_axis_100 = [tc.check_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.check_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.check_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.check_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]

axs[2].plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
axs[2].plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1" )
axs[2].plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
axs[2].plot(nvar_axis, bi_time_axis_10000, '-*', label = "10000 clauses", color = "C3")
axs[2].set_xscale('log')
axs[2].set_yscale('log')
axs[2].set_title('(c) Check', fontsize = 14)


bi_time_axis_100 = [tc.backtrack_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.backtrack_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.backtrack_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.backtrack_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]

axs[3].plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
axs[3].plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1" )
axs[3].plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
axs[3].plot(nvar_axis, bi_time_axis_10000, '-*', label = "10000 clauses", color = "C3")
axs[3].set_xscale('log')
axs[3].set_yscale('log')
axs[3].set_title('(d) Backtrack', fontsize = 14)


# plt.xlabel('Number of variables (n)')

for ax in axs.flat:
    ax.set_aspect(1.0 / ax.get_data_ratio(), adjustable='box')
    ax.set(xlabel='Number of variables (n)')
axs[0].set(ylabel= 'Time (s)')

handles, labels = axs[0].get_legend_handles_labels()
f.legend(handles, labels, loc='upper center', ncol = 4)
plt.savefig("./figs_new/microbenchmark.pdf", bbox_inches='tight', dpi=200)
plt.show()
