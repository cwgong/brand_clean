#!/usr/bin/env python3
#coding=utf-8

import os
import tool_v1
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
            self._exchange_brand_dict = self._get_exchange_brand_pair(brand_exchange_file)

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

    def _brand_pair_checking(self, exchange_dict):
        s1 = set(list(exchange_dict.keys()))
        s2 = set(list(exchange_dict.values()))
        s3 = s1 & s2
        if len(s3) > 0:
            return False, s3
        else:
            return True, None

    def _get_exchange_brand_pair(self, ex_file):
        exchange_dict = {}
        if not os.path.exists(ex_file):
            raise Exception("%s does not exists!" % ex_file)
        with open(ex_file,"r",encoding="utf-8") as f2:
            for line in f2:
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                lst1 = line.split("|")
                if len(lst1) != 2:
                    continue
                lst1 = [z.strip() for z in lst1]
                k,v = lst1
                if k not in exchange_dict and k != v:
                    exchange_dict[k] = v

        # 品牌对检测
        chk_flag, conflict_brand_set = self._brand_pair_checking(exchange_dict)
        if not chk_flag:
            err_s = "exchang-brand-pair error: %s" % "\t".join(list(conflict_brand_set))
            raise Exception(err_s)

        return exchange_dict

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
        idx_ori_brand_dict = {}  # 品牌的原始字符串
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
                if len(lst1) != 5:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, b_name, cat1_id, cat1, gmv = lst1

                # idx-brand
                idx_ori_brand_dict[b_id] = b_name
                cat1_dict[cat1_id] = cat1
                if b_name in self._exchange_brand_dict:
                    b_name = self._exchange_brand_dict[b_name]
                r_brand_set = tool_v1.brand_dealing(b_name)

                brand_gmv_dict[b_id] = round(float(gmv), 3)
                idx_brand_lst_dict[b_id] = list(r_brand_set)
                # brand-idx
                for r in r_brand_set:
                    if len(r) == 1: continue
                    if tool_v1.is_number(r): continue
                    is_eng = tool_v1.is_all_eng(r)
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

        return brand_idx_dict, idx_ori_brand_dict, \
               brand_cat1_dict, cat1_brand_dict, \
               cat1_clean_brand_dict, brand_gmv_dict, cat1_dict


class BrandRefRuleOpt(object):
    """
    功能：根据brand_rule.cfg中配置的规则进行品牌的处理
    配置的每一个规则对应一个方法，每一个规则对应一份规则使用的数据，并且这个数据仅仅用于这个方法中

    """
    def __init__(self, brand_reg_rule_file):
        if not os.path.exists(brand_reg_rule_file):
            raise Exception("%s does not exists!" % brand_reg_rule_file)

        self.config = configparser.ConfigParser()
        self.config.read(brand_reg_rule_file, encoding="utf-8")
        self.brand_word_rule_dict = self._getting_rule_dict("brand_word_rule")
        self.brand_cat1_rule_dict = self._getting_rule_dict("brand_cat1_rule")
        self.brand_cat1_fixed_dict = self._getting_brand_cat1_fixed_pair()
        self.phone_brand_not_appear_same_cat1_id, self.phone_brand_not_appear_same_dict \
            = self._getting_phone_brand_not_appear_same()


    def _getting_rule_dict(self, rule_tag):
        s1 = self.config["rule_method_cfg"][rule_tag]
        r_dict = {}
        for tmp in s1.strip().split(","):
            d2 = self._getting_cfg_items(tmp)
            r_dict = dict(r_dict, **d2)

        return r_dict

    def _getting_cfg_items(self, cfg_header):
        try:
            s1 = self.config[cfg_header]["brand_name"]
            lst1 = s1.strip().split(",")
            lst1 = [tmp.strip() for tmp in lst1]

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
                b_name, cat1_id = lst3
                if b_name in d1:
                    z = d1[b_name]
                    d1[b_name] = z + [cat1_id]
                else:
                    d1[b_name] = [cat1_id]
        return d1

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

            return cat1_id.strip(), d1
        except Exception as e:
            raise e

        pass

    def brand_word_rule_func(self, b_name, p_name):
        if len(self.brand_word_rule_dict) == 0: return True
        b_name = b_name.strip()
        p_name = tool_v1.multi_blank_clean(p_name.strip())
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

    def phone_brand_not_appear_same_fun(self, brand_name_lst, product_cat1_id):
        product_cat1_id = product_cat1_id.strip()
        if product_cat1_id != self.phone_brand_not_appear_same_cat1_id:
            return brand_name_lst
        r_set = set()
        for i in range(len(brand_name_lst)):
            a_ori = brand_name_lst[i]
            a = a_ori.replace("|1", "").replace("|0", "").lower()
            for j in range(i+1, len(brand_name_lst)):
                b_ori = brand_name_lst[j]
                b = b_ori.replace("|1", "").replace("|0", "").lower()
                k1 = "%s|%s" % (a, b)
                k2 = "%s|%s" % (b, a)
                if k1 not in self.phone_brand_not_appear_same_dict and \
                        k2 not in self.phone_brand_not_appear_same_dict:
                    r_set.add(a_ori)
                    r_set.add(b_ori)

        return list(r_set)
