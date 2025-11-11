>MongoDB由C++语言实现

官网：https://github.com/mongodb/mongo

# 数据模型

## BSON协议

[BSON官方文档](https://bsonspec.org/)

大多数情况下，使用JSON作为数据交互格式已经是理想的选择，<font color="#f79646">但是JSON基于文本的解析效率并不是最好的</font>，在某些场景下往往会考虑选择更合适的编/解码格式，一些做法如：

- 在微服务架构中，使用gRPC（基于Google的Protobuf）可以获得更好的网络利用率。
- 分布式中间件、数据库，使用私有定制的TCP数据包格式来提供高性能、低延时的计算能力。

BSON（Binary JSON）即二进制版的JSON。<font color="#f79646">其在性能方面有更优的表现</font>。BSON在许多方面和JSON保持一致，其同样也支持内嵌的文档对象和数组结构。<font color="#f79646">二者最大的区别在于JSON是基于文本的，而BSON则是二进制（字节流）编/解码的形式。除此之外，BSON还提供了一些扩展的数据类型，比如日期、二进制数据等</font>。

BSON由10gen团队设计并开源，目前主要用于MongoDB数据库。

MongoDB在文档存储、命令协议上都采用了BSON作为编/解码格式，主要具有如下<font color="#f79646">优势</font>：

- <font color="#c0504d">类JSON的轻量级语义</font>，支持简单清晰的嵌套、数组层次结构，可以实现无模式（模式灵活）的文档结构。
- <font color="#c0504d">更高效的遍历</font>，BSON在编码时会记录每个元素的长度，可以直接通过seek操作进行元素的内容读取，相对JSON解析来说，遍历速度更快。
	- 对JSON格式来说，太大的JSON结构会导致数据遍历非常慢。在JSON中，要跳过一个文档进行数据读取，需要对此文档进行扫描才行，需要进行麻烦的数据结构匹配，比如括号的匹配，而BSON对JSON的一大改进就是，它会将JSON的每一个元素的长度存在元素的头部，这样你只需要读取到元素长度就能直接seek到指定的点上进行读取了。
- <font color="#c0504d">更丰富的数据类型</font>，除了JSON的基本数据类型，BSON还提供了MongoDB所需的一些扩展类型，这更加方便数据的表示和操作。

<font color="#f79646">劣势：在空间的使用上，BSON相比JSON并没有明显的优势！</font>

## BSON数据类型

JSON数据六种类型：
1. 字符串
2. 数字
3. JSON对象
4. 数组
5. 布尔
6. Null

[官方文档BSON类型](https://docs.mongoing.com/mongo-introduction/bson-types)

BSON数据类型：
1. Double
2. String
3. Object
4. Array
5. Binary data
6. ObjectId
7. Boolean
8. Date
9. Null
10. Regular Expression
11. Timestamp
12. 64-bit integer
13. Decimal128
14. Min key
15. Max key
16. 等等具体可以查看官方文档，部分已经不推荐使用了...

## ObjectId

MongoDB集合中所有的文档都有一个唯一的_id字段，作为集合的主键。在默认情况下，_id字段使用ObjectId类型。如下面的代码：

```json
{
	"_id" : ObjectId("65f9298554f517cc47b9d509")
}
```

这里的_id是自动生成的，其中`65f9298554f517cc47b9d509`是ObjectId的<font color="#f79646">16进制编码</font>形式，该字段总共为<font color="#f79646">12个字节</font>。

分为3个部分：

* 4个字节表示Unix时间戳（单位秒）
* 5个字节表示随机数
* 3个字节表示计数器

因此：

* <font color="#f79646">可以保证唯一性</font>：经过多个字段随机组合后，出现重复的概率是极低的。
	* 虽然可能出现重复概率，但是默认情况下，MongDB在创建集合期间会在`_id`字段上创建唯一索引。
	* 其实为服务端存储时保证唯一性，但是在客户端生成时可能会重复。
* <font color="#f79646">无法保证单调性</font>：尽管ObjectId值应随时间增加，但不一定是单调的。这是因为他们：
	- 仅包含一秒的时间分辨率，因此 在同一秒内创建的ObjectId值没有保证的顺序。
	- 并且由客户端生成（<font color="#c0504d">比如MongDB Java Driver</font>），客户端可能具有不同的系统时钟。

## 日期

MongoDB中的日期使用Date类型表示，在其内部实现中采用了一个64位长的整数，该整数代表的是自1970年1月1日零点时刻（UTC）以来所经过的毫秒数。Date类型的数值范围非常大，<font color="#f79646">可以表示上下2.9亿年的时间范围</font>，负值则表示1970年之前的时间。

MongoDB的日期类型使用UTC（Coordinated Universal Time）进行存储，也就是+0时区的时间。一般客户端会根据本地时区自动转换为UTC时间，代码如下：

```js
new Date();
// 结果: ISODate("2024-03-19T13:50:03.750+08:00") 可以看到+08:00为东八区
```

在这里，ISODate是对于UTC时间的包装类。

```js
var d1 = Date();         // 比ISODate多8小时！！！
var d2 = new Date();     // 语义与ISODate相同
var d3 = ISODate();
var obj = {
    date1: d1,
    date2: d2,
    date3: d3
}

db.dates.insert(obj);
db.dates.find({});
```

返回结果：

```js
{
	"_id" : ObjectId("65f9298554f517cc47b9d509"),
	"date1" : "Tue Mar 19 2024 13:58:29 GMT+0800 (中国标准时间)", // 比ISODate多8小时！！！
	"date2" : ISODate("2024-03-19T13:58:29.844+08:00"),         // 语义与ISODate相同
	"date3" : ISODate("2024-03-19T13:58:29.844+08:00")
}
```

可以看到，<font color="#f79646">使用new Date与ISODate的语义是相同的</font>，两者最终都会生成ISODate类型的字段（对应于UTC时间）。而Date与两者都不同，它会以字符串形式返回当前的系统时间。由于当前正处于+8时区（北京标准时间），因此输出的时间值比ISODate多8个小时。

```js
print(typeof(Date()))        // string
print(typeof(new Date()))    // object
print(typeof(ISODate()))     // object
```


## 固定集合

>数据写入时遵循<font color="#f79646">FIFO</font>原则！


```js
// capped:true 表示固定集合
// size(必选) 指定集合空间占用最大值，一般为2的n次方，单位是kb
// max(可选) 指定集合文档数量最大值

// 这两个参数会同时对集合的上限产生影响。也就是说，只要任一条件达到阈值都会认为集合已经写满。其中size是必选的，而max则是可选的！
db.createCollection("testLogs", {capped:true,size:100,max:10})
// 查看文档统计信息
db.testLogs.stats()
{
	"ns" : "test.testLogs",
	"size" : 0,
	"count" : 0,
	"storageSize" : 4096,
	"capped" : true,
	"max" : 10,        // 10为文档数量最大值
	"maxSize" : 256,   // 256则是文档总大小的上限，必须为2的n次方，这里我们设置为的100，会被自动对齐为256
	"sleepCount" : 0,
	"sleepMS" : 0,
	"wiredTiger" : {
		// ...
	},
	"nindexes" : 1,
	"totalIndexSize" : 4096,
	"indexSizes" : {
		"_id_" : 4096
	},
	"ok" : 1
}
```

### 特征

固定集合在底层使用的是<font color="#f79646">顺序I/O</font>操作，而普通集合使用的是<font color="#f79646">随机I/O</font>。众所周知，顺序I/O在磁盘操作上由于寻道次数少而比随机I/O要高效得多，因此<font color="#f79646">固定集合的写入性能是很高的</font>。此外，如果按写入顺序进行数据读取，也会获得非常好的性能表现。

### 限制

* <font color="#c0504d">无法动态修改存储的上限</font>，如果需要修改max或size，则只能先执行collection.drop命令，将集合删除后再重新创建。
* <font color="#c0504d">无法删除已有的数据</font>。
* <font color="#c0504d">对已有数据进行修改，新文档大小必须与原来的文档大小一致</font>，否则不允许更新。
* 默认情况下，固定集合只有一个_id索引，而且最好是按数据写入的顺序进行读取。当然，也可以添加新的索引，但这会降低数据写入的性能。
* <font color="#c0504d">固定集合不支持分片</font>，同时，在MongoDB 4.2版本中规定了事务中也无法对固定集合执行写操作。

### 适合场景


# 索引



## 索引类型

* 单字段索引：对单个字段创建索引
* 复合索引：对多个字段创建索引
* 多键索引：对数组中的每个元素创建索引
* 文本索引
* 通配符索引
* 地理空间索引
* 哈希索引

## 索引属性

* 唯一索引
* TTL索引
* 稀疏索引


# 时间序列集合

> MongDB 5.0版本新增


# 副本集

>主节点

主节点是副本集中唯一接受写入操作的节点。MongoDB在主节点上应用写入操作，然后将这些操作记录到主节点的<font color="#f79646">oplog</font>中。从节点复制该oplog，并将记录的操作应用于其数据集。

在以下三节点副本集中，主节点接受所有写入操作。然后，从节点复制oplog以应用于其数据集。

![[Pasted image 20240319164113.png|300]]

副本集的所有节点都可以接受读取操作。但是，默认情况下，应用程序将其读取操作定向到主节点。

* 写：仅在主节点上。
* 读：默认也是主节点，可修改读取从节点。

副本集最多可以有一个主节点。

>从节点

![[Pasted image 20240319164546.png|300]]

# 分片

分片是指在将数据进行水平切分之后，将其存储到多个不同的服务器节点上的一种扩展方式。分片在概念上非常类似于应用开发中的<font color="#f79646">水平分表</font>。不同的点在于，MongoDB本身就自带了分片管理的能力，对于开发者来说可以做到开箱即用。

下图为生产重使用的常见分片集群部署架构：

![[Pasted image 20240319164916.png|600]]

* 数据分片：分片用于存储真正的数据，并提供最终的数据读写访问。分片仅仅是一个逻辑的概念，它可以是一个单独的mongod实例，也可以是一个副本集。在生产环境中也一般会使用副本集的方式，这是为了防止数据节点出现单点故障。
* 配置服务（Config Server）：配置服务器包含多个节点，并组成一个副本集结构。<font color="#f79646">配置副本集中保存了整个分片集群中的元数据</font>，其中包含各个集合的分片策略，以及分片的路由表等。
* 查询路由（Mongos）：Mongos是分片集群的访问入口，其<font color="#f79646">本身并不持久化数据</font>。
	* Mongos启动后，会从配置服务器中加载元数据。之后Mongos开始提供访问服务，并将用户的请求路由到对应的分片。
	* 在分片集群中可以部署多个Mongos以分担客户端请求的压力。


仅用于开发目的的分片集群架构：

![[Pasted image 20240319165011.png|600]]

