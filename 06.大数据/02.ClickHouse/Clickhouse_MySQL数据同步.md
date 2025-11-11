# 实现方案

https://blog.csdn.net/lixia0417mul2/article/details/134797376

## 使用Cannal&Kafka


## 使用MaterializedMySQL引擎

* https://blog.csdn.net/u011197085/article/details/135227736

```SQL
-- 整库同步
CREATE DATABASE IF NOT EXISTS windranger_emr_200_01 ENGINE = 
MaterializedMySQL('10.2.3.200:3306', 'windranger_emr', 'user', 'Lachesis-mh_1024');

-- 部分表同步
CREATE DATABASE IF NOT EXISTS windranger_emr_200_01 ENGINE = 
MaterializedMySQL('10.2.3.200:3306', 'windranger_emr', 'user', 'Lachesis-mh_1024')  
SETTINGS materialized_mysql_tables_list = 'pat_inhos_order_group_bak202403,pat_inhos_order_bak202403';
```

