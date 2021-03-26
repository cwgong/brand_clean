import re
from pyhive import hive
import os
import traceback

def get_data_from_hive(data_table):
    conn = hive.connect(host='172.20.207.6', port=10000, username='supdev')
    cur = conn.cursor()

    try:
        sql = """select * from %s""" % (data_table)
        cur.execute(sql)
        data_tuple = cur.fetchall()
        return data_tuple
    except Exception as e:
        print(traceback.format_exc())



def check_lack_douyin(data_table,standard_file):
    idx = 0
    product_dict = {}
    B_brand_dict = {}
    A_brand_dict = {}
    sort_A_brand_dict = {}
    sort_B_brand_dict = {}
    brand_stat_dict = {}
    B_top100_product_list = []
    A_B_top100_product_list = []

    brand_dict,ori_brand_dict = split_standard_brand(standard_file)
    print(len(brand_dict))

    data_tuple = get_data_from_hive(data_table)     #数据格式为:((1,2,3,4,5),(1,2,3,4,5),(1,2,3,4,5))

    # with open(input_file,"r",encoding="utf-8") as f1:

    for data_item in data_tuple:
        idx += 1
        if idx%10000 == 0:print(idx)
        # if len(line) == 0:continue
        # line_list = line.strip().split("\t")
        if len(data_item) != 9:continue
        # line_list = [tmp.strip() for tmp in line_list]
        # product_id,product_name,brand_words,key_words,category1_id,category1_name,brand_id,brand_name,match_type,dt,rn,sale_count,gmv,url = line_list
        product_id, product_name, gmv, first_type_id, first_type_name, brand_id, brand_name, \
        platform_name,rn = data_item
        key_words_ = re.sub('\W+', '', product_name).replace("_", '').lower()
        product_dict[product_id.strip()] = [product_id, product_name, gmv, first_type_id, first_type_name,\
        brand_id, brand_name,platform_name,rn]
        if brand_id not in B_brand_dict:
            B_brand_dict[brand_id] = [product_id]
        else:
            B_brand_dict[brand_id].append(product_id)
        for brand_id_item,brand_name_item_list in brand_dict.items():
            for brand_name_item in brand_name_item_list:
                # brand_name_item_ = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',brand_name_item,re.S)
                # brand_name_item_ = re.sub('\W+', '', brand_name_item).replace("_", '')
                # if brand_id_item == '10421087':
                #     print(brand_name_item + "   " + key_words)
                # key_words_ = re.sub('\W+', '', key_words).replace("_", '')
                if len(key_words_.split(brand_name_item)) > 1:
                    if brand_id_item not in A_brand_dict:
                        A_brand_dict[brand_id_item] = [product_id]
                    else:
                        A_brand_dict[brand_id_item].append(product_id)
                    break

    for item,values_list in A_brand_dict.items():
        sorted_list = sorted(values_list,key = lambda k:float(product_dict[k][2]),reverse=True)
        sort_A_brand_dict[item] = sorted_list

    for item,values_list in B_brand_dict.items():
        sorted_list = sorted(values_list,key = lambda k:float(product_dict[k][2]),reverse=True)
        sort_B_brand_dict[item] = sorted_list


    for brand in ori_brand_dict:
        brand_name = ori_brand_dict[brand]
        A_gmv = 0.0
        A_product_num = 0
        B_gmv = 0.0
        B_product_num = 0
        B_top100_gmv = 0.0
        A_B_brand_list = []
        A_B_gmv = 0.0
        A_B_top100_gmv = 0.0
        B_divide_A_num = 0.0
        B_divide_A_gmv = 0.0
        B_top100_gmv_rate = 0.0
        A_B_top100_gmv_rate = 0.0

        if brand in sort_A_brand_dict:
            A_product_num = len(sort_A_brand_dict[brand])
            for product_item in sort_A_brand_dict[brand]:
                A_gmv = A_gmv + float(product_dict[product_item][2])
                if brand not in sort_B_brand_dict:
                    A_B_brand_list = sort_A_brand_dict[brand]
                else:
                    if product_item not in sort_B_brand_dict[brand]:
                        A_B_brand_list.append(product_item)

        if brand in sort_B_brand_dict:
            index = 0
            B_product_num = len(sort_B_brand_dict[brand])
            for product_item in sort_B_brand_dict[brand]:
                index += 1
                B_gmv = B_gmv + float(product_dict[product_item][2])
                if index <= 100:
                    B_top100_gmv = B_top100_gmv + float(product_dict[product_item][2])
                    B_top100_product_list.append(str(brand) + "\t" + str(brand_name) + "\t" + str(product_item) + "\t" + str(product_dict[product_item][2]) + "\t" + str(product_dict[product_item][3]) + "\t" + str(product_dict[product_item][4]) + "\t" + str(product_dict[product_item][1]))


        if len(A_B_brand_list) != 0:
            index = 0
            for product in A_B_brand_list:
                index += 1
                A_B_gmv = A_B_gmv + float(product_dict[product][2])
                if index <= 100:
                    A_B_top100_gmv = A_B_top100_gmv + float(product_dict[product][2])
                    A_B_top100_product_list.append(str(brand) + "\t" + str(brand_name) + "\t" + str(product) + "\t" + str(product_dict[product][2]) + "\t" + str(product_dict[product][5]) + "\t" + str(product_dict[product][6]) + "\t" + str(product_dict[product][3]) + "\t" + str(product_dict[product][4]) + "\t" + str(product_dict[product][1]))


        if A_product_num >= B_product_num and A_product_num != 0:
            B_divide_A_num = B_product_num/A_product_num

        if A_gmv >= B_gmv and A_gmv != 0.0:
            B_divide_A_gmv = B_gmv / A_gmv

        if B_gmv != 0.0:
            B_top100_gmv_rate = B_top100_gmv/B_gmv
        if A_B_gmv != 0.0:
            A_B_top100_gmv_rate = A_B_top100_gmv/A_B_gmv

        brand_stat_dict[brand] = [brand,brand_name,A_product_num,A_gmv,B_product_num,B_gmv,B_top100_gmv,A_B_top100_gmv,B_divide_A_num,B_divide_A_gmv,B_top100_gmv_rate,A_B_top100_gmv_rate]


    return brand_stat_dict,B_top100_product_list,A_B_top100_product_list


