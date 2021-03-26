import unittest
from brand_reg_tool import BrandRegTool
import configparser


class TestBrandRegTool(unittest.TestCase):
    """Test BrandRegTool"""

    def setUp(self):
        self.bReg = BrandRegTool("brand_recall_info.txt", "del_brand_info.txt", "exchange_brand_info.txt", "rule_brand.cfg")
        self.test_exp_dict = {}
        self.config = configparser.ConfigParser()
        self.config.read("rule_test_brand.cfg",encoding="utf-8")
        test_name = self.config["test_exp"]["test_name"]
        self.test_list = test_name.strip().split(",")

    def test_clean_brand(self):
        for test_item in self.test_list:
            pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = self.bReg.brand_recognition(self.config[test_item]['ori_str'].replace("@", "\001"))
            if pre_brand_id == None:continue
            self.assertEqual(self.config[test_item]['target_brand_id'], pre_brand_id)


if __name__ == '__main__':
    unittest.main()

