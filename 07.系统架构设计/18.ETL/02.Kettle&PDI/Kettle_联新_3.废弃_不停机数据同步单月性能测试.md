# 数据同步_单月出院医嘱

## 场景信息

![[Pasted image 20240407132407.png|560]]

```ad-tip
公司内部环境MySQL数据库一般最大连接数800，业务占用情况需要根据实际线上情况而定。
```

PDI程序配置

| <font color="#4f81bd">EMR_R数据库选项</font> | <font color="#4f81bd">EMR_W数据库选项</font> | <font color="#4f81bd">EMR_W数据库连接池</font> | <font color="#4f81bd">PDI程序JVM参数配置</font> | <font color="#9bbb59">场景</font> | <font color="#9bbb59">读并发</font> | <font color="#9bbb59">写并发</font> |
| --------------------------------------- | --------------------------------------- | ---------------------------------------- | ----------------------------------------- | ------------------------------- | -------------------------------- | -------------------------------- |
| useCursorFetch=true                     | useCursorFetch=true                     | initialSize=100                          | -Xms1024m -Xmx2048m                       | 202208单月数据同步                    | 1                                | 100/插入更新方式                       |
| defaultFetchSize=500                    | defaultFetchSize=500                    | maxActive=100                            |                                           |                                 |                                  |                                  |

说明：

* EMR_R：对应读取连接
* EMR_W：对应写入连接

参数说明：

* useCursorFetch：是否允许部分数据到客户端就进行处理，如果为false表示所有数据到达客户端后，才进行处理。
* defaultFetchSize：每次与数据库交互，读多少条数据加入内存中缓存，不设置默认把所有数据读取出来，容易内存溢出，默认设置500，大表CPU性能高建议设置更大值，不能超过65535。

数据量统计：

```sql
-- 1061949 单月数据总量为100w+
select count(*)  
 from pat_inhos_order pioa  
 left join pat_inhos_record pir on pioa.inhos_code = pir.inhos_code  
  where pir.inhos_code is not null and pir.status = 0 and pir.out_date is not null and date_format(out_date, '%Y%m') = '202208';
```

>整个过程耗时：6分38秒，后续多次测试可缩短至3分20秒左右。实际情况根据不同环境可能会存在差异，此处性能测试只为测试其性能同步性能瓶颈所在地方。

## 监控信息

><font color="#f79646">1.Linux服务器</font>

![[Pasted image 20240407113354.png|1600]]

><font color="#f79646">2.MySQL服务</font>

![[Pasted image 20240407114022.png|1600]]

><font color="#f79646">3.PDI程序</font>

![[Pasted image 20240407114232.png|1600]]

## 测试汇总

| **性能测试** | 读数据库                                                                                                       | 写数据库 | **PDI程序JVM参数配置**                                 | **场景**                                                  | **读并发** | **写并发**                                                                    | **耗时** | **Linux'CPU** | PDI'CPU | **内存增幅**              |
| :------: | ---------------------------------------------------------------------------------------------------------- | ---- | ------------------------------------------------ | ------------------------------------------------------- | ------- | -------------------------------------------------------------------------- | ------ | ------------- | ------- | --------------------- |
|    1     | 选项<br>1.useCursorFetch=true<br>2.defaultFetchSize=500<br><br>连接池配置<br>1.initialSize=100<br>2.maxActive=100 | 共用   | -Xms1024m -Xmx2048m                              | 202208单月数据同步<br><font color="#00b050">1061949条数据</font> | 1个线程    | 插入/更新 100个线程（<font color="#9bbb59">仅新增</font>）                             | 3分20秒  | 85%           |         | 仅PDI程序内存增幅<br>且未发生FGC |
|    2     | 同上                                                                                                         | 同上   | -Xms1024m -Xmx2048m                              | 同上                                                      | 同上      | 插入/更新 100个线程（<font color="#f79646">仅更新</font>）                             | 1分40秒  | 100%          |         | 仅PDI程序内存增幅<br>且未发生FGC |
|    3     | 同上                                                                                                         | 同上   | <font color="#c0504d">-Xms2048m -Xmx4096m</font> | 同上                                                      | 同上      | 插入/更新 100个线程（<font color="#f79646">仅更新</font>）                             | 1分40秒  | 100%          |         | 仅PDI程序内存增幅<br>且未发生FGC |
|    4     | 同上                                                                                                         | 同上   | -Xms1024m -Xmx2048m                              | 同上                                                      | 同上      | 插入/更新 <font color="#c0504d">10个线程</font>（<font color="#9bbb59">仅新增</font>） | 3分20秒  | 80%           |         | 仅PDI程序内存增幅<br>且未发生FGC |
|    5     | 同上                                                                                                         | 同上   | -Xms1024m -Xmx2048m                              | 同上                                                      | 同上      | 插入/更新 <font color="#c0504d">5个线程</font>（<font color="#9bbb59">仅新增</font>）  | 5分0秒   | 40%           | 23%     | 仅PDI程序内存增幅<br>且未发生FGC |
|    6     | 同上                                                                                                         | 同上   | -Xms1024m -Xmx2048m                              | 同上                                                      | 同上      | 插入/更新 <font color="#c0504d">1个线程</font>（<font color="#f79646">仅更新</font>）  | 12分40秒 | 10%           | 7%      | 仅PDI程序内存增幅<br>且未发生FGC |
|    7     | 同上                                                                                                         | 同上   | -Xms1024m -Xmx2048m                              | 同上                                                      | 同上      | 插入/更新 <font color="#c0504d">1个线程</font>（<font color="#9bbb59">仅新增</font>）  | 22分10秒 | 10%           | 5%      | 仅PDI程序内存增幅<br>且未发生FGC |

# 数据校验_单月出院医嘱

## 场景信息

单表比对转换设计

![[Pasted image 20240407180443.png|700]]

## 测试汇总

| **场景**                     | EMR_R数据库选项                                  | **耗时** | **Linux'CPU** | PDI'CPU | **内存增幅**              |
| -------------------------- | ------------------------------------------- | ------ | ------------- | ------- | --------------------- |
| 202208单月数据同步<br>1061949条数据 | useCursorFetch=true<br>defaultFetchSize=500 | 1分     | 35%           | 28%     | 仅PDI程序内存增幅<br>且未发生FGC |


