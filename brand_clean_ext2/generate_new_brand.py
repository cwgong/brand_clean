import io

def generate_new_brand(ori_brand_file,inc_brand_file,output_file):
    special_dict = {}
    update_special_dict = {}
    all_special_dict = {}
    with open(ori_brand_file, "r", encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0: continue
            line_list = line.strip().split("\t")
            if len(line_list) != 2: continue
            id_, brand_name = line_list
            all_special_dict[brand_name] = [id_,brand_name]

    with open(inc_brand_file, "r", encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:
                continue
            line_list_ = line.strip().split("\t")
            if len(line_list_) != 4:
                continue
            id_, brand_name, cat1, gmv = line_list_
            all_special_dict[brand_name] = [id_,brand_name]

    all_special_list = list(all_special_dict.keys())
    with io.open(output_file,"w",encoding="utf-8") as f3:
        for item in all_special_list:
            f3.write(all_special_dict[item][0] + "\t" + all_special_dict[item][1] + "\n")
        f3.flush()


if __name__ == "__main__":
    ori_brand_file = "xiaowu_standard_brand.txt"
    inc_brand_file = "update_brand_file.txt"
    output_file = "all_brand.txt"
    generate_new_brand(ori_brand_file,inc_brand_file,output_file)



