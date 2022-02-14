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
                "steps": float(strs[3])
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
        if (case["genotype"] == "n3" or case["genotype"] == "n6" ):
            case["prop_steps"] = case["steps"] * heuristics_proportion[h]* factor
        else:
            if h == "det":
                case["heuristics"] = "wrand"
                case["prop_steps"] = case["steps"] * 2.5
            if h == "wrand":
                case["heuristics"] = "det"
                case["prop_steps"] = case["steps"] * 0.48
            if h == "rand":
                case["prop_steps"] = case["steps"]




    # separate into 6 lines, and sort each according to prop_steps
    result = {}
    for genotype in ["n3", "n6", "n1", "n2", "n4", "n5", "n7","n8" ]:
        for h in ["det", "rand", "wrand"]:
            cases = [case for case in all_cases if case["heuristics"] == h and case["genotype"] == genotype and case["prop_steps"] <= 1750000]
            cases.sort(key=lambda c : c["prop_steps"]) # sort by prop_steps
            cases_le_me = 0
            for case in cases:
                cases_le_me += 1
                case["ratio"] = cases_le_me / 29
            xs = [case["prop_steps"] for case in cases]
            ys = [case["ratio"] for case in cases]
            # xs.append(175000)
            if len(ys) != 0:
                xs.append(200000)
                ys.append(ys[-1])
                xs = [0] + xs
                ys = [0] + ys

            else:
                xs.append(0)
                ys.append(0)
                xs.append(200000)
                ys.append(0)
            # ys.append(last_ratio)

            result[genotype, h] = (xs, ys)
    return result

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
#
# (x, y) = result2["n3r3", "wrand"]
# plt.plot(x, y, '-g*', label = "$|G|=3, r=3$, Weighted-RAND", color = "C1")
#
# (x, y) = result2["n3r3", "rand"]
# plt.plot(x, y, '-g|', label = "$|G|=3, r=3$, RAND", color = "C1")
#
# (x, y) = result2["n3r3", "det"]
# plt.plot(x, y, '-g>', label = "$|G|=3, r=3$, DLIS", color = "C1")
#
# (x, y) = result2["n3r4", "wrand"]
# plt.plot(x, y, '-g*', label = "$|G|=3, r=4$, Weighted-RAND", color = "C2")
#
# (x, y) = result2["n3r4", "rand"]
# plt.plot(x, y, '-g|', label = "$|G|=3, r=4$, RAND", color = "C2")
#
# (x, y) = result2["n3r4", "det"]
# plt.plot(x, y, '-g>', label = "$|G|=3, r=4$, DLIS", color = "C2")
#
# (x, y) = result2["n3r5", "wrand"]
# plt.plot(x, y, '-g*', label = "$|G|=3, r=5$, Weighted-RAND", color = "C3")
#
# (x, y) = result2["n3r5", "rand"]
# plt.plot(x, y, '-g|', label = "$|G|=3, r=5$, RAND", color = "C3")
#
# (x, y) = result2["n3r5", "det"]
# plt.plot(x, y, '-g>', label = "$|G|=3, r=5$, DLIS", color = "C3")
#

import os
lstyle = ['solid', 'dashed', 'dotted']
marker = ['x', '', 'd', 'p', 'v', '+', 's', '*' ]
j = 0
# size = ["$(60, 170)$", "(150, 170)", "(250, 1400)", "(350, 2600)",  "(400, 4000)",  "(600, 6000)",  "(800, 8000)",  "(900, 10000)"]
# for i in range(1,9):
#     result = process_genotype_data("./benchmark_result/"+"n"+str(i)+ ".watch")
#     para = str(i)
#     (x, y) = result["n"+para, "wrand"]
#     plt.plot(x, y,  '-'+marker[0], label="$|G|=$"+para+", W", color="C"+para)
#    # j = (j + 1) % 8
#     (x, y) = result["n"+para, "rand"]
#     plt.plot(x, y,  '-'+marker[1], label="$|G|=$"+para+", R", color="C"+para)
#    # j = (j + 1) % 8
#     (x, y) = result["n"+para, "det"]
#     plt.plot(x, y,  '-'+marker[7], label="$|G|=$"+para+", D", color="C"+para)
    #j = (j + 1) % 8
   # print(j)

# x = [0, 0];
# y = [0, 0];
# plt.plot(x, y,  'r-', label =  "$(\#var, \#clause)$", alpha=0)


for i in range(1,9):
    # if (i == 6 or i ==3):
    #     continue;
    result = process_genotype_data("./benchmark_result/"+"n"+str(i)+ ".watch")
    para = str(i)
    (x, y) = result["n"+para, "wrand"]
    plt.plot(x, y,  '-'+marker[i-1],  label="$|G|=$"+para+", W", color="C"+para)
    j = (j + 1) % 8
    (x, y) = result["n"+para, "rand"]
    plt.plot(x, y,  '-'+marker[1], label="$|G|=$"+para+", R", color="C"+para)
   # j = (j + 1) % 8
    (x, y) = result["n"+para, "det"]
    plt.plot(x, y,  '-'+marker[7], label="$|G|=$"+para+", D", color="C"+para)
    j = (j + 1) % 8
    print(j)




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
          fancybox=True, ncol= 2)

fig.savefig('./figs_new/benchmark_system.pdf', bbox_extra_artists = (lgd,),
            bbox_inches='tight' )
plt.show()



