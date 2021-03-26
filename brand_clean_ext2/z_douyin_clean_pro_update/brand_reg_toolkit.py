#!/usr/bin/env python3
#coding=utf-8

import os
import tool
import configparser

class BrandInfoLoading(object):
    def __init__(self, brand_info_file, del_brand_file=None, brand_exchange_file=None, ):
        if not os.path.exists(brand_info_file):
            raise Exception("%s does not exists!" % brand_info_file)
        self._brand_info_file = brand_info_file
        self._del_brand_dict = {}
        self._exchange_brand_dict = {}
        if del_brand_file != None:
            self._del_brand_dict = self._get_del_brand(del_brand_file)

        if brand_exchange_file != None:
            self._exchange_brand_dict = tool.get_exchange_brand_pair()

    def _get_del_brand(self, _del_brand_p):
        if not os.path.exists(_del_brand_p):
            raise Exception("%s does not exist!" % _del_brand_p)

        del_dict = {}
        with open(_del_brand_p,"r",encoding="utf-8") as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                del_dict[line] = 0
        return del_dict

    def _amend_brand(self):
        """
        原因: 这些品牌在15万的标准品牌中没有出现，但是这些品牌在抖音中出现，导致品牌清洗错误
        影响: 指定品牌召回
        1 OLOMLB -> MLB
        2 佐高梵  -> 高梵
        :return:
        """
        return ["OLOMLB|0", "佐高梵|1"]

    def brand_info_loading(self):
        cat1_brand_dict = {}  # 一级类下包含哪些品牌
        cat1_clean_brand_dict = {}
        cat1_dict = {}
        brand_cat1_dict = {}  # {brand_id: [cat1, cat2]}
        brand_idx_dict = {}  # {"苹果": [1, 2]}
        idx_ori_brand_dict = {}  #
        name_ori_brand_dict = {} # 品牌名称原始字符串
        brand_gmv_dict = {}  # 品牌的gmv
        idx_brand_lst_dict = {}  # 处理后的品牌，比如：[1 Apple/苹果] -》{'1': ['apple', '苹果']}
        idx = 0

        with open(self._brand_info_file,"r",encoding="utf-8") as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                # brand_id, brand_name, cat1_id, cat1, gmv
                lst1 = line.split("\t")
                if len(lst1) != 6:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, b_name_ori, b_name, cat1_id, cat1, gmv = lst1
                # idx-brand
                idx_ori_brand_dict[b_id] = b_name
                name_ori_brand_dict[b_id] = b_name_ori
                cat1_dict[cat1_id] = cat1
                if b_name in self._exchange_brand_dict:
                    b_name = self._exchange_brand_dict[b_name]
                r_brand_set = tool.brand_dealing(b_name)

                brand_gmv_dict[b_id] = round(float(gmv), 3)
                idx_brand_lst_dict[b_id] = list(r_brand_set)
                # brand-idx
                for r in r_brand_set:
                    if len(r) == 1: continue
                    if tool.is_number(r): continue
                    is_eng = tool.is_all_eng(r)
                    if is_eng and len(r) < 3: continue
                    # 需要删除的品牌
                    if r in self._del_brand_dict: continue
                    flag = "0" if is_eng else "1"

                    r = "%s|%s" % (r, flag)
                    if r in brand_idx_dict:
                        z = brand_idx_dict[r]
                        z = [b_id] + z
                        z = list(set(z))
                        brand_idx_dict[r] = z
                    else:
                        brand_idx_dict[r] = [b_id]

                    if cat1_id in cat1_clean_brand_dict:
                        p = cat1_clean_brand_dict[cat1_id]
                        cat1_clean_brand_dict[cat1_id] = p + [r]
                    else:
                        cat1_clean_brand_dict[cat1_id] = [r]

                # mkt2-brand
                if cat1 != "NULL":
                    if b_id in brand_cat1_dict:
                        xx = brand_cat1_dict[b_id]
                        brand_cat1_dict[b_id] = xx + [cat1_id]
                    else:
                        brand_cat1_dict[b_id] = [cat1_id]

                    if cat1_id in cat1_brand_dict:
                        lst_9 = cat1_brand_dict[cat1_id]
                        cat1_brand_dict[cat1_id] = ["%s|%s" % (b_id, b_name)] + lst_9
                    else:
                        cat1_brand_dict[cat1_id] = ["%s|%s" % (b_id, b_name)]
                else:
                    continue

        return brand_idx_dict, idx_ori_brand_dict, name_ori_brand_dict,\
               brand_cat1_dict, cat1_brand_dict, \
               cat1_clean_brand_dict, brand_gmv_dict, cat1_dict


