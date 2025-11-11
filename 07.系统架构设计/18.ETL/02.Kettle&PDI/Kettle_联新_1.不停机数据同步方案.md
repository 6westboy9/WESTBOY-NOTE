# 1.背景

要求：

* 不停机（具体来说只是短暂停机，目前给定时间范围要求是30分钟以内）
* 数据同步稳定
* 数据一致性

目标：

1. 数据无差异
2. 用户无感知
3. 异常可监控
4. 方案可回滚

# 2.说明

>基于Kettle/PDI程序

![[Pasted image 20240409115225.png|900]]

说明：

1. 表结构准备
	- 对于in表是与原始表结构一模一样的 -- <font color="#c0504d">自增长属性和自增长值</font>
		- 数据迁移完成前，先不设置<font color="#c0504d">自增长属性和自增长值 & 索引</font> <font color="#4f81bd">-- 校验数据后再设置</font>
	- 对于out表需要注意3点：<font color="#4f81bd">-- 见示例1</font>
		- <font color="#c0504d">删除自增长属性和删除自增长值</font>
		- <font color="#c0504d">新增出院时间字段</font>
		- 数据迁移完成前，先不设置<font color="#c0504d">索引</font> <font color="#4f81bd">-- 校验数据后再设置</font>
	- ? 创建表时带索引和不带索引性能测试
2. 基于PDI完成数据迁移 <font color="#4f81bd">-- 详细内容见下文</font>
	- 存量数据同步
	- 增量数据同步
3. 基于PDI完成数据校验 <font color="#4f81bd">-- 详细内容见下文</font>

>示例1.xxx_out表结构改造点

```sql
CREATE TABLE `pat_inhos_order` (  
  `seq_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增长流水号',                     # 1.删除AUTO_INCREMENT属性
  ...
  `NURSE_CODE` int(11) DEFAULT NULL,  
  `STOP_NURSE_CODE` int(11) DEFAULT NULL,
  `out_date` datetime DEFAULT NULL COMMENT '出院日期',                                            # 2.新增出院时间字段                                      
  PRIMARY KEY (`seq_id`),  
  UNIQUE KEY `uq_pat_inhos_order_1` (`order_code`),  
  KEY `idx_pat_inhos_order_2` (`pat_code`),  
  KEY `idx_pat_inhos_order_4` (`ordering_dept`,`enter_date_time`),  
  KEY `idx_pat_inhos_order_5` (`start_date_time`),  
  KEY `idx_pat_inhos_order_6` (`stop_date_time`),  
  KEY `enter_date_time` (`enter_date_time`),  
  KEY `create_time_idx` (`create_time`) USING BTREE,  
  KEY `idx_pat_inhos_order_7` (`ordering_dept`,`inhos_code`),  
  KEY `idx_pat_inhos_order_3` (`order_group_no`,`inhos_code`),  
  KEY `idx_pat_inhos_order_8` (`inhos_code`)  
) ENGINE=InnoDB AUTO_INCREMENT=73449252 DEFAULT CHARSET=utf8 COMMENT='病历模块-住院医嘱表'          # 3.删除AUTO_INCREMENT=73449252
```

# 3.作业概述

* 作业-1.1.数据同步作业-医嘱表
* 作业-1.2.数据校验作业-医嘱表
* 作业-2.1.数据同步作业-医嘱批次表
* 作业-2.2.数据校验作业-医嘱批次表

![[Pasted image 20240409114528.png|900]]

>已经归位一个作业了~

# 4.变量定义

kettle.properties下

| LACHESIS_JOB_CONFIG_PATH | D:\Document\Pentaho\lx_pentaho_repository\lacheis.properties |
| ------------------------ | ------------------------------------------------------------ |

| 序号  | 参数名                                      | 默认值                            | 说明                                                                                         | 示例                                                                           |     |
| --- | ---------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- | --- |
| 1   | LACHESIS_JOB_IS_INIT                     | false                          | 是否删除重建表：true.是；false.否                                                                     |                                                                              |     |
| 2   | LACHESIS_JOB_MIN_TIME                    | 空字符串                           | 设置同步数据update_time/create_time的最小边界（<font color="#f79646">前闭</font>，格式：yyyy-MM-dd HH:mm:ss） | 2021-01-01 00:00:00，更新时间<font color="#f79646">大于等于</font>2021-01-01 00:00:00 |     |
| 3   | LACHESIS_JOB_MAX_TIME                    | 空字符串                           | 设置同步数据update_time/create_time的最大边界（<font color="#f79646">后闭</font>，格式：yyyy-MM-dd HH:mm:ss） | 2022-01-01 00:00:00，更新时间<font color="#f79646">小于等于</font>2021-01-01 00:00:00 |     |
| 4   | LACHESIS_JOB_SOURCE_TABLE_NAME           |                                | 原始表名称                                                                                      | pat_inhos_order                                                              |     |
| 5   | LACHESIS_JOB_SOURCE_OUT_MIN_MONTH        | min(pat_inhos_record.out_date) | min(pat_inhos_record.out_date)，出院表最小分片（<font color="#f79646">前闭</font>，格式：yyyyMM）          | 202201                                                                       |     |
| 6   | LACHESIS_JOB_SOURCE_OUT_MAX_MONTH        | max(pat_inhos_record.out_date) | max(pat_inhos_record.out_date)，出院表最大分片（<font color="#f79646">后闭</font>，格式：yyyyMM）          | 202304                                                                       |     |
| 7   | LACHESIS_JOB_TARGET_IN_TABLE_NAME        |                                | 目标<font color="#f79646">在院</font>表名称                                                       | pat_inhos_order_inv2                                                         |     |
| 8   | LACHESIS_JOB_SOURCE_IN_CREATE_TABLE_SQL  |                                | 创建在院表结构DDL语句，<font color="#f79646">需要校对一次，防止新增或者表结构改变</font>                               |                                                                              |     |
| 9   | LACHESIS_JOB_TARGET_OUT_TABLE_PREFIX     |                                | 目标<font color="#f79646">出院</font>表名称前缀                                                     | pat_inhos_order_outv2\_，比如最终生成的表名：pat_inhos_order_outv2_202303               |     |
| 10  | LACHESIS_JOB_SOURCE_OUT_CREATE_TABLE_SQL |                                | 创建出院表结构DDL语句，<font color="#f79646">需要校对一次，防止新增或者表结构改变</font>                               |                                                                              |     |
| 11  | LACHESIS_JOB_TARGET_SYNC_IS_TEST_SINGLE  | false                          | 一般仅限调试时使用                                                                                  | false                                                                        |     |
| 12  | LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL       | 空字符串                           | 一般仅限调试时使用，减少同步数据量                                                                          | 比如调试时，只需要同步10条数据，可设置为limit 10                                                |     |
| 13  | LACHESIS_JOB_TARGET_SYNC_THREAD_NUM      |                                | 同步数据库增删改操作线上数                                                                              | 100                                                                          |     |

# 5.迁移阶段

>这里拿医嘱同步作业举例说明

![[Pasted image 20240409113639.png|1200]]

* 运行阶段一
	* 开启数据同步定时任务
		* 抽取数据时间取值规则
			* 抽取数据时间范围-开始时间：参数LACHESIS_JOB_MIN_TIME配置时间 > 上次抽取数据时间范围-结束时间 > 取患者表出院最小时间
			* 抽取数据时间范围-结束时间：参数LACHESIS_JOB_MAX_TIME配置时间 > 取当前时间
	* 当同步数据较少时，关闭同步定时任务，手动触发一次<font color="#c0504d">存量数据校验</font>，在此过程中，因为程序在运行，可能会存在不一致的数据
* 停机阶段一
	* 手动触发一次数据同步任务，此操作目的是同步<font color="#c0504d">运行阶段一中数据校验过程</font>中产生的<font color="#c0504d">增量数据</font>
	* 手动触发一次<font color="#c0504d">存量数据校验</font>，正常情况下，不会存在不一致的数据。不正常情况下呢？
		* 先启动程序，保证业务正常运行
		* 不一致的数据，会记录到日志中，排查问题原因
	* 数据校验完成后，修改EMR程序配置为双链路但返回旧链路：<font color="#c0504d">ALL_RETURN_OLD</font>
* 运行阶段二
	* 因为没有做灰度功能，所以一定要验证双链路操作的情况下，需要保证（按优先级从上至下）：
		* 同步程序和EMR在双链路时，<font color="#c0504d">保证旧链路没有任何问题</font>，支持修改配置走旧链路（可回滚）
		* 同步程序和EMR在双链路<font color="#c0504d">写操作</font>数据一致（即至少保证增删改没有任何问题）
		* 性能稳定
	* 关注点
		* 业务功能正常
		* 查看监控记录，是否存在双链路操作不一致的情况？是否存在操作异常信息？是否存在操作性能问题？
	* <font color="#4bacc6">定心丸</font>
		* 全覆盖测试：EMR和同步程序涉及所有改动Mapper接口进行全覆盖测试
		* 性能测试：EMR和同步程序涉及所有改动Mapper接口进行性能测试
* 停机阶段二
	* 观察稳定运行一段时间后，修改EMR程序配置为双链路但返回新链路：<font color="#c0504d">NEW</font>
* 运行阶段三

```ad-important
这里我们重点关注运行阶段一和停机阶段二！
```

# 6.实现方案
## 1.总体流程

![[Pasted image 20240422180914.png|1600]]

## 2.目标单表流程

![[Pasted image 20240422181348.png|1200]]

### 1.出院操作-医嘱批次

![[Pasted image 20240422181633.png|1200]]


### 2.出院操作-医嘱

![[Pasted image 20240422181551.png|1200]]

### 3.在院操作-医嘱批次

![[Pasted image 20240422181710.png|1200]]

### 4.在院操作-医嘱

![[Pasted image 20240422181519.png|1200]]

# 7.注意事项

## 配置

* 默认KETTLE_EMPTY_STRING_DIFFERS_FROM_NULL为N，从数据库查询字符串和null均视为null，需要设置为Y。
	* 不然在同步过程中，数据库设置的为not null，但是对于空串数据旧无法插入。
	* 注意全局变量修改后，需要重启程序。

## 依赖

* 添加MySQL依赖驱动包
* 添加Java脚本依赖包

* 目标路径：`pdi-ce-9.4.0.0-343/data-integration/lib`

在测试环境下遇到同步报错：`Timestamp : Unable to get timestamp from resultset at index 21...`，详细报错如下，具体解决方案使用MySQL驱动版本至8.0.23以上。

```
org.pentaho.di.core.exception.KettleDatabaseException: 
Couldn't get row from result set

