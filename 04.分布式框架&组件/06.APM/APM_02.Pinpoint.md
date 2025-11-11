# 概述

* 官方文档：[Introduction - Pinpoint (gitbook.io)](https://pinpoint-apm.gitbook.io/pinpoint/)
* Github：[Github For Pinpoin]([GitHub - pinpoint-apm/pinpoint: APM, (Application Performance Management) tool for large-scale distributed systems.](https://github.com/pinpoint-apm/pinpoint))
* 快速部署Pinpoint服务：[[虚拟机服务部署_CentOS_7#Docker Compose#Pinpoint 2.5.3]]

# 架构设计

![[Pasted image 20231031104827.png]]

# 项目实战

## SpringBoot整合

服务起来了，如何在SpringBoot项目集成Pinpoint呢？

1.下载并配置

https://github.com/pinpoint-apm/pinpoint/releases/download/v2.5.3/pinpoint-agent-2.5.3.tar.gz

解压并修改配置，这里Pinpoint使用多环境的配置方式：

```
profiles
├ local
│  ├ log4j2.xml
│  └ pinpoint.config
└ release
   ├ log4j2.xml
   └ pinpoint.config
pinpoint-root.config
```

查看pinpoint-root.config文件头部注释：

1. 使用Profiles方式，一种是通过-D参数指定，一种是在配置文件中指定
	1. 指定`-Dpinpoint.profiler.profiles.active=release/local`自由定制对应环境的配置。
	2. 修改`$PINPOINT_AGENT_DIR/pinpoint-root.config`中的`pinpoint.profiler.profiles.active=release/local`配置。
2. 支持扩展Profile
	1. 创建`$PINPOINT_HOME/profiles/MyProfile`，添加和修改`log4j2.xml`和`pinpoint.config`配置文件。
	2. 使用`-Dpinpoint.profiler.profiles.active=MyProfile`参数指定扩展Profile。
3. 支持额外的属性
	1. 通过`-Dpinpoint.config=$MY_CONFIG_PATH/pinpoint.config`，额外属性配置，在此个人理解是不是可以自由定制属性呢？还是？

修改`$PINPOINT_HOME/profiles/local`下`pinpoint.config`配置：

```
# 修改服务端IP地址，实际只需要配置其中一个即可，具体配置哪个看你使用GRPC/THRIFT，下面统一修改了IP地址
profiler.transport.grpc.collector.ip=192.168.172.102
profiler.collector.ip=192.168.172.102
# 修改应用类型
profiler.applicationservertype=SPRING_BOOT
```

2.指定JavaAgent启动

```
-javaagent:E:\下载\pinpoint-agent-2.5.3\pinpoint-bootstrap.jar -Dpinpoint.agentId=ds-01 -Dpinpoint.applicationName=ds -Dpinpoint.profiler.profiles.active=local
```


3.查看监控信息

![[Pasted image 20231030182958.png|1100]]

