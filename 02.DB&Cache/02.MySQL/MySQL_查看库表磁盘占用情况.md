
# 查询所有数据库占用磁盘空间大小

```sql
select a.table_schema as '数据库',  
       a.data_size as '数据容量(MB)',  
       a.index_size as '索引容量(MB)' from (  
select table_schema,  
sum(data_length) as sum_data_length,  
concat(truncate(sum(data_length)/1024/1024,2),'MB') as data_size,  
concat(truncate(sum(index_length)/1024/1024,2),'MB') as index_size  
from information_schema.tables  
group by table_schema) as a  
order by a.sum_data_length desc;
```

| 数据库                    | 数据容量\(MB\) | 索引容量\(MB\) |
| :--------------------- | :--------- | :--------- |
| windranger\_emr        | 27813.21MB | 46102.23MB |
| windranger\_mnis       | 26688.18MB | 45806.79MB |
| windranger\_sync       | 381.48MB   | 24.68MB    |
| windranger\_qm         | 198.04MB   | 45.89MB    |
| windranger\_foundation | 41.21MB    | 6.64MB     |
| windranger\_hospital   | 25.34MB    | 4.93MB     |
| mysql                  | 6.42MB     | 0.12MB     |

# 查看指定库所有表占用磁盘空间大小

```sql
select  
table_schema as '数据库',  
table_name as '表名',  
table_rows as '记录数',  
truncate(data_length/1024/1024, 2) as '数据容量(MB)',  
truncate(index_length/1024/1024, 2) as '索引容量(MB)'  
from information_schema.tables  
where table_schema='windranger_emr'  
order by data_length desc, index_length desc;
```

| 数据库             | 表名                                    | 记录数      | 数据容量\(MB\) | 索引容量\(MB\) |
| :-------------- | :------------------------------------ | :------- | :--------- | :--------- |
| windranger\_emr | pat\_inhos\_order\_group              | 32003800 | 4896.00    | 12149.98   |
| windranger\_emr | pat\_inhos\_order                     | 20141525 | 4744.00    | 9693.73    |
| windranger\_emr | pat\_inhos\_order\_group\_in          | 3856907  | 881.00     | 1485.18    |
| windranger\_emr | pat\_nurse\_plan\_item                | 1908998  | 629.00     | 222.00     |
| windranger\_emr | pat\_inhos\_order\_group\_out\_202312 | 2526179  | 573.00     | 939.39     |
| windranger\_emr | pat\_inhos\_order\_group\_out\_202308 | 2349359  | 471.00     | 785.18     |
| windranger\_emr | pat\_inhos\_order\_group\_out\_202304 | 2048295  | 464.00     | 765.17     |
| windranger\_emr | pat\_inhos\_order\_group\_out\_202306 | 2019941  | 464.00     | 763.15     |
| windranger\_emr | pat\_inhos\_order\_group\_out\_202310 | 2124479  | 461.00     | 764.17     |
| windranger\_emr | pat\_inhos\_order\_group\_out\_202311 | 2159475  | 459.00     | 763.18     |

