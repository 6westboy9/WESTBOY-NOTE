经典：[美团-聊聊MyBatis缓存机制](https://tech.meituan.com/2018/01/19/mybatis-cache.html)
# 一级缓存

## 配置

## 实践

## 原理

有两个选项

- SESSION（默认）：一个MyBatis会话中执行的所有语句，都会共享这一个缓存
- STATEMENT：缓存只对当前执行的这一个Statement有效

## 总结

1. MyBatis一级缓存的生命周期和SqlSession一致。
2. MyBatis一级缓存内部设计简单，只是一个没有容量限定的HashMap，在缓存的功能性上有所欠缺。
3. MyBatis的一级缓存最大范围是SqlSession内部，有多个SqlSession或者分布式的环境下，数据库写操作会引起脏数据，建议设定缓存级别为Statement。

## 扩展

### Spring整合后一级缓存失效问题

* 程序执行了多次函数，调用相同的SQL，Mybatis默认开启了一级缓存，因此理论上来看，应该只有第一次是走了SQL。后续都是走缓存才对。但是实际上却每次都执行了SQL。
* Mybatis的一级缓存是通过SqlSession来实现的，对应的实现是DefaultSqlSession。 <font color="#c0504d">package org.apache.ibatis.session.defaults</font>
* 因为Spring管理了Mybatis，因此这个时候SqlSession的实现被替换成了SqlSessionTemplate。<font color="#c0504d">package org.mybatis.spring</font>
* SqlSessionTemplate中主要是通过JDK动态代理创建出了一个SqlSession代理对象。
* <font color="#f79646">因此每执行一次函数，哪怕SQL相同，Spring都会创建一个新的SqlSession</font>，并且在执行完毕之后，还会将事务提交、关闭SqlSession。因此多次请求之间无法通过SqlSession来共享缓存。
* 从而造成了多次执行，多次调用SQL、缓存失效的现象。

[Mybatis-Spring整合后一级缓存失效了](https://blog.csdn.net/Zong_0915/article/details/127125010)

# 二级缓存

在上文中提到的一级缓存中，其最大的共享范围就是一个SqlSession内部，如果多个SqlSession之间需要共享缓存，则需要使用到二级缓存。

## 配置

1.在MyBatis的配置文件中开启二级缓存。

```xml
<setting name="cacheEnabled" value="true"/>
```

2.在MyBatis的映射XML中配置`cache`或者`cache-ref`。

* `type`：cache使用的类型，默认是`PerpetualCache`，是对Cache接口最基本的实现，其实现非常简单，内部持有HashMap，对一级缓存的操作实则是对HashMap的操作。
- `eviction`：定义回收的策略，常见的有FIFO，LRU。
- `flushInterval`：配置一定时间自动刷新缓存，单位是毫秒。
- `size`：最多缓存对象的个数。
- `readOnly`：是否只读，若配置可读写，则需要对应的实体类能够序列化。
- `blocking`：若缓存中找不到对应的key，是否会一直blocking，直到有对应的数据进入缓存。

`cache-ref`代表引用别的命名空间的Cache配置，两个命名空间的操作使用的是同一个Cache。

```xml
<cache-ref namespace="mapper.StudentMapper"/>
```

## 实践

```xml
<cache type="com.lachesis.windranger.emr.cache.MybatisRedisCache" eviction="LRU"
      flushInterval="6000000" size="1024" readOnly="false"/>
```


>缓存命中的关键词<font color="#f79646">Cache Hit Ratio</font>在<font color="#f79646">DEBUG</font>日志中~

```
-- 第一次查询
2024-05-24 09:50:25.917 [MRHandler-1] DEBUG c.l.windranger.emr.dao.PatInhosRecordMapperExt - Cache Hit Ratio [com.lachesis.windranger.emr.dao.PatInhosRecordMapperExt]: 0.0
2024-05-24 09:50:26.278 [MRHandler-1] DEBUG c.l.w.e.dao.PatInhosRecordMapperExt.getPatForMnis - ==>  Preparing: select a.* from pat_inhos_record a where 1=1 and status != '2' and a.inhos_code = ? 
2024-05-24 09:50:26.320 [MRHandler-1] DEBUG c.l.w.e.dao.PatInhosRecordMapperExt.getPatForMnis - ==> Parameters: 17124459(String)
2024-05-24 09:50:26.372 [MRHandler-1] DEBUG c.l.w.e.dao.PatInhosRecordMapperExt.getPatForMnis - <==      Total: 1
-- 第二次查询
2024-05-24 09:50:26.727 [MRHandler-2] DEBUG c.l.windranger.emr.dao.PatInhosRecordMapperExt - Cache Hit Ratio [com.lachesis.windranger.emr.dao.PatInhosRecordMapperExt]: 0.5
```

## 原理


## 总结

1. MyBatis的二级缓存相对于一级缓存来说，实现了`SqlSession`之间缓存数据的共享，同时粒度更加的细，能够到`namespace`级别，通过Cache接口实现类不同的组合，对Cache的可控性也更强。
2. MyBatis在多表查询时，极大可能会出现脏数据，有设计上的缺陷，安全使用二级缓存的条件比较苛刻。
3. 在分布式环境下，由于默认的MyBatis Cache实现都是基于本地的，分布式环境下必然会出现读取到脏数据，需要使用集中式缓存将MyBatis的Cache接口实现，有一定的开发成本，直接使用Redis、Memcached等分布式缓存可能成本更低，安全性也更高。
	- <font color="#c0504d">补充：对于服务A和服务B都采用了二级缓存，那必须适用Redis等分布式缓存，且服务A和服务B配置的缓存策略实现必须一致！</font>

# 全文总结

MyBatis缓存特性在生产环境中进行关闭，单纯作为一个ORM框架使用可能更为合适！