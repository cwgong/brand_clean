import re
import configparser
import json
# from brand_reg_tool import BrandRegTool
# own_eng_rgx = ""
def judge_eng(s):
    own_eng_rgx = re.findall('[a-zA-Z]+', s)
    all_eng_rgx = re.findall('[\u4e00-\u9fa5]+',s)

    if own_eng_rgx == []:
        own_eng_flag = False
    else:
        own_eng_flag = True

    if all_eng_rgx == []:
        all_eng_flag = True
    else:
        all_eng_flag = False

    return own_eng_flag,all_eng_flag


def judge_telephone(telephone_name,goods_str):
    telephone_list = ["苹果","华为","三星","一加","小米","oppo","vivo","诺基亚","摩托罗拉","iphone","联想","金立","中兴","宏达",\
                      "索尼","美图","酷派","锤子","努比亚","360","魅族"]
    tools_list = ["手机壳","支架","钢化膜","手机套","数据线","充电线","磨砂壳","麦克风","声卡","水凝膜","无线充电器"]
    flag_1 = 0
    flag_2 = 0

    for telephone in telephone_list:
        if telephone in goods_str:
            flag_1 = 1
            break

    for tool in tools_list:
        if tool in goods_str:
            flag_2 = 1
            break

    if telephone_name in telephone_list and flag_1 == 1 and flag_2 == 1:
        return False
    else:
        return True

def getting_special_brand_dict(brand_file):
    special_brand_dict = {}
    with open(brand_file,"r",encoding="utf-8") as f1:
        for line in f1:
            line = line.strip()
            if line == "": continue
            #if idx % 1000 == 0: print("loading standard-brand: %s" % idx)
            # brand_id, brand_name, cat1_id, cat1, gmv
            lst1 = line.split("\t")
            if len(lst1) != 2:
                continue
            lst1 = [tmp.strip() for tmp in lst1]
            b_id, b_name = lst1
            special_brand_dict[b_id] = b_name
    return special_brand_dict

def extend_special_brand(standard_brand_file,s_brand_dict):
    idx = 0
    standard_brand_id_list = []
    standard_brand_list = {}
    s_extension_brand_dict = {}
    with open(standard_brand_file,"r",encoding="utf-8") as f1:
        while True:
            line = f1.readline()
            if line != "":
                line_ = line.strip()
                idx += 1
                if line_ == "":continue
                lst1 = line.split("\t")
                if len(lst1) != 5:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, b_name, cat1_id, cat1, gmv = lst1
                standard_brand_list[b_id] = b_name
                standard_brand_id_list.append(b_id)
            else:
                break

    s_brand_value_list = list(s_brand_dict.values())

    idx_ = 0
    for s_name in s_brand_value_list:
        # idx += 1
        # if idx % 10 == 0: print(s_name)
        for standard_brand_id in standard_brand_id_list:
            if s_name in standard_brand_list[standard_brand_id]:
                idx_ += 1
                s_extension_brand_dict[standard_brand_id] = standard_brand_list[standard_brand_id]
    return s_extension_brand_dict

def _loading_co_occurrence(co_occurrence_file):
    co_occurrence_dict = {}
    config = configparser.ConfigParser()
    config.read(co_occurrence_file, encoding="utf-8")
    co_occurrence_config = config['co_occurrence_cfg']
    co_occurrence_list = co_occurrence_config['co_occurrence_variety'].split(",")
    for co_occurrence in co_occurrence_list:
        co_occurrence_brand = config[co_occurrence]
        words_list = co_occurrence_brand['words'].split(",")
        brand_list = co_occurrence_brand['brand_name'].split(",")
        for brand in brand_list:
            co_occurrence_dict[brand] = words_list
    return co_occurrence_dict

def correct_fault(brand_name, goods_str):
    '''
    new version is updated by gcw in 2020.09.14.
    :param brand_name:
    :param goods_str:
    :return:
    '''
    telephone_list = ["苹果","华为","三星","一加","小米","oppo","vivo","诺基亚","摩托罗拉","iphone","联想","金立","中兴","宏达",\
                      "索尼","美图","酷派","锤子","努比亚","360","魅族","HUAWEI","Samsung","oneplus","xiaomi","motorola",\
                      "nokia","lenovo","gionee","zte","htc","sony","meitu","coolpad","meizu","nubia","hammer"]
    tools_list = ["手机壳", "支架", "钢化膜", "手机套", "数据线", "充电线", "磨砂壳", "麦克风", "声卡", "水凝膜", "无线充电器"]

    if brand_name not in telephone_list:return True
    for tool in tools_list:
        if len(goods_str.split(tool)) > 1:
            return False
    return True

