# 文档操作


## 新增文档


## 查询文档


## 更新文档


## 删除文档


## 聚合操作


## 计算文档大小

```js
use coms;
var obj = db.mapperRouterLog.findOne();
Object.bsonsize(obj);                   // 单个时
Object.bsonsize([doc1,doc2,doc3]);      // 多个时
```

# 统计信息

[官方：db.stats() — MongoDB 手册](https://www.mongodb.com/zh-cn/docs/manual/reference/method/db.stats/)

## 查看集合统计信息

```js
db.status();
```

## 查看文档统计信息

```js
use coms;
db.mapperRouterLog.stats();          // 默认按byte显示
db.mapperRouterLog.stats(1024);      // 按kb显示数据
db.mapperRouterLog.stats(1024*1024); // 按mb显示数据
```

```js
{
    "ns" : "coms.mapperRouterLog",           // 名称攻坚
    "size" : 13509005.0,                     // 集合大小
    "count" : 5590.0,                        // 集合文档总数，可能不会准确，详见：https://www.mongodb.com/zh-cn/docs/manual/reference/method/db.stats说明
    "avgObjSize" : 2416.0,                   // 平均每个Obj大小
    "storageSize" : 8044544.0,               // 分配的存储空间，当删除集合中的文档时，该值并不会降低
    "capped" : false,                        // 是否固定集合
    "wiredTiger" : {                         // wiredTiger存储引擎相关信息
	    // 省略...
    },
    "nindexes" : 4.0,                        // 索引数量
    "totalIndexSize" : 475136.0,             // 索引占用磁盘大小
    "indexSizes" : {                         // 集合索引列表及每个索引占用大小
        "_id_" : 192512.0,
        "mapperMethodIdIndex" : 69632.0,
        "tLogIdIndex" : 102400.0,
        "createTimeIndex" : 110592.0
    },
    "ok" : 1.0
}

// ---------------- 按照kb显示数据 ----------------

{
    "ns" : "coms.mapperRouterLog",
    "size" : 13046.0,
    "count" : 5655.0,
    "avgObjSize" : 2362.0,
    "storageSize" : 7856.0,
    "capped" : false,
    "wiredTiger" : {
        // 省略...
    },
    "nindexes" : 4.0,
    "totalIndexSize" : 464.0,
    "indexSizes" : {
        "_id_" : 188.0,
        "mapperMethodIdIndex" : 68.0,
        "tLogIdIndex" : 100.0,
        "createTimeIndex" : 108.0
    },
    "ok" : 1.0
}
```

# mongo shell

mongo shell支持JS标准语法，因此可以在mongo shell中加入一些自定义的功能集。

编辑~/.mongorc.js文件，添加如下内容：

```js
function showDate() {
    var today = new Date();
    var year = today.getFullYear() + "年";
    var month = (today.getMonth() + 1) + "月";
    var date = today.getDate() + "日";
    var quarter = "一年中的第" + Math.floor((today.getMonth() + 3) /3)+"个季度";
    var text = "欢迎回来，今天是" + year + month + date + "，" + quarter + "。"
    print(text)
}

showDate()
// 执行结果：欢迎回来，今天是2024年3月19日，一年中的第1个季度。
```

上述代码，首先定义一个showDate函数，用于输出当前的日期信息。代码的最后对该函数做了一次调用。

将该文件保存，再次启动本地的mongo shell，便发现输出了想要的信息：
