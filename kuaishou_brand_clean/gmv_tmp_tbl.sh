hive -e "add jar hdfs://db-cluster/user/hive/warehouse/udfs/udf-1.0-jar-with-dependencies.jar;
create temporary function edw_week_sunday as 'com.databurning.edw.udf.UDFWeekSunday';
drop table tmp.tmp_kuaishou_product_gmv_detail;
create table tmp.tmp_kuaishou_product_gmv_detail as
select product_id
      ,product_name
      ,gmv
      ,first_type_id
      ,first_type_name
      ,brand_id
      ,brand_name
      ,platform_name
      ,row_number()over(partition by brand_id order by gmv desc)rn
  from
    (
      select '快手' platform_name
            ,a.product_id
            ,a.jumptoken product_url
            ,jiangtao.product_name product_name
            ,jiangtao.good_type brand_word
            ,a.gmv
            ,'直播' product_attr
            ,b.matching_rate as similar_value
            ,c.category1_id_std as first_type_id
            ,c.category1_std    as first_type_name
            ,c.category2_id_std as second_type_id
            ,c.category2_std    as second_type_name
            ,c.category3_id_std as third_type_id
            ,c.category3_std    as third_type_name
            ,0 as type_match_result
            ,cast(null as string) as type_first_update_time
            ,cast(null as string) as type_second_update_time
            ,case when a.source_platform = '快手' then '快手-自营'
                  when a.source_platform = '淘宝' then '快手-淘系'
                  when a.source_platform = '魔筷' then '快手-魔筷'
                  when a.source_platform = '有赞' then '快手-有赞'
                  when a.source_platform = '课程专区' then '快手-课程专区'
                  when a.source_platform = '闪电购' then '快手-闪电购'
                  else '快手-其他'
              end as product_source
            ,brand.brand_id_std as brand_id
            ,brand.brand_name_std as brand_name
            ,0 as brand_match_result
            ,'' as product_label
            ,cast(null as string) as brand_first_update_time
            ,cast(null as string) as brand_second_update_time
            ,edw_week_sunday('2020-11-12') create_time
            ,c.secondary_mkt_industry1 as industry_name
            ,case when a.source_platform = '快手' then 'ks_xd'
                  when a.source_platform = '淘宝' then 'ks_tx'
                  when a.source_platform = '魔筷' then 'ks_mk'
                  when a.source_platform = '有赞' then 'ks_yz'
                  when a.source_platform = '课程专区' then 'ks_kczq'
                  when a.source_platform = '闪电购' then 'ks_sdg'
                  else 'ks_qt'
              end platform_type
            ,a.dt
            ,row_number() over(partition by a.good_type,a.product_id order by a.gmv desc)rn
        from dwd.dwd_kslive_wares_copy a
        left join dim.dim_kuaishou_category_std b on a.product_id = b.product_id and a.good_type = b.good_type
        left join
          (
            select category1_id_std
                  ,category1_std
                  ,category2_id_std
                  ,category2_std
                  ,category3_id_std
                  ,category3_std
                  ,primary_mkt_industry1_id
                  ,primary_mkt_industry1
                  ,primary_mkt_industry2_id
                  ,primary_mkt_industry2
                  ,primary_mkt_industry3_id
                  ,primary_mkt_industry3
                  ,secondary_mkt_industry1_id
                  ,secondary_mkt_industry1
                  ,secondary_mkt_industry2_id
                  ,secondary_mkt_industry2
                  ,row_number() over(partition by category2_std order by category2_std desc) rn
              from dim.dim_investrch_standard_category
          )c
          on b.category2_std = c.category2_std
            and c.rn = 1
        left join
          (
            select product_id
                  ,product_name
                  ,good_type
                  ,category1_id
                  ,category1
                  ,brand_id_std
                  ,brand_name_std
                  ,category1_id_std
                  ,category1_std
                  ,match_type
                  ,dt
                  ,row_number() over(partition by product_id,good_type order by dt desc)rn
              from dim.dim_kuaishou_brand_std_wy
              where dt = '2021-01-13'
          )jiangtao
          on a.product_id = jiangtao.product_id
            and a.good_type = jiangtao.good_type
            and jiangtao.rn = 1
        left join dim.dim_retailers_online_standard_brand brand
          on jiangtao.brand_id_std = brand.brand_id_std
        where a.dt >= '2020-11-01' and a.dt <= '2021-01-12'
          and jiangtao.product_id is not null
    )a
  where rn = 1"