def _correct_fault(brand_name, goods_str,co_occurrence_dict):
    '''
    new version is updated by gcw in 2020.09.14.
    :param brand_name:
    :param goods_str:
    :return:
    '''
    flag = 0
    if brand_name not in co_occurrence_dict:return True
    for brand_item in co_occurrence_dict[brand_name]:
        if len(goods_str.split(brand_item)) > 1:
            flag = 1
    if flag == 1:
        return False
    else:
        return True

def loading_test_data():
    brand_name_list = ["bear","小熊"]
    with open("./douyin_data.txt",encoding="utf-8") as f1:
        pass

def english_brand_recognition(standard_brand_name, s_name):
    c_set = {'a':'', 'b':'', 'c':'', 'd':'', 'e':'', 'f':'', 'g':'', 'h':'', \
             'i':'', 'j':'', 'k':'', 'l':'', 'm':'', 'n':'', 'o':'', 'p':'', \
             'q':'', 'r':'', 's':'', 't':'', 'u':'', 'v':'', \
             'w':'', 'x':'', 'y':'', 'z':''}
    tmp_brand = None
    if standard_brand_name in s_name:
        lst1 = s_name.split(standard_brand_name)
        for tmp in range(1, len(lst1)):
            pre_str = lst1[tmp - 1]
            next_str = lst1[tmp]
            if pre_str == "" or next_str == "":
                tmp_brand = standard_brand_name
                break
            else:
                a, b = pre_str[-1], next_str[0]
                if a not in c_set and b not in c_set:
                    tmp_brand = standard_brand_name
                    break
    else:
        tmp_brand = None

    return tmp_brand

def extract_id_rule(input_file,ori_data):
    config = configparser.ConfigParser()
    config.read(input_file, encoding="utf-8")
    brand_name_str = config['brand_word_pair']['brand_name']
    brand_name_list = brand_name_str.strip().split(",")
    brand_dict = {}
    brand_id_list = []
    with open(ori_data,"r",encoding="utf-8") as f1:
        for line in f1:
            if line == "":continue
            line_list = line.split("\t")
            if len(line_list) != 5:continue
            id_,name_,category_id,category,gmv = line_list
            brand_dict[name_] = id_
    for brand_name in brand_name_list:
        if brand_name in brand_dict:
            brand_id_list.append(brand_dict)

