import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl
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



dashes = ["-", "--", "-.", ":"]
#colors2 = ["r", "b+", "gx", "bv"]
colors = ["#eb3426", "#37e650", "#142f8a"]
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



results_det = data_process("result_det")
results_rand = data_process("result")
results_wrand = data_process("result_w_r")
results_wrand_p = data_process("wrand.result.plaintext")
results_det_p = data_process("det.result.plaintext")
results_rand_p = data_process("rand.result.plaintext")


nvar_axis = [10, 50, 100, 1000]

init_plotting()
fig1 = plt.figure(1)

#mpl.style.use("default")
plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')

bi_time_axis_100 = [tc.unit_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.unit_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.unit_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.unit_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]

bi_time_axis_100_p = [tc.unit_time for tc in results_wrand_p if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000_p = [tc.unit_time for tc in results_wrand_p if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000_p = [tc.unit_time for tc in results_wrand_p if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000_p = [tc.unit_time for tc in results_wrand_p if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]


plt.plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
plt.plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1" )
plt.plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
plt.plot(nvar_axis, bi_time_axis_10000, '-yv', label = "10000 clauses", color = "C3")
plt.xscale('log')
plt.yscale('log')

ax = plt.subplot(111)
plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')

c_time = np.array([tc.unit_time for tc in results_det if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.unit_time for tc in results_det_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print("unit search:", ratio)


# ax2 = ax.twinx()
# ax2.plot(nvar_axis, bi_time_axis_100_p, '-gD', label = "100 clauses, plaintext", color = "C0", linestyle = "dashed")
# ax2.plot(nvar_axis, bi_time_axis_1000_p, '-b^',  label = "1000 clauses, plaintext", color = "C1", linestyle = "dashed" )
# ax2.plot(nvar_axis, bi_time_axis_5000_p, '-r|',  label = "5000 clauses, plaintext", color = "C2", linestyle = "dashed")
# ax2.plot(nvar_axis, bi_time_axis_10000_p, '-yv', label = "10000 clauses, plaintext", color = "C3", linestyle = "dashed")

ax.legend(loc='upper left',
          fancybox= False, ncol= 1, frameon=False)



fig1.savefig('./figs_new/unit_search_bi.pdf', bbox_inches='tight', dpi=200)

bi_time_axis_100 = [tc.propagation_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.propagation_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.propagation_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.propagation_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]

#mpl.style.use("default")
init_plotting()
fig2 = plt.figure(2)

plt.plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
plt.plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1")
plt.plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
plt.plot(nvar_axis, bi_time_axis_10000, '-yv', label = "10000 clauses", color = "C3")
plt.xscale('log')
plt.yscale('log')

plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')

#plt.title("Propagation Using ADS of Algorithm 1 ")
ax = plt.subplot(111)
ax.legend(loc='upper left', frameon=False)

fig2.savefig('./figs_new/propagation_bi.pdf', bbox_inches='tight', dpi=200)


bi_time_axis_100 = [tc.check_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.check_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.check_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.check_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]

#mpl.style.use("default")
init_plotting()

fig3 = plt.figure(3)

plt.plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
plt.plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1")
plt.plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
plt.plot(nvar_axis, bi_time_axis_10000, '-yv', label = "10000 clauses", color = "C3")
plt.xscale('log')
plt.yscale('log')

plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')


init_plotting()
ax = plt.subplot(111)

#plt.title("Check Using ADS of Algorithm 1 ")
ax.legend(loc='upper left', frameon=False)

fig3.savefig('./figs_new/check_bi.pdf', bbox_inches='tight', dpi=200)

init_plotting()
fig4 = plt.figure(4)

bi_time_axis_100 = [tc.backtrack_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.backtrack_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.backtrack_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.backtrack_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]


plt.plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
plt.plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1")
plt.plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
plt.plot(nvar_axis, bi_time_axis_10000, '-yv', label = "10000 clauses", color = "C3")
plt.xscale('log')
plt.yscale('log')

plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')

init_plotting()
ax = plt.subplot(111)

ax.legend(loc='upper left', frameon=False)

fig4.savefig('./figs_new/backtrack_bi.pdf', bbox_inches='tight', dpi=200)

init_plotting()
fig5 = plt.figure(5)

bi_time_axis_100 = [tc.total_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.total_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.total_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.total_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]


plt.plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
plt.plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1")
plt.plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
plt.plot(nvar_axis, bi_time_axis_10000, '-yv', label = "10000 clauses", color = "C3")
plt.xscale('log')
plt.yscale('log')

plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')

#plt.title("Total Time Using ADS of Algorithm 1 ")
init_plotting()
ax = plt.subplot(111)
ax.legend(loc='upper left', frameon=False)

fig5.savefig('./figs_new/total_bi.pdf', bbox_inches='tight', dpi=200)


bi_time_axis_100 = [tc.guess_time for tc in results_det if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.guess_time for tc in results_det if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.guess_time for tc in results_det if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.guess_time for tc in results_det if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]

init_plotting()
fig6 = plt.figure(6)
#mpl.style.use("default")

plt.plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
plt.plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1")
plt.plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
plt.plot(nvar_axis, bi_time_axis_10000, '-yv', label = "10000 clauses", color = "C3")
plt.xscale('log')
plt.yscale('log')

plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')

init_plotting()
ax = plt.subplot(111)
ax.legend(loc='upper left', frameon=False)
fig6.savefig('./figs_new/decision_bi_det.pdf', bbox_inches='tight', dpi=200)

init_plotting()
fig7 = plt.figure(7)
#mpl.style.use("default")


bi_time_axis_100 = [tc.guess_time for tc in results_rand if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.guess_time for tc in results_rand if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.guess_time for tc in results_rand if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.guess_time for tc in results_rand if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]


plt.plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
plt.plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1")
plt.plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
plt.plot(nvar_axis, bi_time_axis_10000, '-yv', label = "10000 clauses", color = "C3")
plt.xscale('log')
plt.yscale('log')

plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')

ax = plt.subplot(111)
ax.legend(loc='upper left', frameon=False)

fig7.savefig('./figs_new/decision_bi_rand.pdf', bbox_inches='tight', dpi=200)


fig8 = plt.figure(8)


bi_time_axis_100 = [tc.guess_time for tc in results_wrand if tc.ncls == 100 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_1000 = [tc.guess_time for tc in results_wrand if tc.ncls == 1000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_5000 = [tc.guess_time for tc in results_wrand if tc.ncls == 5000 and tc.nvar in nvar_axis and tc.nltr == 3]
bi_time_axis_10000 = [tc.guess_time for tc in results_wrand if tc.ncls == 10000 and tc.nvar in nvar_axis and tc.nltr == 3]

#mpl.style.use("default")

plt.plot(nvar_axis, bi_time_axis_100, '-gD', label = "100 clauses", color = "C0")
plt.plot(nvar_axis, bi_time_axis_1000, '-b^',  label = "1000 clauses", color = "C1")
plt.plot(nvar_axis, bi_time_axis_5000, '-r|',  label = "5000 clauses", color = "C2")
plt.plot(nvar_axis, bi_time_axis_10000, '-yv', label = "10000 clauses", color = "C3")
plt.xscale('log')
plt.yscale('log')

plt.ylabel ('Time (s)')
plt.xlabel ('Number of variables (n)')

ax = plt.subplot(111)
ax.legend(loc='upper left', frameon=False)

fig8.savefig('./figs_new/decision_bi_wrand.pdf', bbox_inches='tight', dpi=200)


plt.show()

c_time = np.array([tc.unit_time for tc in results_det if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.unit_time for tc in results_det_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print("unit search:", ratio)


c_time = np.array([tc.propagation_time for tc in results_det if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.propagation_time for tc in results_det_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print("propagation:", ratio)

c_time = np.array([tc.check_time for tc in results_det if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.check_time for tc in results_det_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print("check:", ratio)

c_time = np.array([tc.backtrack_time for tc in results_det if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.backtrack_time for tc in results_det_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print("backtrack:", ratio)

c_time = np.array([tc.guess_time for tc in results_rand if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.guess_time for tc in results_rand_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print("rand:", ratio)

c_time = np.array([tc.total_time for tc in results_rand if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.total_time for tc in results_rand_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print(c_time)
print(p_time)
print("rand_t:", ratio)

# c_time = np.array([tc.guess_time for tc in results_wrand if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
# p_time = np.array([tc.guess_time for tc in results_wrand_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
# ratio = c_time/p_time
# print(c_time)
# print(p_time)
# print("wrand:", ratio)

c_time = np.array([tc.total_time for tc in results_wrand if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.total_time for tc in results_wrand_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print(c_time)
print(p_time)
print("wrand_t:", ratio)

# c_time = np.array([tc.guess_time for tc in results_det if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
# p_time = np.array([tc.guess_time for tc in results_det_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
# ratio = c_time/p_time
# print("det:", ratio)

c_time = np.array([tc.total_time for tc in results_det if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
p_time = np.array([tc.total_time for tc in results_det_p if (tc.nvar == 50 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 100 and tc.ncls == 10000 and tc.nltr == 3) or (tc.nvar == 1000 and tc.ncls == 5000 and tc.nltr == 3)])
ratio = c_time/p_time
print(c_time)
print(p_time)
print("det_t:", ratio)

