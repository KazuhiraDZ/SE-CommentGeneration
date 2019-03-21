import re
import json
import math
import random
from tqdm import tqdm
from collections import Counter
from collections import defaultdict
# 将数据集中的注释过滤掉
def filter_sentence_comment_and_enter(data):
    # 定义注释逻辑和空行逻辑
    pattern_1 = "[\t]{0,}\/\/[\S ]{0,}\n"
    pattern_2 = "\n[\n\t]{0,}\n"

    ret1 = re.findall(pattern_1, data)
    #ret2 = re.findall(pattern_2, data)

    # 删除注释
    for r in ret1:
        data = data.replace(r,"")
    # # 删除空行（一定概率不行）
    # for r in ret2:
    #     data = data.replace(r[1:],"")
    return data

# 制作数据集，这里不区分train/valid/test
def create_dataset(file_p, src_p, com_p):

    com_dict = {}
    with open(src_p, 'r') as fp, open(com_p,'r') as fp2:
        src = json.load(fp, parse_int=True)
        com = fp2.readlines()

    for com_str in com:
        num, comment = com_str.split("\t")
        # 取得正确的注释(去掉\n)，并且存入dict
        com_dict[num] = comment[:-1]

    # 读取source code，由于comment文件编号和src不同
    # 因此上面取得了dict之后根据key查到相应的comment
    count = 0
    miss = 0
    with open(file_p, "w") as f:
        for funid, code in tqdm(src.items()):
            counter = Counter(code)
            # 过滤注释和空行
            code = filter_sentence_comment_and_enter(code)
            nl = com_dict[funid]
            line_num = counter["\n"]
            # 过滤掉匹配错误以及行号小于5的
            if nl == 0 or line_num <= 5:
                if nl == 0:
                    miss += 1
                continue
            # 加入fun_id, code, nl以及line四项参数
            dict = {"fun_id":funid, "code":code, "nl":com_dict[funid], "line":line_num}
            json_dict = json.dumps(dict)
            count += 1
            f.write(json_dict+"\n")
    print("done!")

def split_dataset(dataset_p, data_path, valid_size = 0.05, test_size = 0.05):

    print("reading json...")
    with open(dataset_p, "r") as f:
        data = f.readlines()

    # 读取pid文件，保存成根据fid->pid的字典
    f = 'fid_pid'
    fidtopid = defaultdict(list)
    pidtofid = defaultdict(list)
    for line in open(data_path + f, 'r').readlines()[1:]:
        t = line.split('\t')
        fid = int(t[0])
        pid = int(t[1])
        fidtopid[fid] = pid
        pidtofid[pid].append(fid)

    shuffle_list = list(pidtofid.keys())
    random.shuffle(shuffle_list)

    testnum = math.ceil(len(shuffle_list) * test_size)
    validnum = math.ceil(len(shuffle_list) * valid_size)

    # 获得三种集合的pid编号
    testset = shuffle_list[:testnum]
    validset = shuffle_list[testnum:(testnum + validnum)]
    trainset = shuffle_list[(testnum + validnum):]

    print("Project counts:")
    print("Train: {} Valid: {} Test: {}".format(len(trainset), len(validset), len(testset)))

    # 获得三种集合的fid编号
    train_fid = [fid for pid in trainset for fid in pidtofid[pid]]
    valid_fid = [fid for pid in validset for fid in pidtofid[pid]]
    test_fid = [fid for pid in testset for fid in pidtofid[pid]]
    print("Function counts:")
    print("Train: {} Valid: {} Test: {}".format(len(train_fid), len(valid_fid), len(test_fid)))

    with open(data_path+"train.json","w") as f1, open(data_path+"valid.json","w") as f2, \
            open(data_path+"test.json","w") as f3:
        for item in tqdm(data):
            cur_item = eval(item)
            cur_fun_id = cur_item["fun_id"]
            if fidtopid[int(cur_fun_id)] in trainset:
                json_dict = json.dumps(cur_item)
                f1.write(json_dict + "\n")
            elif fidtopid[int(cur_fun_id)] in validset:
                json_dict = json.dumps(cur_item)
                f2.write(json_dict + "\n")
            elif fidtopid[int(cur_fun_id)] in testset:
                json_dict = json.dumps(cur_item)
                f3.write(json_dict + "\n")
            else:
                print("missing error!")
    print("done!")

# 从训练集、验证集、测试集三个原数据集中摘选出需要对比的数据
# 准备进行和ICSE的对比实验
def select_source_data_by_fun_id(data_p, dataset_path):
    print("reading myjson...")
    funid_list = []
    # 读取我们的数据
    with open(data_p, "r") as f:
        data = f.readline()

    # 获得数据中的fun_id
    for item in data:
        cur_funid = int(item.split("\t")[0])
        funid_list.append(cur_funid)
    data = []

    # 存储原始数据集的functions和comments
    dataset_list = [dataset_path+"/functions", dataset_path+"/comments"]
    dataset = []
    for src_file in dataset_list:
        dataelement = {}
        for line in open(src_file, "r"):
            tmp = line.split("\t")
            num = int(tmp[0])
            code_token = tmp[1]
            dataelement[num] = code_token
        dataset.append(dataelement)

    # 根据数据的fun_id找到原始数据集的对应数据
    # 写入到对应的新文件中
    with open(dataset_path+"/functions.filter1","w") as f1, open(dataset_path+"/comments.filter1","w") as f2:
        for id in funid_list:
            function = dataset[0][id]
            comment = dataset[1][id]
            f1.write(id + "\t" + function + "\n")
            f2.write(id + "\t" + comment + "\n")

    print("filter all the data in files.")


if __name__ == "__main__":

    src_path = "/Users/zhao/Desktop/amazon_data/funcom_processed/functions.json"
    com_path = "/Users/zhao/Desktop/amazon_data/funcom_processed/comments.filtered"
    file_path = "/Users/zhao/Desktop/amazon_data/funcom_processed/Myfile.json"

    split_dataset(file_path,"/Users/zhao/Desktop/amazon_data/funcom_processed/")

    select_source_data_by_fun_id(file_path,"/Users/zhao/Desktop/amazon_data/funcom_processed/")
