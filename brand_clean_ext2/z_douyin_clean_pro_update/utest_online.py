import unittest
from brand_reg_tool import BrandRegTool
import configparser

bReg = BrandRegTool("brand_recall_info.txt", "del_brand_info.txt", "exchange_brand_info.txt", "rule_brand.cfg")
config = configparser.ConfigParser()
config.read("utest_online_data.cfg", encoding="utf-8")

class TestBrandRegTool(unittest.TestCase):
    """Test BrandRegTool"""

    def test_clean_brand1(self):
        pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['test1']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test1']['target_brand_id'], pre_brand_id)

    def test_clean_brand2(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test2']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test2']['target_brand_id'], pre_brand_id)

    def test_clean_brand3(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test3']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test3']['target_brand_id'], pre_brand_id)

    def test_clean_brand4(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test4']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test4']['target_brand_id'], pre_brand_id)

    def test_clean_brand5(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test5']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test5']['target_brand_id'], pre_brand_id)

    def test_clean_brand6(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test6']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test6']['target_brand_id'], pre_brand_id)

    def test_clean_brand7(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test7']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test7']['target_brand_id'], pre_brand_id)

    def test_clean_brand8(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test8']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test8']['target_brand_id'], pre_brand_id)

    def test_clean_brand9(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test9']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test9']['target_brand_id'], pre_brand_id)

    def test_clean_brand10(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test10']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test10']['target_brand_id'], pre_brand_id)

    def test_clean_brand11(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test11']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test11']['target_brand_id'], pre_brand_id)

    def test_clean_brand12(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test12']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test12']['target_brand_id'], pre_brand_id)

    def test_clean_brand13(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test13']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test13']['target_brand_id'], pre_brand_id)

    def test_clean_brand14(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test14']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test14']['target_brand_id'], pre_brand_id)

    def test_clean_brand15(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test15']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test15']['target_brand_id'], pre_brand_id)

    def test_clean_brand16(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test16']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test16']['target_brand_id'], pre_brand_id)

    def test_clean_brand17(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test17']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test17']['target_brand_id'], pre_brand_id)

    def test_clean_brand18(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test18']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test18']['target_brand_id'], pre_brand_id)

    def test_clean_brand19(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test19']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test19']['target_brand_id'], pre_brand_id)

    def test_clean_brand20(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test20']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test20']['target_brand_id'], pre_brand_id)

    def test_clean_brand21(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test21']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test21']['target_brand_id'], pre_brand_id)

    def test_clean_brand22(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test22']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test22']['target_brand_id'], pre_brand_id)

    def test_clean_brand23(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test23']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test23']['target_brand_id'], pre_brand_id)

    def test_clean_brand24(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test24']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test24']['target_brand_id'], pre_brand_id)

    def test_clean_brand25(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test25']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test25']['target_brand_id'], pre_brand_id)

    def test_clean_brand26(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test26']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test26']['target_brand_id'], pre_brand_id)

    def test_clean_brand27(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test27']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test27']['target_brand_id'], pre_brand_id)

    def test_clean_brand28(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test28']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test28']['target_brand_id'], pre_brand_id)

    def test_clean_brand29(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test29']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test29']['target_brand_id'], pre_brand_id)

    def test_clean_brand30(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test30']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test30']['target_brand_id'], pre_brand_id)

    def test_clean_brand31(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test31']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test31']['target_brand_id'], pre_brand_id)

    def test_clean_brand32(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test32']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test32']['target_brand_id'], pre_brand_id)

    def test_clean_brand33(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test33']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test33']['target_brand_id'], pre_brand_id)

    def test_clean_brand34(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test34']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test34']['target_brand_id'], pre_brand_id)

    def test_clean_brand35(self):
        pre_brand_id, pre_brand, match_type, b_cat1_id, b_cat1_name, cat1_id, cat1_name = bReg.brand_recognition(
            config['test35']['ori_str'].replace("@", "\001"))
        if pre_brand_id == None:
            pre_brand_id = "None"
        self.assertEqual(config['test35']['target_brand_id'], pre_brand_id)

