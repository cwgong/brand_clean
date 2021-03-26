#!/usr/bin/env python3
#coding=utf-8

import os
import tool
import re
import traceback

class PddCat3BrandRegFileTool(object):
    def __init__(self, cat1_en_name):
        self.BASE_FOLDER = "%s_config" % (cat1_en_name)
        self.BRAND_FOLDER = "%s/%s_brand_info" % (self.BASE_FOLDER, cat1_en_name)
        self.BRAND_ORI_FILE = "%s/%s_brand_ori.txt" % (self.BRAND_FOLDER, cat1_en_name)
        self.BRAND_CAT3_RECALL_FILE = "%s/%s_brand_cat3_recall.txt" % (self.BRAND_FOLDER, cat1_en_name)
        self.BRAND_CAT2_RECALL_FILE = "%s/%s_brand_cat2_recall.txt" % (self.BRAND_FOLDER, cat1_en_name)
        self.BRAND_CAT1_RECALL_FILE = "%s/%s_brand_cat1_recall.txt" % (self.BRAND_FOLDER, cat1_en_name)
        self.DEL_BRAND_FILE = "%s/%s_del_brand_info.txt" % (self.BASE_FOLDER, cat1_en_name)
        self.EXCHANGE_BRAND_FILE = "%s/%s_exchange_brand_info.txt" % (self.BASE_FOLDER, cat1_en_name)
        self.RULE_BRAND = "%s/%s_rule_brand.cfg" % (self.BASE_FOLDER, cat1_en_name)
        self.DEL_BRANDID_FILE = "%s/%s_del_brandID.txt" % (self.BASE_FOLDER, cat1_en_name)

