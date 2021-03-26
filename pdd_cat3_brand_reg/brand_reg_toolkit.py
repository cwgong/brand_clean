#!/usr/bin/env python3
#coding=utf-8

import os
import tool
import configparser


class BrandRefRuleOpt(object):
    '''
    # ***规则参数为：品牌的名称***
    '''
    def __init__(self, brand_reg_rule_file):
        '''
        :param brand_reg_rule_file: 规则文件
        :param idx_ori_brand_dict: 原始的brand_id: brand_name1/brand_name2/brand_name3的字典
        '''
        if not os.path.exists(brand_reg_rule_file):
            raise Exception("%s does not exists!" % brand_reg_rule_file)

        self.config = configparser.ConfigParser()
        self.config.read(brand_reg_rule_file, encoding="utf-8")
        self.co_appear_del_brand_dict = self._getting_co_appear_del_brand()
        self.no_brand_word_dict = self._getting_no_brand_word_dict()

        #
        self.mainBrand_appear_subBrand_dict = self._getting_maimBrand_appear_subBrand()
        self.laoban_bname, self.laoban_brand_dict = \
            self._getting_laoban_brand_rule_dict()

        self.product_name_del_word_dict = self._getting_product_name_del_word_dict()
        self.co_appear_del_brand_dict = self._getting_co_appear_del_brand()

        self.phone_brand_id_dict, self.phone_brand_word_dict, \
        self.phone_brand_cat3_dict = self._getting_phone_brand_word_rule_dict()

        self.phone_brand_not_appear_same_cat1_en_name, \
        self.phone_brand_not_appear_same_lst, \
        self.phone_brand_not_appear_skip_dict = self._getting_phone_brand_not_appear_same()

    def _is_empty_rule(self, rule_str):
        rule_str = rule_str.strip()
        if rule_str == "UNK" or rule_str == "unk":
            return True
        else:
            return False

    def _getting_phone_brand_not_appear_same(self):
        try:
            s1 = self.config["phone_brand_not_appear_simultaneously"]["cat1_en_name"].strip()
            s2 = self.config["phone_brand_not_appear_simultaneously"]["skip_pair"].strip()
            s3 = self.config["phone_brand_not_appear_simultaneously"]["phone_brand_id"].strip()
            if self._is_empty_rule(s1) or self._is_empty_rule(s2) or self._is_empty_rule(s3):
                return "", [], {}

            cat1_en_name = s1

            skip_pair_dict = {}
            for c in s2.split(","):
                x1, x2 = c.strip().lower().split("|")
                if x1 in skip_pair_dict:
                    z = skip_pair_dict[x1]
                    zz = list(set([x2] + z))
                    skip_pair_dict[x1] = zz
                else:
                    skip_pair_dict[x1] = [x2]

            lst1 = [tmp.strip() for tmp in s3.split(",")]
            return cat1_en_name, lst1, skip_pair_dict

        except Exception as e:
            raise e

    def _getting_phone_brand_word_rule_dict(self):
        s1 = self.config["phone_brand_word_pair"]['brand_id'].strip()
        s2 = self.config["phone_brand_word_pair"]["rule"].strip()
        s3 = self.config["phone_brand_word_pair"]["rule_ch_cat3"].strip()
        if self._is_empty_rule(s1) or self._is_empty_rule(s2) or self._is_empty_rule(s3):
            return {}, {}, ""

        bid_dict = {}
        for a1 in s1.split(','):
            a1 = a1.strip()
            if a1 == "": continue
            bid_dict[a1] = ""

        w_dict = {}
        for a2 in s2.split(','):
            a2 = a2.strip()
            if a2 == "": continue
            w_dict[a2] = ''
        cat3_dict = {}
        for a3 in s3.split(','):
            a3 = a3.strip()
            if a3 == "": continue
            cat3_dict[a3] = ""

        return bid_dict, w_dict, cat3_dict

    def _getting_laoban_brand_rule_dict(self):
        b_name = self.config["laoban_brand_rule"]["brand_name"]
        s1 = self.config["laoban_brand_rule"]["rule"]
        d1 = {}
        if self._is_empty_rule(s1): return None, d1

        for tmp in s1.strip().split(","):
            d1["%s%s" % (tmp, b_name)] = ''

        return b_name, d1

    def _getting_co_appear_del_brand(self):
        s1 = self.config["co_appear_del_brand"]["brand_id"]
        d1 = {}
        if self._is_empty_rule(s1): return d1
        for tmp in s1.strip().split(","):
            tmp = tmp.strip()
            if tmp == "": continue
            d1[tmp] = ''

        return d1

    def _getting_no_brand_word_dict(self):
        s1 = self.config["no_brand_word"]["rule1"]
        s2 = self.config["no_brand_word"]["rule2"]
        d1 = {}
        if self._is_empty_rule(s1) and self._is_empty_rule(s2): return d1
        s1 = s1 + "," + s2
        for w in s1.strip().split(","):
            w = w.strip()
            if w == "": continue
            d1[w] = ''

        return d1

    def _getting_product_name_del_word_dict(self):
        s1 = self.config["product_name_del_word_rule"]["rule"]
        d1 = {}
        if self._is_empty_rule(s1): return d1
        for w in s1.strip().split(","):
            w = w.lower().strip()
            if w == "": continue
            d1[w] = ''

        return d1

    def _getting_co_appear_del_brand(self):
        s1 = self.config["co_appear_del_brand"]["brand_id"]
        d1 = {}
        if self._is_empty_rule(s1): return d1
        for tmp in s1.strip().split(","):
            tmp = tmp.strip()
            if tmp == "": continue
            d1[tmp] = ''
        return d1

    def _getting_maimBrand_appear_subBrand(self):
        s1 = self.config["mainBrand_appear_simultaneously_with_subBrand"]["rule"]
        re_dict = {}
        if self._is_empty_rule(s1): return re_dict
        for itm in s1.strip().split(','):
            main_B, sub_B = itm.strip().split('|')
            main_B, sub_B = main_B.strip(), sub_B.strip()

            re_dict["%s|%s" % (main_B, sub_B)] = sub_B
            re_dict["%s|%s" % (sub_B, main_B)] = sub_B

        return re_dict

    def co_appear_del_brand_func(self, bname_tuple_lst):
        '''
        品牌编号规则
        :param bname_tuple_lst:
        :return:
        '''
        if len(bname_tuple_lst) == 1: return bname_tuple_lst
        new_b_name_lst = []
        for tmp in bname_tuple_lst:
            bname, bid = tmp
            if bid in self.co_appear_del_brand_dict: continue
            new_b_name_lst.append(tmp)

        return new_b_name_lst

    def no_brand_word_func(self, ori_s_name):
        '''
        字符串规则
        :param ori_s_name:
        :return:
        '''
        flag = False
        for k, v in self.no_brand_word_dict.items():
            if len(ori_s_name.split(k)) >= 2:
                flag = True
        return flag

    def mainBrand_appear_simultaneously_with_subBrand_func(self, bid1, bid2):
        '''
        品牌编号规则
        :param bid1:
        :param bid2:
        :return:
        '''
        bid1, bid2 = bid1.strip(), bid2.strip()
        k1 = "%s|%s" % (bid1, bid2)
        k2 = "%s|%s" % (bid2, bid1)
        if k1 in self.mainBrand_appear_subBrand_dict:
            return self.mainBrand_appear_subBrand_dict[k1]
        elif k2 in self.mainBrand_appear_subBrand_dict:
            return self.mainBrand_appear_subBrand_dict[k2]
        else:
            return None

    def laoban_brand_rule_func(self, pname, bname):
        '''
        品牌编号、扩展后品牌名称、商品名称规则
        :param pname:
        :param bid:
        :param bname:
        :return:
        '''
        pname, bname = pname.strip(), bname.strip()
        if self.laoban_bname == None or self.laoban_bname == "": return False
        if bname != self.laoban_bname: return False
        r_flag = False
        for k, v in self.laoban_brand_dict.items():
            if len(pname.split(k)) >= 2:
                r_flag = True
                break
            else:
                continue

        return r_flag

    def product_name_del_word_func(self, ori_s_name):
        s_name = ori_s_name
        for k, v in self.product_name_del_word_dict.items():
            if len(ori_s_name.split(k)) >= 2:
                s_name = s_name.replace(k, " ")

        return s_name

    def co_appear_del_brand_func(self, bname_tuple_lst):
        if len(bname_tuple_lst) == 1: return bname_tuple_lst
        new_b_name_lst = []
        for tmp in bname_tuple_lst:
            bname, bid = tmp
            if bid == "": continue
            if bid in self.co_appear_del_brand_dict: continue
            new_b_name_lst.append(tmp)

        return new_b_name_lst

    def phone_brand_word_rule_func(self, bid, cat3_ch_name, p_name):
        if len(self.phone_brand_id_dict) == 0 or \
                len(self.phone_brand_word_dict) == 0 or \
                len(self.phone_brand_cat3_dict) == 0:
            return True
        if cat3_ch_name not in self.phone_brand_cat3_dict: return True
        if bid not in self.phone_brand_id_dict: return True

        flag = True
        for rule_word, _ in self.phone_brand_word_dict.items():
            if len(p_name.split(rule_word)) > 1:
                flag = False
                break
        return flag

    def phone_brand_not_appear_same_fun(self, brand_id_lst, cat1_en_name):
        cat1_en_name = cat1_en_name.strip()
        if cat1_en_name != self.phone_brand_not_appear_same_cat1_en_name:
            return brand_id_lst
        if len(brand_id_lst) == 1: return brand_id_lst

        set1 = set(self.phone_brand_not_appear_same_lst)
        set2 = set(brand_id_lst)

        set1_intersection = set1 & set2
        if len(set1_intersection) == 1: return brand_id_lst

        # skip strategy
        skip_brand_set = set()
        def skip_opt(cur_bid, skip_value_lst):
            for x1 in set1_intersection:
                if x1 == cur_bid: continue
                for x2 in skip_value_lst:
                    if x1 == x2:
                        skip_brand_set.add(cur_bid)
                        skip_brand_set.add(x2)

        for z in set1_intersection:
            if z not in self.phone_brand_not_appear_skip_dict: continue
            tmp_skip_lst = self.phone_brand_not_appear_skip_dict[z]
            skip_opt(z, tmp_skip_lst)
        #
        set3 = set()
        for y1 in set1_intersection:
            if y1 not in skip_brand_set:
                set3.add(y1)
        r_dict = {}
        for z1 in  brand_id_lst:
            if z1 in set3: continue
            r_dict[z1] = ''

        return r_dict

