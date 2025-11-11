
# 单表数据同步_场景分析

>程序和数据库在不同服务器上

* 表：pat_inhos_order_group_in
* 数据：4012320
* 同步/校验完成耗时：1658668毫秒 接近28分钟

```sql
-- 4012320 consume=10min+
select count(*)  
 from pat_inhos_order_group piog  
 left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code  
 where pir.inhos_code is null or pir.status != 0 or pir.out_date is null;
```

* Linux_173：http://10.2.43.101:3000/goto/AzgT31fIR?orgId=1
* Linux_66：http://10.2.43.101:3000/goto/ibdb4bfIR?orgId=1
* MySQL_173：http://10.2.43.101:3000/goto/MXTT31BSR?orgId=1
* JVM_66：http://10.2.43.101:3000/goto/_dAqrJfIR?orgId=1

## 两阶段

><font color="#f79646">阶段一 13:24:00 ~ 13:40:00</font> 数据库准备数据 <font color="#9bbb59">16min左右</font>

耗时为何如此之久？

```sql
-- 4012320 consume=10min+
select count(*)  
 from pat_inhos_order_group piog  
 left join pat_inhos_record pir on piog.inhos_code = pir.inhos_code  
 where pir.inhos_code is null or pir.status != 0 or pir.out_date is null;
```

应该是用到了临时表，根据MySQL的Handlers监控信息，可以得知，先将数据查询出来，再插入到临时表中。

猜测：上述Handlers监控可以看到读取数据有两个波分，每个波分都有相同的规律：

- 先读取数据 -- 紫色线条
- 再插入数据到临时表 -- 红色线条

<font color="#c0504d">如何证明确实是有临时表存在呢？</font>


><font color="#f79646">阶段二 13:40:00 ~ 13:52:00</font> 传输并处理数据 <font color="#9bbb59">10min左右</font>

pat_inhos_order_group_in表数据也就900mb左右，如果以Network Traffic最大传输速度3mb/s传输的话，也就5分钟左右。

| 数据库             | 表名                           | 记录数     | 数据容量\(MB\) | 索引容量\(MB\) |     |
| :-------------- | :--------------------------- | :------ | :--------- | :--------- | --- |
| windranger\_emr | pat\_inhos\_order\_group\_in | 3856907 | 881.00     | 1485.18    |     |

观察JVM内存在此阶段一直维持在1GB左右，也发生了几次GC。

>通过查看MySQL所在服务器的监控信息也可以看到CPU、磁盘IO、网络IO得以证实~

## 监控信息

### Linux_173

![[Pasted image 20240427172704.png|800]]

### Linux_66

![[Pasted image 20240427173236.png|800]]

### MySQL_173

![[Pasted image 20240427141814.png|1200]]

>关于write的资料：https://juejin.cn/s/mysql%20handler%20write

![[Pasted image 20240427142933.png|800]]

![[Pasted image 20240427143150.png|800]]

### JVM_66

![[Pasted image 20240427144247.png|800]]

![[Pasted image 20240427144356.png|800]]

![[Pasted image 20240427144538.png|800]]

![[Pasted image 20240427150631.png|800]]


# 单表数据同步_部署影响

>程序和数据库在不同服务器上

* 场景：程序在66上
* 耗时：<font color="#f79646">1714192ms 大概29分钟</font>
* 监控时间段：2024-04-27 16:37:20 ~ 2024-04-27 17:08:20
	* Linux_173：http://10.2.43.101:3000/goto/uI7h7xfIR?orgId=1
	* Linux_66：http://10.2.43.101:3000/goto/GgAp7bBIg?orgId=1
	* MySQL_173：http://10.2.43.101:3000/goto/K3mKnxBSR?orgId=1
	* JVM_66：http://10.2.43.101:3000/goto/d9ZT7xBSg?orgId=1

>程序和数据库在同一服务器上

* 场景：程序在173上
* 耗时：<font color="#f79646">1292457ms 大概20分钟</font>
* 监控时间段：2024-04-27 17:10:00 ~ 2024-04-27 17:40:00
	* Linux_173：http://10.2.43.101:3000/goto/eCM7SxfIR?orgId=1
	* MySQL_173：http://10.2.43.101:3000/goto/E1DSSxfSR?orgId=1
	* JVM_173：忘记加监控了...后续补充

> [!summary] 时间节省了10分钟，但是相应资源占用就会增加~



