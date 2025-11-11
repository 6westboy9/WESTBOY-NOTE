


# 数据类型

| 序号  | PDI字段类型          | 分组      | Java类型               | SQL类型（Path:java.sql.Types）                            | 备注          |
| --- | ---------------- | ------- | -------------------- | ----------------------------------------------------- | ----------- |
| 1   | String           | String  | java.lang.String     | CHAR、VARCHAR、NVARCHAR、LONGVARCHAR、CLOB、NCLOB          |             |
| 2   | Integer          | Numeric | java.lang.Long       | TINYINT、SMALLINT、INTEGER、BIGINT、DECIMAL和NUMERIC中的特殊情况 |             |
| 3   | Number           | Numeric | java.lang.Double     | DECIMAL、DOUBLE、FLOAT、REAL、NUMERIC                     |             |
| 4   | BigNumber        | Numeric | java.math.BigDecimal | DECIMAL、DOUBLE、FLOAT、REAL、NUMERIC中的特殊情况               |             |
| 5   | Date             | Date    | java.util.Date       | DATE、TIME                                             |             |
| 6   | Boolean          | Boolean | java.lang.Boolean    | BOOLEAN、BIT                                           |             |
| 7   | Binary           | Binary  | byte[]               | BINARY、BLOB、VARBINARY、LONGVARBINARY                   |             |
| 8   | Serializable     |         |                      |                                                       |             |
| 9   | Timestamp        | Date    | java.lang.String     | TIMESTAMP                                             | 数据库输入的时候会出现 |
| 10  | Internet Address |         |                      |                                                       |             |
>源码中对应的实现

![[ValueMetaInterface.png|1600]]


# 转换



## 1.输入


## 2.输出


### 1.Excel输出


### 2.文本文件输出


### 3.SQL文件输出


### 4.表输出


### 5.更新&插入/更新


* 更新：更新是将数据库表中的数据和数据流中的数据做对比，如果不同就更新，<font color="#f79646">如果数据流中的数据比数据库中的数据多，那么就报错</font>。
* 插入/更新：与更新不同的是，<font color="#f79646">数据不存在就插入</font>。

## 3.转换


### 1.Concat fields

将多个字段连拼接成一个字段。

### 2.值映射/Value Mapper

A库表中存的性别是男女，但是B库中存的性别是F/M，需要进行值映射转换。

### 3.增加常量&增加序列

* 增加常量就是本身的数据流里面添加一列数据，该列的数据都是相同的值。
* 增加序列是给数据流添加一个序列字段，可以自定义该序列字段的递增步长。

### 4.字段选择

字段选择是从数据流中选择字段、改变名称、修改数据类型。

比如：1.添加字段选择控件，移除掉firstname字段，并将lastname重命名为name；2.将salary重名为money。

### 5.计算器


### 6.字符串剪切&替换&操作

* 字符串剪切：等同于Java中字符串的subString方法。
* 字符串替换（Replace in string）：替换字符串内容。
* 字符串操作：主要是去除字符串两端的空格和大小写切换，并生成新的字段。

### 7.排序记录&去除重复记录

去除重复记录是去除数据流里面相同的数据行。但是此控件使用之前<font color="#f79646">要求必须先对数据进行排序</font>，对数据排序用的控件是排序记录，排序记录控件可以按照指定字段的升序或者降序对数据流进行排序。因此排序记录+去除重复记录控件常常配合组队使用。

### 8.唯一行_哈希值

<font color="#4f81bd">唯一行_哈希值</font>就是删除数据流重复的行。此控件的效果和（排序记录+去除重复记录）的效果是一样的，但是实现原理不同。

* 排序记录+去除重复记录对比的是每两行之间的数据
* <font color="#4f81bd">唯一行_哈希值</font>是给每一行的数据建立哈希值，通过哈希值来比较数据是否重复 --- <font color="#f79646">效率比较高</font>

>为了避免哈希碰撞，可以另加其它字段，多字段复合保证唯一性~

### 9.拆分字段

拆分字段就是把字段按照分割符拆分成两个或者多个字段。<font color="#f79646">需要注意的是，字段拆分以后，原字段就会从数据流中消失</font>。


### 10.列拆分为多行