class BrandRefRuleOpt(object):
    """
    功能：根据brand_rule.cfg中配置的规则进行品牌的处理
    配置的每一个规则对应一个方法，每一个规则对应一份规则使用的数据，并且这个数据仅仅用于这个方法中

    2020-10-10 修改
    原因: 规则文件由原来的【brand_name--规则】修改为【brand_id--规则】
    """
    def __init__(self, brand_reg_rule_file, idx_ori_brand_dict):
        '''
        :param brand_reg_rule_file: 规则文件
        :param idx_ori_brand_dict: 原始的brand_id: brand_name1/brand_name2/brand_name3的字典
        '''
        if not os.path.exists(brand_reg_rule_file):
            raise Exception("%s does not exists!" % brand_reg_rule_file)

        if len(idx_ori_brand_dict) == 0:
            raise Exception("cfg idx_ori_brand_dict error!")
        self.idx_ori_brand_dict = idx_ori_brand_dict
        self.config = configparser.ConfigParser()
        self.config.read(brand_reg_rule_file, encoding="utf-8")
        self.brand_word_rule_dict = self._getting_rule_dict("brand_word_rule")
        self.brand_cat1_rule_dict = self._getting_rule_dict("brand_cat1_rule")
        self.brand_cat1_fixed_dict = self._getting_brand_cat1_fixed_pair()
        self.phone_brand_not_appear_same_cat1_id, \
        self.phone_brand_not_appear_same_dict, \
        self.phone_brand_not_appear_skip_dict = self._getting_phone_brand_not_appear_same()
        self.brand_not_appear_same_dict = self._getting_brand_not_appear_same_dict()
        self.co_appear_del_brand_dict = self.getting_co_appear_del_brand()
        self.appoint_co_appear_del_brand_dict = self.getting_appoint_co_appear_del_brand()
        self.appoint_product_clean_dict = self.get_appoint_product_clean_dict()

    def bid_2_bname(self, b_id):
        # 10530851	jimmisum/吉米森jimmisum/吉米森/jimmisum吉米森
        b_id = b_id.strip()
        if b_id not in self.idx_ori_brand_dict:
            return []
        else:
            return self.idx_ori_brand_dict[b_id].split("/")

    def get_appoint_product_clean_dict(self):
        product_clean_rule = self.config['rule_method_cfg']['appoint_product_clean']
        product_pair_list = self.config[product_clean_rule]['appoint_product_2_brand'].split(',')
        d = {}
        for product_pair in product_pair_list:
            product_id, brand_id = product_pair.strip().split('|')
            d[product_id] = brand_id
        return d

    def _getting_rule_dict(self, rule_tag):
        s1 = self.config["rule_method_cfg"][rule_tag]
        r_dict = {}
        for tmp in s1.strip().split(","):
            d2 = self._getting_cfg_items(tmp)
            for k, v in d2.items():
                if k in r_dict:
                    z = r_dict[k]
                    r_dict[k] = z + v
                else:
                    r_dict[k] = v

        return r_dict

    def _getting_cfg_items(self, cfg_header):
        try:
            s1 = self.config[cfg_header]["brand_id"]
            lst1 = []
            for a1 in s1.strip().split(","):
                a1 = a1.strip()
                if a1 not in self.idx_ori_brand_dict: continue
                # 10530851	jimmisum/吉米森jimmisum/吉米森/jimmisum吉米森
                for a2 in self.bid_2_bname(a1):
                    lst1.append(a2.strip().lower())

            s2 = self.config[cfg_header]["rule"]
            lst2 = s2.strip().split(",")
            lst2 = [tmp.strip() for tmp in lst2]
            d1 = {}
            for z in lst1:
                if z not in d1:
                    d1[z] = lst2
            return d1

        except Exception as e:
            raise e

    def _getting_brand_cat1_fixed_pair(self):
        s1 = self.config["rule_method_cfg"]["brand_cat1_fixed_rule"]
        d1 = {}
        for tmp in s1.strip().split(","):
            s2 = self.config[tmp]["rule"].lower()
            lst2 = s2.strip().split(",")
            lst2 = [x.strip() for x in lst2]
            for z in lst2:
                lst3 = z.strip().split("|")
                if len(lst3) != 2:
                    raise Exception("%s -> %s config error!" % (tmp, z))
                    break
                lst3 = [y.strip() for y in lst3]
                b_id, cat1_id = lst3
                if b_id not in self.idx_ori_brand_dict: continue
                for z1 in self.bid_2_bname(b_id):
                    b_name = z1.strip().lower()
                    if b_name in d1:
                        z = d1[b_name]
                        d1[b_name] = z + [cat1_id]
                    else:
                        d1[b_name] = [cat1_id]
        return d1

    # def _getting_phone_brand_not_appear_same(self):
    #     skip_pair_dict = {}
    #     lst9 = self.config["phone_brand_not_appear_simultaneously"]["skip_pair"].split(",")
    #     for c in lst9:
    #         x1, x2 = c.strip().lower().split("|")
    #         k1 = "%s|%s" % (x1, x2)
    #         k2 = "%s|%s" % (x2, x1)
    #         skip_pair_dict[k1] = ''     #华为|荣耀
    #         skip_pair_dict[k2] = ''     #荣耀|华为
    #
    #     d1 = {}
    #     def _gen_pair(s1, s2):
    #         a = s1.strip()
    #         b = s2.strip()
    #         k1 = "%s|%s" % (a, b)
    #         k2 = "%s|%s" % (b, a)
    #         d1[k1] = ''
    #         d1[k2] = ''
    #
    #     try:
    #         lst1 = self.config["phone_brand_not_appear_simultaneously"]["phone_brand_name"].split(",")
    #         cat1_id_list = [tmp_id.strip() for tmp_id in self.config["phone_brand_not_appear_simultaneously"]["product_cat1_id"].split(",")]
    #         for j in range(len(lst1)):
    #             for k in range(j+1, len(lst1)):
    #                 _gen_pair(lst1[j], lst1[k])
    #
    #         return cat1_id_list, d1, skip_pair_dict
    #     except Exception as e:
    #         raise e
    #
    #     pass

    def _getting_phone_brand_not_appear_same(self):
        skip_pair_dict = {}
        lst9 = self.config["phone_brand_not_appear_simultaneously"]["skip_pair"].split(",")
        for c in lst9:
            x1, x2 = c.strip().lower().split("|")
            k1 = "%s|%s" % (x1, x2)
            k2 = "%s|%s" % (x2, x1)
            skip_pair_dict[k1] = ''
            skip_pair_dict[k2] = ''

        d1 = {}
        def _gen_pair(s1, s2):
            pre_lst = s1.strip().lower().split("|")
            cur_lst = s2.strip().lower().split("|")
            for a in pre_lst:
                a = a.strip()
                for b in cur_lst:
                    b = b.strip()
                    k1 = "%s|%s" % (a, b)
                    k2 = "%s|%s" % (b, a)
                    if k1 not in skip_pair_dict:
                        d1[k1] = ''
                    if k2 not in skip_pair_dict:
                        d1[k2] = ''

        try:
            lst1 = self.config["phone_brand_not_appear_simultaneously"]["phone_brand_name"].split(",")
            cat1_id = self.config["phone_brand_not_appear_simultaneously"]["product_cat1_id"]
            for j in range(len(lst1)):
                for k in range(j+1, len(lst1)):
                    _gen_pair(lst1[j], lst1[k])

            return cat1_id.strip(), d1, skip_pair_dict
        except Exception as e:
            raise e

        pass

    def _getting_brand_not_appear_same_dict(self):
        r_dict = {}
        def generate_key_pair(a_lst, b_lst):
            for g in a_lst:
                g = g.strip()
                for h in b_lst:
                    h = h.strip()
                    k1 = "%s|%s" % (g, h)
                    k2 = "%s|%s" % (h, g)
                    if k1 not in r_dict:r_dict[k1] = ''
                    if k2 not in r_dict:r_dict[k2] = ''

        s1 = self.config["rule_method_cfg"]["brand_not_appear_simultaneously"]
        b_name_str_lst = []
        for tmp in s1.strip().split(","):
            s2 = self.config[tmp]["brand_id"]
            lst2 = s2.strip().split("|")
            lst2 = [x.strip() for x in lst2]
            for a in lst2:
                tmp_lst = []
                for b in a.strip().split(","):
                    if b not in self.idx_ori_brand_dict: continue
                    tmp_lst += self.bid_2_bname(b)
                b_name_str_lst.append(tmp_lst)
        for c in b_name_str_lst:
            for i in range(len(c)):
                a_lst = c[i].strip().split("/")
                for j in range(i + 1, len(c)):
                    b_lst =  c[j].strip().split("/")
                    generate_key_pair(a_lst, b_lst)

        return r_dict

    def getting_co_appear_del_brand(self):
        s1 = self.config["co_appear_del_brand"]["brand_id"]
        d1 = {}
        for tmp in s1.strip().split(","):
            tmp = tmp.strip()
            if tmp == "": continue
            if tmp not in self.idx_ori_brand_dict: continue
            for b in self.bid_2_bname(tmp):
                d1[b] = ''
        return d1

    def getting_appoint_co_appear_del_brand(self):
        s1 = self.config["appoint_co_appear_del_brand"]["brand_id"]
        d1 = {}
        for tmp in s1.strip().split(","):
            tmp = tmp.strip()
            if tmp == "": continue
            lst1 = tmp.split("|")
            if len(lst1) != 2: continue
            lst1 = [zz.strip() for zz in lst1]
            b1, b2 = lst1
            if b1 not in self.idx_ori_brand_dict or \
                    b2 not in self.idx_ori_brand_dict: continue
            n1_lst, n2_lst = self.bid_2_bname(b1), self.bid_2_bname(b2)
            for x1 in n1_lst:
                for x2 in n2_lst:
                    x1, x2 = x1.lower(), x2.lower()
                    if x1 in d1:
                        xx = d1[x1]
                        xx = list(set(xx + [x2]))
                        d1[x1] = xx
                    else:
                        d1[x1] = [x2]

        return d1

    def brand_word_rule_func(self, b_name, p_name):
        if len(self.brand_word_rule_dict) == 0: return True
        b_name = b_name.strip()
        p_name = tool.multi_blank_clean(p_name.strip())
        if b_name not in self.brand_word_rule_dict: return True
        flag = True
        for rule_word in self.brand_word_rule_dict[b_name]:
            if len(p_name.split(rule_word)) > 1:
                flag = False
                break
        return flag

    def brand_cat1_rule_func(self, b_name, p_cat1_name):
        if len(self.brand_cat1_rule_dict) == 0: return True
        p_cat1_name, b_name = p_cat1_name.strip(), b_name.strip()
        if b_name not in self.brand_cat1_rule_dict: return True
        flag = True
        for rule_cat1 in self.brand_cat1_rule_dict[b_name]:
            if rule_cat1 == p_cat1_name:
                flag = False
                break
        return flag

    def brand_cat1_fixed_rule_func(self, brand_name, p_cat1_id):
        if len(self.brand_cat1_fixed_dict) == 0: return True
        brand_name, p_cat1_id = brand_name.strip(), p_cat1_id.strip()
        if brand_name not in self.brand_cat1_fixed_dict: return True
        if p_cat1_id in self.brand_cat1_fixed_dict[brand_name]:
            return True
        else:
            return False

    # def phone_brand_not_appear_same_fun(self, brand_id_lst, product_cat1_id):
    #     product_cat1_id = product_cat1_id.strip()
    #     if product_cat1_id not in self.phone_brand_not_appear_same_cat1_id:
    #         return brand_id_lst
    #     if len(brand_id_lst) == 1: return brand_id_lst
    #     r_set = set()
    #     for i in range(len(brand_id_lst)):
    #         a_ori = brand_id_lst[i]       #小米
    #         # a = a_ori.replace("|1", "").replace("|0", "").lower()
    #         for j in range(i+1, len(brand_id_lst)):
    #             b_ori = brand_id_lst[j]       #华为
    #             # b = b_ori.replace("|1", "").replace("|0", "").lower()
    #             k1 = "%s|%s" % (a_ori, b_ori)
    #             k2 = "%s|%s" % (b_ori, a_ori)
    #             if k1 in self.\
    #                     phone_brand_not_appear_skip_dict and \
    #                     k2 in self.phone_brand_not_appear_skip_dict and len(brand_id_lst) <= 2:
    #                 r_set.add(a_ori)
    #                 r_set.add(b_ori)
    #             elif k1 not in self.phone_brand_not_appear_same_dict and \
    #                     k2 not in self.phone_brand_not_appear_same_dict:
    #                 r_set.add(a_ori)
    #                 r_set.add(b_ori)
    #             else:
    #                 pass
    #
    #     return list(r_set)

    def phone_brand_not_appear_same_fun(self, brand_name_lst, product_cat1_id):
        product_cat1_id = product_cat1_id.strip()
        if product_cat1_id != self.phone_brand_not_appear_same_cat1_id:
            return brand_name_lst
        if len(brand_name_lst) == 1: return brand_name_lst
        r_set = set()
        for i in range(len(brand_name_lst)):
            a_ori = brand_name_lst[i]
            a = a_ori.replace("|1", "").replace("|0", "").lower()
            for j in range(i+1, len(brand_name_lst)):
                b_ori = brand_name_lst[j]
                b = b_ori.replace("|1", "").replace("|0", "").lower()
                k1 = "%s|%s" % (a, b)
                k2 = "%s|%s" % (b, a)
                if k1 in self.phone_brand_not_appear_skip_dict and \
                        k2 in self.phone_brand_not_appear_skip_dict:
                    r_set.add(a_ori)
                    r_set.add(b_ori)
                elif k1 not in self.phone_brand_not_appear_same_dict and \
                        k2 not in self.phone_brand_not_appear_same_dict:
                    r_set.add(a_ori)
                    r_set.add(b_ori)
                else:
                    pass

        return list(r_set)

    def brand_not_appear_same_fun(self, brand_name_lst):
        if len(brand_name_lst) == 1: return brand_name_lst
        r_set = set()
        for i in range(len(brand_name_lst)):
            a_ori = brand_name_lst[i]
            a = a_ori.replace("|1", "").replace("|0", "").lower()
            for j in range(i + 1, len(brand_name_lst)):
                b_ori = brand_name_lst[j]
                b = b_ori.replace("|1", "").replace("|0", "").lower()
                k1 = "%s|%s" % (a, b)
                k2 = "%s|%s" % (b, a)
                if k1 not in self.brand_not_appear_same_dict and \
                        k2 not in self.brand_not_appear_same_dict:
                    r_set.add(a_ori)
                    r_set.add(b_ori)
                else:
                    pass

        return list(r_set)

    def co_appear_del_brand_func(self, b_name_lst):
        if len(b_name_lst) == 1: return b_name_lst
        new_b_name_lst = []
        for tmp in b_name_lst:
            tmp = tmp.strip()
            if tmp == "": continue
            b, _ = tmp.split('|')
            if b in self.co_appear_del_brand_dict: continue
            new_b_name_lst.append(tmp)

        return new_b_name_lst

    def apppint_co_appear_del_brand_func(self, b_name_lst):
        if len(b_name_lst) == 1: return b_name_lst
        del_brand_dict = {}
        for tmp in b_name_lst:
            b_name, _ = tmp.split('|')
            if b_name not in self.appoint_co_appear_del_brand_dict: continue
            tmp_lst = self.appoint_co_appear_del_brand_dict[b_name]
            for yy in b_name_lst:
                del_name, _ = yy.split('|')
                if del_name in tmp_lst:
                    del_brand_dict[yy] = ''
                else:
                    continue

        new_b_name_lst = []
        for xx in b_name_lst:
            if xx in del_brand_dict: continue
            new_b_name_lst.append(xx)

        return new_b_name_lst