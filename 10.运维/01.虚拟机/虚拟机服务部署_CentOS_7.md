# 虚拟机

## 1.准备

>Win10+VMware17+CentOS7

## 2.使用镜像

>镜像版本：CentOS-7-x86_64-Minimal-2009.iso

## 3.VMWare16安装系统

>User Account：root/@Wpb1993

## 4.配置网络

这里需要与宿主机所在局域网互通，并实现虚拟机可以访问外网。参考资料：[VMWare16虚拟机CentOS7的网络设置桥接模式](https://blog.csdn.net/sulia1234567890/article/details/123437096)

```
[root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-ens33 
TYPE=Ethernet
PROXY_METHOD=none
BROWSER_ONLY=no
BOOTPROTO=static                      <---
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=yes
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens33
UUID=a2bffa6a-58ee-4fcb-978f-82b3e46f8255
DEVICE=ens33
ONBOOT=yes                            <---
IPADDR=10.2.43.66                     <---
NETMASK=255.255.255.0                 <---
GATEWAY=10.2.43.1                     <---
DNS1=10.2.3.74                        <---
DNS2=114.114.114.114                  <---
DNS3=8.8.8.8
DNS4=4.2.2.2
```

```
systemctl restart network.service
```

## 5.基础配置

### VIM

```bash
yum install -y vim
```

### 时间同步

设置时区

```bash
# 查看时区
timedatectl status|grep 'Time zone'
# 设置硬件时钟调整为与本地时钟一致
timedatectl set-local-rtc 1
# 设置时区为上海
timedatectl set-timezone Asia/Shanghai
```

使用ntpdate同步时间

```bash
# 安装ntpdate
yum -y install ntpdate
# 同步时间
ntpdate -u cn.ntp.org.cn
# 同步完成后查看时间是否正确
date
```

另外再分享下几个常用的ntp server，如果需要更多可以前往[http://www.ntp.org.cn](http://www.ntp.org.cn/)获取。

```bash
#中国
cn.ntp.org.cn
#中国香港
hk.ntp.org.cn
#美国
us.ntp.org.cn
```
同步时间后可能部分服务器过一段时间又会出现偏差，因此最好设置crontab来定时同步时间，方法如下：  

```sh
# 创建crontab任务
crontab -e
# 添加定时任务（每20分钟进行一次时间同步）
*/20 * * * * /usr/sbin/ntpdate pool.ntp.org > /dev/null 2>&1
# 每分钟执行一次
*/5 * * * * /usr/sbin/ntpdate pool.ntp.org > /dev/null 2>&1
# 重启crontab
service crond reload
# 查看执行记录
tailf /var/log/cron
```

注意/usr/sbin/ntpdate为ntpdate命令所在的绝对路径，不同的服务器可能路径不一样，可以使用which命令来找到绝对路径:

```bash
[root@localhost ~]# which ntpdate
/usr/sbin/ntpdate
```

### 关闭防火墙

```bash
systemctl status firewalld.service
systemctl stop firewalld.service
systemctl disable firewalld.service
```

# 拓扑

| 计算机 | IP | 网络模式 | 来源 | 基础程序安装 | 备注 |
| ---- | ---- | ---- | ---- | ---- | ---- |
| CentOS_7_64_001 | 10.2.43.66（可能存在IP冲突） | 桥接模式 | BASE |  | 不打算用了~ |
| CentOS_7_64_002 | 192.168.172.102 |  | COPY FROM BASE | Docker 24.0.7 + Docker Compose | 暂时留着 |
| CentOS_7_64_003 | 10.2.43.67（可能存在IP冲突） | 桥接模式 | COPY FROM BASE | Redis+MySQL+夜莺+VM时序数据库，目前主要10.2.3.167的MySQL，Linux，ShardingSphere-Proxy使用 | 暂时留着 |
| CentOS-001 | 10.2.43.66（替换旧的虚拟机） | 桥接模式 | BASE |  |  |
注意[Docker Compose的文件格式与Docker的版本兼容性](https://blog.csdn.net/whatday/article/details/108865782)

# Docker 24.0.7

## 安装

Docker从1.13.x版本开始，版本分为企业版EE和社区版CE，版本号也改为按照时间线来发布，比如17.03就是2017年3月。

* 安装：[https://cloud.tencent.com/developer/article/1701451](https://cloud.tencent.com/developer/article/1701451)
* 版本： Standalone 18.03.1-ce
* 官方文档：https://tutorials.tinkink.net/zh-hans/linux/how-to-install-docker-on-centos-7.html


基础命令：

```shell
$ systemctl start docker
$ systemctl status docker
$ docker --version
$ docker info
$ docker -v
Docker version 24.0.7, build afdd53b
```

## 使用国内镜像源


```shell
$ vi /etc/docker/daemon.json
```

```json
{
	"registry-mirrors": [
		"https://registry.docker-cn.com",
		"https://docker.mirrors.ustc.edu.cn",
		"http://hub-mirror.c.163.com",
		"https://cr.console.aliyun.com/"
	]
}
```

```shell
$ systemctl restart docker
```

## <font color="#c0504d">挂梯子</font>

https://blog.csdn.net/2401_85480529/article/details/139693869

## 部署_Portainer 2.16

```shell
mkdir -p /opt/docker-volumes/portainer/data

# 随Docker自启动
docker run -d -p 8000:8000 -p 9000:9000 --name portainer --restart=always \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /etc/localtime:/etc/localtime \
-v /opt/docker-volumes/portainer/data:/data \
portainer/portainer-ce
```

页面地址：http://10.2.43.68:9000

```
账号: admin
密码: Lx_123456789
```
## 部署_MySQL 8.0.21

``` shell
# 准备
mkdir -p /opt/docker-volumes/mysql_8.0.21
docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:8.0.21
# 复制容器中数据与配置
docker cp [CONTAINER_ID]:/var/lib/mysql /opt/docker-volumes/mysql_8.0.21/data
docker cp [CONTAINER_ID]:/etc/mysql/conf.d /opt/docker-volumes/mysql_8.0.21/conf.d
docker cp [CONTAINER_ID]:/etc/mysql/my.cnf /opt/docker-volumes/mysql_8.0.21/my.cnf

docker cp mysql:/var/lib/mysql /opt/docker-volumes/mysql_8.0.21/data
docker cp mysql:/etc/mysql/conf.d /opt/docker-volumes/mysql_8.0.21/conf.d
docker cp mysql:/etc/mysql/my.cnf /opt/docker-volumes/mysql_8.0.21/my.cnf

# 删除默认容器
docker stop [CONTAINER_ID]
docker rm [CONTAINER_ID]

docker stop mysql
docker rm mysql

# 新建并运行容器
docker run  -d \
--name mysql8 \
--privileged=true \
-p 3306:3306 \
-v /opt/docker-volumes/mysql_8.0.21/data:/var/lib/mysql \
-v /opt/docker-volumes/mysql_8.0.21/conf.d:/etc/mysql/conf.d \
-v /opt/docker-volumes/mysql_8.0.21/my.cnf:/etc/mysql/my.cnf \
-v /etc/localtime:/etc/localtime \
-e MYSQL_ROOT_PASSWORD=123456 \
mysql:8.0.21 \
--default-time-zone=+8:00
```

客户端连接时报错：Caused by: com.zaxxer.hikari.pool.HikariPool$PoolInitializationException: Failed to initialize pool: Unable to load authentication plugin 'caching_sha2_password'.

```
MySQL配置文件目录: /etc/mysql
端口: 3306
账号: root
密码: 123456
```

如果登录不上去，可以创建用户并授权：

```SQL
CREATE USER 'user'@'%' IDENTIFIED BY 'Lachesis-mh_1024';  
GRANT ALL ON *.* TO 'user'@'%';
```

启用3个MySQL节点

```shell
# 准备
mkdir -p /opt/docker-volumes/mysql_8.0.21_01
mkdir -p /opt/docker-volumes/mysql_8.0.21_02
mkdir -p /opt/docker-volumes/mysql_8.0.21_03

docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -d mysql:8.0.21

# 复制容器中数据与配置
docker cp mysql:/var/lib/mysql /opt/docker-volumes/mysql_8.0.21_01/data      # docker cp 5c19ac73a479:/var/lib/mysql /opt/docker-volumes/mysql_8.0.21_01/data
docker cp mysql:/var/lib/mysql /opt/docker-volumes/mysql_8.0.21_02/data
docker cp mysql:/var/lib/mysql /opt/docker-volumes/mysql_8.0.21_03/data

docker cp mysql:/etc/mysql/conf.d /opt/docker-volumes/mysql_8.0.21_01/conf.d # docker cp 5c19ac73a479:/etc/mysql/conf.d /opt/docker-volumes/mysql_8.0.21_01/conf.d
docker cp mysql:/etc/mysql/conf.d /opt/docker-volumes/mysql_8.0.21_02/conf.d
docker cp mysql:/etc/mysql/conf.d /opt/docker-volumes/mysql_8.0.21_03/conf.d

docker cp mysql:/etc/mysql/my.cnf /opt/docker-volumes/mysql_8.0.21_01/my.cnf # docker cp 5c19ac73a479:/etc/mysql/my.cnf /opt/docker-volumes/mysql_8.0.21_01/my.cnf
docker cp mysql:/etc/mysql/my.cnf /opt/docker-volumes/mysql_8.0.21_02/my.cnf
docker cp mysql:/etc/mysql/my.cnf /opt/docker-volumes/mysql_8.0.21_03/my.cnf

# 删除默认容器
docker stop mysql # docker stop 5c19ac73a479
docker rm mysql   # docker rm 5c19ac73a479

# 新建并运行容器
docker run  -d \
--name mysql8-1 \
--privileged=true \
-p 3311:3306 \
-v /opt/docker-volumes/mysql_8.0.21_01/data:/var/lib/mysql \
-v /opt/docker-volumes/mysql_8.0.21_01/conf.d:/etc/mysql/conf.d \
-v /opt/docker-volumes/mysql_8.0.21_01/my.cnf:/etc/mysql/my.cnf \
-v /etc/localtime:/etc/localtime \
-e MYSQL_ROOT_PASSWORD=123456 \
mysql:8.0.21 \
--default-time-zone=+8:00

docker run  -d \
--name mysql8-2 \
--privileged=true \
-p 3312:3306 \
-v /opt/docker-volumes/mysql_8.0.21_02/data:/var/lib/mysql \
-v /opt/docker-volumes/mysql_8.0.21_02/conf.d:/etc/mysql/conf.d \
-v /opt/docker-volumes/mysql_8.0.21_02/my.cnf:/etc/mysql/my.cnf \
-v /etc/localtime:/etc/localtime \
-e MYSQL_ROOT_PASSWORD=123456 \
mysql:8.0.21 \
--default-time-zone=+8:00

docker run  -d \
--name mysql8-3 \
--privileged=true \
-p 3313:3306 \
-v /opt/docker-volumes/mysql_8.0.21_03/data:/var/lib/mysql \
-v /opt/docker-volumes/mysql_8.0.21_03/conf.d:/etc/mysql/conf.d \
-v /opt/docker-volumes/mysql_8.0.21_03/my.cnf:/etc/mysql/my.cnf \
-v /etc/localtime:/etc/localtime \
-e MYSQL_ROOT_PASSWORD=123456 \
mysql:8.0.21 \
--default-time-zone=+8:00
```

## 部署_RestCloud

官方Docker安装文档：[RestCloud数据集成平台](https://www.etlcloud.cn/restcloud/view/page/helpDocument.html?id=648ac032c5ccee14c6641a94#title11)

```
# 1.拉取镜像
docker pull restcloud/restcloud-etl:V2.6

# 2.创建容器中mongodb数据库要映射的文件夹
mkdir -p /opt/docker-volumes/restcloud_etl/mongodb/db

# 3.执行启动镜像
docker run -d --restart=always \
--restart=on-failure:5 \
--privileged=true \
--name restcloud-etl-V2.6 \
-v /opt/docker-volumes/restcloud_etl/mongodb/db:/data/mongodb/db \
-p 8080:8080 \
-p 27017:27017 \
restcloud/restcloud-etl:V2.6
```

- http://{IP}:8080/restcloud/admin/login
- 登录账号：admin
- 登陆密码：pass

详细情况见官方文档。


## 部署\_Clickhouse_单节点

```bash
$ mkdir -p /opt/docker-volumes/clickhouse/data /opt/docker-volumes/clickhouse/conf /opt/docker-volumes/clickhouse/log
$ docker run -d --name clickhouse-server --ulimit nofile=262144:262144 -p 9000:9000 yandex/clickhouse-server
```

## 部署\_MongDB_单节点


参考资料：[使用Docker部署MongDB单节点副本集](https://blog.csdn.net/weixin_39786582/article/details/131225646)


## 部署_禅道 20.0

官网：https://www.zentao.net/page/download.html

```
$ docker pull hub.zentao.net/app/zentao:20.0
```


## 部署_Redis

```
docker run --name redis \
-p 6379:6379 \
-v /docker-data/redis/redis.conf:/etc/redis/redis.conf \
-v /docker-data/redis:/data \
-d redis redis-server /etc/redis/redis.conf --appendonly yes
```

**说明：**

- -p 6379:6379：端口映射，前面是[宿主机](https://cloud.tencent.com/product/cdh?from_column=20065&from=20065)，后面是容器。
- –name redis：指定该容器名称。
- -v 挂载文件或目录：前面是宿主机，后面是容器。
- -d redis redis-server /etc/redis/redis.conf：表示后台启动redis，以配置文件启动redis，加载容器内的conf文件。
- appendonly yes：开启redis 持久化。

# Docker Compose 1.27.4

## 安装

* 注意[Docker Compose的文件格式与Docker的版本兼容性](https://blog.csdn.net/whatday/article/details/108865782)
* 对应的映射关系查看[发布页面](https://github.com/docker/compose/releases)

这里Docker的版本是24.0.7，对应兼容Docker Compose版本是Docker Compose 1.27.4。

<font color="#4f81bd">1.从GitHub下载文件</font>

```
curl -L https://github.com/docker/compose/releases/download/1.27.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
```

由于在Linux中执行命令下载实在太慢或者无法下载，直接下载到本地，再将该文件上传至目标服务`/usr/local/bin`目录下，并命名为docker-compose即可。

<font color="#4f81bd">2.添加执行权限和软连接</font>

```shell
# 添加执行权限
$ chmod +x /usr/local/bin/docker-compose
# 添加软连接
$ ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
# 查看版本信息
$ docker-compose -v
```

## 部署_Pinpoint 2.5.3

* 注意查看Pinpiont的Docker版本要求，当前官方文档中所要求的最低版本是18.02.0+。
* 文档链接：[GitHub -Official Dockerized components of the Pinpoint](https://github.com/pinpoint-apm/pinpoint-docker#pinpoint-docker-for-pinpoint)

下载地址：

```
git clone https://github.com/pinpoint-apm/pinpoint-docker.git
```

如果不想在服务器上配置Git的话，可以直接下载。

```shell
$ pwd
/opt/docker-compose/pinpoint
$ ll
total 7860
drwxr-xr-x. 14 root root    4096 Oct 11 10:44 pinpoint-docker-2.5.3
-rw-r--r--.  1 root root 8043182 Oct 30 15:59 pinpoint-docker-2.5.3.zip
$ cd pinpoint-docker-2.5.3
$ ll
total 48
-rw-r--r--. 1 root root  8404 Oct 11 10:44 docker-compose-metric.yml
-rw-r--r--. 1 root root 10623 Oct 11 10:44 docker-compose.yml
drwxr-xr-x. 2 root root    22 Oct 11 10:44 docs
-rw-r--r--. 1 root root 11355 Oct 11 10:44 License
drwxr-xr-x. 3 root root    92 Oct 11 10:44 pinpoint-agent
drwxr-xr-x. 4 root root    32 Oct 11 10:44 pinpoint-agent-attach-example
drwxr-xr-x. 3 root root    92 Oct 11 10:44 pinpoint-batch
drwxr-xr-x. 3 root root   117 Oct 11 10:44 pinpoint-collector
drwxr-xr-x. 4 root root   110 Oct 11 10:44 pinpoint-flink
drwxr-xr-x. 3 root root   134 Oct 11 10:44 pinpoint-hbase
drwxr-xr-x. 2 root root    79 Oct 11 10:44 pinpoint-mysql
drwxr-xr-x. 3 root root    92 Oct 11 10:44 pinpoint-quickstart
drwxr-xr-x. 3 root root   117 Oct 11 10:44 pinpoint-web
drwxr-xr-x. 2 root root    32 Oct 11 10:44 pinpoint-zookeeper
-rw-r--r--. 1 root root 10874 Oct 11 10:44 Readme.md
$ docker-compose pull && docker-compose up -d
Pulling pinpoint-mysql      ... done
Pulling zoo1                ... done
Pulling pinpoint-hbase      ... done
Pulling pinpoint-batch      ... done
Pulling pinpoint-collector  ... done
Pulling pinpoint-agent      ... done
Pulling pinpoint-quickstart ... done
Pulling pinpoint-web        ... done
Pulling zoo2                ... done
Pulling zoo3                ... done
Pulling jobmanager          ... done
Pulling taskmanager         ... done
Creating network "pinpoint-docker-253_pinpoint" with driver "bridge"
Creating volume "pinpoint-docker-253_data-volume" with default driver
Creating volume "pinpoint-docker-253_mysql_data" with default driver
Creating volume "pinpoint-docker-253_hbase_data" with default driver
Creating pinpoint-docker-253_zoo3_1 ... done
Creating pinpoint-docker-253_zoo2_1 ... done
Creating pinpoint-docker-253_zoo1_1 ... done
Creating pinpoint-mysql             ... done
Creating pinpoint-flink-jobmanager  ... done
Creating pinpoint-hbase             ... done
Creating pinpoint-flink-taskmanager ... done
Creating pinpoint-collector         ... done
Creating pinpoint-web               ... done
Creating pinpoint-batch             ... done
Creating pinpoint-agent             ... done
Creating pinpoint-quickstart        ... done
```

漫长的等待后~

访问页面：http://10.2.43.101:8080

![[Pasted image 20231030171351.png|900]]

其中关于MySQL、HBase相关服务的用户名和密码均在/opt/docker-compose/pinpoint/pinpoint-docker-2.5.3/.env文件中。

停止所有服务

```shell
$ docker-compose down
```

应用接入：
* TODO



## 部署_Elasticsearch + Kibana 7.16.2

1.系统配置

```shell
$ sysctl -w vm.max_map_count=262144
```

2.创建文件

```shell
$ mkdir -p /opt/docker-volumes/elasticsearch_7.16.2/{config,data,logs}
$ mkdir -p /opt/docker-volumes/kibana_7.16.2/config
```

3.编辑配置

```
$ vim /opt/docker-volumes/elasticsearch_7.16.2/config/elasticsearch.yml
```

```yml
cluster.name: "docker-cluster"
network.host: 0.0.0.0
http.port: 9200
http.cors.enabled: true
http.cors.allow-origin: "*"
http.cors.allow-headers: Authorization
xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
```


```
$ vim /opt/docker-volumes/kibana_7.16.2/config/kibana.yml
```

```yml
server.name: kibana
server.host: "0.0.0.0"
elasticsearch.hosts: [ "http://elasticsearch:9200" ]
xpack.monitoring.ui.container.elasticsearch.enabled: true
elasticsearch.username: "elastic"
elasticsearch.password: "123456"
i18n.locale: zh-CN
```

```shell
$ mkdir -p /opt/docker-compose/elasticsearch_7.16.2/ 
$ vim /opt/docker-compose/elasticsearch_7.16.2/docker-compose.yml
```

```yml
version: '3'

services:
  elasticsearch:
    image: elasticsearch:7.16.2
    container_name: elasticsearch
    restart: unless-stopped
    volumes:
      - "/opt/docker-volumes/elasticsearch_7.16.2/data:/usr/share/elasticsearch/data"
      - "/opt/docker-volumes/elasticsearch_7.16.2/logs:/usr/share/elasticsearch/logs"
      - "/opt/docker-volumes/elasticsearch_7.16.2/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml"
    environment:
      TZ: Asia/Shanghai
      LANG: en_US.UTF-8
      discovery.type: single-node
      ES_JAVA_OPTS: "-Xmx512m -Xms512m"
      ELASTIC_PASSWORD: "123456"
      TAKE_FILE_OWNERSHIP: "true"
    ports:
      - "9200:9200"
      - "9300:9300"
    networks:
      - es

  kibana:
    image: kibana:7.16.2
    container_name: kibana
    restart: unless-stopped
    volumes:
      - "/opt/docker-volumes/kibana_7.16.2/config/kibana.yml:/usr/share/kibana/config/kibana.yml"
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
    links:
      - elasticsearch
    networks:
      - es

networks:
  es:
```

4.拉取与启动

```
$ cd /opt/docker-compose/elasticsearch_7.16.2
$ docker-compose pull
$ docker-compose up -d
```

5.访问

```
ES访问地址: http://{IP}:9200
默认账号密码: elastic/123456

kibana访问地址: http://{IP}:5601
默认账号密码: elastic/123456
```


```
GET _cat/indices?v&pretty
health status index                           uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases                mV3P5BkxSh2tkEzxV8XDXg   1   0         40            0     37.8mb         37.8mb
green  open   .security-7                     pmal5H-USG-Wl1QDvQvN5A   1   0         53            0    261.5kb        261.5kb
green  open   .apm-custom-link                mcbbNvDTTAi2Jrerp2cEcA   1   0          0            0       226b           226b
green  open   .kibana_task_manager_7.16.2_001 lAs8gBrVSMS2MlcpFFCJMg   1   0         18          198     63.6kb         63.6kb
green  open   .kibana_7.16.2_001              RnxPkZ6vSjaz-It0olSqzg   1   0         16            0      2.3mb          2.3mb
green  open   .apm-agent-configuration        -BzW8c_qTaWWg_QuOzgdYw   1   0          0            0       226b           226b
```

## 部署_SkyWalking 9.3.0


```yml
version: '3.3'
services:
  es8:
    image: elasticsearch:8.7.0
    container_name: es8
    ports:
      # 前面是本机端口
      - 9200:9200
      - 9300:9300
    environment:
      xpack.security.enabled: "false"
      discovery.type: "single-node" #单例模式
      ingest.geoip.downloader.enabled: "false"
      # 锁定物理内存地址，防止es内存被交换出去，也就是避免es使用swap交换分区，频繁的交换，会导致IOPS变高
      bootstrap.memory_lock: "true"
      TZ: Asia/Shanghai
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      # 前面是本机数据存储
      - /opt/docker-volumes/skywaling-es/data:/usr/share/elasticsearch/data
 
  skywalking-oap:
    image: apache/skywalking-oap-server:9.3.0
    container_name: skywalking-oap
    restart: always
    depends_on:
      - es8
    links:
      - es8
    ports:
      - 11800:11800
      - 12800:12800
    environment:
      SW_CORE_RECORD_DATA_TTL: 7 #记录数据的有效期，单位天
      SW_CORE_METRICS_DATA_TTL: 7 #分析指标数据的有效期，单位天
      SW_ENABLE_UPDATE_UI_TEMPLATE: "true" # 开启dashboard编辑修改功能
      SW_HEALTH_CHECKER: default
      TZ: Asia/Shanghai
      SW_STORAGE: elasticsearch
      JAVA_OPTS: "-Xms2048m -Xmx2048m"
      SW_STORAGE_ES_CLUSTER_NODES: es8:9200
      
  skywalking-ui:
    image: apache/skywalking-ui:9.3.0
    container_name: skywalking-ui
    restart: always
    depends_on:
      - skywalking-oap
    links:
      - skywalking-oap
    ports:
      - 8080:8080
    environment:
      TZ: Asia/Shanghai
      SW_HEALTH_CHECKER: default
      SW_OAP_ADDRESS: http://skywalking-oap:12800
```

```
$ docker-compose pull
$ docker-compose up -d
```

* http://10.2.43.101:8080

### 遇到问题

启动ES时，报错：`java.lang.IllegalStateException: failed to obtain node locks, tried [/usr/share/elasticsearch/data]; maybe these locations are not writable or multiple nodes were started on the same data path?`

解决方案：

```
chmod -R 777 /opt/docker-volumes/skywaling-es/data
```

### 客户端使用

下载JavaAgent，地址：https://skywalking.apache.org/downloads

![[Pasted image 20231031150833.png|800]]

>第1种方式：直接修改配置文件

```shell
$ vim config/agent.config
agent.service_name=${SW_AGENT_NAME:mnis}
collector.backend_service=${SW_AGENT_COLLECTOR_BACKEND_SERVICES:10.2.43.101:11800}
```

```
-javaagent:E:\下载\skywalking-agent\skywalking-agent.jar
```

>第2种方式：配置环境变量

```
SW_AGENT_NAME=mnis
SW_AGENT_COLLECTOR_BACKEND_SERVICES=10.2.43.101:11800
```

```
-javaagent:E:\下载\skywalking-agent\skywalking-agent.jar
```

>第3种方式：指定参数

```
-javaagent:E:\下载\skywalking-agent\skywalking-agent.jar -Dskywalking.agent.service_name=mnis -Dskywalking.collector.backend_service=10.2.43.101:11800
```

## 部署_KettlePack

https://hub.docker.com/r/congjing/kettlepack

- 浏览器中访问: http://localhost:9089  
- 默认用户名: admin
- 默认密码: congjingkeji

# 虚拟机部署


## OpenJDK 1.8

基于yum的安装方式：

```shell
$ yum search java | grep jdk
$ yum install java-1.8.0-openjdk
# 如果仅执行完成上述安装，可能执行jps命令会发现找不到此命令，需要再执行以下命令进行安装
$ yum search java | grep openjdk-devel
$ yum install java-1.8.0-openjdk-devel.x86_64
```

优点：操作简单~



>启动后，直接访问：http://10.2.43.101:3000
>默认用户名密码：admin/admin
>修改后密码：Lx_123456789
## Nexus 3.65.0

解压后的目录：

```
[root@localhost nexus-3.65.0]# tree -L 1
.
├── nexus-3.65.0-02  # 程序目录。包含了Nexus运行所需要的文件。是Nexus运行必须的。
└── sonatype-work    # 仓库目录。包含了Nexus生成的配置文件、日志文件、仓库文件等。当我们需要备份Nexus的时候默认备份此目录即可。
```

```sh
cd /opt/nexus-3.65.0/nexus-3.65.0-02/bin
./nexus start
```

启动报错：

```
Caused by: com.orientechnologies.orient.core.exception.OLowDiskSpaceException: Error occurred while executing a write operation to database 'OSystem' due to limited free space on the disk (3948 MB). The database is now working in read-only mode. Please close the database (or stop OrientDB), make room on your hard drive and then reopen the database. The minimal required space is 4096 MB. Required space is now set to 4096MB (you can change it by setting parameter storage.diskCache.diskFreeSpaceLimit) .
```

找到nexus二进制文件中的配置：

```sh
INSTALL4J_ADD_VM_PARAMS=-Dstorage.diskCache.diskFreeSpaceLimit=2048
```

查看：http://10.2.43.101:8081

用户：admin
密码：`/opt/nexus-3.65.0/sonatype-work/nexus3/admin.password`

进去后直接修改密码为：admin123