def split_standard_brand(standard_file):
    brand_dict = {}
    ori_brand_dict = {}
    with open(standard_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            brand_name = line.strip()
            brand_name_list = brand_name.split("\t")
            if len(brand_name_list) != 2:continue
            brand_name_id,brand_name = brand_name_list
            ori_brand_dict[brand_name_id.strip()] = brand_name.strip()
            name_list = [tmp.lower() for tmp in brand_name.split("/")]
            name_list_ = []
            for item in name_list:
                brand_name_item_ = re.sub('\W+', '', item).replace("_", '')
                name_list_.append(brand_name_item_)
            brand_dict[brand_name_id.strip()] = name_list_
    return brand_dict,ori_brand_dict


if __name__ == "__main__":
    # 查漏环节开发
    brand_file = "./check_ab_set.txt"
    # input_file = "./data/kuaishou_data.txt"
    data_table = 'tmp.tmp_kuaishou_product_gmv_detail'
    brand_stat_dict, B_top100_product_list, A_B_top100_product_list = check_lack_douyin(data_table, brand_file)
    with open("./data/check_brand_stat.txt", "w", encoding="utf-8") as f1:
        for brand, vlaues_list in brand_stat_dict.items():
            vlaues_list = [str(tmp) for tmp in vlaues_list]
            f1.write("\t".join(vlaues_list))
            f1.write("\n")
        f1.flush()
    with open("./data/B_top100_product.txt", "w", encoding="utf-8") as f2:
        f2.write("\n".join(B_top100_product_list))
    with open("./data/A_B_top100_product.txt", "w", encoding="utf-8") as f3:
        f3.write("\n".join(A_B_top100_product_list))