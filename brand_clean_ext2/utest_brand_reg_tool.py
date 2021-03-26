#encon
from brand_reg_tool import BrandRegTool
import tool
import traceback
import configparser

traceback.format_exc()
# def __init__(self, standard_brand_file, del_brand_file=None, exchange_brand_file=None, rule_brand_file=None):
#
bReg = BrandRegTool("brand_recall_info.txt", "del_brand_info.txt", "exchange_brand_info.txt", "rule_brand.cfg")

s1 = " 行营"
s2 = tool.s_name_dealing('（买一送一）手工精绑主线组')
s3 = tool.s_name_dealing("行营")
# print(tool.s_name_dealing(s2 + " " + s3))

# print(bReg.brand_idx_dict)

idx = 0
err_lst = []
flag = 0

def write_config(new_test, ori_config):
    config = configparser.ConfigParser()
    config.read(ori_config,encoding="utf-8")
    sec = config.sections()

    if new_test[0] not in sec:
        config.add_section(new_test[0])
        config.set(new_test[0],'product_id',new_test[0])
        config.set(new_test[0], 'ori_str', new_test[1])
        config.set(new_test[0], 'target_brand_name', new_test[2])
        config.set(new_test[0], 'target_brand_id', new_test[3])
        config.set(new_test[0], 'target_cat1_name', new_test[4])
        config.set(new_test[0], 'target_cat1_id', new_test[5])
        with open(ori_config, mode='w', encoding='utf-8') as f:
            config.write(f)

with open("douyin_data.txt","r",encoding="utf-8") as f1:
    for line in f1:
        try:
            line = line.strip()
            if line == "": continue
            lst1 = line.split("\001")
            if len(lst1) != 5:
                # print(lst1)
                continue

            idx += 1

            lst1 = [tmp.strip() for tmp in lst1]
            product_id, product_name, brand_word, cat1_id, cat1 = lst1
            '''
            if product_id not in ["3416468988480342466"]:
                #["3430512378675096131"]:
                #['3420540042093967614','3430630092982850935', '3429622676191327009', '3404061549483132357', '3431098226802049044', '3430532274658141732', '3430162766265223134', '3427225824267505184', '3431448580613892761', '3428720073454567789', '3431693217630920222', '3427554312073687200', '3430328180395910029', '3429621468214990761']:

                #['3427554312073687200', '3427225824267505184']:
                #['3430162766265223134', '3427554312073687200', '3427225824267505184', '3430328180395910029']:
                #['3420540042093967614','3430630092982850935', '3429622676191327009', '3404061549483132357', '3431098226802049044', '3430532274658141732', '3430162766265223134', '3427225824267505184', '3431448580613892761', '3428720073454567789', '3431693217630920222', '3427554312073687200', '3430328180395910029', '3429621468214990761']:
                continue
            '''

            '''
            flag = False
            if "转接头" in product_name:
                ok = 1
                flag = True

            if cat1 == "生鲜" and "苹果" in product_name:
                ok = 2
                flag = True

            if flag == False: continue
            '''
            # if product_id not in ["3431813551977835032", "3434084541613109981", "3400284318290021202", "3428544113082017102"]: continue
            # if product_id not in ["3400471044862127146"]: continue
            # if product_id not in ["3436340101679086536", "3432625045128778267", "3424086933435992400", "3434855073778387047", "3436340101679086536"]: continue
            # if product_id not in ['3432742510454288500', '3436868129337275480', '3436867686989178116']: continue
            # if product_id not in ['3431813551977835032','3434084541613109981','3400284318290021202','3428544113082017102','3400471044862127146','3436340101679086536','3432625045128778267','3424086933435992400','3434855073778387047','3436340101679086536','3432742510454288500','3436868129337275480','3436867686989178116','3355592858823480484','3411798860086001815','3423538998570802670','3422411309952710608','3418828334392561031','3355592858823480484','3422411309952710608','3418828334392561031','3431813551977835032','3434084541613109981','3400284318290021202','3400471044862127146','3432742510454288500']: continue
            # if product_id not in ["3434101983466937016", "3425415609368885164", "3354685409459341232", "3426111097860667817","3401616162600130251","3403150395785271393","3355592858823480484","3357085538191592175","3423645268946595861","3425211641489445438","3384173514230777960","3416648243235438963","3415864514741168743","3421897522199802328","3410543769668440301","3369894145832411458","3411824198245607566","3419769275710372814","3386404760302309717","3405190000600595627","3431124812649647120"]:continue
            if product_id not in ['3443153000187697928']:continue
            '''
            if idx > 100: break
            #print(bReg.brand_recognition(product_name, brand_word))
            p_name = tool.s_name_dealing(product_name)
            b_name = tool.s_name_dealing(brand_word)
            print(bReg.brand_recognition("%s %s") % (p_name, b_name))
            '''
            # if idx >= 100: break
            pre_brand_id, pre_brand, match_type, \
            b_cat1_id, b_cat1_name, cat1_id, \
            cat1_name = bReg.brand_recognition(line)
            print(line.replace("@","").replace("\001","@"))
            print("%s\t%s\t%s\t%s\t%s\t%s\t%s" % (pre_brand_id, pre_brand, match_type,b_cat1_id, b_cat1_name, cat1_id,cat1_name))
            if flag == 1:
                tmp_list = [product_id, line.replace("@","").replace("\001","@"), pre_brand, pre_brand_id, cat1_id,cat1_name]
                for i in range(len(tmp_list)):
                    if tmp_list[i] == None:
                        tmp_list[i] = "None"
                ori_config_file = "utest_online_data_update.cfg"
                write_config(tmp_list,ori_config_file)
            if pre_brand != None and match_type != None:
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (product_id, product_name, brand_word, cat1_id, cat1, \
                                                                  pre_brand_id, pre_brand, b_cat1_id, b_cat1_name,
                                                                  match_type))
            else:
                err_lst.append(product_id)
                # print(lst1)
        except Exception as e:
            print(traceback.format_exc())
    # print(err_lst)

# a = bReg.english_brand_recognition("vero moda".lower(), "Vero Moda2020春季新款棉收腰宽摆风衣外套女 320121527 VERO MODA".lower())
# print(a)