Timestamp : Unable to get timestamp from resultset at index 21
HOUR_OF_DAY: 2 -> 3


	at org.pentaho.di.core.database.Database.getRow(Database.java:2753)
	at org.pentaho.di.core.database.Database.getRow(Database.java:2723)
	at org.pentaho.di.core.database.Database.getRow(Database.java:2701)
	at org.pentaho.di.trans.steps.tableinput.TableInput.doQuery(TableInput.java:265)
	at org.pentaho.di.trans.steps.tableinput.TableInput.processRow(TableInput.java:143)
	at org.pentaho.di.trans.step.RunThread.run(RunThread.java:62)
	at java.lang.Thread.run(Thread.java:748)
Caused by: org.pentaho.di.core.exception.KettleDatabaseException: 
Timestamp : Unable to get timestamp from resultset at index 21
HOUR_OF_DAY: 2 -> 3

	at org.pentaho.di.core.row.value.ValueMetaTimestamp.getValueFromResultSet(ValueMetaTimestamp.java:524)
	at org.pentaho.di.core.database.BaseDatabaseMeta.getValueFromResultSet(BaseDatabaseMeta.java:2138)
	at org.pentaho.di.core.database.DatabaseMeta.getValueFromResultSet(DatabaseMeta.java:3030)
	at org.pentaho.di.core.database.Database.getRow(Database.java:2745)
	... 6 more
Caused by: java.sql.SQLException: HOUR_OF_DAY: 2 -> 3
	at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:129)
	at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:97)
	at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:89)
	at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:63)
	at com.mysql.cj.jdbc.exceptions.SQLError.createSQLException(SQLError.java:73)
	at com.mysql.cj.jdbc.exceptions.SQLExceptionsMapping.translateException(SQLExceptionsMapping.java:85)
	at com.mysql.cj.jdbc.result.ResultSetImpl.getTimestamp(ResultSetImpl.java:1019)
	at org.pentaho.di.core.row.value.ValueMetaTimestamp.getValueFromResultSet(ValueMetaTimestamp.java:520)
	... 9 more
Caused by: com.mysql.cj.exceptions.WrongArgumentException: HOUR_OF_DAY: 2 -> 3
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method)
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62)
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423)
	at com.mysql.cj.exceptions.ExceptionFactory.createException(ExceptionFactory.java:61)
	at com.mysql.cj.exceptions.ExceptionFactory.createException(ExceptionFactory.java:105)
	at com.mysql.cj.result.SqlTimestampValueFactory.createFromTimestamp(SqlTimestampValueFactory.java:104)
	at com.mysql.cj.result.SqlTimestampValueFactory.createFromTimestamp(SqlTimestampValueFactory.java:46)
	at com.mysql.cj.result.ZeroDateTimeToNullValueFactory.createFromTimestamp(ZeroDateTimeToNullValueFactory.java:64)
	at com.mysql.cj.result.BaseDecoratingValueFactory.createFromTimestamp(BaseDecoratingValueFactory.java:61)
	at com.mysql.cj.result.BaseDecoratingValueFactory.createFromTimestamp(BaseDecoratingValueFactory.java:61)
	at com.mysql.cj.protocol.a.MysqlTextValueDecoder.decodeTimestamp(MysqlTextValueDecoder.java:183)
	at com.mysql.cj.protocol.result.AbstractResultsetRow.decodeAndCreateReturnValue(AbstractResultsetRow.java:87)
	at com.mysql.cj.protocol.result.AbstractResultsetRow.getValueFromBytes(AbstractResultsetRow.java:250)
	at com.mysql.cj.protocol.a.result.TextBufferRow.getValue(TextBufferRow.java:132)
	at com.mysql.cj.jdbc.result.ResultSetImpl.getNonStringValueFromRow(ResultSetImpl.java:656)
	at com.mysql.cj.jdbc.result.ResultSetImpl.getDateOrTimestampValueFromRow(ResultSetImpl.java:679)
	... 11 more
Caused by: java.lang.IllegalArgumentException: HOUR_OF_DAY: 2 -> 3
	at java.util.GregorianCalendar.computeTime(GregorianCalendar.java:2829)
	at java.util.Calendar.updateTime(Calendar.java:3393)
	at java.util.Calendar.getTimeInMillis(Calendar.java:1782)
	at com.mysql.cj.result.SqlTimestampValueFactory.createFromTimestamp(SqlTimestampValueFactory.java:100)
	... 21 more
```

# 8.性能测试

## 医嘱

### 场景信息

PDI程序配置

| <font color="#4f81bd">EMR_R数据库选项</font> | <font color="#4f81bd">EMR_W数据库选项</font> | <font color="#4f81bd">EMR_W数据库连接池</font> | <font color="#4f81bd">PDI程序JVM参数配置</font> | <font color="#9bbb59">场景</font> | <font color="#9bbb59">读并发</font> | <font color="#9bbb59">写并发</font> |
| --------------------------------------- | --------------------------------------- | ---------------------------------------- | ----------------------------------------- | ------------------------------- | -------------------------------- | -------------------------------- |
| useCursorFetch=true                     | useCursorFetch=true                     | initialSize=100                          | -Xms1024m -Xmx2048m                       | 存量出院数据同步                        | 1                                | 100/插入更新方式                       |
| defaultFetchSize=500                    | defaultFetchSize=500                    | maxActive=100                            |                                           |                                 |                                  |                                  |
存量在院统计

```sql
-- 医嘱表总数：20291151
-- 患者表总数：148752
-- 有效存量在院医嘱总数：637455 consume=4min+
select count(*)  
 from pat_inhos_order pioa  
 left join pat_inhos_record pir on pioa.inhos_code = pir.inhos_code  
 where pir.inhos_code is null or pir.status != 0 or pir.out_date is null;
