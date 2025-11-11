<font color="#f79646">鲁班老师的藏宝图项目</font>


# 部署

![[Pasted image 20231116163412.png|325]]


## 1.启动ES

docker-compose.yml

```yml
version: '3.3'
services:
  elasticsearch:
    image: elasticsearch:5.6.6
    command: -Ecluster.name=cbt_es -Etransport.host=0.0.0.0
    ports:
      - "9200:9200"
      - "9300:9300"
    environment:
      - "discovery.type=single-node"
  kibana:
    image: kibana:5.6.6
    environment:
        - "ELASTICSEARCH_HOSTS=http://elasticsearch:9200/"
    ports:
      - "5601:5601"
    links:
     - elasticsearch
```

可能起不来，需要设置：

```
sudo sysctl -w vm.max_map_count=262144
```

## 2.启动cbt-server


注册（没有注册过时）

登录（已经注册了）
* user
* user


# 解剖


## 项目


* 项目下有多个用户
* 项目下有多个应用

应用加入项目

* 手动注册
* 自动注册（心跳保活）

## 系统快照
### 设计思路

所谓快照就是用例

* 基本信息
	* 标签
	* 创建人
	* 创建时间
	* 更新人
	* 更新时间
* 执行逻辑
* 快照版本（历史快照）
* 快照周期（存在时长）

快照一定要保证实时性，需要有一个新鲜度，即保质期。

比如最新执行一次对应的版本是：v1.5版本，这样才能与上一个版本v1.4进行比较。

快照应该以线上运行版本为主。

快照可能是跨应用的，所以设计快照所属应用属性严格一点是<font color="#f79646">不合理</font>的。

### 快照实现

* 视频节点：11章1:20:00左右
* 对应模块：apm-server

<font color="#f79646">点击测试用例 -> 生成链路信息 -> 保存快照</font>

保存快照的底层逻辑
* 查询TraceID下所有节点
* 解析节点（包括SQL、远程调用和本地方法调用）
* 保存入库

保存的时候会选择相应的快照信息

![[Pasted image 20231030232719.png|600]]

<font color="#f79646">快照存储数据结构设计</font>

ES的Nested和Object类型区别

### 存储内容


<font color="#f79646">数据库操作</font>

SQL的解析工具类（会进行抽象语法树解析）：com.alibaba.druid.sql.SQLUtils

<font color="#f79646">执行代码</font>

作者没有记录执行代码行号

<font color="#f79646">远程调用</font>

![[Pasted image 20231030234155.png|800]]


## 系统地图

有是个什么东西呢？

依赖关系

![[Pasted image 20231031231730.png|800]]

快照和应用的关系

![[Pasted image 20231031235807.png|675]]