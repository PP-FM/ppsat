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


import matplotlib.pyplot as plt
bi_det = "result_det"
bi_random= "result"
results = data_process(bi_det)

def i_forget():
    s = set()
    for tc in results:
        s.add(tc.nvar)
    print(sorted(s))

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


i_forget()
init_plotting()
s = set()
for tc in results:
    s.add(tc.ncls)
print(sorted(s))

labels = ['m = 1000, n = 1000', 'm = 10000, n = 100', 'm = 5000, n = 1000']

unit_search_det = [tc.unit_time for tc in results if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
check_det = [tc.check_time for tc in results  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
decision_det = [tc.guess_time for tc in results  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
propagation_det = [tc.propagation_time for tc in results  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
backtrack_det = [tc.backtrack_time for tc in results  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
gate = [tc.num_of_gate for tc in results  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]

results1 = data_process(bi_random)

unit_search_r = [tc.unit_time for tc in results1 if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
check_r = [tc.check_time for tc in results1  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
decision_r = [tc.guess_time for tc in results1  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
propagation_r = [tc.propagation_time for tc in results1  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
backtrack_r = [tc.backtrack_time for tc in results1  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
gate_r = [tc.num_of_gate for tc in results1  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]

results2 = data_process("result_w_r")
unit_search_w = [tc.unit_time for tc in results2 if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
check_w = [tc.check_time for tc in results2  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
decision_w = [tc.guess_time for tc in results2  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
propagation_w = [tc.propagation_time for tc in results2  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
backtrack_w = [tc.backtrack_time for tc in results2  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]
gate_w_r = [tc.num_of_gate for tc in results2  if (tc.ncls == 1000 and tc.nvar == 1000 and tc.nltr == 3)  or (tc.ncls == 10000 and tc.nvar == 100  and tc.nltr == 3) or (tc.ncls == 5000 and tc.nvar == 1000  and tc.nltr == 3) ]

import matplotlib.pyplot as plt
import  numpy as np
# fig, ax = plt.subplots()
#
# de_bar_list = [plt.bar([0, 1, 2], df.usd, align='edge', width= 0.2),
#                plt.bar([0, 1, 2], df.cd, align='edge', width= 0.2),
#                plt.bar([0, 1, 2], df.dd, align='edge', width=0.2),
#                plt.bar([0, 1, 2], df.pd, align='edge', width=0.2),
#                plt.bar([0, 1, 2], df.bd, align='edge', width=0.2)
#                ]
#
# rand_bar_list = [plt.bar([0, 1, 2], df.usr, align='edge', width= -0.15),
#                plt.bar([0, 1, 2], df.cr, align='edge', width= -0.15),
#                plt.bar([0, 1, 2], df.dr, align='edge', width=-0.15),
#                plt.bar([0, 1, 2], df.pr, align='edge', width=-0.15),
#                plt.bar([0, 1, 2], df.br, align='edge', width=-0.15)
#               ]


width = 0.15     # the width of the bars: can also be len(x) sequence

fig, ax = plt.subplots(figsize=(30, 14))

total = unit_search_det
total_r = unit_search_r
total_w = unit_search_w
x = np.arange(len(labels))
x = x /1.40

ax.bar(x- width -0.03,  unit_search_det, width, label='Unit Search',  edgecolor='black', color = 'pink')
ax.bar(x,  unit_search_r, width, edgecolor='black', color = 'pink')
ax.bar(x+ width +0.03,  unit_search_w, width, edgecolor='black', color = 'pink')

ax.bar(x- width -0.03,  decision_det, width,  bottom=total, label='Decision', hatch = '/',  edgecolor='black',  color = 'lightskyblue')
ax.bar(x, decision_r, width,  bottom=total_r, hatch = '/',  edgecolor='black',  color = 'lightskyblue')
ax.bar(x+ width + 0.03, decision_w, width,  bottom=total_w, hatch = '/',  edgecolor='black',  color = 'lightskyblue')



total = [x + y for x,y in zip(decision_det, total)]
total_r = [x + y for x,y in zip(decision_r, total_r)]
total_w = [x + y for x,y in zip(decision_w, total_w)]


rects_det =  ax.bar(x- width -0.03, check_det, width,  bottom=total,
       label='Check', edgecolor='black', hatch = '\\',  color = 'bisque')
rects_r = ax.bar(x, check_r, width,  bottom=total_r,
        edgecolor='black', hatch = '\\',  color = 'bisque')
rects_w = ax.bar(x+ width +0.03, check_w, width,  bottom=total_w,
        edgecolor='black', hatch = '\\',  color = 'bisque')

total = [x + y for x,y in zip(check_det, total)]
total_r = [x + y for x,y in zip(check_r, total_r)]
total_w = [x + y for x,y in zip(check_w, total_w)]

ax.bar(x -  width-0.03, propagation_det, width,  bottom=total,
       label='Propagation', hatch = '+',  edgecolor='black',  color = 'thistle')
ax.bar(x  , propagation_r, width,  bottom=total_r,
       hatch = '+',  edgecolor='black',  color = 'thistle')
ax.bar(x + width +0.03, propagation_w, width,  bottom=total_w,
       hatch = '+',  edgecolor='black',  color = 'thistle')

total =   [x + y for x,y in zip(propagation_det, total)]
total_r =   [x + y for x,y in zip(propagation_r, total_r)]
total_w =   [x + y for x,y in zip(propagation_w, total_w)]


rects_det =  ax.bar(x- width -0.03, backtrack_det, width,  bottom=total,
       label='Backtrack', edgecolor='black', hatch = '/',  color = 'red')
rects_r = ax.bar(x, backtrack_r, width,  bottom=total_r,
        edgecolor='black', hatch = '/',  color = 'red')
rects_w = ax.bar(x+ width +0.03, backtrack_w, width,  bottom=total_w,
        edgecolor='black', hatch = '/',  color = 'red')


ax.set_xticks(x)
ax.set_xticklabels(labels,  horizontalalignment = 'center', fontsize = 60)
# ax.tick_params(axis='', which='major', pad=10)


ax.set_ylabel ('Time (s)', fontsize = 80 )
ax.legend(loc='upper left', bbox_to_anchor=(1, 0.6), ncol= 1, fancybox=True, shadow= False, fontsize = 60)
ax.yticks(fontsize = 60)



case = ["R", "R", "R"]
for height, rect, label in zip(total_r, rects_r, case):
    ax.text(rect.get_x() + rect.get_width() / 2 , height + 0.1, label,
            ha='center', va='bottom', fontsize = 40)

case = ["D", "D", "D"]
for height, rect, label in zip(total, rects_det, case):
    ax.text(rect.get_x() + rect.get_width() / 2 , height + 0.1, label,
            ha='center', va='bottom', fontsize = 40)
case = ["W", "W", "W"]
for height, rect, label in zip(total_w, rects_w, case):
    ax.text(rect.get_x() + rect.get_width() / 2, height + 0.1, label,
            ha='center', va='bottom',fontsize = 40  )

props = dict(boxstyle='round', facecolor='w', alpha=0.5)

textstr = "D: DLIS  \nR: RAND  \nW: Weighted-RAND "
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=60,
        verticalalignment='top', bbox=props)

# ax2 = ax.twinx()
# ax2.plot(gate, linestyle='-', marker='o', linewidth=2.0, label = "D: DILS heuristic")
# ax2.plot(gate_w_r, linestyle='-', marker='>', linewidth=2.0,  label = "R: RAND heuristic")
# ax2.plot(gate_r, linestyle='-', marker='*', linewidth=2.0, label = "W: weighted-RAND heuristic")
# ax2.set_ylim(10**7, 10**10)
# ax2.set_yscale("log")
# ax2.set_yscale("log")
# ax2.set_ylabel("number of gates")
# ax2.legend(loc = "upper left")

fig.savefig('./figs_new/stackedbarchart.pdf', bbox_inches='tight', dpi=200)







# init_plotting(16, 4)
# labels = ['pri']#'ResNet50', 'ResNet50A', 'ResNet101', 'ResNet101B']
# total = [0, 0]
# width = 0.2       # the width of the barhs: can also be len(x) sequence
# fig, ax = plt.subplots(frameon=False)
#
# for i in range():
# 	value = [res101pri[i]]#, res101pub[i]]
# 	ax.barh([1], value, width, left = total, label=stage[i])
# 	total = [x + y for x,y in zip(value, total)]
# plt.legend(loc='upper center', ncol = 5)
# plt.ylim([0.6,1.4])
# plt.savefig("time.pdf", bbox_inches='tight', dpi=400)