```

存量出院统计

```sql
-- 医嘱表总数：20291151
-- 患者表总数：148752
-- 有效存量出院医嘱总数：19653696 consume=4min+
select count(*)  
 from pat_inhos_order pioa  
 left join pat_inhos_record pir on pioa.inhos_code = pir.inhos_code  
 where pir.inhos_code is not null and pir.status = 0 and pir.out_date is not null;
```

月度分布情况

```sql
-- consume=
select a.out_date_month, concat('pat_inhos_order_outv2_', a.out_date_month) create_table_name, a.cnt  
from (select distinct date_format(out_date, '%Y%m') as out_date_month, count(*) as cnt  
      from pat_inhos_order pioa left join pat_inhos_record pir on pioa.inhos_code = pir.inhos_code  
      where pir.inhos_code is not null and pir.status = 0 and pir.out_date is not null group by date_format(out_date, '%Y%m')) as a order by out_date_month;
```

统计同步情况

```sql
-- consume=36min+
select 'out_202203' month, count(*) cnt from pat_inhos_order_out_202203 union all  
select 'out_202204' month, count(*) cnt from pat_inhos_order_out_202204 union all  
select 'out_202205' month, count(*) cnt from pat_inhos_order_out_202205 union all  
select 'out_202206' month, count(*) cnt from pat_inhos_order_out_202206 union all  
select 'out_202207' month, count(*) cnt from pat_inhos_order_out_202207 union all  
select 'out_202208' month, count(*) cnt from pat_inhos_order_out_202208 union all  
select 'out_202209' month, count(*) cnt from pat_inhos_order_out_202209 union all  
select 'out_202210' month, count(*) cnt from pat_inhos_order_out_202210 union all  
select 'out_202211' month, count(*) cnt from pat_inhos_order_out_202211 union all  
select 'out_202212' month, count(*) cnt from pat_inhos_order_out_202212 union all  
select 'out_202301' month, count(*) cnt from pat_inhos_order_out_202301 union all  
select 'out_202302' month, count(*) cnt from pat_inhos_order_out_202302 union all  
select 'out_202303' month, count(*) cnt from pat_inhos_order_out_202303 union all  
select 'out_202304' month, count(*) cnt from pat_inhos_order_out_202304 union all  
select 'out_202305' month, count(*) cnt from pat_inhos_order_out_202305 union all  
select 'out_202306' month, count(*) cnt from pat_inhos_order_out_202306 union all  
select 'out_202307' month, count(*) cnt from pat_inhos_order_out_202307 union all  
select 'out_202308' month, count(*) cnt from pat_inhos_order_out_202308 union all  
select 'out_202309' month, count(*) cnt from pat_inhos_order_out_202309 union all  
select 'out_202310' month, count(*) cnt from pat_inhos_order_out_202310 union all  
select 'out_202311' month, count(*) cnt from pat_inhos_order_out_202311 union all  
select 'out_202312' month, count(*) cnt from pat_inhos_order_out_202312 union all  
select 'out_202401' month, count(*) cnt from pat_inhos_order_out_202401 union all  
select 'in' month, count(*) cnt from pat_inhos_order_in;
```

| id  | out_date_month | create_table_name          | cnt     | 同步后数量   |
| --- | -------------- | -------------------------- | ------- | ------- |
| 1   | 202203         | pat_inhos_order_out_202203 | 189964  | 189964  |
| 2   | 202204         | pat_inhos_order_out_202204 | 718022  | 718022  |
| 3   | 202205         | pat_inhos_order_out_202205 | 276835  | 276835  |
| 4   | 202206         | pat_inhos_order_out_202206 | 325436  | 325436  |
| 5   | 202207         | pat_inhos_order_out_202207 | 648357  | 648357  |
| 6   | 202208         | pat_inhos_order_out_202208 | 1061949 | 1061949 |
| 7   | 202209         | pat_inhos_order_out_202209 | 895981  | 895981  |
| 8   | 202210         | pat_inhos_order_out_202210 | 807723  | 807723  |
| 9   | 202211         | pat_inhos_order_out_202211 | 869205  | 869205  |
| 10  | 202212         | pat_inhos_order_out_202212 | 1079049 | 1079049 |
| 11  | 202301         | pat_inhos_order_out_202301 | 961398  | 961398  |
| 12  | 202302         | pat_inhos_order_out_202302 | 868919  | 868919  |
| 13  | 202303         | pat_inhos_order_out_202303 | 1058733 | 1058733 |
| 14  | 202304         | pat_inhos_order_out_202304 | 1015626 | 1015626 |
| 15  | 202305         | pat_inhos_order_out_202305 | 1026788 | 1026788 |
| 16  | 202306         | pat_inhos_order_out_202306 | 1028785 | 1028785 |
| 17  | 202307         | pat_inhos_order_out_202307 | 1032414 | 1032414 |
| 18  | 202308         | pat_inhos_order_out_202308 | 1040154 | 1040154 |
| 19  | 202309         | pat_inhos_order_out_202309 | 976910  | 976910  |
| 20  | 202310         | pat_inhos_order_out_202310 | 982496  | 982496  |
| 21  | 202311         | pat_inhos_order_out_202311 | 1054588 | 1054588 |
| 22  | 202312         | pat_inhos_order_out_202312 | 1220653 | 1220653 |
| 23  | 202401         | pat_inhos_order_out_202401 | 513711  | 513711  |
| 24  |                | pat_inhos_order_in         | 637455  | 637455  |

### 测试汇总

| 测试场景 | 读数据库                                                                                                       | 写数据库 | PDI程序JVM参数配置        | 读并发  | 写并发             | 耗时  | Linux'CPU | PDI'CPU | 内存增幅      | 监控详情                                                                                                                                                               |
| :--: | ---------------------------------------------------------------------------------------------------------- | ---- | ------------------- | ---- | --------------- | --- | --------- | ------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 存量同步 | 选项<br>1.useCursorFetch=true<br>2.defaultFetchSize=500<br><br>连接池配置<br>1.initialSize=100<br>2.maxActive=100 | 共用   | -Xms4096m -Xmx4096m | 1个线程 | 插入/更新/删除各100个线程 | 3h+ | 75%       | 50%     | PDI的JVM内存 | Linux http://10.2.43.101:3000/goto/sg9lzSBSR?orgId=1<br>MySQL http://10.2.43.101:3000/goto/urSkmSBSg?orgId=1<br>PDI http://10.2.43.101:3000/goto/yhammIfIg?orgId=1 |
| 存量校验 | 同上                                                                                                         | 同上   | -Xms4096m -Xmx4096m | 同上   | 同上              |     |           |         |           |                                                                                                                                                                    |


存量耗时统计

| id  | out_date_month | create_table_name          | cnt     | 同步后数量   | 同步耗时                                | 校验耗时                                |
| --- | -------------- | -------------------------- | ------- | ------- | ----------------------------------- | ----------------------------------- |
| 1   | 202203         | pat_inhos_order_out_202203 | 189964  | 189964  | 97862                               | 92291                               |
| 2   | 202204         | pat_inhos_order_out_202204 | 718022  | 718022  | 355121                              | 198162                              |
| 3   | 202205         | pat_inhos_order_out_202205 | 276835  | 276835  | 170046                              | 124231                              |
| 4   | 202206         | pat_inhos_order_out_202206 | 325436  | 325436  | 183425                              | 130452                              |
| 5   | 202207         | pat_inhos_order_out_202207 | 648357  | 648357  | 310252                              | 148076                              |
| 6   | 202208         | pat_inhos_order_out_202208 | 1061949 | 1061949 | <font color="#c0504d">213632</font> | <font color="#c0504d">542812</font> |
| 7   | 202209         | pat_inhos_order_out_202209 | 895981  | 895981  | 371875                              | 381748                              |
| 8   | 202210         | pat_inhos_order_out_202210 | 807723  | 807723  | 334786                              | 313628                              |
| 9   | 202211         | pat_inhos_order_out_202211 | 869205  | 869205  | 469248                              | 379214                              |
| 10  | 202212         | pat_inhos_order_out_202212 | 1079049 | 1079049 | 575676                              |                                     |
| 11  | 202301         | pat_inhos_order_out_202301 | 961398  | 961398  |                                     |                                     |
| 12  | 202302         | pat_inhos_order_out_202302 | 868919  | 868919  |                                     |                                     |
| 13  | 202303         | pat_inhos_order_out_202303 | 1058733 | 1058733 |                                     |                                     |
| 14  | 202304         | pat_inhos_order_out_202304 | 1015626 | 1015626 |                                     |                                     |
| 15  | 202305         | pat_inhos_order_out_202305 | 1026788 | 1026788 |                                     |                                     |
| 16  | 202306         | pat_inhos_order_out_202306 | 1028785 | 1028785 |                                     |                                     |
| 17  | 202307         | pat_inhos_order_out_202307 | 1032414 | 1032414 |                                     |                                     |
| 18  | 202308         | pat_inhos_order_out_202308 | 1040154 | 1040154 |                                     |                                     |
| 19  | 202309         | pat_inhos_order_out_202309 | 976910  | 976910  |                                     |                                     |
| 20  | 202310         | pat_inhos_order_out_202310 | 982496  | 982496  |                                     |                                     |
| 21  | 202311         | pat_inhos_order_out_202311 | 1054588 | 1054588 |                                     |                                     |
| 22  | 202312         | pat_inhos_order_out_202312 | 1220653 | 1220653 |                                     |                                     |
| 23  | 202401         | pat_inhos_order_out_202401 | 513711  | 513711  |                                     |                                     |
| 24  |                | pat_inhos_order_in         | 637455  | 637455  |                                     |                                     |


## 医嘱批次

### 场景信息

PDI程序配置

| <font color="#4f81bd">EMR_R数据库选项</font> | <font color="#4f81bd">EMR_W数据库选项</font> | <font color="#4f81bd">EMR_W数据库连接池</font> | <font color="#4f81bd">PDI程序JVM参数配置</font> | <font color="#9bbb59">场景</font> | <font color="#9bbb59">读并发</font> | <font color="#9bbb59">写并发</font> |
| --------------------------------------- | --------------------------------------- | ---------------------------------------- | ----------------------------------------- | ------------------------------- | -------------------------------- | -------------------------------- |
| useCursorFetch=true                     | useCursorFetch=true                     | initialSize=100                          | -Xms1024m -Xmx2048m                       | 存量出院数据同步                        | 1                                | 100/插入更新方式                       |
| defaultFetchSize=500                    | defaultFetchSize=500                    | maxActive=100                            |                                           |                                 |                                  |                                  |
存量在院统计

```sql
-- 医嘱批次表总数：37702578 consume=1min40s+
-- 患者表总数：148752
-- 有效存量在院医嘱批次总数：4012320 consume=8min+
select count(*)
 from pat_inhos_order_group piog
 left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code
 where pir.inhos_code is null or pir.status != 0 or pir.out_date is null;
