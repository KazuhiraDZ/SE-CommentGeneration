from collections import Counter
from tqdm import tqdm
import matplotlib.pyplot as plt

def count_for_line(line):
    num, rest_portion = line.split("\t")
    nodes = rest_portion.split(" ")
    return num, nodes

def distribution_for_file(file="../data_version8.0/train/train.token.code"):

    token_counter = Counter()
    num2nodes = {}
    max_sum = 0
    max_num = 0
    min_sum = 10000
    min_num = 0

    with open(file,"r") as f:
        lines = f.readlines()
        for line in tqdm(lines):
            t_num, t_nodes = count_for_line(line)
            t_node_dict = {}
            t_node_dict["node"] = t_nodes
            t_node_dict["token_num"] = len(t_nodes)

            if min_sum > len(t_nodes):
                min_sum = len(t_nodes)
                min_num = t_num
            if max_sum < len(t_nodes):
                max_sum = len(t_nodes)
                max_num = t_num

            num2nodes[str(t_num)] = t_node_dict
            token_counter[len(t_nodes)] += 1

    ans = token_counter.most_common(200)

    #print(num2nodes["100"]["token_num"])
    # 一共有多少类别
    print("all categories:")
    print(len(token_counter))

    # 统计x和y
    x = [item[0] for item in ans]
    y = [item[1] for item in ans]
    y_all = [item for item in token_counter.values()]
    #print(ans)
    print("top-{} take {:.4}".format(len(ans), float(sum(y))/sum(y_all)))


    # 统计出现频率
    print(sum(y))

    # 最短数据&最长数据
    print(min_num, min_sum)
    print(max_num, max_sum)
    # print(num2nodes[str(min_num)]["node"])
    # print(num2nodes[str(max_num)]["node"])

    plt.scatter(x,y)
    plt.show()

def count_token_for_dict(dictfile="../data_version8.0/vocab.code", keywords=["SplitInvocationToken","SplitMethodToken"]):

    with open(dictfile,"r") as f:
        words = f.readlines()

    method_count = 0
    invocation_count = 0

    for word in words:
        if keywords[0] in word:
            invocation_count += 1
        elif keywords[1] in word:
            method_count += 1

    print("number of all word: {}".format(len(words)))
    print("number of methodtoken: {}  |  {:.4}".format(method_count, float(method_count)/len(words)))
    print("number of invocationtoken: {}  |  {:.4}".format(invocation_count, float(invocation_count)/len(words)))

if __name__ == "__main__":
    distribution_for_file("../data_version8.0/train/train.token.code")
    #count_token_for_dict("../data_version8.0/vocab.code")

