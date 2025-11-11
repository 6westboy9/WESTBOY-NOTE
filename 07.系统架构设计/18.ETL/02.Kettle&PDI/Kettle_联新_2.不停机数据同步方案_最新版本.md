
# 准备


## 硬件要求


>[!danger] 因为迁移期间，数据为双份存储，务必保证双倍存储空间！

## 备份表（存疑）

```
-rwxr-xr-x. 1 root root         964 Feb 12 18:16 backup_table.sh
```

## 准备表结构

```
-rwxr-xr-x. 1 root root         944 Feb 12 19:48 create_in_table.sh
-rwxr-xr-x. 1 root root        1951 Feb 14 11:23 create_out_table.sh
```


```sh
# 生成在院表
./create_in_table.sh pat_inhos_order
./create_in_table.sh pat_inhos_order_group

# 生成出院表
./create_out_table.sh pat_inhos_order
./create_out_table.sh pat_inhos_order_group
```


## 安装-ShardingProxy

## 执行创建表


## update_time is not null

主要是方便后续根据`update_time`查询时可以命中索引。
### 脚本

```sql
-- 数据量：33112780 耗时：13min
update pat_inhos_order set update_time = create_time where update_time is null;
-- 数据量：60421583 耗时：
update pat_inhos_order_group set update_time = create_time where update_time is null;

select count(*) all_cnt from pat_inhos_order where update_time is null;               -- 0 (验证执行成功)
select count(*) all_cnt from pat_inhos_order_group where update_time is null;         -- 0 (验证执行成功)
```

2.洗数据

```sql
drop index idx_update_time on pat_inhos_order;
create index idx_update_time on pat_inhos_order (update_time);
--  数据量：33112780 耗时：
drop index idx_update_time on pat_inhos_order_group;
create index idx_update_time on pat_inhos_order_group (update_time);
```

### 同步程序

同步步程序在新增记录时，必须给`update_time`赋值，默认等于`create_time`。

### 医嘱表不存在关联患者的数据

<font color="#c0504d">默认进入xxx_in表。</font>

## 表数据分布

### 按照患者出院的医嘱数据分布

|                       | 表数据      | 在院      | 出院       |
| --------------------- | -------- | ------- | -------- |
| pat_inhos_order       | 33112780 | 563767  | 32549013 |
| pat_inhos_order_group | 60421583 | 1091685 | 59329898 |

# 数据迁移


## 配置


```yaml
server:
  port: 8888
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://10.2.3.160:3306/windranger_emr?characterEncoding=utf8&serverTimezone=GMT%2B8&allowMultiQueries=true
    username: user
    password: Lachesis-mh_1024
    hikari:
      maximum-pool-size: 200
  sql:
    init:
      schema-locations: classpath*:db/schema.sql
      mode: always
      platform: mysql
logging:
  config: classpath:logs/logback-spring.xml

transfer:
  global:
    # 边界值
    update-time: '2025-02-18 00:00:00'
    # 是否需要重新初始化任务
    reset: false
  jobs:
    - table-name: pat_inhos_order
      # 是否开启作业
      enable: true
      # 单个作业拆分任务数量
      task-num: 50
      # 需要处理的最小业务序号，一般多用于测试使用（闭区间[1,task-num]，但是必须小于等于task-max-sequence）
      task-min-sequence: 1
      # 需要处理的最大业务序号，一般多用于测试使用（闭区间[1,task-num]，但是必须大于等于于task-min-sequence）
      task-max-sequence: 50
      # 单个作业任务并发处理器
      task-handler-num: 5
      # 子任务数量=10×10=100
      task-sub-handler-num: 20
      # 任务批量查询数量限制
      task-sub-handler-query-limit: 2000
    - table-name: pat_inhos_order_group
      # 是否开启作业
      enable: true
      # 单个作业拆分任务数量
      task-num: 50
      # 需要处理的最小业务序号，一般多用于测试使用（闭区间[1,task-num]，但是必须小于等于task-max-sequence）
      task-min-sequence: 1
      # 需要处理的最大业务序号，一般多用于测试使用（闭区间[1,task-num]，但是必须大于等于于task-min-sequence）
      task-max-sequence: 50
      # 单个作业任务并发处理器
      task-handler-num: 5
      # 子任务数量=10×10=100
      task-sub-handler-num: 20
      # 任务批量查询数量限制
      task-sub-handler-query-limit: 2000
```


## 执行


```
cd /usr/local/springboot/transfer
./transfer start
```


## 监控



## 数据校验