def check_recall_brand(ori_file,update_file):
    ori_data_list = []
    update_data_list = []
    with open(ori_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if line == "":continue
            line_list = line.split("\t")
            if len(line_list) != 5:continue
            id_,name_,category_id,category,gmv = line_list
            ori_data_list.append(id_)
    print(len(ori_data_list))
    with open(update_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if line == "":continue
            line_list = line.split("\t")
            if len(line_list) != 5:continue
            id_,name_,category_id,category,gmv = line_list
            update_data_list.append(id_)
    print(len(update_data_list))

    for ori_item in ori_data_list:
            if ori_item not in update_data_list:
                print(ori_item)

def test_return():
    return "aaa","ass","ddd"

def stat_same_occur(input_file1,input_file2):
    special_dict = {}
    update_special_dict = {}
    occur_data_list = []
    difference_list = []
    error_list = []
    idx = 0
    no_len = []
    all_dict = {}
    with open(input_file1,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 2:continue
            id_, brand_name = line_list
            special_dict[brand_name] = line

    with open(input_file2,"r",encoding="utf-8") as f2:
        for line in f2:
            idx += 1
            if len(line) == 0:
                no_len.append(line)
                continue
            line_list_ = line.strip().split("\t")
            if len(line_list_) != 4:
                error_list.append(line)
                continue
            id_,brand_name,cat1,gmv = line_list_
            update_special_dict[brand_name] = line

    special_list = list(special_dict.keys())
    update_special_list = list(update_special_dict.keys())
    print(len(update_special_list))
    print(len(error_list))
    print(idx)
    print(len(no_len))
    print(len(special_list))
    for update_special_item in update_special_list:
        if update_special_item in special_list:
            occur_data_list.append(update_special_dict[update_special_item])
        else:
            difference_list.append(update_special_dict[update_special_item])

    # print(occur_data_list)
    with open("./occur_brand.txt","w",encoding="utf-8") as f3:
        f3.write("".join(occur_data_list))
        f3.flush()

    with open("./difference_brand.txt","w",encoding="utf-8") as f4:
        f4.write("".join(difference_list))
        f4.flush()


def stat_brand_gmv(input_file,xw_brand_file,expand_brand_file):
    special_dict = {}
    update_special_dict = {}
    expand_product_dict = {}
    expand_product_gmv = 0
    xw_product_dict = {}
    xw_product_gmv = 0
    brand_gmv_dict = {}
    no_product_list = []
    with open(xw_brand_file, "r", encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 2: continue
            id_, brand_name = line_list
            special_dict[brand_name] = line

    with open(expand_brand_file, "r", encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:
                continue
            line_list_ = line.strip().split("\t")
            if len(line_list_) != 4:
                continue
            id_, brand_name, cat1, gmv = line_list_
            if brand_name in special_dict:continue
            update_special_dict[brand_name] = line

    with open(input_file,"r",encoding="utf-8") as f3:
        for line in f3:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 7:continue
            id_,_,_,product_name,brand_name,gmv,product_num = line_list
            if brand_name in update_special_dict:
                expand_product_gmv = expand_product_gmv + float(gmv)
                if brand_name in expand_product_dict:
                    expand_product_dict[brand_name].append(line)
                else:
                    expand_product_dict[brand_name] = [line]
            if brand_name in special_dict:
                xw_product_gmv = xw_product_gmv + float(gmv)
                if brand_name in xw_product_dict:
                    xw_product_dict[brand_name].append(line)
                else:
                    xw_product_dict[brand_name] = [line]
    print(expand_product_gmv)
    print(xw_product_gmv)

    expand_product_list = list(expand_product_dict.keys())
    for update_special in update_special_dict:
        if update_special not in expand_product_list:
            no_product_list.append(update_special)

    print(len(no_product_list))

    for expand_brand in expand_product_dict:
        brand_gmv = 0
        for product_item in expand_product_dict[expand_brand]:
            if len(product_item) == 0: continue
            line_list = product_item.strip().split("\t")
            if len(line_list) != 7: continue
            id_, _, _, product_name, brand_name, gmv, product_num = line_list
            brand_gmv = brand_gmv + float(gmv)
        brand_gmv_dict[expand_brand] = [brand_gmv,len(expand_product_dict[expand_brand])]
    brand_gmv_list = [(k,v[1],v[0]) for k,v in brand_gmv_dict.items()]
    brand_gmv_list_ = sorted(brand_gmv_list,key=lambda x:x[1],reverse=True)
    with open("stat_reporter.txt","w",encoding="utf-8") as f4:
        for item in brand_gmv_list_:
            f4.write(item[0] + "\t" + str(item[1]) + "\t" + str(item[2]) + "\n")
        f4.flush()

def get_brand_id(input_file1,input_file2):
    online_brand_dict = {}
    xw_brand_dict = {}
    update_online_dict = {}
    with open(input_file1,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 1:continue
            online_brand_dict[line_list[0]] = ''
    with open(input_file2,"r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 2:continue
            id_,brand_name = line_list
            xw_brand_dict[brand_name] = id_

    for xw_brand in xw_brand_dict:
        for online_brand in online_brand_dict:
            if xw_brand == online_brand:
                update_online_dict[xw_brand] = xw_brand_dict[xw_brand]
    update_online_list = [(v,k) for k,v in update_online_dict.items()]
    with open("./data/online_all.txt","w",encoding="utf-8") as f3:
        for item in update_online_list:
            f3.write(item[0] + "\t" + item[1] + "\n")
        f3.flush()

def get_brand_id_update(input_file1,input_file2):
    online_brand_dict = {}
    xw_brand_dict = {}
    update_online_dict = {}
    with open(input_file1,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 1:continue
            online_brand_dict[line_list[0]] = ''
    with open(input_file2,"r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 4:continue
            id_,brand_name,cat1,gmv= line_list
            xw_brand_dict[brand_name] = id_

    for xw_brand in xw_brand_dict:
        for online_brand in online_brand_dict:
            if xw_brand == online_brand:
                update_online_dict[xw_brand] = xw_brand_dict[xw_brand]
    update_online_list = [(v,k) for k,v in update_online_dict.items()]
    with open("./data/online_all_update.txt","w",encoding="utf-8") as f3:
        for item in update_online_list:
            f3.write(item[0] + "\t" + item[1] + "\n")
        f3.flush()


if __name__ == "__main__":
    idx = 0
    # with open("./standard_brand_info.txt","r",encoding="utf-8") as f:
    #     for line in f:
    #         idx += 1
    #         if idx > 200:break
    #         line = line.strip()
    #         line_list = line.split("\t")
    #         if len(line_list) != 4:continue
    #         s_id, s_name, b_id, b_name = line_list
    #         s_name_ = s_name.strip()
    #         own_eng_flag,all_eng_flag = judge_eng(s_name_)
    #         print(s_name_,"\t",own_eng_flag,"\t",all_eng_flag)
    # goods_str = "【羽沛】苹果防偷窥手机膜高清膜护眼篮光膜钢化膜"
    # telephone_name = "苹果"
    # print(judge_telephone(telephone_name,goods_str))
    # s_brand_dict = getting_special_brand_dict("./xiaowu_standard_brand.txt")
    # s_extension_brand_dict = extend_special_brand("./standard_brand_info.txt",s_brand_dict)
    # print(len(s_extension_brand_dict))
    # print(s_extension_brand_dict)
    # config = configparser.ConfigParser()
    # config.read('./rule_brand.cfg',encoding="utf-8")
    # co_occurrence = config['co-occurrence-cfg']
    # co_occurrence_list = co_occurrence['co_occurrence_variety'].split(",")
    # print(co_occurrence_list)
    # print(type(co_occurrence_phone))
    # telephone_list_str = co_occurrence_phone['brand_name']
    # print(telephone_list_str)
    # telephone_list = list(telephone_list_str)
    # print(type(telephone_list))
    # print(co_occurrence_phone['brand_name'])
    # goods_str = "华为huawei手机壳卖光了"
    # brand_name = "华为"
    # # print(correct_fault(brand_name,goods_str))
    # co_occurrence_dict = _loading_co_occurrence("./rule_brand.cfg")
    # print(co_occurrence_dict)
    # print(_correct_fault(brand_name,goods_str,co_occurrence_dict))

    # brand_reg = BrandRegTool("standard_brand_info.txt","rule_brand.cfg")
    # print(brand_reg._correct_fault(brand_name,goods_str))

    # tmp_dict = {"1":2,"3":4}
    # for x in tmp_dict:
    #     print(x)

    # s1 = re.sub('\d+万?像素', "", "oppo reno4 4800万像素全身摄影")
    # print(s1)
    #标准品牌，召回品牌，加载小乌品牌
    # standard_brand_name = "MAKE UP FOR EVER"
    # standard_brand_name = "MAKEUPFOREVER"
    # standard_brand_name = "B.Duck"
    # s_name = "BDuck"
    # standard_brand_name = "BDuck"
    # s_name = "BDUCK"
    # standard_brand_name = "Gucci"
    # s_name = "917抖C（1号）/Gucci/9新/4170186"
    # print(english_brand_recognition(standard_brand_name, s_name))

    #将品牌名切换成id
    # input_file = "rule_brand.cfg"
    # ori_data = "brand_recall_info.txt"
    # extract_id_rule(input_file,ori_data)

    #检验召回品牌的id
    # ori_file = "brand_recall_info.txt"
    # update_file = "brand_recall_info_.txt"
    # check_recall_brand(ori_file,update_file)

    #测试品牌返回结果demo
    # item = test_return()
    # print(type(item))
    # print(item)

    #小测试
    # input_file = "no_len.txt"
    # with open(input_file,"r",encoding="utf-8") as f1:
    #     line_list = json.load(f1)
    # print(len(line_list))


    #计算两种品牌的交集
    # stat_same_occur("xiaowu_standard_brand.txt","update_brand_file.txt")
    # stat_brand_gmv("z_gmv.txt","xiaowu_standard_brand.txt","update_brand_file.txt")

    #上线品牌补全id信息
    input_file1 = "./data/online_brand.txt"
    input_file2 = "xiaowu_standard_brand.txt"
    get_brand_id(input_file1,input_file2)