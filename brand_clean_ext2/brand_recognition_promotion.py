import io

def get_brand(input_file,recall_file):
    recall_data_list = []
    with io.open(recall_file,"r",encoding="utf-8") as f2:
        for line in f2:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 6:continue
            id_,brand_name,brand_recall_name,cat1_id,cat1_name,gmv = line_list
            recall_data_list.append(id_)
    with io.open(input_file,"r",encoding="utf-8") as f1:
        for line in f1:
            if len(line) == 0:continue
            line_list = line.strip().split("\t")
            if len(line_list) != 5:continue
            id_,brand_name,reason,num_a,num_b = line_list
            if id_ not in recall_data_list:
                print(line.strip())

if __name__ == "__main__":
    input_file = "optimize_brand.txt"
    recall_file = "brand_recall_info.txt"
    get_brand(input_file,recall_file)