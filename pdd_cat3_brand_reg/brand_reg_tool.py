#!/usr/bin/env python3
#coding=utf-8

import os
import tool
from brand_recall_opt import PddCat3BrandRegFileTool
from brand_reg_toolkit import BrandRefRuleOpt

class BrandRegTool(object):
    def __init__(self, cat1_en_name, is_cat2_brand_reg=True, is_cat1_brand_reg=True):
        file_sys_obj = PddCat3BrandRegFileTool(cat1_en_name)
        brand_cat3_recall_file = file_sys_obj.BRAND_CAT3_RECALL_FILE
        brand_cat2_recall_file = file_sys_obj.BRAND_CAT2_RECALL_FILE
        brand_cat1_recall_file = file_sys_obj.BRAND_CAT1_RECALL_FILE
        if not os.path.exists(brand_cat3_recall_file):
            raise Exception("%s does not exists!" % brand_cat3_recall_file)
        if not os.path.exists(brand_cat2_recall_file):
            raise Exception("%s does not exists!" % brand_cat2_recall_file)

        rule_brand_file = file_sys_obj.RULE_BRAND
        self.cat1_en_name = cat1_en_name
        self.is_cat2_brand_reg, self.is_cat1_brand_reg = is_cat2_brand_reg, is_cat1_brand_reg
        try:
            self.cat3_ori_brandId_name_dict, self.cat3_ext_brandId_name_dict, \
            self.cat3_to_brandId_dict = self._brand_recall_info_loading(brand_cat3_recall_file, cat_level=3)
            if self.is_cat2_brand_reg:
                self.cat2_ori_brandId_name_dict, self.cat2_ext_brandId_name_dict, \
                self.cat2_to_brandId_dict = self._brand_recall_info_loading(brand_cat2_recall_file, cat_level=2)
            else:
                self.cat2_ori_brandId_name_dict, self.cat2_ext_brandId_name_dict, \
                self.cat2_to_brandId_dict = {}, {}, {}

            if self.is_cat1_brand_reg:
                self.cat1_ori_brandId_name_dict, self.cat1_ext_brandId_name_dict, \
                self.cat1_to_brandId_dict = self._brand_recall_info_loading(brand_cat1_recall_file, cat_level=1)
            else:
                self.cat1_ori_brandId_name_dict, self.cat1_ext_brandId_name_dict, \
                self.cat1_to_brandId_dict = {}, {}, {}

            self.brand_rule_obj = BrandRefRuleOpt(rule_brand_file)
        except Exception as e:
            raise e

    def _brand_recall_info_loading(self, brand_recall_file, cat_level=3):
        ori_brandId_name_dict = {}  # brand_id: brand_name
        ext_brandId_name_dict = {}  # brand_id: ext_brand_name
        cat_2_brandId_dict = {}    # cat3_name: [bid1, bid2, ...]

        with open(brand_recall_file,"r",encoding="utf-8") as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                # brand_id, brand_ext_name, brand_name, cat1_name, cat2_name, cat3_name
                lst1 = line.split("\t")
                if len(lst1) != 6:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, b_name_ext, b_name_ori, cat1_name, cat2_name, cat3_name = lst1

                ori_brandId_name_dict[b_id] = b_name_ori
                ext_brandId_name_dict[b_id] = b_name_ext
                if cat_level == 3:
                    cat_key = cat3_name
                elif cat_level == 2:
                    cat_key = cat2_name
                elif cat_level == 1:
                    cat_key = cat1_name
                else:
                    continue
                if cat_key in cat_2_brandId_dict:
                    z = cat_2_brandId_dict[cat_key]
                    z = list(set([b_id] + z))
                    cat_2_brandId_dict[cat_key] = z
                else:
                    cat_2_brandId_dict[cat_key] = [b_id]

        return ori_brandId_name_dict, ext_brandId_name_dict, cat_2_brandId_dict,

    def english_brand_recognition(self, standard_brand_name, s_name):
        c_set = {'a':'', 'b':'', 'c':'', 'd':'', 'e':'', 'f':'', 'g':'', 'h':'', \
                 'i':'', 'j':'', 'k':'', 'l':'', 'm':'', 'n':'', 'o':'', 'p':'', \
                 'q':'', 'r':'', 's':'', 't':'', 'u':'', 'v':'', \
                 'w':'', 'x':'', 'y':'', 'z':''}
        standard_brand_name = standard_brand_name.strip()
        if standard_brand_name == "": return None
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

    def _ext_name_sorted(self, ext_bname):
        b_lst = []
        for tmp in ext_bname.strip().split('/'):
            b_lst.append((len(tmp), tmp))

        b_lst = sorted(b_lst, key=lambda x: x[0], reverse=True)
        rb_lst = [y[1] for y in b_lst]
        return rb_lst

    def shoujipeijian_rule_opt(self, p_name, opt_set, cat3_ch_name):
        bid_set = set()
        for z1 in opt_set:
            r_bname, r_bid = z1
            bid_set.add(r_bid)

        re_list = self.brand_rule_obj.phone_brand_not_appear_same_fun(list(bid_set), self.cat1_en_name)
        opt1_set = set()
        for z2 in opt_set:
            r_bname, r_bid = z2
            if r_bid in re_list: opt1_set.add(z2)

        opt2_set = set()
        for z1 in list(opt1_set):
            tmp_bname, tmp_bid = z1
            if self.brand_rule_obj.phone_brand_word_rule_func(tmp_bid, cat3_ch_name, p_name):
                opt2_set.add(z1)

        return opt2_set

    def rule_opt(self, p_name, pair_tuple_lst, cat3_ch_name):
        stp1_pair_tuple_lst = self.brand_rule_obj.co_appear_del_brand_func(pair_tuple_lst)
        if len(stp1_pair_tuple_lst) == 0: return []

        tmp_lst = self.brand_rule_obj.co_appear_del_brand_func(pair_tuple_lst)
        opt0_set = set(tmp_lst)
        if len(opt0_set) == 0: return []

        #
        opt1_set = set()
        for itm in stp1_pair_tuple_lst:
            r_bname, r_bid = itm
            f1 = self.brand_rule_obj.laoban_brand_rule_func(p_name, r_bname)
            if f1: continue

            opt1_set.add(itm)

        if len(opt1_set) == 0: return []

        tmp_del_dict = {}
        for xx in opt1_set:
            _, id1 = xx
            for yy in opt1_set:
                _, id2 = yy
                if id1 == id2: continue
                tmp_id = self.brand_rule_obj.mainBrand_appear_simultaneously_with_subBrand_func(id1, id2)
                if tmp_id == id1:
                    tmp_del_dict[id2] = ''
                elif tmp_id == id2:
                    tmp_del_dict[id1] = ''
                else:
                    continue

        opt2_set = set()
        for zz in opt1_set:
            _, tmp_id = zz
            if tmp_id in tmp_del_dict: continue
            else:
                opt2_set.add(zz)
        # 手机配件规则
        if self.cat1_en_name == "shoujipeijian":
            r_set = self.shoujipeijian_rule_opt(p_name, opt2_set, cat3_ch_name)
        else:
            r_set = opt2_set

        return list(r_set)

    def brand_reg(self, s_name, brand_lst, brand_id):
        r_lst = []

        for ext_bname in brand_lst:
            if tool.is_all_eng(ext_bname) and tool.is_own_eng(s_name) and ext_bname in s_name:
                en_reg_bname = self.english_brand_recognition(ext_bname, s_name)
                if en_reg_bname != None:
                    reg_bname = en_reg_bname
                else:
                    continue
            elif ext_bname in s_name:
                reg_bname = ext_bname
            else:
                continue
            r_lst.append((reg_bname, brand_id))
        #rule_opt_lst = self.rule_opt(s_name, r_lst)
        #return rule_opt_lst
        return r_lst

    def _multi_brand_opt(self, reg_bname_lst):
        length_reg_brand_dict = {}
        max_length = -1
        for xx in reg_bname_lst:
            tmp_l = len(xx[0])
            if tmp_l >= max_length: max_length = tmp_l
            if tmp_l in length_reg_brand_dict:
                yy = length_reg_brand_dict[tmp_l]
                yy = [xx] + yy
                length_reg_brand_dict[tmp_l] = yy
            else:
                length_reg_brand_dict[tmp_l] = [xx]

        final_bname_lst = list(set(length_reg_brand_dict[max_length]))

        if len(final_bname_lst) == 1:
            reg_bname, reg_bid = final_bname_lst[0]
        else:
            tmp_lst = []
            for zz in final_bname_lst:
                tmp_lst.append("%s|%s" % (zz[0], zz[1]))

            reg_bid, reg_bname = "", "#".join(tmp_lst)

        return reg_bname, reg_bid

    def brand_reg_main(self, ori_product_name, cat1_name, cat2_name, cat3_name):
        try:
            ori_product_name, cat3_name = ori_product_name.strip(), cat3_name.strip()
            if ori_product_name == "":
                raise Exception("ori_product_name is empty!")
            if cat3_name == '':
                raise Exception("cat3_name is empty!")
            if cat3_name not in self.cat3_to_brandId_dict:
                raise Exception("%s is not in self.cat3_to_brandId_dict" % cat3_name)
            cat3_ext_name = {}
            for bid in self.cat3_to_brandId_dict[cat3_name]:
                if bid not in self.cat3_ori_brandId_name_dict or \
                        bid not in self.cat3_ext_brandId_name_dict: continue
                cat3_ext_name[bid] = self._ext_name_sorted(self.cat3_ext_brandId_name_dict[bid])

            s_name = tool.s_name_dealing(ori_product_name)
            # 删除
            s_name = self.brand_rule_obj.product_name_del_word_func(s_name)

            # "dirty words" in product name
            if self.brand_rule_obj.no_brand_word_func(s_name): return None, None, None
            # 三级类目品牌识别
            reg_bname_lst = []
            for k, v in cat3_ext_name.items():
                reg_bname_lst += self.brand_reg(s_name, v, k)

            # 二级类目品牌识别
            if len(reg_bname_lst) == 0 and self.is_cat2_brand_reg:
                cat2_ext_name = {}
                for bid in self.cat2_to_brandId_dict[cat2_name]:
                    if bid not in self.cat2_ori_brandId_name_dict or \
                            bid not in self.cat2_ext_brandId_name_dict: continue
                    cat2_ext_name[bid] = self._ext_name_sorted(self.cat2_ext_brandId_name_dict[bid])

                for k, v in cat2_ext_name.items():
                    reg_bname_lst += self.brand_reg(s_name, v, k)
            # 一级类目品牌识别
            if len(reg_bname_lst) == 0 and self.is_cat1_brand_reg:
                cat1_ext_name = {}
                for bid in self.cat1_to_brandId_dict[cat1_name]:
                    if bid not in self.cat1_ori_brandId_name_dict or \
                            bid not in self.cat1_ext_brandId_name_dict: continue
                    cat1_ext_name[bid] = self._ext_name_sorted(self.cat1_ext_brandId_name_dict[bid])

                for k, v in cat1_ext_name.items():
                    reg_bname_lst += self.brand_reg(s_name, v, k)


            if len(reg_bname_lst) == 0: return None, None, None

            rule_opt_lst = self.rule_opt(s_name, reg_bname_lst, cat3_name)
            brand_id_set = set()
            for zz in rule_opt_lst:
                brand_id_set.add(zz[1])

            if len(brand_id_set) == 0: return None, None, None
            if len(brand_id_set) == 1:
                reg_bname, reg_bid = rule_opt_lst[0]
            else:
                reg_bname, reg_bid = self._multi_brand_opt(rule_opt_lst)

            if reg_bid in self.cat3_ori_brandId_name_dict:
                r_ori_name = self.cat3_ori_brandId_name_dict[reg_bid]
            elif reg_bid in self.cat2_ori_brandId_name_dict:
                r_ori_name = self.cat2_ori_brandId_name_dict[reg_bid]
            else:
                r_ori_name = ''
            return reg_bid, reg_bname, r_ori_name

        except Exception as e:
            raise e
