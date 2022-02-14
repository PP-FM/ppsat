import sys

def process_genotype_data(filename):
    # read file
    all_cases = []
    with open(filename) as infile:
        lines = infile.readlines()
        for line in lines:
            strs = line.split()
            # print(strs)
            if (len(strs) < 2):
                continue
            if strs[1] == "process-time:" :
                return (strs[len(strs) -2])
                # for i in range(len(strs)+1):
                #     if strs[i] == "seconds":
                #         return strs[i-1]
                #     else:
                #         return 10000000


if __name__ == "__main__":
    filename = sys.argv[1];
    time = process_genotype_data(filename)
    print(sys.argv[2], sys.argv[3],sys.argv[4], time)