#!/usr/bin/env python3.8
import matplotlib.pyplot as plt
import matplotlib as mpl
import math

heuristics_proportion = {
    "det": 0.5,
    "rand": 0.4,
    "wrand": 1
}

def process_genotype_data(filename):
    # read file
    all_cases = []
    with open(filename) as infile:
        lines = infile.readlines()
        for line in lines:
            strs = line.split()
            case = {
                "genotype": strs[0],
                "casenum": int(strs[1]),
                "heuristics": strs[2],
                "steps": int(strs[3])
            }
            if case["steps"] == -1:
                continue
            all_cases.append(case)

    # add propotional steps
    for case in all_cases:
        h = case["heuristics"]
        if (case["genotype"] == "n6"):
            factor = 36
        if (case["genotype"] == "n3"):
            factor = 3
        if (case["genotype"] == "n3r3"):
            factor = 1
        if (case["genotype"] == "n3r3"):
            factor = 1
        if (case["genotype"] == "n3r4"):
            factor = 1.5
        if (case["genotype"] == "n3r5"):
            factor = 2.4





        case["prop_steps"] = case["steps"] * heuristics_proportion[h]* factor

    # separate into 6 lines, and sort each according to prop_steps
    result = {}
    for genotype in ["n3", "n6", "n3r3", "n3r4", "n3r5"]:
        for h in ["det", "rand", "wrand"]:
            cases = [case for case in all_cases if case["heuristics"] == h and case["genotype"] == genotype and case["prop_steps"] <= 1750000]
            cases.sort(key=lambda c : c["prop_steps"]) # sort by prop_steps
            cases_le_me = 0
            for case in cases:
                cases_le_me += 1
                case["ratio"] = cases_le_me / 29

            xs = [0] + [case["prop_steps"] for case in cases]
            ys = [0] + [case["ratio"] for case in cases]
            # xs.append(175000)

            if len(ys) != 0:
                xs.append(175000)
                ys.append(ys[-1])
            else:
                xs.append(0)
                ys.append(0)
                xs.append(175000)
                ys.append(0)
            # ys.append(last_ratio)
            result[genotype, h] = (xs, ys)
    return result

result1 = process_genotype_data("SAT.watch")
# print(result["n3", "det"])
# print(result["n3", "rand"])
# print(result["n3", "wrand"])
# print(result["n6", "det"])
# print(result["n6", "rand"])
# print(result["n6", "wrand"])
result2 = process_genotype_data("UNSAT.watch")

def init_plotting(fig_width = 8, fig_height = 0, font= 20):
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
fig = plt.figure()
init_plotting()


(x, y) = result2["n3r3", "wrand"]
plt.plot(x, y,  label ="$r=3$, W", color = "C2", linestyle = "dashdot")

(x, y) = result2["n3r3", "rand"]
plt.plot(x, y,  label ="$r=3$, R", color = "C2", linestyle = "dashed")

(x, y) = result2["n3r3", "det"]
plt.plot(x, y,  label ="$ r=3$, D", color = "C2")

(x, y) = result2["n3r4", "wrand"]
plt.plot(x, y, '-p', label = "$r=4$, W", color = "C1")

(x, y) = result2["n3r4", "rand"]
plt.plot(x, y, '-s', label = "$r=4$, R", color = "C1")

(x, y) = result2["n3r4", "det"]
plt.plot(x, y, '-go', label = "$r=4$, D", color = "C1")


(x, y) = result2["n3r5", "wrand"]
plt.plot(x, y, '-1', label = "$r=5$, W", color = "C3")

(x, y) = result2["n3r5", "rand"]
plt.plot(x, y, '-x', label = "$r=5$, R", color = "C3")

(x, y) = result2["n3r5", "det"]
plt.plot(x, y, '-|', label = "$r=5$, D", color = "C3")

(x, y) = result1["n3", "wrand"]
plt.plot(x, y, '-*', label = "$r=6$, W", color = "C4")

(x, y) = result1["n3", "rand"]
plt.plot(x, y, '-d', label = "$r=6$, R", color = "C4")

(x, y) = result1["n3", "det"]
plt.plot(x, y, '-g>', label = "$r=6$, D", color = "C4")

# (x, y) = result1["n6", "wrand"]
# plt.plot(x, y, '-g*', label = "$|G|=6, r=12$, Weighted-RAND", color = "C5")
#
# (x, y) = result1["n6", "det"]
# plt.plot(x, y, '-g>', label = "$|G|=6, r=12$, DLIS", color = "C5")
#
# (x, y) = result1["n6", "rand"]
# plt.plot(x, y, '-g|', label = "$|G|=6, r=12$, RAND", color = "C5")






ax = plt.subplot(111)
ax.set_ylabel ('Proportion of instances solved')
ax.set_xlabel ('Time (s)')
ax.set_xscale('log')

#
props = dict(boxstyle='round', facecolor='w', alpha=0.5)
textstr = "D: DLIS heuristic  ~~R: RAND heuristic ~~W: Weighted-RAND heuristic"
txt = ax.text(0.03, 1.1,  textstr, transform=ax.transAxes, fontsize=15,
        verticalalignment='top', bbox=props)
#
lgd = plt.legend(loc='upper left', bbox_to_anchor=(1, 1.13),
          fancybox=True, ncol= 1)

fig.savefig('./figs_new/benchmark_system_r.pdf', bbox_extra_artists = (lgd, txt,),
            bbox_inches='tight' )