列拆分为多行就是把指定字段按照指定分割符进行拆分为多行，然后其它字段直接复制。

1. 选择要拆分的字段
2. 设置合适的分割符
3. 设置分割以后的新字段
4. 选择是否输出新数据的排列行号，行号是否重复

| id  | name     | age | hobby                                 |
| --- | -------- | --- | ------------------------------------- |
| 1   | zhangsan | 20  | baseball,basketball,football,pingpang |

| id  | name     | age | hobby                                 | hobby2     |
| --- | -------- | --- | ------------------------------------- | ---------- |
| 1   | zhangsan | 20  | baseball,basketball,football,pingpang | baseball   |
| 1   | zhangsan | 20  | baseball,basketball,football,pingpang | basketball |
| 1   | zhangsan | 20  | baseball,basketball,football,pingpang | football   |
| 1   | zhangsan | 20  | baseball,basketball,football,pingpang | pingpang   |

### 11.行扁平化

行扁平化就是把同一组的多行数据合并成为一行，可以理解为列拆分为多行的逆向操作。但需要注意行扁平化控件使用有两个条件：

1. <font color="#f79646">使用之前需要对数据进行排序</font>；
2. 每个分组的数据条数要保持一致，否则数据会有错乱。
	* 如何理解？即每个分组的组内元素数量是相同的，比如下面zhangsan，lisi，wangwu均应该是3条。

| id  | name     | age | hobby      |
| --- | -------- | --- | ---------- |
| 1   | zhangsan | 20  | baseball   |
| 1   | zhangsan | 20  | basketball |
| 1   | zhangsan | 20  | pingpang   |
| 2   | lisi     | 25  | pingpang   |
| 2   | lisi     | 25  | baseball   |
| 2   | lisi     | 25  | basketball |
| 3   | wangwu   | 24  | football   |
| 3   | wangwu   | 24  | pingpang   |
| 3   | wangwu   | 24  | basketball |

| id  | name     | age | hobby1   | hobby2     | hobby3     |
| --- | -------- | --- | -------- | ---------- | ---------- |
| 1   | zhangsan | 20  | baseball | basketball | pingpang   |
| 2   | lisi     | 25  | pingpang | baseball   | basketball |
| 3   | wangwu   | 24  | football | pingpang   | basketball |

借助Concat fields控件可以再将三个字段合并拼接成一个字段。

| id  | name     | age | hobby1   | hobby2     | hobby3     | hobby                        |
| --- | -------- | --- | -------- | ---------- | ---------- | ---------------------------- |
| 1   | zhangsan | 20  | baseball | basketball | pingpang   | baseball,basketball,pingpang |
| 2   | lisi     | 25  | pingpang | baseball   | basketball | pingpang,baseball,basketball |
| 3   | wangwu   | 24  | football | pingpang   | basketball | football,pingpang,basketball |

><font color="#f79646">反例</font>

| id  | name     | age | hobby      |
| --- | -------- | --- | ---------- |
| 1   | zhangsan | 20  | baseball   |
| 1   | zhangsan | 20  | basketball |
| 1   | zhangsan | 20  | pingpang   |
| 1   | zhangsan | 20  | football   |
| 2   | lisi     | 25  | pingpang   |
| 2   | lisi     | 25  | baseball   |
| 2   | lisi     | 25  | basketball |
| 3   | wangwu   | 24  | football   |
| 3   | wangwu   | 24  | pingpang   |
| 4   | zhaoliu  | 26  | basketball |
执行结果：TODO

### 12.列转行

<font color="#f79646">注意：列转行之前数据必须按照分组字段排序，否则数据会错乱！</font>

* 关键字段：从数据内容变成列名的字段（星期）
* 分组字段：列转行，转变以后的分组字段（姓名）
* 目标字段：增加列的列名称字段（见下配置）
* 数据字段：目标字段的数据字段（见下配置）
* 关键字值：数据字段查询时的关键字，也可以理解为Key（见下配置）

>配置

| 目标字段 | 数据字段 | 关键字值 | 类型     |
| ---- | ---- | ---- | ------ |
| 周一   | 工作小时 | 周一   | String |
| 周二   | 工作小时 | 周二   | String |
| 周三   | 工作小时 | 周三   | String |
| 周四   | 工作小时 | 周四   | String |
| 周五   | 工作小时 | 周五   | String |
><font color="#f79646">目标字段和关键字值不一定完全相同</font>，可以理解目标字段为别名，而关键字值必须是存在的。

