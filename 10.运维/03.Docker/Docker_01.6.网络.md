
https://juejin.cn/post/7154441859556147236

当项目大规模使用Docker时，容器通信的问题也就产生了。要解决容器通信问题，必须先了解很多关于网络的知识。Docker作为目前最火的轻量级容器技术，有很多令人称道的功能，如Docker的镜像管理。然而，Docker同样有着很多不完善的地方，<font color="#f79646">网络方面就是Docker比较薄弱的部分</font>。因此，我们有必要深入了解Docker的网络知识，以满足更高的网络需求。

# 网络模式

```sh
[root@localhost ~]# docker network ls
NETWORK ID     NAME                 DRIVER    SCOPE
a4a014c9df7d   bridge               bridge    local
1bb45ea296ee   host                 host      local
69d19fddd71b   none                 null      local
```

| 模式        | 简介                                                                                                    |
| --------- | ----------------------------------------------------------------------------------------------------- |
| bridge    | 为每个容器分配、设置IP等，并将容器连接到一个docker0虚拟网桥，<font color="#f79646">默认为该模式</font>                                |
| host      | 容器将不会虚拟出自己的网卡，配置自己的IP等，而是<font color="#f79646">使用宿主机的IP和端口</font>                                     |
| none      | 容器有独立的Network Namespace，但并没有对其进行任何网络设置，如分配veth pair和网桥连接，IP等                                          |
| container | 新创建的容器不会创建自己的网卡和配置自己的IP，而是和一个指定的容器共享IP、端口范围等。(<font color="#c0504d">不属于默认网络，但在Kubernetes中会使用到</font>) |

![[Pasted image 20240605114313.png|500]]

# 自定义网络


# 容器间网络通信