```

存量出院统计

```sql
-- 医嘱批次表总数：37702578 consume=1min40s+
-- 患者表总数：148752
-- 有效存量出院医嘱批次总数：33690258 consume=8min+
select count(*)
 from pat_inhos_order_group piog
 left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code
 where pir.inhos_code is not null and pir.status = 0 and pir.out_date is not null;
```

月度分布情况

```sql
-- consume=7min+
select a.out_date_month, concat('pat_inhos_order_group_outv2_', a.out_date_month) create_table_name, a.cnt  
from (select distinct date_format(out_date, '%Y%m') as out_date_month, count(*) as cnt  
      from pat_inhos_order_group piog left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code  
      where pir.inhos_code is not null and pir.status = 0 and pir.out_date is not null group by date_format(out_date, '%Y%m')) as a order by out_date_month;
```

| id  | out_date_month | create_table_name                | cnt     |     |
| --- | -------------- | -------------------------------- | ------- | --- |
| 1   | 202202         | pat_inhos_order_group_out_202202 | 133284  |     |
| 2   | 202203         | pat_inhos_order_group_out_202203 | 456611  |     |
| 3   | 202204         | pat_inhos_order_group_out_202204 | 687201  |     |
| 4   | 202205         | pat_inhos_order_group_out_202205 | 339898  |     |
| 5   | 202206         | pat_inhos_order_group_out_202206 | 478702  |     |
| 6   | 202207         | pat_inhos_order_group_out_202207 | 842042  |     |
| 7   | 202208         | pat_inhos_order_group_out_202208 | 1161484 |     |
| 8   | 202209         | pat_inhos_order_group_out_202209 | 1016859 |     |
| 9   | 202210         | pat_inhos_order_group_out_202210 | 1038642 |     |
| 10  | 202211         | pat_inhos_order_group_out_202211 | 1186088 |     |
| 11  | 202212         | pat_inhos_order_group_out_202212 | 1587255 |     |
| 12  | 202301         | pat_inhos_order_group_out_202301 | 1448234 |     |
| 13  | 202302         | pat_inhos_order_group_out_202302 | 1277410 |     |
| 14  | 202303         | pat_inhos_order_group_out_202303 | 1671082 |     |
| 15  | 202304         | pat_inhos_order_group_out_202304 | 2015228 |     |
| 16  | 202305         | pat_inhos_order_group_out_202305 | 2033609 |     |
| 17  | 202306         | pat_inhos_order_group_out_202306 | 2080701 |     |
| 18  | 202307         | pat_inhos_order_group_out_202307 | 2038142 |     |
| 19  | 202308         | pat_inhos_order_group_out_202308 | 2249689 |     |
| 20  | 202309         | pat_inhos_order_group_out_202309 | 2115785 |     |
| 21  | 202310         | pat_inhos_order_group_out_202310 | 2169808 |     |
| 22  | 202311         | pat_inhos_order_group_out_202311 | 2145999 |     |
| 23  | 202312         | pat_inhos_order_group_out_202312 | 2525776 |     |
| 24  | 202401         | pat_inhos_order_group_out_202401 | 990729  |     |
| 24  |                | pat_inhos_order_group_in         | 1972883 |     |

### 测试汇总

| 版本  | 作业版本 | 测试场景 | 读数据库                                                                                                       | 写数据库 | PDI程序JVM参数配置        | 读并发  | 写并发                                         | 耗时  | Linux'CPU | PDI'CPU | 内存增幅      | 监控详情                    |
| :-: | :--: | :--: | ---------------------------------------------------------------------------------------------------------- | ---- | ------------------- | ---- | ------------------------------------------- | --- | --------- | ------- | --------- | ----------------------- |
|  1  |  v1  | 存量同步 | 选项<br>1.useCursorFetch=true<br>2.defaultFetchSize=500<br><br>连接池配置<br>1.initialSize=100<br>2.maxActive=100 | 共用   | -Xms4096m -Xmx4096m | 1个线程 | 插入/更新/删除各<font color="#f79646">50</font>个线程 |     |           |         | PDI的JVM内存 | Linux <br>MySQL <br>PDI |
|  1  |  v1  | 存量校验 | 同上                                                                                                         | 同上   | -Xms4096m -Xmx4096m | 同上   | 同上                                          |     |           |         |           |                         |

><font color="#f79646">统计详情</font>

| 序号  | 对应单表名称                           | 需要同步数量  | 实际同步数量                                 | 1.同步耗时 <font color="#1f497d">单位:ms</font> | 1.校验耗时 <font color="#1f497d">单位:ms</font>               |     | 2.校验耗时 |
| --- | -------------------------------- | ------- | -------------------------------------- | ----------------------------------------- | ------------------------------------------------------- | --- | ------ |
| 2   | pat_inhos_order_group_out_202203 | 456611  | 456611                                 | 421962  ≈ 07min 01s                       |                                                         |     |        |
| 3   | pat_inhos_order_group_out_202204 | 687201  | 687201                                 | 585003  ≈ 09min 45s                       |                                                         |     |        |
| 4   | pat_inhos_order_group_out_202205 | 339898  | 339898                                 | 326075  ≈ 05min 26s                       |                                                         |     |        |
| 5   | pat_inhos_order_group_out_202206 | 478702  | 478702                                 | 420306  ≈ 07min 02s                       |                                                         |     |        |
| 6   | pat_inhos_order_group_out_202207 | 842042  | 842042                                 | 721470  ≈ 12min 00s                       |                                                         |     |        |
| 7   | pat_inhos_order_group_out_202208 | 1161484 | 1161484                                | 1014618 ≈ 16min 52s                       |                                                         |     |        |
| 8   | pat_inhos_order_group_out_202209 | 1016859 | 1016859                                | 894200  ≈ 14min 52                        |                                                         |     |        |
| 9   | pat_inhos_order_group_out_202210 | 1038642 | 1038642                                | 912572  ≈ 15min 12s                       | 330033 ≈ 5min30s  330033≈   330033≈   330033≈   330033≈ |     |        |
| 10  | pat_inhos_order_group_out_202211 | 1186088 | 1186088                                | 1045520 ≈ 17min 25s                       |                                                         |     |        |
| 11  | pat_inhos_order_group_out_202212 | 1587255 | 1587255                                | 1352344 ≈ 22min 32s                       |                                                         |     |        |
| 12  | pat_inhos_order_group_out_202301 | 1448234 | 1448234                                | 1177269 ≈ 19min 37s                       |                                                         |     |        |
| 13  | pat_inhos_order_group_out_202302 | 1277410 | 1277410                                | 1033869 ≈ 17min 13s                       |                                                         |     |        |
| 14  | pat_inhos_order_group_out_202303 | 1671082 | 1671082                                | 1418770 ≈ 23min 38s                       |                                                         |     |        |
| 15  | pat_inhos_order_group_out_202304 | 2015228 | 2015228                                | 1638540 ≈ 27min 18s                       |                                                         |     |        |
| 16  | pat_inhos_order_group_out_202305 | 2033609 | 2033609                                | 1790188 ≈ 29min 50s                       |                                                         |     |        |
| 17  | pat_inhos_order_group_out_202306 | 2080701 | 2080701                                | 1755187 ≈ 29min 13s                       |                                                         |     |        |
| 18  | pat_inhos_order_group_out_202307 | 2038142 | 2038142                                | 1737329 ≈ 28min 55s                       |                                                         |     |        |
| 19  | pat_inhos_order_group_out_202308 | 2249689 | 2249689                                | 2063662 ≈ 34min 23                        |                                                         |     |        |
| 20  | pat_inhos_order_group_out_202309 | 2115785 | 2115785                                | 1938405 ≈ 32mi                            |                                                         |     |        |
| 21  | pat_inhos_order_group_out_202310 | 2169808 | 2169808                                | 1961887 ≈                  s              |                                                         |     |        |
| 22  | pat_inhos_order_group_out_202311 | 2145999 | 2145999                                | 197048                 n 50s              |                                                         |     |        |
| 23  | pat_inhos_order_group_out_202312 | 2525776 | 2525776                                | 24                 41min 02s              |                                                         |     |        |
| 24  | pat_inhos_order_group_out_202401 | 990729  | 990729                   1 ≈ 17min 03s |                                           |                                                         |     |        |
| 24  | pat_inhos_order_in               | 637455  |                                        |                                           |                                                         |     |        |
|     |                                  |         |                                        | 总耗时 ≈ 8h14min                             |                                                         |     |        |


# 9.上线发布


## 表结构与数据

> [!important] 
> - 目标在院表与原始表结构<font color="#f79646">不同</font>：1.没有自增属性 --- <font color="#c0504d">注意：记得后续在停机校验完成之后，启动服务之前添加自增属性与原始表相同</font>
> - 目标出院表与原始表结构<font color="#f79646">不同</font>：1.没有自增属性；2.新增患者出院时间字段 --- <font color="#c0504d">要求：患者出院时间字段不为null且需要添加索引</font>
> - 基于运行期稳定同步考虑，<font color="#f79646">在创建表时可以不用去掉索引</font>，慢慢同步，不然后续停机校验完整数据前后还需要进行索引创建，导致停机时间拉长
> - 在此期间如果没有改变表结构的话，则以下面收集表结构和数据为准

### 医嘱-在院表

#### 表结构

```sql
-- ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} 会动态替换为在院表，比如：pat_inhos_order_in
-- 注意：1.没有自增属性
CREATE TABLE IF NOT EXISTS ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} (
	`seq_id` bigint(20) UNSIGNED NOT NULL COMMENT '自增长流水号',
	`order_code` varchar(50) NOT NULL COMMENT '医嘱号',
	`inhos_code` varchar(20) NOT NULL COMMENT '病人住院号',
	`pat_code` varchar(20) NOT NULL COMMENT '病人标识号',
	`order_group_no` varchar(50) DEFAULT '' COMMENT '医嘱组号',
	`order_sub_no` varchar(16) DEFAULT '' COMMENT '医嘱子序号',
	`repeat_indicator` int(16) DEFAULT NULL COMMENT '长期医嘱标志(1-长期，0-临时)',
	`order_class_code` varchar(30) DEFAULT NULL COMMENT '医嘱类型编号',
	`order_class` varchar(16) DEFAULT '' COMMENT '医嘱类型名称',
	`order_text` varchar(128) DEFAULT '' COMMENT '医嘱正文',
	`order_text_abbr` varchar(30) DEFAULT '' COMMENT '医嘱简称',
	`order_remark` varchar(200) DEFAULT NULL COMMENT '医嘱批注',
	`item_code` varchar(50) DEFAULT '' COMMENT '项目编号,如药品编号',
	`item_specification` varchar(50) DEFAULT NULL COMMENT '项目规格',
	`item_price` decimal(10, 4) DEFAULT NULL COMMENT '项目价格',
	`total_dosage` decimal(11, 5) DEFAULT '0.00000' COMMENT '药品使用总量',
	`total_dosage_units` varchar(16) DEFAULT '' COMMENT '药品使用问题单位',
	`dosage` decimal(11, 5) DEFAULT '0.00000' COMMENT '药品一次使用剂量',
	`dosage_units` varchar(16) DEFAULT '' COMMENT '剂量单位',
	`administration_code` varchar(30) DEFAULT NULL COMMENT '用法编号',
	`administration` varchar(16) DEFAULT '' COMMENT '给药途径和方法',
	`start_date_time` datetime DEFAULT NULL COMMENT '本医嘱起始日期及时间',
	`stop_date_time` datetime DEFAULT NULL COMMENT '本医嘱停止日期及时间',
	`duration` int(11) DEFAULT NULL COMMENT '一次执行的持续时间',
	`duration_units` varchar(16) DEFAULT '' COMMENT '持续时间单位',
	`frequency_code` varchar(30) DEFAULT NULL COMMENT '频率编号',
	`frequency` varchar(16) DEFAULT '' COMMENT '执行频率描述',
	`freq_counter` int(11) DEFAULT NULL COMMENT '频率次数',
	`freq_interval` int(11) DEFAULT NULL COMMENT '频率间隔',
	`freq_interval_unit` varchar(16) DEFAULT '' COMMENT '频率间隔单位',
	`freq_detail` varchar(16) DEFAULT '' COMMENT '执行时间详细描述',
	`is_self_prepare` varchar(1) DEFAULT NULL COMMENT '是否为自备药',
	`is_emergent` varchar(1) DEFAULT NULL COMMENT '是否紧急',
	`is_continue` varchar(1) DEFAULT '' COMMENT '医嘱是否有延续性  0-没有 1-有延续性',
	`need_skintest` varchar(1) DEFAULT NULL COMMENT '是否需要皮试',
	`perform_result` varchar(16) DEFAULT '' COMMENT '执行结果',
	`ordering_dept` varchar(16) DEFAULT '' COMMENT '开医嘱科室',
	`doctor` varchar(50) DEFAULT '' COMMENT '开医嘱医生',
	`stop_doctor` varchar(50) DEFAULT '' COMMENT '停医嘱医生',
	`nurse` varchar(50) DEFAULT '' COMMENT '开医嘱校对护士',
	`confirm_date_time` datetime DEFAULT NULL COMMENT '确认时间',
	`stop_nurse` varchar(50) DEFAULT '' COMMENT '停医嘱校对护士',
	`enter_date_time` datetime DEFAULT NULL COMMENT '开医嘱录入日期及时间',
	`stop_order_date_time` datetime DEFAULT NULL COMMENT '停医嘱录入日期及时间',
	`order_status` varchar(16) DEFAULT '' COMMENT '医嘱状态(新开、校对、执行、停止等)',
	`skintest_type` varchar(200) DEFAULT '' COMMENT '皮试类型',
	`is_dispense` int(11) DEFAULT NULL COMMENT '是否静配  0-非静配 1-静配',
	`order_dosage` decimal(11, 5) DEFAULT NULL COMMENT '医嘱用量(his计算好的)',
	`firstday_times` int(11) DEFAULT NULL COMMENT '首日执行次数',
	`lastday_times` int(11) DEFAULT NULL COMMENT '末日拆分次数',
	`nurse_remark` varchar(100) DEFAULT '' COMMENT '医嘱护士批注',
	`firstday_plan_time` varchar(50) DEFAULT NULL COMMENT '首日计划执行时间',
	`endday_plan_time` varchar(50) DEFAULT NULL COMMENT '末日计划执行时间',
	`dripping_speed` varchar(200) DEFAULT NULL COMMENT '滴速',
	`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
	`create_person` varchar(50) NOT NULL COMMENT '创建人',
	`update_time` datetime DEFAULT NULL COMMENT '修改时间',
	`update_person` varchar(50) DEFAULT '' COMMENT '修改人',
	`ordering_dept_code` int(11) DEFAULT NULL,
	`doctor_code` varchar(4) DEFAULT NULL,
	`stop_doctor_code` varchar(4) DEFAULT NULL,
	`nurse_code` int(11) DEFAULT NULL,
	`stop_nurse_code` int(11) DEFAULT NULL,
	PRIMARY KEY (`seq_id`),
	UNIQUE KEY `uq_pat_inhos_order_1` (`order_code`),
	KEY `idx_pat_inhos_order_2` (`pat_code`),
	KEY `idx_pat_inhos_order_4` (`ordering_dept`, `enter_date_time`),
	KEY `idx_pat_inhos_order_5` (`start_date_time`),
	KEY `idx_pat_inhos_order_6` (`stop_date_time`),
	KEY `enter_date_time` (`enter_date_time`),
	KEY `create_time_idx` USING BTREE (`create_time`),
	KEY `idx_pat_inhos_order_7` (`ordering_dept`, `inhos_code`),
	KEY `idx_pat_inhos_order_3` (`order_group_no`, `inhos_code`),
	KEY `idx_pat_inhos_order_8` (`inhos_code`),
	KEY `idx_update_time` (`update_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '病历模块-住院医嘱表(在院患者)';
```

#### 表数据

```sql
select pio.*, unix_timestamp(ifnull(pio.update_time, pio.create_time)) * 1000 latest_time  
from pat_inhos_order pio  
 left join pat_inhos_record pir on pio.inhos_code = pir.inhos_code  
 where pir.inhos_code is null or pir.status != 0 or pir.out_date is null order by pio.seq_id ${LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL}
```
### 医嘱-出院表

#### 表结构

```sql
-- ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} 会动态替换为相应分片表，比如：pat_inhos_order_out_20240401
-- 注意：1.没有自增属性；2.新增患者出院字段
CREATE TABLE IF NOT EXISTS ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} (
	`seq_id` bigint(20) UNSIGNED NOT NULL COMMENT '自增长流水号',
	`order_code` varchar(50) NOT NULL COMMENT '医嘱号',
	`inhos_code` varchar(20) NOT NULL COMMENT '病人住院号',
	`pat_code` varchar(20) NOT NULL COMMENT '病人标识号',
	`order_group_no` varchar(50) DEFAULT '' COMMENT '医嘱组号',
	`order_sub_no` varchar(16) DEFAULT '' COMMENT '医嘱子序号',
	`repeat_indicator` int(16) DEFAULT NULL COMMENT '长期医嘱标志(1-长期，0-临时)',
	`order_class_code` varchar(30) DEFAULT NULL COMMENT '医嘱类型编号',
	`order_class` varchar(16) DEFAULT '' COMMENT '医嘱类型名称',
	`order_text` varchar(128) DEFAULT '' COMMENT '医嘱正文',
	`order_text_abbr` varchar(30) DEFAULT '' COMMENT '医嘱简称',
	`order_remark` varchar(200) DEFAULT NULL COMMENT '医嘱批注',
	`item_code` varchar(50) DEFAULT '' COMMENT '项目编号,如药品编号',
	`item_specification` varchar(50) DEFAULT NULL COMMENT '项目规格',
	`item_price` decimal(10, 4) DEFAULT NULL COMMENT '项目价格',
	`total_dosage` decimal(11, 5) DEFAULT '0.00000' COMMENT '药品使用总量',
	`total_dosage_units` varchar(16) DEFAULT '' COMMENT '药品使用问题单位',
	`dosage` decimal(11, 5) DEFAULT '0.00000' COMMENT '药品一次使用剂量',
	`dosage_units` varchar(16) DEFAULT '' COMMENT '剂量单位',
	`administration_code` varchar(30) DEFAULT NULL COMMENT '用法编号',
	`administration` varchar(16) DEFAULT '' COMMENT '给药途径和方法',
	`start_date_time` datetime DEFAULT NULL COMMENT '本医嘱起始日期及时间',
	`stop_date_time` datetime DEFAULT NULL COMMENT '本医嘱停止日期及时间',
	`duration` int(11) DEFAULT NULL COMMENT '一次执行的持续时间',
	`duration_units` varchar(16) DEFAULT '' COMMENT '持续时间单位',
	`frequency_code` varchar(30) DEFAULT NULL COMMENT '频率编号',
	`frequency` varchar(16) DEFAULT '' COMMENT '执行频率描述',
	`freq_counter` int(11) DEFAULT NULL COMMENT '频率次数',
	`freq_interval` int(11) DEFAULT NULL COMMENT '频率间隔',
	`freq_interval_unit` varchar(16) DEFAULT '' COMMENT '频率间隔单位',
	`freq_detail` varchar(16) DEFAULT '' COMMENT '执行时间详细描述',
	`is_self_prepare` varchar(1) DEFAULT NULL COMMENT '是否为自备药',
	`is_emergent` varchar(1) DEFAULT NULL COMMENT '是否紧急',
	`is_continue` varchar(1) DEFAULT '' COMMENT '医嘱是否有延续性  0-没有 1-有延续性',
	`need_skintest` varchar(1) DEFAULT NULL COMMENT '是否需要皮试',
	`perform_result` varchar(16) DEFAULT '' COMMENT '执行结果',
	`ordering_dept` varchar(16) DEFAULT '' COMMENT '开医嘱科室',
	`doctor` varchar(50) DEFAULT '' COMMENT '开医嘱医生',
	`stop_doctor` varchar(50) DEFAULT '' COMMENT '停医嘱医生',
	`nurse` varchar(50) DEFAULT '' COMMENT '开医嘱校对护士',
	`confirm_date_time` datetime DEFAULT NULL COMMENT '确认时间',
	`stop_nurse` varchar(50) DEFAULT '' COMMENT '停医嘱校对护士',
	`enter_date_time` datetime DEFAULT NULL COMMENT '开医嘱录入日期及时间',
	`stop_order_date_time` datetime DEFAULT NULL COMMENT '停医嘱录入日期及时间',
	`order_status` varchar(16) DEFAULT '' COMMENT '医嘱状态(新开、校对、执行、停止等)',
	`skintest_type` varchar(200) DEFAULT '' COMMENT '皮试类型',
	`is_dispense` int(11) DEFAULT NULL COMMENT '是否静配  0-非静配 1-静配',
	`order_dosage` decimal(11, 5) DEFAULT NULL COMMENT '医嘱用量(his计算好的)',
	`firstday_times` int(11) DEFAULT NULL COMMENT '首日执行次数',
	`lastday_times` int(11) DEFAULT NULL COMMENT '末日拆分次数',
	`nurse_remark` varchar(100) DEFAULT '' COMMENT '医嘱护士批注',
	`firstday_plan_time` varchar(50) DEFAULT NULL COMMENT '首日计划执行时间',
	`endday_plan_time` varchar(50) DEFAULT NULL COMMENT '末日计划执行时间',
	`dripping_speed` varchar(200) DEFAULT NULL COMMENT '滴速',
	`create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
	`create_person` varchar(50) NOT NULL COMMENT '创建人',
	`update_time` datetime DEFAULT NULL COMMENT '修改时间',
	`update_person` varchar(50) DEFAULT '' COMMENT '修改人',
	`ordering_dept_code` int(11) DEFAULT NULL,
	`doctor_code` varchar(4) DEFAULT NULL,
	`stop_doctor_code` varchar(4) DEFAULT NULL,
	`nurse_code` int(11) DEFAULT NULL,
	`stop_nurse_code` int(11) DEFAULT NULL,
	`out_date` datetime NOT NULL COMMENT '出院日期',
	PRIMARY KEY (`seq_id`),
	UNIQUE KEY `uq_pat_inhos_order_1` (`order_code`),
	KEY `idx_pat_inhos_order_2` (`pat_code`),
	KEY `idx_pat_inhos_order_4` (`ordering_dept`, `enter_date_time`),
	KEY `idx_pat_inhos_order_5` (`start_date_time`),
	KEY `idx_pat_inhos_order_6` (`stop_date_time`),
	KEY `enter_date_time` (`enter_date_time`),
	KEY `create_time_idx` USING BTREE (`create_time`),
	KEY `idx_pat_inhos_order_7` (`ordering_dept`, `inhos_code`),
	KEY `idx_pat_inhos_order_3` (`order_group_no`, `inhos_code`),
	KEY `idx_pat_inhos_order_8` (`inhos_code`),
	KEY `idx_update_time` (`update_time`),
	KEY `idx_out_date` (`out_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT '病历模块-住院医嘱表(出院患者)';
```

#### 表数据

```sql
-- 原始数据_优化前
select pio.*, pir.out_date,  
unix_timestamp(ifnull(pio.update_time, pio.create_time)) * 1000 as latest_time  
from pat_inhos_order pio  
 left join pat_inhos_record pir on pio.inhos_code = pir.inhos_code  
 where pir.inhos_code is not null and pir.status = 0 and pir.out_date is not null and date_format(pir.out_date, '%Y%m') = '${LACHESIS_JOB_RUNNING_OUT_DATE_MONTH}' order by pio.seq_id ${LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL}


-- 原始_优化v1_当前是用版本
select pio.*,pir.out_date,  
       unix_timestamp(ifnull(pio.update_time, pio.create_time)) * 1000 as latest_time  
from pat_inhos_order pio  
 right join pat_inhos_record pir on pio.inhos_code = pir.inhos_code    
where pir.out_date >= '${LACHESIS_JOB_RUNNING_OUT_BEGIN_DATE_MONTH}' and pir.out_date < '${LACHESIS_JOB_RUNNING_OUT_END_DATE_MONTH}' and pir.status = 0 order by pio.seq_id ${LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL}
```

### 医嘱批次-在院表

#### 表结构

```sql
-- ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} 会动态替换为在院表，比如：pat_inhos_order_group_in
-- 注意：1.没有自增属性
CREATE TABLE IF NOT EXISTS ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} (  
  `seq_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增长编号',  
  `group_unique_code` varchar(60) NOT NULL COMMENT '批次唯一编号',  
  `order_group_no` varchar(50) DEFAULT '' COMMENT '医嘱批次编号',  
  `inhos_code` varchar(20) DEFAULT '' COMMENT '病人住院号',  
  `orderbar` varchar(40) DEFAULT '' COMMENT '医嘱条码',  
  `package_bar` varchar(50) DEFAULT NULL COMMENT '药箱条码',  
  `plan_time` datetime DEFAULT NULL COMMENT '计划执行时间',  
  `order_sort_no` int(11) DEFAULT NULL COMMENT '医嘱排序编号',  
  `source_type` varchar(20) DEFAULT '' COMMENT '数据来源',  
  `isprint` int(11) NOT NULL DEFAULT '0' COMMENT '是否已打印 0 否; 1 是',  
  `execute_status` int(11) NOT NULL DEFAULT '0' COMMENT '执行状态  0 - 未执行， 1- 执行中， 2 - 已执行， 3-停止，4-作废',  
  `execute_date` datetime DEFAULT NULL COMMENT '执行时间',  
  `print_date` datetime DEFAULT NULL COMMENT '打印时间',  
  `execute_person` varchar(20) DEFAULT '' COMMENT '执行人',  
  `print_person` varchar(20) DEFAULT '' COMMENT '打印人',  
  `apply_time` datetime DEFAULT NULL COMMENT '开立时间',  
  `is_dispensed` int(11) NOT NULL DEFAULT '0' COMMENT '是否已配药 1-是， 0 - 否',  
  `remark` varchar(100) DEFAULT '' COMMENT ' 医嘱备注',  
  `reason` varchar(100) DEFAULT NULL COMMENT '手动或作废执行的原因',  
  `execute_type` int(11) DEFAULT '0' COMMENT '执行方式 0-无效， 1- 扫描执行， 2 - 手动执行',  
  `start_execute_user` varchar(20) DEFAULT NULL COMMENT '手动补录开始执行人',  
  `start_execute_date` datetime DEFAULT NULL COMMENT '手动补录开始执行时间',  
  `start_check_user` varchar(20) DEFAULT NULL COMMENT '手动补录开始核对人',  
  `end_execute_user` varchar(20) DEFAULT NULL COMMENT '手动补录结束执行人',  
  `end_execute_date` datetime DEFAULT NULL COMMENT '手动补录结束执行时间',  
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
  `create_person` varchar(50) NOT NULL DEFAULT '' COMMENT '创建人',  
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',  
  `update_person` varchar(50) DEFAULT NULL COMMENT '修改人',  
  PRIMARY KEY (`seq_id`),  
  UNIQUE KEY `uq_pat_inhos_order_group_1` (`group_unique_code`),  
  KEY `idx_pat_inhos_order_group_1` (`order_group_no`),  
  KEY `idx_pat_inhos_order_group_2` (`orderbar`),  
  KEY `idx_pat_inhos_order_group_3` (`execute_date`),  
  KEY `idx_pat_inhos_order_group_4` (`plan_time`),  
  KEY `idx_idx_pat_inhos_order_group_5` (`inhos_code`),  
  KEY `idx_pat_inhos_order_group_6` (`inhos_code`,`plan_time`,`execute_status`)  
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='医嘱批次表(在院患者)';
```

#### 表数据

```sql
-- 目标
select piog.*,unix_timestamp(ifnull(piog.update_time, piog.create_time)) * 1000 latest_time from ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} piog order by piog.seq_id ${LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL}

-- 原始
select piog.*,unix_timestamp(ifnull(piog.update_time, piog.create_time)) * 1000 latest_time
 from pat_inhos_order_group piog  
 left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code  
 where pir.inhos_code is null or pir.status != 0 or pir.out_date is null order by piog.seq_id ${LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL}
```

### 医嘱批次-出院表

#### 表结构

```sql
-- ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} 会动态替换为相应分片表，比如：pat_inhos_order_group_out_20240401
-- 注意：1.没有自增属性；2.新增患者出院字段
CREATE TABLE IF NOT EXISTS ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} (  
  `seq_id` bigint(20) NOT NULL COMMENT '自增长编号',  
  `group_unique_code` varchar(60) NOT NULL COMMENT '批次唯一编号',  
  `order_group_no` varchar(50) DEFAULT '' COMMENT '医嘱批次编号',  
  `inhos_code` varchar(20) DEFAULT '' COMMENT '病人住院号',  
  `orderbar` varchar(40) DEFAULT '' COMMENT '医嘱条码',  
  `package_bar` varchar(50) DEFAULT NULL COMMENT '药箱条码',  
  `plan_time` datetime DEFAULT NULL COMMENT '计划执行时间',  
  `order_sort_no` int(11) DEFAULT NULL COMMENT '医嘱排序编号',  
  `source_type` varchar(20) DEFAULT '' COMMENT '数据来源',  
  `isprint` int(11) NOT NULL DEFAULT '0' COMMENT '是否已打印 0 否; 1 是',  
  `execute_status` int(11) NOT NULL DEFAULT '0' COMMENT '执行状态  0 - 未执行， 1- 执行中， 2 - 已执行， 3-停止，4-作废',  
  `execute_date` datetime DEFAULT NULL COMMENT '执行时间',  
  `print_date` datetime DEFAULT NULL COMMENT '打印时间',  
  `execute_person` varchar(20) DEFAULT '' COMMENT '执行人',  
  `print_person` varchar(20) DEFAULT '' COMMENT '打印人',  
  `apply_time` datetime DEFAULT NULL COMMENT '开立时间',  
  `is_dispensed` int(11) NOT NULL DEFAULT '0' COMMENT '是否已配药 1-是， 0 - 否',  
  `remark` varchar(100) DEFAULT '' COMMENT ' 医嘱备注',  
  `reason` varchar(100) DEFAULT NULL COMMENT '手动或作废执行的原因',  
  `execute_type` int(11) DEFAULT '0' COMMENT '执行方式 0-无效， 1- 扫描执行， 2 - 手动执行',  
  `start_execute_user` varchar(20) DEFAULT NULL COMMENT '手动补录开始执行人',  
  `start_execute_date` datetime DEFAULT NULL COMMENT '手动补录开始执行时间',  
  `start_check_user` varchar(20) DEFAULT NULL COMMENT '手动补录开始核对人',  
  `end_execute_user` varchar(20) DEFAULT NULL COMMENT '手动补录结束执行人',  
  `end_execute_date` datetime DEFAULT NULL COMMENT '手动补录结束执行时间',  
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',  
  `create_person` varchar(50) NOT NULL DEFAULT '' COMMENT '创建人',  
  `update_time` datetime DEFAULT NULL COMMENT '修改时间',  
  `update_person` varchar(50) DEFAULT NULL COMMENT '修改人',
  `out_date` datetime NOT NULL COMMENT '出院日期',  
  PRIMARY KEY (`seq_id`),  
  UNIQUE KEY `uq_pat_inhos_order_group_1` (`group_unique_code`),  
  KEY `idx_pat_inhos_order_group_1` (`order_group_no`),  
  KEY `idx_pat_inhos_order_group_2` (`orderbar`),  
  KEY `idx_pat_inhos_order_group_3` (`execute_date`),  
  KEY `idx_pat_inhos_order_group_4` (`plan_time`),  
  KEY `idx_idx_pat_inhos_order_group_5` (`inhos_code`),  
  KEY `idx_pat_inhos_order_group_6` (`inhos_code`,`plan_time`,`execute_status`),
  KEY `idx_out_date` (`out_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='医嘱批次表(出院患者)';
```

#### 表数据

```sql
-- 目标
select piog.*,unix_timestamp(ifnull(piog.update_time, piog.create_time)) * 1000 latest_time from ${LACHESIS_JOB_RUNNING_TARGET_TABLE_NAME} piog order by piog.seq_id ${LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL}

-- 原始_优化前
select piog.*, pir.out_date, unix_timestamp(ifnull(piog.update_time, piog.create_time)) * 1000 latest_time
 from pat_inhos_order_group piog
 left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code
 where pir.inhos_code is not null and pir.status = 0 and pir.out_date is not null and date_format(pir.out_date, '%Y%m') = '${LACHESIS_JOB_RUNNING_OUT_DATE_MONTH}' ${LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL}

-- 原始_优化v1_当前是用版本
select piog.*, pir.out_date, unix_timestamp(ifnull(piog.update_time, piog.create_time)) * 1000 latest_time  
 from pat_inhos_order_group piog  
 right join pat_inhos_record pir on piog.inhos_code = pir.inhos_code  
 where pir.out_date >= '${LACHESIS_JOB_RUNNING_OUT_BEGIN_DATE_MONTH}' and pir.out_date < '${LACHESIS_JOB_RUNNING_OUT_END_DATE_MONTH}' and pir.status = 0 order by piog.seq_id ${LACHESIS_JOB_TARGET_SYNC_LIMIT_SQL}

-- 原始_优化v2
select piog.*, pir.out_date, unix_timestamp(ifnull(piog.update_time, piog.create_time)) * 1000 latest_time  
from pat_inhos_order_group piog  
right join (  
    select inhos_code, out_date  
    from pat_inhos_record pir  
    where pir.out_date >= '${LACHESIS_JOB_RUNNING_OUT_BEGIN_DATE_MONTH}' and pir.out_date < '${LACHESIS_JOB_RUNNING_OUT_END_DATE_MONTH}' and  pir.status = 0  
) pir on piog.inhos_code = pir.inhos_code  
order by piog.seq_id
```

## Linux服务端操作

### 准备

```bash
unzip pdi-ce-9.4.0.0-343.zip
cd /usr/local/kettle/pdi-ce-9.4.0.0-343/data-integration
rm -rf logs
chmod +x *.sh
```

```ad-warning
线上使用需要删除启动脚本中的Javaagent的监控埋点！
```

### 配置

第一处修改

>对应配置文件：/用户目录/.kettle/kettle.properties，像我们一般使用的都是root用户，所以对应路径为：/root/.kettle/kettle.properties

```bash
KETTLE_EMPTY_STRING_DIFFERS_FROM_NULL=Y
```

第二处修改

>对应配置文件：/用户目录/.kettle/repositories.xml，像我们一般使用的都是root用户，所以对应路径为：/root/.kettle/repositories.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<repositories>
  <repository>
    <id>KettleFileRepository</id>
    <name>lx_pentaho_repository</name>
    <description />
    <is_default>true</is_default>
    <base_directory>/usr/local/kettle/lx_pentaho_repository</base_directory>
    <read_only>N</read_only>
    <hides_hidden_files>N</hides_hidden_files>
  </repository>
</repositories>
```

### 启停

```bash
cd /usr/local/kettle/pdi-ce-9.4.0.0-343/data-integration

# 医嘱同步-测试
./kitchen.sh -rep=lx_pentaho_repository -job=main -param:LACHESIS_JOB_SYNC_CONFIG_PATH=/usr/local/kettle/lx_pentaho_repository/config/sync_order.properties -level=Detailed
# 医嘱批次同步-测试
./kitchen.sh -rep=lx_pentaho_repository -job=main -param:LACHESIS_JOB_SYNC_CONFIG_PATH=/usr/local/kettle/lx_pentaho_repository/config/sync_order_group.properties -level=Detailed

# 查看进程
ps -ef | grep kitchen

# 医嘱同步-后台运行
nohup ./kitchen.sh -rep=lx_pentaho_repository -job=main -param:LACHESIS_JOB_SYNC_CONFIG_PATH=/usr/local/kettle/lx_pentaho_repository/config/sync_order.properties &
# 医嘱批次同步-后台运行
nohup ./kitchen.sh -rep=lx_pentaho_repository -job=main -param:LACHESIS_JOB_SYNC_CONFIG_PATH=/usr/local/kettle/lx_pentaho_repository/config/sync_order_group.properties &
```


