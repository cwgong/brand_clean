#!/usr/bin/env python3
#coding=utf-8

import os
import tool
import configparser
import json
from  brand_reg_toolkit import BrandInfoLoading, BrandRefRuleOpt

class BrandRegTool(object):
    def __init__(self, standard_brand_file, del_brand_file=None, exchange_brand_file=None, rule_brand_file=None):
        if not os.path.exists(standard_brand_file):
            raise Exception("%s does not exists!" % standard_brand_file)
        try:
            self.brand_loading_obj = BrandInfoLoading(standard_brand_file,del_brand_file, exchange_brand_file)

            #直接读取进行过品牌扩展的文件
            self.brand_idx_dict, self.idx_ori_brand_dict, self.name_ori_brand_dict, self.brand_cat1_dict, \
            self.cat1_brand_dict, self.cat1_clean_brand_dict, self.brand_gmv_dict, \
            self.cat1_dict = self.brand_loading_obj.brand_info_loading()
            self.brand_rule_obj = BrandRefRuleOpt(rule_brand_file, self.idx_ori_brand_dict)

        except Exception as e:
            raise e

    def product_name_del_word(self, ori_s_name):
        del_word_dict = {"网红":'', '美的布谷':'', '珂丝兰珂润万物丝兰完美':'', '淘米家用':'', \
                         '家用':'', 'OLOMLB':'', 'TESIRIS':'', '文和友演出门票':'', '淘米':'', \
                         '小米推荐':'', '小米众筹':'', '小米家人':'', '内蒙':'', '牛肉干':'', \
                         '小米诺':'', '小米琦':'', '小米粒':'', '小米奇':'','小米生态链':'', \
                         '小米有品同款':'', '小米同款':''}
        s_name = ori_s_name
        for k, v in del_word_dict.items():
            if k in s_name:
                s_name = s_name.replace(k, "")

        return s_name

    def english_brand_recognition(self, standard_brand_name, s_name):
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

    def brand_inclusion_relation_dealing(self, b_name_lst):
        del_brand_dict = {}
        for a in b_name_lst:
            a1, _ = a.strip().lower().split("|")
            for b in b_name_lst:
                b1, _ = b.strip().lower().split("|")
                if a1 == b1: continue
                if a1 in b1: del_brand_dict[a] = ''
                elif b1 in a1: del_brand_dict[b] = ''
                else: continue

        r_b_name_lst = []
        for c in b_name_lst:
            if c not in del_brand_dict:
                r_b_name_lst.append(c)

        return r_b_name_lst

    def getting_high_gmv_brand(self, same_cat1_bid_lst):
        tmp_gmv_lst = []
        for y in same_cat1_bid_lst:
            tmp_gmv_lst.append((self.brand_gmv_dict[y], self.name_ori_brand_dict[y], y))
        tmp_gmv_lst = sorted(tmp_gmv_lst, key=lambda n: n[0], reverse=True)
        return tmp_gmv_lst[0][1], tmp_gmv_lst[0][2]

    def same_cat1_strategy(self, cat1_id, clean_brand_lst, clean_brand_id_lst):
        pre_brand_id, pre_brand, match_type = None, None, None
        same_id_lst = []
        for a in clean_brand_lst:
            same_id_lst += self.brand_idx_dict[a]

        tmp_name_lst = []
        for b in clean_brand_id_lst:
            tmp_name_lst.append(self.name_ori_brand_dict[b])

        same_cat1_bid_lst = []
        for y in same_id_lst:
            if cat1_id in self.brand_cat1_dict[y]:
                pre_brand = self.name_ori_brand_dict[y]
                pre_brand_id = y
                same_cat1_bid_lst.append(y)
            else:
                pass

        if len(same_cat1_bid_lst) == 1 and pre_brand != None:
            match_type = "1:匹配到相同品牌名(%s)多个不同品牌(%s)，2:选择相同一级类目的品牌" % \
                         (clean_brand_lst[0], "|".join(tmp_name_lst))
        # 相同一级类目，相同品牌名称，选择高GMV品牌
        elif len(same_cat1_bid_lst) > 1:
            pre_brand, pre_brand_id = self.getting_high_gmv_brand(same_cat1_bid_lst)
            match_type = "1:匹配到相同品牌名(%s)多个不同品牌(%s)，2:选择相同一级类目的高GMV品牌" % \
                         (clean_brand_lst[0], "|".join(tmp_name_lst))
        else:
            pass

        return pre_brand_id, pre_brand, match_type

    def same_length_strategy(self, clean_brand_lst, clean_brand_id_lst):
        same_id_lst = []
        for a in clean_brand_lst:
            same_id_lst += self.brand_idx_dict[a]

        tmp_name_lst = []
        for b in clean_brand_id_lst:
            tmp_name_lst.append(self.name_ori_brand_dict[b])

        if len(same_id_lst) == 1:
            y = same_id_lst[0]
            pre_brand = self.name_ori_brand_dict[y]
            pre_brand_id = y
            match_type = "1:匹配到多个不同品牌(%s)，2:选择最长品牌: %s" % ("|".join(tmp_name_lst), pre_brand)
        else:
            pre_brand,pre_brand_id = self.getting_high_gmv_brand(same_id_lst)
            match_type = "1:匹配到多个相同最长度品牌名(%s)，2:选择相同一级类目的高GMV品牌: %s" % \
                         ("|".join(tmp_name_lst), pre_brand)

        return pre_brand_id, pre_brand, match_type

    def same_cat1_gmv_strategy(self, cat1_id, clean_brand_lst, clean_brand_id_lst):
        pre_brand_id, pre_brand, match_type = None, None, None
        same_id_lst = []
        for a in clean_brand_lst:
            same_id_lst += self.brand_idx_dict[a]

        tmp_name_lst = []
        for b in clean_brand_id_lst:
            tmp_name_lst.append(self.name_ori_brand_dict[b])

        num = 0
        for y in same_id_lst:
            if cat1_id in self.brand_cat1_dict[y]:
                pre_brand = self.name_ori_brand_dict[y]
                pre_brand_id = y
                num += 1
            else:
                pass

        if num == 1 and pre_brand != None:
            match_type = "1:匹配到相同品牌名(%s)多个不同品牌(%s)，2:选择相同一级类目的品牌" % \
                         (clean_brand_lst[0], "|".join(tmp_name_lst))
        else:
            pre_brand, pre_brand_id = self.getting_high_gmv_brand(same_id_lst)
            match_type = "1:匹配到相同品牌名(%s)多个不同品牌(%s)，2:选择高GMV品牌" % \
                         (clean_brand_lst[0], "|".join(tmp_name_lst))

        return pre_brand_id, pre_brand, match_type

    def numerous_cat1_rule_func(self, b_id_lst):
        d1 = {}
        for z in b_id_lst:
            if z not in self.brand_cat1_dict: continue
            for y in self.brand_cat1_dict[z]:
                if y in d1:
                    x = d1[y]
                    d1[y] = x + 1
                else:
                    d1[y] = 1
        lst1 = [(k, v) for k,v in d1.items()]
        lst1 = sorted(lst1, key=lambda x: x[1], reverse=True)

        c_id_1, c_num_1 = lst1[0]
        if c_num_1 >= 3:
            return False
        '''
        if len(lst1) >= 2:
            c_id_2, c_num_2 = lst1[1]
            if c_num_2 >=2 and c_num_1 >= 2:
                return False
        '''
        return True

    # def rule_opt(self, pre_brand_name_lst, cur_p_name, cur_cat1_id, cur_cat1_name,pre_clean_brand_id_lst):
    #     r_set = set()
    #     r_id_lst = []
    #     tmp_name_list = []
    #     r_name_list = []
    #
    #     stp0_clean_lst = self.brand_rule_obj.phone_brand_not_appear_same_fun(pre_clean_brand_id_lst, cur_cat1_id)
    #
    #     for tmp in list(stp0_clean_lst):
    #         if tmp not in self.idx_ori_brand_dict: continue
    #         tmp_name_list = tmp_name_list + self.brand_rule_obj.bid_2_bname(tmp)
    #     for b_name in tmp_name_list:
    #         b_name = b_name.lower()
    #         is_eng = tool.is_all_eng(b_name)
    #         flag = "0" if is_eng else "1"
    #         r_name_list.append("%s|%s" % (b_name, flag))
    #
    #     stp1_clean_lst = self.brand_inclusion_relation_dealing(r_name_list)
    #     stp2_clean_lst = self.brand_rule_obj.co_appear_del_brand_func(stp1_clean_lst)
    #     stp3_clean_lst = self.brand_rule_obj.apppint_co_appear_del_brand_func(stp2_clean_lst)
    #     # stp2_clean_lst = self.brand_rule_obj.phone_brand_not_appear_same_fun(stp1_clean_lst, cur_cat1_id)
    #     stp4_clean_lst = self.brand_rule_obj.brand_not_appear_same_fun(stp3_clean_lst)
    #     for b_name in stp4_clean_lst:
    #         tmp_b_name, _ = b_name.split('|')
    #         # 修正过程。如“苹果手机支架”不为“苹果”手机，此时将“苹果”从候选列表中移除
    #         f1 = self.brand_rule_obj.brand_word_rule_func(tmp_b_name, cur_p_name)
    #         if f1 == False: continue
    #         f2 = self.brand_rule_obj.brand_cat1_rule_func(tmp_b_name, cur_cat1_name)
    #         if f2 == False: continue
    #         f3 = self.brand_rule_obj.brand_cat1_fixed_rule_func(tmp_b_name, cur_cat1_id)
    #         if f3 == False: continue
    #         r_set.add(b_name)
    #         r_id_lst += self.brand_idx_dict[b_name]
    #     r_b_name_lst, r_b_id_lst = list(r_set), list(set(r_id_lst))
    #     if len(r_b_id_lst) == 0:
    #         return [], []
    #     if not self.numerous_cat1_rule_func(r_b_id_lst):
    #         return [], []
    #     else:
    #         return r_b_name_lst, r_b_id_lst

    def rule_opt(self, pre_brand_name_lst, cur_p_name, cur_cat1_id, cur_cat1_name):
        r_set = set()
        r_id_lst = []
        stp0_clean_lst = self.brand_inclusion_relation_dealing(pre_brand_name_lst)
        stp1_clean_lst = self.brand_rule_obj.co_appear_del_brand_func(stp0_clean_lst)
        stp2_clean_lst = self.brand_rule_obj.apppint_co_appear_del_brand_func(stp1_clean_lst)
        stp3_clean_lst = self.brand_rule_obj.phone_brand_not_appear_same_fun(stp2_clean_lst, cur_cat1_id)
        stp4_clean_lst = self.brand_rule_obj.brand_not_appear_same_fun(stp3_clean_lst)
        for b_name in stp4_clean_lst:
            tmp_b_name, _ = b_name.split('|')
            # 修正过程。如“苹果手机支架”不为“苹果”手机，此时将“苹果”从候选列表中移除
            f1 = self.brand_rule_obj.brand_word_rule_func(tmp_b_name, cur_p_name)
            if f1 == False: continue
            f2 = self.brand_rule_obj.brand_cat1_rule_func(tmp_b_name, cur_cat1_name)
            if f2 == False: continue
            f3 = self.brand_rule_obj.brand_cat1_fixed_rule_func(tmp_b_name, cur_cat1_id)
            if f3 == False: continue
            r_set.add(b_name)
            r_id_lst += self.brand_idx_dict[b_name]
        r_b_name_lst, r_b_id_lst = list(r_set), list(set(r_id_lst))
        if len(r_b_id_lst) == 0:
            return [], []
        if not self.numerous_cat1_rule_func(r_b_id_lst):
            return [], []
        else:
            return r_b_name_lst, r_b_id_lst

    def getting_cat1_info(self, brand_id):
        brand_cat1_lst = self.brand_cat1_dict[brand_id]
        brand_cat1_id = ",".join(brand_cat1_lst)
        brand_cat1_name_lst = []
        for yy in brand_cat1_lst:
            brand_cat1_name_lst.append(self.cat1_dict[yy])
        brand_cat1_name = ",".join(brand_cat1_name_lst)

        return brand_cat1_id, brand_cat1_name

    def brand_recognition(self, line_str):
        '''
        brand_recognition is updated by gcw in 2020.09.12.
        '''
        try:
            line = line_str.strip()
            if line == "": return None, None, None, None, None, None, None
            lst_z = line.split("\001")
            if len(lst_z) != 5: return None, None, None, None, None, None, None
            lst1 = [tmp.strip() for tmp in lst_z]
            product_id, ori_product_name, ori_brand_word, cat1_id, cat1_name = lst1

            if product_id in self.brand_rule_obj.appoint_product_clean_dict:
                brand_id = self.brand_rule_obj.appoint_product_clean_dict[product_id]
                brand_cat1_id, brand_cat1_name = self.getting_cat1_info(brand_id)
                return brand_id, self.name_ori_brand_dict[brand_id], "匹配到唯一标准品牌", \
                       brand_cat1_id, brand_cat1_name, cat1_id, cat1_name

            # s_name小写字母
            s_name = tool.s_name_dealing("%s %s" % (ori_product_name, ori_brand_word))
            s_name = self.product_name_del_word(s_name)
            clean_brand_lst = []
            clean_brand_id_lst = []

            # 1、清洗后的品牌
            # 2、清洗后的品牌对应的多个品牌编号
            for ori_b_str, same_brand_id_lst in self.brand_idx_dict.items():
                # 品牌小写字母
                b_str = ori_b_str.lower()
                lst_z = b_str.split('|')
                if len(lst_z) != 2: continue
                b, is_eng = lst_z
                if is_eng == "0" and tool.is_own_eng(s_name) and b in s_name:
                    tmp_b = self.english_brand_recognition(b, s_name)
                    if tmp_b != None:
                        clean_brand_lst.append(ori_b_str)
                        clean_brand_id_lst += same_brand_id_lst
                elif b in s_name:
                    clean_brand_lst.append(ori_b_str)
                    clean_brand_id_lst += same_brand_id_lst
                else:
                    continue
            clean_brand_lst = list(set(clean_brand_lst))
            clean_brand_id_lst = list(set(clean_brand_id_lst))
            if len(clean_brand_lst) == 0: return None, None, "没有匹配到标准品牌", None, None, None, None
            # 人为规则的过滤
            clean_brand_lst, clean_brand_id_lst = self.rule_opt(clean_brand_lst, ori_product_name, cat1_id, cat1_name)

            if len(clean_brand_lst) == 0:
                return None, None, "没有匹配到标准品牌", None, None, None, None

            if len(clean_brand_id_lst) == 1:
                b_id = clean_brand_id_lst[0]
                brand_cat1_id, brand_cat1_name = self.getting_cat1_info(b_id)
                return b_id, \
                       self.name_ori_brand_dict[clean_brand_id_lst[0]], \
                       "匹配到唯一标准品牌", brand_cat1_id, brand_cat1_name, cat1_id, cat1_name

            pre_brand_id, pre_brand, match_type = None, None, None
            if len(clean_brand_lst) == 1:
                pre_brand_id, pre_brand, match_type = \
                    self.same_cat1_gmv_strategy(cat1_id, clean_brand_lst, clean_brand_id_lst)
            else:
                len_brand_dict = {}
                for tmp in clean_brand_lst:
                    l = len(tmp)
                    if l in len_brand_dict:
                        x = len_brand_dict[l]
                        len_brand_dict[l] = x + [tmp]
                    else:
                        len_brand_dict[l] = [tmp]

                r_lst = [(k, v) for k, v in len_brand_dict.items()]
                r_lst = sorted(r_lst, key=lambda m: m[0], reverse=True)
                for u in r_lst:
                    tmp_l, tmp_clean_brand_lst = u
                    pre_brand_id, pre_brand, match_type = self.same_cat1_strategy(cat1_id, tmp_clean_brand_lst,
                                                                                  clean_brand_id_lst)
                    if pre_brand == None or pre_brand_id == None:
                        pre_brand_id, pre_brand, match_type = self.same_length_strategy(tmp_clean_brand_lst, clean_brand_id_lst)

                    if pre_brand != None and match_type != None:
                        break

            if pre_brand_id != None:
                brand_cat1_id, brand_cat1_name = self.getting_cat1_info(pre_brand_id)
            else:
                brand_cat1_id = None
                brand_cat1_name = None
            return pre_brand_id, pre_brand, match_type, \
                   brand_cat1_id, brand_cat1_name, cat1_id, cat1_name
        except Exception as e:
            raise e

    def brand_same_cat1_recognition(self, line_str):
        '''
        brand_recognition is updated by gcw in 2020.09.12.
        '''
        try:
            line = line_str.strip()
            if line == "": return None, None, None, None, None, None, None
            lst_z = line.split("\001")
            if len(lst_z) != 5: return None, None, None, None, None, None, None
            lst1 = [tmp.strip() for tmp in lst_z]
            product_id, ori_product_name, ori_brand_word, cat1_id, cat1_name = lst1

            # s_name小写字母
            s_name = tool.s_name_dealing("%s %s" % (ori_product_name, ori_brand_word))
            s_name = self.product_name_del_word(s_name)
            clean_brand_lst = []
            clean_brand_id_lst = []

            # 1、清洗后的品牌
            # 2、清洗后的品牌对应的多个品牌编号
            for ori_b_str, same_brand_id_lst in self.brand_idx_dict.items():

                # 品牌小写字母
                b_str = ori_b_str.lower()
                lst_z = b_str.split('|')
                if len(lst_z) != 2: continue

                b, is_eng = lst_z
                if is_eng == "0" and tool.is_own_eng(s_name) and b in s_name:
                    tmp_b = self.english_brand_recognition(b, s_name)
                    if tmp_b != None:
                        clean_brand_lst.append(ori_b_str)
                        clean_brand_id_lst += same_brand_id_lst
                elif b in s_name:
                    clean_brand_lst.append(ori_b_str)
                    clean_brand_id_lst += same_brand_id_lst
                else:
                    continue
            clean_brand_lst = list(set(clean_brand_lst))
            clean_brand_id_lst = list(set(clean_brand_id_lst))
            if len(clean_brand_lst) == 0: return None, None, "没有匹配到标准品牌", None, None, None, None
            # 人为规则的过滤
            clean_brand_lst, clean_brand_id_lst = self.rule_opt(clean_brand_lst, ori_product_name, cat1_id, cat1_name)

            if len(clean_brand_lst) == 0:
                return None, None, "没有匹配到标准品牌", None, None, None, None

            if len(clean_brand_id_lst) == 1:
                b_id = clean_brand_id_lst[0]
                brand_cat1_id, brand_cat1_name = self.getting_cat1_info(b_id)
                return b_id, \
                       self.name_ori_brand_dict[clean_brand_id_lst[0]], \
                       "匹配到唯一标准品牌", brand_cat1_id, brand_cat1_name, cat1_id, cat1_name

            pre_brand_id, pre_brand, match_type = None, None, None
            if len(clean_brand_lst) == 1:
                pre_brand_id, pre_brand, match_type = \
                    self.same_cat1_gmv_strategy(cat1_id, clean_brand_lst, clean_brand_id_lst)
            else:
                len_brand_dict = {}
                for tmp in clean_brand_lst:
                    l = len(tmp)
                    if l in len_brand_dict:
                        x = len_brand_dict[l]
                        len_brand_dict[l] = x + [tmp]
                    else:
                        len_brand_dict[l] = [tmp]

                r_lst = [(k, v) for k, v in len_brand_dict.items()]
                r_lst = sorted(r_lst, key=lambda m: m[0], reverse=True)
                for u in r_lst:
                    tmp_l, tmp_clean_brand_lst = u
                    pre_brand_id, pre_brand, match_type = self.same_cat1_strategy(cat1_id, tmp_clean_brand_lst,
                                                                                  clean_brand_id_lst)
                    if pre_brand != None and match_type != None:
                        break
                # 兜底处理
                if pre_brand == None and match_type == None:
                    pre_brand_id, pre_brand, match_type = \
                        self.same_cat1_gmv_strategy(cat1_id, clean_brand_lst, clean_brand_id_lst)

            if pre_brand_id != None:
                brand_cat1_id, brand_cat1_name = self.getting_cat1_info(pre_brand_id)
            else:
                brand_cat1_id = None
                brand_cat1_name = None
            return pre_brand_id, pre_brand, match_type, \
                   brand_cat1_id, brand_cat1_name, cat1_id, cat1_name
        except Exception as e:
            raise e
