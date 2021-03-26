#!/usr/bin/env python3
#coding=utf8

#import tool
#tool.appoint_brand_recall("standard_brand_info.txt", "xiaowu_standard_brand.txt")


from brand_recall_opt import BrandRecallOpt
obj = BrandRecallOpt("standard_brand_info.txt", \
                     "xiaowu_standard_brand.txt",\
                     "xiaowu_standard_brand_new.txt")
obj.brand_recall()