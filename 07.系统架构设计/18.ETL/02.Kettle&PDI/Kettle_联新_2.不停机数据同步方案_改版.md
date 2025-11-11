# 其它方向尝试

1. 患者数据加载到内存中去
2. 遍历所有医嘱数据

```sql
select * from pat_inhos_order order by inhos_code, seq_id limit 10

-- 测试
-- 不存在(在院) 326592 
-- 出院 11766448
select * from ((select * from pat_inhos_order where inhos_code = '326592' order by inhos_code, seq_id limit 10) union  
(select * from pat_inhos_order where inhos_code = '11766448' order by inhos_code, seq_id limit 10)) as a;
```

```sql
select inhos_code as pat_inhos_code, status as pat_status, out_date as pat_out_date  
from pat_inhos_record order by inhos_code, seq_id limit 10

-- 测试
select inhos_code as pat_inhos_code, status as pat_status, out_date as pat_out_date  
from pat_inhos_record where inhos_code in ('326592','11766448') order by inhos_code, seq_id limit 10
```


```sql
select pio.*, pir.status as pat_status, pir.out_date as pat_out_date from pat_inhos_order pio
left join pat_inhos_record pir on pio.inhos_code = pir.inhos_code
where pio.inhos_code in ('326592','11766448')
order by pio.seq_id
```

---
医嘱批次

```sql
select * from pat_inhos_order_group where seq_id >= ${TAST_MIN_SEQ_ID} and seq_id <= ${TAST_MAX_SEQ_ID} order by seq_id
```

```sql
-- 测试
-- 不存在(在院) 326592 
-- 出院 11766448
select * from ((select * from pat_inhos_order_group where inhos_code = '326592' seq_id limit 10) union  
(select * from pat_inhos_order_group where inhos_code = '11766448' seq_id limit 10)) as a;

-- 出院 11766448
select * from pat_inhos_order_group where inhos_code = '11766448' order by  seq_id limit 10
select * from pat_inhos_order_group where inhos_code = '326592' order by  seq_id limit 10
```

# 原始基础方向优化


```sql
-- 优化前
select piog.seq_id, piog.group_unique_code, piog.order_group_no, piog.inhos_code, piog.orderbar, piog.package_bar, piog.plan_time, piog.order_sort_no, piog.source_type, piog.isprint, piog.execute_status, piog.execute_date, piog.print_date, piog.execute_person, piog.print_person, piog.apply_time, piog.is_dispensed, piog.remark, piog.reason, piog.execute_type, piog.start_execute_user, piog.start_execute_date, piog.start_check_user, piog.end_execute_user, piog.end_execute_date, piog.create_time, piog.create_person, piog.update_time, piog.update_person, pir.out_date, unix_timestamp(ifnull(piog.update_time, piog.create_time)) * 1000 latest_time from pat_inhos_order_group piog left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code where pir.inhos_code is not null and pir.status = 0 and pir.out_date is not null and date_format(pir.out_date, '%Y%m') = '202203' order by seq_id limit 100


-- 优化后
select piog.seq_id, piog.group_unique_code, piog.order_group_no, piog.inhos_code, piog.orderbar, piog.package_bar, piog.plan_time, piog.order_sort_no, piog.source_type, piog.isprint, piog.execute_status, piog.execute_date, piog.print_date, piog.execute_person, piog.print_person, piog.apply_time, piog.is_dispensed, piog.remark, piog.reason, piog.execute_type, piog.start_execute_user, piog.start_execute_date, piog.start_check_user, piog.end_execute_user, piog.end_execute_date, piog.create_time, piog.create_person, piog.update_time, piog.update_person,  
pir.out_date,  
unix_timestamp(ifnull(piog.update_time, piog.create_time)) * 1000 latest_time  
 from pat_inhos_order_group piog  
 left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code  
 where  pir.inhos_code is not null and  pir.out_date >= '2022-03-01' and pir.out_date < '2022-04-01' and  pir.status = 0 order by seq_id limit 100
```


## v2改动

1.新增索引

```sql
create index idx_update_time on pat_inhos_order_group (update_time);
```

2.洗数据

```sql
update pat_inhos_order set update_time = create_time where update_time is null;
update pat_inhos_order_group set update_time = create_time where update_time is null;
```

3.程序改动

新增医嘱和医嘱批次时，设置update_time=create_time。


## v2前后比对

10 

