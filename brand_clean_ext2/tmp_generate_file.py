import unittest
from brand_reg_tool import BrandRegTool
import configparser

bReg = BrandRegTool("brand_recall_info.txt", "del_brand_info.txt", "exchange_brand_info.txt", "rule_brand.cfg")
config = configparser.ConfigParser()
config.read("utest_online_data_update.cfg", encoding="utf-8")

class TestBrandRegTool(unittest.TestCase):

	def test_clean_brand_3357085538191592175(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3357085538191592175']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3357085538191592175']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3401616162600130251(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3401616162600130251']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3401616162600130251']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3426111097860667817(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3426111097860667817']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3426111097860667817']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3416648243235438963(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3416648243235438963']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3416648243235438963']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3421897522199802328(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3421897522199802328']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3421897522199802328']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3431124812649647120(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3431124812649647120']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3431124812649647120']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3434101983466937016(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3434101983466937016']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3434101983466937016']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3405190000600595627(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3405190000600595627']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3405190000600595627']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3410543769668440301(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3410543769668440301']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3410543769668440301']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3419769275710372814(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3419769275710372814']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3419769275710372814']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3354685409459341232(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3354685409459341232']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3354685409459341232']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3415864514741168743(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3415864514741168743']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3415864514741168743']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3369894145832411458(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3369894145832411458']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3369894145832411458']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3384173514230777960(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3384173514230777960']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3384173514230777960']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3411824198245607566(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3411824198245607566']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3411824198245607566']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3425415609368885164(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3425415609368885164']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3425415609368885164']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3423645268946595861(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3423645268946595861']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3423645268946595861']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3425211641489445438(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3425211641489445438']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3425211641489445438']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3355592858823480484(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3355592858823480484']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3355592858823480484']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3386404760302309717(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3386404760302309717']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3386404760302309717']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3403150395785271393(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3403150395785271393']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3403150395785271393']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3423538998570802670(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3423538998570802670']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3423538998570802670']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3428544113082017102(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3428544113082017102']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3428544113082017102']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3424086933435992400(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3424086933435992400']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3424086933435992400']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3431813551977835032(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3431813551977835032']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3431813551977835032']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3400284318290021202(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3400284318290021202']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3400284318290021202']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3418828334392561031(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3418828334392561031']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3418828334392561031']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3422411309952710608(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3422411309952710608']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3422411309952710608']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3432625045128778267(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3432625045128778267']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3432625045128778267']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3411798860086001815(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3411798860086001815']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3411798860086001815']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3400471044862127146(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3400471044862127146']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3400471044862127146']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3432742510454288500(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3432742510454288500']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3432742510454288500']['target_brand_id'], pre_brand_id)

	def test_clean_brand_3434084541613109981(self):
		pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['3434084541613109981']['ori_str'].replace('@',''))
		if pre_brand_id == None:
			pre_brand_id = 'None'
		self.assertEqual(config['3434084541613109981']['target_brand_id'], pre_brand_id)