转换前

| 姓名       | 星期  | 工作小时 |
| -------- | --- | ---- |
| zhangsan | 周一  | 8    |
| zhangsan | 周二  | 9    |
| zhangsan | 周三  | 10   |
| zhangsan | 周四  | 8    |
| zhangsan | 周五  | 9    |
转换后

| 姓名       | 周一  | 周二  | 周三  | 周四  | 周五  |
| -------- | --- | --- | --- | --- | --- |
| zhangsan | 8   | 9   | 10  | 8   | 9   |

### 13.行转列

列转行的逆向操作。


## 4.应用


### 1.替换NULL值


### 2.写日志


## 5.流程


### 1.Switch/case



### 2.过滤记录


### 3.空操作


### 4.中止

![[Pasted image 20240416185519.png|600]]

选项说明

* Abort the running transformation
* Abort and log as an error
* Stop input processing

## 6.查询

### 1.数据库查询


### 2.流查询


## 7.连接

### 1.Merge Join


### 2.合并记录

合并记录是用于将两个不同来源的数据合并，这两个来源的数据分别为旧数据和新数据，该步骤将旧数据和新数据按照指定的关键字匹配、比较、合并。

![[Pasted image 20240418183435.png|600]]

需要设置的参数：

- 旧数据源
- 新数据源
- 标志字段：设置标志字段的名称，标志字段用于保存比较的结果，比较结果有下列几种：
	- <font color="#4bacc6">identical</font>：旧数据和新数据一样
	- <font color="#4bacc6">changed</font>：数据发生了变化
	- <font color="#4bacc6">new</font>：新数据中有而旧数据中没有的记录
	- <font color="#4bacc6">deleted</font>：旧数据中有而新数据中没有的记录
- 匹配的关键字-关键字段：用于匹配两个数据源中的同一条记录
- 匹配的关键字-数据字段：最终比较的数据字段

合并后的数据将包括旧数据来源和新数据来源里的<font color="#f79646">所有数据</font>，对于变化的数据，使用新数据代替旧数据，同时在结果里用一个标示字段，来指定新旧数据的比较结果。

```ad-warning
- 旧数据和新数据需要事先按照关键字段排序
- 旧数据和新数据要有相同的字段名称
```



### 3.排序合并


### 4.记录关联_笛卡尔积输出


## 8.统计


## 9.映射


## 10.脚本


### 1.Java脚本


### 2.执行SQL脚本


# 作业



# 资源库

资源管理入口
资源管理





![[Pasted image 20240417102017.png|600]]

点击探索资源库显示如下信息

![[Pasted image 20240417101549.png|750]]


参数语法

```
[/-]name[[:=]value]
```

## Linux下执行转换

执行脚本：pan.sh

| 序号  | 参数名称  | 参数含义 |     |
| --- | ----- | ---- | --- |
|     | file  |      |     |
|     | param |      |     |
|     | level |      |     |
|     |       |      |     |

```
./pan.sh -param:LACHESIS_JOB_SOURCE_TABLE_NAME=pat_inhos_order -file=/usr/local/kettle/lx_pentaho_repository/get_source_table_min_time.ktr
```

## Linux下执行作业

执行脚本：kitchen.sh

| name    | 参数含义  |     |
| ------- | ----- | --- |
| norep   |       |     |
| rep     | 资源库名称 |     |
| user    |       |     |
| pass    |       |     |
| listrep |       |     |
| dir     |       |     |
| listdir |       |     |
| file    |       |     |
| level   |       |     |
| logfile |       |     |
| version |       |     |

```
./kitchen.sh -listrep

List of repositories:
#1 : lx_pentaho_repository [lx_pentaho_repository]  id=KettleFileRepository
```



```sh
# 使用文件资源库的方式
nohup ./kitchen.sh -rep=lx_pentaho_repository -job=main &
./kitchen.sh -rep=lx_pentaho_repository -job=main -param:LACHESIS_JOB_SYNC_CONFIG_PATH=/usr/local/kettle/lx_pentaho_repository/config/sync_order.properties
```