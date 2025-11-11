# 需求背景

有个数据库表数据被改变了，想追踪改变该数据的SQL日志和对应的客户端IP。

# 方案1 - General Log


可以利用MySQL的General Log日志。客户端对于数据库的连接、断开连接、执行SQL的操作日志都会写入该日志。

## 开启日志


默认是关闭的，如何查看和开启呢？

<font color="#f79646">第一种方式：永久生效</font>

修改my.cnf配置文件，修改后重启MySQL服务即可生效。

```
[mysqld]
general_log=1 # 1.开启 0.关闭
```


<font color="#f79646">第二种方式：不重启的方式，当服务重启后失效！</font>

```
mysql> show global variables like '%general%';  
+------------------+------------------------------+
| Variable_name    | Value                        |
+------------------+------------------------------+
| general_log      | OFF                          |
| general_log_file | /var/lib/mysql/localhost.log | -- 日志写入文件
+------------------+------------------------------+

mysql> set global general_log = true;  -- 开启
mysql> set global general_log = false; -- 关闭
```

这种方式是全局生效的，那么怎么仅关闭当前Session的日志记录呢？在当前Session中执行如下SQL：

```
mysql> set SQL_LOG_OFF=ON
```

开启后，当前Session的后续操作不会被记录到日志文件中。

## 检索日志

获取到日志文件，使用关键字进行搜索，定位到具体的操作后，可以看到有个SessionId=52545。

```log
		52545 Query	SELECT a.*,b.* FROM pat_inhos_order_group_out_202307 a
    INNER JOIN pat_inhos_order_out_202307 b ON a.inhos_code=b.inhos_code AND a.order_group_no =
    b.order_group_no
     WHERE  b.order_status != 4
        AND b.ordering_dept='3082'
        and a.plan_time >= '2024-03-28 00:00:00.0'
        and a.plan_time < '2024-03-29 00:00:00.0' 
    ORDER BY a.plan_time ASC
		52545 Query	SELECT a.*,b.* FROM pat_inhos_order_group_out_202308 a
    INNER JOIN pat_inhos_order_out_202308 b ON a.inhos_code=b.inhos_code AND a.order_group_no =
    b.order_group_no
     WHERE  b.order_status != 4
        AND b.ordering_dept='3082'
        and a.plan_time >= '2024-03-28 00:00:00.0'
        and a.plan_time < '2024-03-29 00:00:00.0' 
    ORDER BY a.plan_time ASC
```

## 确定目标

查询Session连接信息，然后根据根据SessionId确定最终的客户端IP和端口。

```SQL
mysql> show processlist; -- 只列出前100条，如果想全列出请使用 show full processlist;
+-------+------+-------------------+-----------------------+---------+-------+-------+------------------+
| Id    | User | Host              | db                    | Command | Time  | State | Info             |
+-------+------+-------------------+-----------------------+---------+-------+-------+------------------+
| 46185 | user | 10.2.15.32:60490  | windranger_foundation | Sleep   |  4196 |       | NULL             |
| 46595 | user | 10.2.15.53:64752  | windranger_emr        | Sleep   | 26894 |       | NULL             |
| 47182 | user | 10.2.15.19:53542  | windranger_hospital   | Sleep   | 28527 |       | NULL             |
| 47183 | user | 10.2.15.19:53546  | windranger_qm         | Sleep   | 28527 |       | NULL             |
| 47184 | user | 10.2.15.19:53545  | windranger_foundation | Sleep   | 28527 |       | NULL             |
| 47185 | user | 10.2.15.19:53562  | NULL                  | Sleep   | 28530 |       | NULL             |
| 47186 | user | 10.2.15.19:53567  | NULL                  | Sleep   | 28529 |       | NULL             |
| 47193 | user | 10.2.15.19:53591  | NULL                  | Sleep   | 28526 |       | NULL             |
| 48609 | user | 10.2.15.102:51302 | windranger_mnis       | Sleep   |  3562 |       | NULL             |
| 48610 | user | 10.2.15.102:51303 | NULL                  | Sleep   | 21197 |       | NULL             |
| 50719 | user | 10.2.3.170:52540  | windranger_iwip       | Sleep   |   154 |       | NULL             |
| 52140 | user | 10.2.3.170:49442  | windranger_iwip       | Sleep   |    34 |       | NULL             |
| 52196 | user | 10.2.3.170:49698  | windranger_emr        | Sleep   |    91 |       | NULL             |
| 52200 | user | 10.2.43.39:64613  | windranger_mnis       | Sleep   |  1130 |       | NULL             |
....
```


参考资料
* [MySQL中的GeneralLog日志](https://cloud.tencent.com/developer/article/1405092)
