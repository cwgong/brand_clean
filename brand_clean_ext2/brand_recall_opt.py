#!/usr/bin/env python3
#coding=utf-8

import os
import tool
import re

class BrandRecallOpt(object):
    """
    todo: 米家需要程序单独处理
    """
    def __init__(self, standard_brand_file, special_brand_file):
        if not os.path.exists(standard_brand_file):
            raise Exception("%s does not exists!" % standard_brand_file)
        if not os.path.exists(special_brand_file):
            raise Exception("%s does not exists!" % special_brand_file)
        self.standard_brand_file = standard_brand_file
        self.special_brand_file = special_brand_file

    def mijia_special_brand_recall(self, b_id, cat1_id, cat1_name):
        """
        标准品牌中将【米家】合并到了小米
        :return:
        """
        # 10698337        Xiaomi/小米     100031  家用电器        1143728907.83730000
        xiaomi_brand_id = "10698337"
        skip_cat1_id = "100035" # 手机及配件
        mijia_brand_id = "10624746"
        mijia_brand_name = "MJ/米家"

        # b_id, ori_b_name, cat1_id, cat1, gmv = lst1
        if b_id == xiaomi_brand_id and cat1_id != skip_cat1_id:
            ext_band_name = self.english_brand_extension(mijia_brand_name)
            return "\t".join([mijia_brand_id, mijia_brand_name, ext_band_name, cat1_id, cat1_name, "0.0"])
        else:
            return ""
        """
        10698337	Xiaomi/小米	Xiaomi/小米Xiaomi/小米/Xiaomi小米	100028	电脑、办公	502831022.86170000
        """


    def english_brand_extension(self, brand_name):
        """
        target: 将扩展的品牌直接保存值召回品牌中
        1）指定品牌
        2）标准品牌

        第一种情况：去特殊字符
        A.H.C/爱和纯  ->  AHC爱和纯  -> A.H.C/爱和纯/AHC爱和纯
        A.O.史密斯    ->  AO史密斯   -> A.O.史密斯/AO史密斯

        第二种情况：去英文的空格
        MAKE UP FOR EVER  -> MAKEUPFOREVER
        COLOR KEY -> COLORKEY
        a b c/某某某  -> abc/a b c/某某某/abc某某某
        :return:
        """
        def _single_brand_ext(tmp_b_name):
            # 去除空格
            b1 = re.sub(r"[\s]+", "", tmp_b_name)
            # 去除.
            b2 = tmp_b_name.replace(".", "").replace("．", "")
            r_lst = list(set([tmp_b_name, b1, b2]))
            return r_lst

        # 10943455        Hisense/海信（黑电）
        ok_brand_name = ""
        tmp = brand_name.strip().replace("（", "(").replace("）", "").replace(")", "")
        lst2 = tmp.split("(")
        if len(lst2) == 2:
            b1 = lst2[0]
            if tool.is_all_eng(lst2[1]):
                b2 = lst2[1]
                ok_brand_name = b2 + "/" + b1
            else:
                ok_brand_name = b1
        else:
            ok_brand_name = brand_name

        brand_lst = ok_brand_name.strip().split("/")
        re_brand_lst = []
        if len(brand_lst) == 1:
            re_brand_lst += _single_brand_ext(brand_lst[0])
        else:
            en_brand_lst = []
            ch_brand_lst = []
            other_brand_lst = []
            for b in brand_lst:
                if tool.is_all_eng(b):
                    en_brand_lst.append(b)
                elif tool.is_all_chinese(b):
                    ch_brand_lst.append(b)
                else:
                    other_brand_lst.append(b)
            en_brand_ext_lst = []
            for z in en_brand_lst:
                en_brand_ext_lst += _single_brand_ext(z)
            mix_brand_lst = []
            for y in en_brand_ext_lst:
                for x in ch_brand_lst:
                    mix_brand_lst.append(y+x)
                    mix_brand_lst.append(x+y)
            re_brand_lst = mix_brand_lst + en_brand_ext_lst + ch_brand_lst + other_brand_lst

        re_brand_lst = list(set(re_brand_lst))
        #print(re_brand_lst)

        return "/".join(re_brand_lst)

    def special_brand_loading(self):
        ex_brand_dict = tool.get_exchange_brand_pair()

        special_brand_list = []
        with open(self.special_brand_file, "r", encoding="utf-8") as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                # brand_id, brand_name, cat1_id, cat1, gmv
                lst1 = line.split("\t")
                if len(lst1) != 2:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, b_name = lst1

                if b_name in ex_brand_dict:
                    b_name = ex_brand_dict[b_name]
                b_name = tool.brand_clean(b_name.lower())
                ext_band_name = self.english_brand_extension(b_name)
                special_brand_list.append(ext_band_name)

        return special_brand_list

    def brand_recall(self, output_file="brand_recall_info.txt"):
        try:
            ex_brand_dict = tool.get_exchange_brand_pair()
            special_brand_list = self.special_brand_loading()
            recall_brand_dict = {}
            mijia_lst = []
            idx = 0
            with open(self.standard_brand_file, "r", encoding="utf-8") as f1:
                for line in f1:
                    line = line.strip()
                    if line == "": continue
                    lst1 = line.split("\t")
                    if len(lst1) != 5:
                        continue
                    lst1 = [tmp.strip() for tmp in lst1]
                    b_id, ori_b_name, cat1_id, cat1, gmv = lst1
                    mijia_str = self.mijia_special_brand_recall(b_id, cat1_id, cat1)
                    if mijia_str != "": mijia_lst.append(mijia_str)
                    if ori_b_name in ex_brand_dict:
                        b_name = ex_brand_dict[ori_b_name]
                    else:
                        b_name = ori_b_name
                    b_name = tool.brand_clean(b_name)
                    ext_band_name = self.english_brand_extension(b_name)
                    for s_name in special_brand_list:
                        s_name_list = s_name.strip().split("/")
                        for s_name_item in s_name_list:
                            idx += 1
                            if idx % 1000000 == 0: print("idx: %s" % idx)
                            if len(ext_band_name.lower().split(s_name_item)) > 1:
                                # 单个“后”字召回的品牌错误率很高
                                if s_name_item == "后":
                                    continue
                                k = "\t".join([b_id, ori_b_name, ext_band_name, cat1_id, cat1, gmv])
                                recall_brand_dict[k] = ''
            r_lst = list(recall_brand_dict.keys()) + mijia_lst
            with open(output_file, "w", encoding="utf-8") as f1:
                f1.write("\n".join(r_lst))
                f1.flush()

        except Exception as e:
            raise e