class BrandRecallOpt(object):
    def __init__(self, cat1_en_name):
        file_sys_obj =  PddCat3BrandRegFileTool(cat1_en_name)
        self.in_file = file_sys_obj.BRAND_ORI_FILE
        if not os.path.exists(self.in_file):
            raise Exception("%s does not exist!" % self.in_file)
        self.cat1_en_name = cat1_en_name
        self.cat3_out_file = file_sys_obj.BRAND_CAT3_RECALL_FILE
        self.cat2_out_file = file_sys_obj.BRAND_CAT2_RECALL_FILE
        self.cat1_out_file = file_sys_obj.BRAND_CAT1_RECALL_FILE
        brand_exchange_file = file_sys_obj.EXCHANGE_BRAND_FILE
        brand_del_file = file_sys_obj.DEL_BRAND_FILE
        brandID_del_file = file_sys_obj.DEL_BRANDID_FILE

        self.brand_exchange_dict = {}
        if os.path.exists(brand_exchange_file):
            self.brand_exchange_dict = self._loading_exchange_brand_pair(brand_exchange_file)

        self.brand_del_dict = {}
        if os.path.exists(brand_del_file):
            self.brand_del_dict = self._loading_del_brand(brand_del_file)

        self.del_brandID_dict = {}
        if os.path.exists(file_sys_obj.DEL_BRANDID_FILE):
            self.del_brandID_dict = self._loading_del_brandID(brandID_del_file)

        self.d1 = {}

    def _cat2_brand_filter(self, cat1_en_name, cat2_ch_name, b_id):
        # 手机配件相关品牌过滤
        # 手机贴膜下面不能出现
        if cat1_en_name == "shoujipeijian":
            # 苹果、小米、红米、oppo、vivo、华为、荣耀、一加、iqoo
            del_brand_id_dict = {'10936677': '苹果', '10365607': '华为', '10698337': '小米', '10561609': '荣耀', '10429338': 'vivo',
             '10694602': 'OPPO', '10489679': '一加', '10282053': '三星', '10943471': 'realme', '10683308': '黑鲨',
             '10620759': '魅族', '10117799': '努比亚', '10130469': '锤子', '10363832': 'Lenovo/联想', '10048785':'Nokia/诺基亚',
             '10653400': 'Coolpad / 酷派'}

            del_cat_name_dict = {'手机配件':''}

            if cat2_ch_name in del_cat_name_dict and b_id in del_brand_id_dict:
                return True
            else:
                return False
        else:
            return False


    def _cat3_brand_filter(self, cat1_en_name, cat3_ch_name, b_id):
        # 手机配件相关品牌过滤
        # 手机贴膜下面不能出现
        if cat1_en_name == "shoujipeijian":
            # 苹果、小米、红米、oppo、vivo、华为、荣耀、一加、iqoo
            del_brand_id_dict = {'10936677': '苹果', '10365607': '华为', '10698337': '小米', '10561609': '荣耀', '10429338': 'vivo',
             '10694602': 'OPPO', '10489679': '一加', '10282053': '三星', '10943471': 'realme', '10683308': '黑鲨',
             '10620759': '魅族', '10117799': '努比亚', '10130469': '锤子'}

            #del_cat_name_dict = {'手机贴膜': '', '手机存储卡': '', '数据线': '', '充电器': '', '创意配件': '', '手机饰品': '', '手机支架': '', '手机电池': '', '手机壳/保护套': ''}
            del_cat_name_dict = { '手机存储卡': '', '数据线': '', '创意配件': '', '手机饰品': '', '手机支架': '', '手机电池': '', '充电器': ''}

            if cat3_ch_name in del_cat_name_dict and b_id in del_brand_id_dict:
                return True
            else:
                return False
        else:
            return False

    def _loading_exchange_brand_pair(self, brand_exchange_file):
        def _brand_pair_checking(exchange_dict):
            s1 = set(list(exchange_dict.keys()))
            s2 = set(list(exchange_dict.values()))
            s3 = s1 & s2
            if len(s3) > 0:
                return False, s3
            else:
                return True, None


        exchange_dict = {}
        with open(brand_exchange_file) as f2:
            for line in f2:
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                lst1 = line.split("|")
                if len(lst1) != 2:
                    continue
                lst1 = [z.strip() for z in lst1]
                k, v = lst1
                if k not in exchange_dict and k != v:
                    exchange_dict[k] = v

        # 品牌对检测
        chk_flag, conflict_brand_set = _brand_pair_checking(exchange_dict)
        if not chk_flag:
            err_s = "exchang-brand-pair error: %s" % "\t".join(list(conflict_brand_set))
            raise Exception(err_s)

        return exchange_dict

    def _loading_del_brand(self, del_brand_file):
        del_dict = {}
        with open(del_brand_file) as f2:
            for line in f2:
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                del_dict[line] = ''
        return del_dict

    def _loading_del_brandID(self, del_brandID_file):
        r_dict = {}
        with open(del_brandID_file) as f2:
            for line in f2:
                line = line.strip()
                if line == "": continue
                if line.startswith("#"): continue
                lst1 = line.split("|")
                if len(lst1) != 2: continue
                lst1 = [tmp.strip() for tmp in lst1]
                del_bid, _ = lst1
                try:
                    int(del_bid)
                    r_dict[del_bid] = ''
                except:
                    continue

        return r_dict

    def _is_all_eng(self, s1):
        return tool.is_all_eng(s1)

    def _is_all_chinese(sefl, s1):
        return tool.is_all_chinese(s1)

    def _finding_sameCat3_sameBName_bak(self, b_lst):
        sameBName_dict = {}
        for tmp in b_lst:
            id1, n1, o1, c11, c12, c13, gmv1 = tmp
            if n1 in sameBName_dict:
                xx = sameBName_dict[n1]
                xx += [tmp]
                sameBName_dict[n1] = list(set(xx))
            else:
                sameBName_dict[n1] = [tmp]
        #print(sameBName_dict)
        lst9 = []
        tmp_del_brand_set = set()
        for k, v in sameBName_dict.items():
            if len(v) > 1:
                sorted_lst = sorted(v, key=lambda x: x[6], reverse=True)
                lst9.append(sorted_lst[0])
                for tmp1 in sorted_lst[1:]:
                    tmp_del_brand_set.add(tmp1[0])
            else:
                lst9.append(v[0])
        r_lst = []
        for tmp2 in lst9:
            if tmp2[0] not in tmp_del_brand_set:
                r_lst.append(tmp2)

        return r_lst

    def _finding_sameCat_sameBName(self, b_lst):
        sameBName_dict = {}
        for tmp in b_lst:
            id1, n1, o1, c11, c12, c13, gmv1 = tmp
            if n1 in sameBName_dict:
                xx = sameBName_dict[n1]
                xx += [tmp]
                sameBName_dict[n1] = list(set(xx))
            else:
                sameBName_dict[n1] = [tmp]

        lst9 = []
        tmp_del_brand_set = set()
        for k, v in sameBName_dict.items():
            if len(v) > 1:
                sorted_lst = sorted(v, key=lambda x: x[6], reverse=True)
                lst9.append(sorted_lst[0])
                for tmp1 in sorted_lst[1:]:
                    tmp_del_brand_set.add(tmp1)
            else:
                lst9.append(v[0])
        r_lst = []
        for tmp2 in lst9:
            if tmp2 not in tmp_del_brand_set:
                r_lst.append(tmp2)

        return r_lst

    def _sameCat3_sameBName_dealing(self):
        cat3_brand_info_dict = {}
        with open(self.in_file) as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                lst1 = line.split("\t")
                if len(lst1) != 6:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv = lst1

                # 三级类目，相关品牌过滤
                if self._cat3_brand_filter(self.cat1_en_name, cat3_name, b_id): continue
                if b_id in self.del_brandID_dict: continue
                if ori_b_name in self.brand_del_dict: continue
                if b_id in self.del_brandID_dict: continue
                if ori_b_name in self.brand_exchange_dict:
                    bname_ext = self.brand_exchange_dict[ori_b_name]
                else:
                    bname_ext = ori_b_name
                ext_lst = [xx.strip() for xx in bname_ext.split('/')]
                b_gmv = float(b_gmv)
                for yy in ext_lst:
                    if cat3_name in cat3_brand_info_dict:
                        zz = cat3_brand_info_dict[cat3_name]
                        zz += [(b_id, yy,  ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv)]
                        cat3_brand_info_dict[cat3_name] = zz
                    else:
                        cat3_brand_info_dict[cat3_name] = [(b_id, yy, ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv)]

        r_lst = []
        for k, v in cat3_brand_info_dict.items():
            r_lst += self._finding_sameCat_sameBName(v)

        return r_lst

    def _sameCat2_sameBName_dealing(self):
        cat2_brand_info_dict = {}
        with open(self.in_file) as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                lst1 = line.split("\t")
                if len(lst1) != 6:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv = lst1
                if self._cat2_brand_filter(self.cat1_en_name, cat2_name, b_id): continue
                if b_id in self.del_brandID_dict: continue
                if ori_b_name in self.brand_del_dict: continue
                if b_id in self.del_brandID_dict: continue
                if ori_b_name in self.brand_exchange_dict:
                    bname_ext = self.brand_exchange_dict[ori_b_name]
                else:
                    bname_ext = ori_b_name
                ext_lst = [xx.strip() for xx in bname_ext.split('/')]
                b_gmv = float(b_gmv)
                for yy in ext_lst:
                    if cat2_name in cat2_brand_info_dict:
                        zz = cat2_brand_info_dict[cat2_name]
                        zz += [(b_id, yy,  ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv)]
                        cat2_brand_info_dict[cat2_name] = zz
                    else:
                        cat2_brand_info_dict[cat2_name] = [(b_id, yy, ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv)]

        r_lst = []
        for k, v in cat2_brand_info_dict.items():
            r_lst += self._finding_sameCat_sameBName(v)

        return r_lst

    def _sameCat1_sameBName_dealing(self):
        cat1_brand_info_dict = {}
        with open(self.in_file) as f1:
            for line in f1:
                line = line.strip()
                if line == "": continue
                lst1 = line.split("\t")
                if len(lst1) != 6:
                    continue
                lst1 = [tmp.strip() for tmp in lst1]
                b_id, ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv = lst1
                if b_id in self.del_brandID_dict: continue
                if ori_b_name in self.brand_del_dict: continue
                if b_id in self.del_brandID_dict: continue
                if ori_b_name in self.brand_exchange_dict:
                    bname_ext = self.brand_exchange_dict[ori_b_name]
                else:
                    bname_ext = ori_b_name
                ext_lst = [xx.strip() for xx in bname_ext.split('/')]
                b_gmv = float(b_gmv)
                for yy in ext_lst:
                    if cat1_name in cat1_brand_info_dict:
                        zz = cat1_brand_info_dict[cat1_name]
                        zz += [(b_id, yy,  ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv)]
                        cat1_brand_info_dict[cat1_name] = zz
                    else:
                        cat1_brand_info_dict[cat1_name] = [(b_id, yy, ori_b_name, cat1_name, cat2_name, cat3_name, b_gmv)]

        r_lst = []
        for k, v in cat1_brand_info_dict.items():
            r_lst += self._finding_sameCat_sameBName(v)

        return r_lst

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

        tmp = brand_name.strip().replace("（", "(").replace("）", "").replace(")", "")
        lst2 = tmp.split("(")
        if len(lst2) == 2:
            b1 = lst2[0]
            if self._is_all_eng(lst2[1]):
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
                if self._is_all_eng(b):
                    en_brand_lst.append(b)
                elif self._is_all_chinese(b):
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

            if len(en_brand_lst) > 1:
                for i in range(len(en_brand_ext_lst)):
                    for j in range(i + 1, len(en_brand_lst)):
                        mix_brand_lst.append(en_brand_lst[i] + en_brand_lst[j])
                        mix_brand_lst.append(en_brand_lst[j] + en_brand_lst[i])

            re_brand_lst = mix_brand_lst + en_brand_ext_lst + ch_brand_lst + other_brand_lst

        r_lst = []
        for tmp in list(set(re_brand_lst)):
            if tmp in self.brand_del_dict: continue
            r_lst.append((len(tmp), tmp))
        r_lst = sorted(r_lst, key=lambda k: k[0], reverse=True)
        tmp_lst = [tmp[1] for tmp in r_lst]
        return "/".join(tmp_lst)

    def _brand_ext(self, ori_b_name):
        if ori_b_name in self.brand_exchange_dict:
            b_name = self.brand_exchange_dict[ori_b_name]
        else:
            b_name = ori_b_name
        b_name = b_name.strip()
        if b_name == "": return ""
        b_name = tool.brand_clean(b_name)
        ext_band_name = self.english_brand_extension(b_name)

        return ext_band_name

    def brand_cat3_recall_local_file_ext(self):
        try:
            cat3_dealing_lst = self._sameCat3_sameBName_dealing()
            cat3_brand_dict = {}
            for lst1 in cat3_dealing_lst:
                b_id, _, ori_b_name, cat1_name, cat2_name, cat3_name, _ = lst1

                if ori_b_name in self.brand_del_dict: continue
                if b_id in self.del_brandID_dict: continue

                ext_band_name = self._brand_ext(ori_b_name)
                if ext_band_name == "": continue
                s2 = "\t".join([b_id, ext_band_name, ori_b_name, cat1_name, cat2_name, cat3_name])
                if cat3_name in cat3_brand_dict:
                    yy = cat3_brand_dict[cat3_name]
                    yy += [s2]

                    cat3_brand_dict[cat3_name] = list(set(yy))
                else:
                    cat3_brand_dict[cat3_name] = [s2]

            r_lst = []
            for k, v in cat3_brand_dict.items():
                r_lst.append("#%s" % k)
                for zz in v:
                    r_lst.append(zz)

            with open(self.cat3_out_file, "w") as f1:
                f1.write("\n".join(r_lst))
                f1.flush()

        except Exception as e:
            raise e

    def brand_cat2_recall_local_file_ext(self):
        try:
            cat2_dealing_lst = self._sameCat2_sameBName_dealing()
            cat2_brand_dict = {}
            for lst1 in cat2_dealing_lst:
                b_id, _, ori_b_name, cat1_name, cat2_name, cat3_name, _ = lst1

                if ori_b_name in self.brand_del_dict: continue
                if b_id in self.del_brandID_dict: continue

                ext_band_name = self._brand_ext(ori_b_name)
                if ext_band_name == "": continue
                s2 = "\t".join([b_id, ext_band_name, ori_b_name, cat1_name, cat2_name, cat3_name])
                if cat2_name in cat2_brand_dict:
                    yy = cat2_brand_dict[cat2_name]
                    yy += [s2]

                    cat2_brand_dict[cat2_name] = list(set(yy))
                else:
                    cat2_brand_dict[cat2_name] = [s2]

            r_lst = []
            for k, v in cat2_brand_dict.items():
                r_lst.append("#%s" % k)
                for zz in v:
                    r_lst.append(zz)

            with open(self.cat2_out_file, "w") as f1:
                f1.write("\n".join(r_lst))
                f1.flush()

        except Exception as e:
            raise e

    def brand_cat1_recall_local_file_ext(self):
        try:
            cat1_dealing_lst = self._sameCat1_sameBName_dealing()
            cat1_brand_dict = {}
            for lst1 in cat1_dealing_lst:
                b_id, _, ori_b_name, cat1_name, cat2_name, cat3_name, _ = lst1
                if ori_b_name in self.brand_del_dict: continue
                if b_id in self.del_brandID_dict: continue

                ext_band_name = self._brand_ext(ori_b_name)
                if ext_band_name == "": continue
                s2 = "\t".join([b_id, ext_band_name, ori_b_name, cat1_name, cat2_name, cat3_name])
                if cat1_name in cat1_brand_dict:
                    yy = cat1_brand_dict[cat1_name]
                    yy += [s2]

                    cat1_brand_dict[cat1_name] = list(set(yy))
                else:
                    cat1_brand_dict[cat1_name] = [s2]

            r_lst = []
            for k, v in cat1_brand_dict.items():
                r_lst.append("#%s" % k)
                for zz in v:
                    r_lst.append(zz)

            with open(self.cat1_out_file, "w") as f1:
                f1.write("\n".join(r_lst))
                f1.flush()

        except Exception as e:
            raise e


    def brand_recall_local_file(self):
        try:
            ex_brand_dict = self.brand_exchange_dict
            r_lst = []
            with open(self.in_file) as f1:
                for line in f1:
                    line = line.strip()
                    if line == "": continue
                    lst1 = line.split("\t")
                    if len(lst1) != 5:
                        continue
                    lst1 = [tmp.strip() for tmp in lst1]
                    b_id, ori_b_name, cat1_name, cat2_name, cat3_name = lst1
                    if ori_b_name in self.brand_del_dict: continue
                    if b_id in self.del_brandID_dict: continue
                    if ori_b_name in ex_brand_dict:
                        b_name = ex_brand_dict[ori_b_name]
                    else:
                        b_name = ori_b_name

                    b_name = tool.brand_clean(b_name)
                    ext_band_name = self.english_brand_extension(b_name)
                    r_lst.append("\t".join([b_id, ext_band_name, ori_b_name, cat1_name, cat2_name, cat3_name]))

            with open(self.out_file, "w") as f1:
                f1.write("\n".join(r_lst))
                f1.flush()

        except Exception as e:
            raise e


if __name__ == "__main__":
    try:
        cat1_en_name = 'jiayongdianqi'
        cat1_en_name = 'meizhuanghufu'
        cat1_en_name = 'shoujipeijian'
        cat1_en_name = 'shuma'
        obj = BrandRecallOpt(cat1_en_name=cat1_en_name)
        obj.brand_cat2_recall_local_file_ext()
        obj.brand_cat3_recall_local_file_ext()
        obj.brand_cat1_recall_local_file_ext()
    except:
        print(traceback.format_exc())


