#!/usr/bin/env python3.8

heuristics_proportion = {
    "det": 12,
    "rand": 9,
    "wrand":21
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
        case["prop_steps"] = case["steps"] * heuristics_proportion[h]

    # separate into 6 lines, and sort each according to prop_steps
    result = {}
    for genotype in ["n3", "n6"]:
        for h in ["det", "rand", "wrand"]:
            cases = [case for case in all_cases if case["heuristics"] == h and case["genotype"] == genotype]
            cases.sort(key=lambda c : c["prop_steps"]) # sort by prop_steps
            cases_le_me = 0
            for case in cases:
                cases_le_me += 1
                case["ratio"] = cases_le_me / 29
            xs = [case["prop_steps"] for case in cases]
            ys = [case["ratio"] for case in cases]
            result[genotype, h] = (xs, ys)
    return result

# test
result = process_genotype_data("watch")
print(result["n3", "det"])
print(result["n3", "rand"])
print(result["n3", "wrand"])
print(result["n6", "det"])
print(result["n6", "rand"])
print(result["n6", "wrand"])
