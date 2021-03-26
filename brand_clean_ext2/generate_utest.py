import configparser
import io

class Utest_Generator():
    def __init__(self,ori_scripts_file,utest_config_file):
        self.ori_scripts = self._get_ori_scripts(ori_scripts_file)
        self.config_exp_list = self._get_config_exp(utest_config_file)

    def _get_ori_scripts(self,ori_scripts_file):
        try:
            with io.open(ori_scripts_file, "r", encoding="utf-8") as f1:
                content = f1.read()
        except Exception as e:
            print(e)
        return content

    def _get_config_exp(self,utest_config_file):
        config = configparser.ConfigParser()
        config.read(utest_config_file,encoding="utf-8")
        sec = config.sections()
        line_list = []
        for sec_item in sec:
            line_list.append("\n")
            line_list.append("\t" + "def test_clean_brand_" + sec_item + "(self):" + "\n")
            line_list.append("\t" + "\t" + "pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name = bReg.brand_recognition(config['" + sec_item + "']['ori_str'].replace('" + "@" + "'," + "'\001'))" + "\n")
            line_list.append("\t" + "\t" + "if pre_brand_id == None:" + "\n")
            line_list.append("\t" + "\t" + "\t" + "pre_brand_id = 'None'" + "\n")
            line_list.append("\t" + "\t" + "self.assertEqual(config['" + sec_item + "']['target_brand_id'], pre_brand_id)")
            line_list.append("\n")
        return line_list

    def write_scripts_utest(self, scripts_file):
        with io.open(scripts_file, "w", encoding="utf-8") as f1:
            f1.write(self.ori_scripts)
            f1.write("".join(self.config_exp_list))

if __name__ == "__main__":
    ori_utest_file = "ori_utest_file.txt"
    utest_config_file = "utest_online_data_update.cfg"
    scripts_file = "tmp_generate_file.py"
    utest_generator = Utest_Generator(ori_utest_file,utest_config_file)
    utest_generator.write_scripts_utest(scripts_file)

