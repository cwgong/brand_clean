import configparser


def write_config(new_file,ori_config,idx):
    new_data_list = []
    with open(new_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:
                continue
            line_list = line.strip().split("\t")
            if len(line_list) != 9:continue
            for i in range(len(line_list)):
                if line_list[i] == None:
                    line_list[i] = 'None'
            ori_str, product_id, target_brand_id, target_brand_name, reason, brand_cat1_id, brand_cat1_name, target_cat1_id, target_cat1_name = line_list
            tmp_list = [product_id,ori_str,target_brand_name,target_brand_id,target_cat1_name,target_cat1_id]
            new_data_list.append(tmp_list)
        config = configparser.ConfigParser()
        config.read(ori_config,encoding="utf-8")
        for x in new_data_list:
            config.add_section('test'+str(idx + 1))
            config.set('test'+str(idx + 1),'product_id',x[0])
            config.set('test' + str(idx + 1), 'ori_str', x[1])
            config.set('test' + str(idx + 1), 'target_brand_name', x[2])
            config.set('test' + str(idx + 1), 'target_brand_id', x[3])
            config.set('test' + str(idx + 1), 'target_cat1_name', x[4])
            config.set('test' + str(idx + 1), 'target_cat1_id', x[5])
            idx = idx + 1
        with open('utest_online_data_update.cfg', mode='w', encoding='utf-8') as f:
            config.write(f)

if __name__ == "__main__":
    new_file = 'new_test_exp.txt'
    ori_config = 'utest_online_data.cfg'
    idx = 14
    write_config(new_file, ori_config, idx)