# 概述

* Github：[GitHub - apache/skywalking: APM, Application Performance Monitoring System](https://github.com/apache/skywalking)
* 官方文档：[Apache SkyWalking](https://skywalking.apache.org/)
* 强烈推荐：[平安健康千亿级的全链路追踪系统的建设与实践](https://skywalking.apache.org/zh/2022-08-30-pingan-jiankang)

# 架构原理

**官网介绍图**

![[Pasted image 20231031105625.png|1000]]

**简易版的架构以及数据流转图**

![[Pasted image 20241008193512.png|600]]

这里有几处要解释一下：

1. Agent上报数据给OAP端，有gRPC通道和Kafka通道，当时就盲猜gRPC通道可能撑不住，所以选择Kafka通道来削峰；<font color="#f79646">Kafka通道是在8.x里加入的</font>。
2. 千亿级的数据用ES来做存储肯定是可以的。
3. 图中L1聚合的意思是：SkyWalking OAP服务端 接收数据后，构建metric并完成metric的Level-1聚合，这里简称L1聚合。
4. 图中L2聚合的意思是：服务端 基于metric的Level-1聚合结果，再做一次聚合，即Level-2聚合，这里简称L2聚合。后续把纯Mixed角色的集群拆成了两个集群。

# 服务端部署

## 单机部署

>没能成功，OAP启动都能成功，但是UI起不来，也没有报错，卡着不动~

### 1.SkyWalking OAP

<font color="#f79646">前提</font>

* JDK 1.8（启动SkyWalking OAP必须）
* 数据存储：Elasticsearch => [[虚拟机服务部署_CentOS-7#Elasticsearch + Kibana 7.16.2]]

1.下载安装包

地址：https://skywalking.apache.org/downloads

![[Pasted image 20231031150801.png|800]]

```
$ mkdir /opt/skywalking
$ wget https://dlcdn.apache.org/skywalking/9.0.0/apache-skywalking-apm-9.1.0.tar.gz
$ tar -zxvf apache-skywalking-apm-9.1.0.tar.gz
$ ll apache-skywalking-apm-bin/
total 88
drwxr-xr-x.  2 root root   241 Oct 31 11:23 bin
drwxr-xr-x. 12 root root  4096 Oct 31 11:23 config
drwxr-xr-x.  2 root root    68 Oct 31 11:23 config-examples
-rw-r--r--.  1 root root 27987 Feb 18  2022 LICENSE
drwxr-xr-x.  3 root root  4096 Oct 31 11:23 licenses
-rw-r--r--.  1 root root 30503 Feb 18  2022 NOTICE
drwxr-xr-x.  2 root root 12288 Feb 18  2022 oap-libs
-rw-r--r--.  1 root root  1951 Feb 18  2022 README.txt
drwxr-xr-x.  3 root root    30 Oct 31 11:23 tools
drwxr-xr-x.  2 root root    53 Oct 31 11:23 webapp
```

2.修改配置

```shell
$ vim /opt/skywalking/apache-skywalking-apm-bin/config/
```

```yml
storage:
  selector: ${SW_STORAGE:elasticsearch}
  elasticsearch:
    clusterNodes: ${SW_STORAGE_ES_CLUSTER_NODES:192.168.172.102:9200}
    user: ${SW_ES_USER:"elastic"}
    password: ${SW_ES_PASSWORD:"123456"}
```

3.启动

```
$ ./bin/oapService.sh 
SkyWalking OAP started successfully!
```

是否真正启动成功，打开 logs/skywalking-oap-server.log日志文件，查看是否有错误日志。 首次启动时，因为SkyWalking OAP会创建Elasticsearch的索引，所以会疯狂打印日志。

最终，我们看到如下日志，基本可以代表SkyWalking OAP服务启动成功：

```
2023-10-31 14:49:33,148 - org.apache.skywalking.oap.server.starter.OAPServerBootstrap - 53 [main] INFO  [] - Version of OAP: 9.1.0-f1f519c
```

### 2.SkyWalking UI

1.修改配置

如果想要修改SkyWalking UI服务的参数，可以编辑webapp/webapp.yml配置文件。

```
server:
  port: 8080

spring:
  cloud:
    discovery:
      client:
        simple:
          instances:
            oap-service:
              - uri: http://192.168.172.102:12800
```

2.启动

```
$ ./bin/webappService.sh 
SkyWalking Web Application started successfully!
```


## Docker Compose部署

![[虚拟机服务部署_CentOS_7#部署_SkyWalking 9.3.0]]

