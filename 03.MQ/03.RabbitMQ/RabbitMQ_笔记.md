入门推荐资料：[专辑：RabbitMQ专题-Java充电社](http://itsoku.com/course/22)

# RabbitMQ概念


## 核心概念


- 生产者
- 消费者
- 交换机
- 队列

## 核心部分


![[Pasted image 20240603112849.png|500]]

- <font color="#f79646">Broker</font>：接收和分发消息的应用，RabbitMQ Server就是Message Broker。
- <font color="#f79646">Virtual Host</font>：出于多租户和安全因素设计的，把AMQP的基本组件划分到一个虚拟的分组中，类似于网络中的namespace概念。当多个不同的用户使用同一个RabbitMQServer提供的服务时，可以划分出多个vhost，每个用户在自己的vhost创建Exchange/Queue等。
- <font color="#f79646">Connection</font>：Poducer/Consumer和Broker之间的TCP连接。
- <font color="#f79646">Channel</font>：
	- 如果每一次访问RabbitMQ都建立一个TCP连接，在消息量大的时候建立TCP连接的开销将是巨大的，效率也较低。
	- Channel是在Connection内部建立的逻辑连接，如果应用程序支持多线程，通常每个Thread创建单独的Channel进行通讯，Channel之间是完全隔离的。Channel作为轻量级的Connection极大减少了操作系统建立TCP连接的开销。
- <font color="#f79646">Exchange</font>：消息到达Broker的第一站，根据分发规则，匹配查询表中的routingkey，分发消息到Queue中去。常用的类型有：
	- `direct` = `point-to-point`
	- `topic` = `publish-subscribe`
	- `fanout` = `multicast`
- <font color="#f79646">Queue</font>：消息最终被送到这里等待Consumer取走。
- <font color="#f79646">Binding</font>：Exchange和Queue之间的虚拟连接，绑定信息被保存到Exchange中的查询表中，用于消息的分发依据。

# Exchanges


RabbitMQ消息传递模型的<font color="#f79646">核心思想</font>：生产者生产的消息从不会直接发送到队列。

- 实际上，通常生产者甚至都不知道这些消息传递传递到了哪些队列中。
- 生产者只能将消息发送到交换机，交换机工作的内容非常简单， 一方面它接收来自生产者的消息，另一方面将它们推入队列。
- 交换机必须确切知道如何处理收到的消息？是应该把这些消息放到特定队列还是说把他们到许多队列中还是说应该丢弃它们， 这就的由交换机的类型来决定。

## 交换机的类型

* direct
* topic
* headers
* fanout

## 无名交换机


# Queue


## 临时队列


# Binding






