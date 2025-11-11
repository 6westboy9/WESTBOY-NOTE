
# 指令详解

参考资料

- https://yeasy.gitbook.io/docker_practice/image/dockerfile
- https://juejin.cn/post/7154441046083141645#heading-9

## <font color="#4f81bd">FROM</font> 指定基础镜像

>基础镜像，必须为Dockerfile的第一个指令~

```sh
# 格式
FROM image
FROM image[:tag]
# 示例
FROM mysql:5.6
# 注：tag是可选的，如果不写，则会默认使用latest版本的基础镜像
```

## <font color="#4f81bd">MAINTAINER</font>

>已过时推荐使用LABEL

## <font color="#4f81bd">LABEL</font> 为镜像添加元数据


## <font color="#4f81bd">RUN</font> 执行命令


## <font color="#4f81bd">EXPOSE</font> 暴露端口

>指定当前容器与外界交互的端口

```sh
# 格式
EXPOSE port [port...]

# 示例
EXPOSE 80 443
EXPOSE 8080
EXPOSE 11211/tcp 11211/udp
```

EXPOSE指令是声明容器运行时提供服务的端口，<font color="#f79646">这只是一个声明</font>，在容器运行时<font color="#f79646">并不会因为这个声明应用就会开启这个端口的服务</font>。

在Dockerfile中写入这样的声明有<font color="#f79646">两个好处</font>：

- 帮助镜像使用者理解这个镜像服务的守护端口，以方便配置映射
- 在运行时使用随机端口映射时，也就是`docker run -P`时，会自动随机映射EXPOSE的端口。要将EXPOSE和在运行时使用`docker run -p <宿主端口>:<容器端口>`区分开来。`-p`是映射宿主端口和容器端口，换句话说，就是将容器的对应端口服务公开给外界访问，<font color="#f79646">而EXPOSE仅仅是声明容器打算使用什么端口而已，并不会自动在宿主进行端口映射</font>。

## <font color="#4f81bd">WORKDIR</font> 指定工作目录

>创建容器后终端默认登录进来的工作目录，一个落脚点，不存在会自动创建

```sh
# 格式
WORKDIR /path/to/workdir
# 示例
WORKDIR /a
# 注：通过WORKDIR设置工作目录后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT、ADD、COPY等命令都会在该目录下执行。在使用docker run运行容器时，可以通过-w参数覆盖构建时所设置的工作目录。
```

## <font color="#4f81bd">ENV</font> 设置环境变量

>用来在构建镜像过程中设置环境变量


## <font color="#4f81bd">COPY</font> 复制文件

## ADD 更高级的复制文件

>将本地文件添加到容器中


## <font color="#4f81bd">CMD</font> 容器启动命令



## <font color="#4f81bd">ENTRYPOINT</font>


## <font color="#4f81bd">ONBUILD</font> 为他人作嫁衣裳


## <font color="#4f81bd">USER</font> 指定当前用户


## <font color="#4f81bd">HEALTHCHECK</font> 健康检查


