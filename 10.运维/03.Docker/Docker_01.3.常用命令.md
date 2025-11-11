# 镜像相关


# 容器相关


## 创建并运行容器

```sh
# 以交互模式运行容器
docker run -it -v 宿主机目录/文件的绝对路径:容器内目录/文件的绝对路径[:rw/ro] -p 主机端口:容器端口 --name=容器名称 镜像ID/镜像名称[:版本号]

# 以后台方式运行容器 (推荐)
docker run -d -v 宿主机目录/文件的绝对路径:容器内目录/文件的绝对路径[:rw/ro] -p 主机端口:容器端口 --name=容器名称 镜像ID/镜像名称[:版本号]
```

## 进入正在运行的容器内并以命令行交互

```sh
# 以exec方式进入到容器
docker exec -it 容器ID/容器名称 /bin/bash 或 /bin/sh

# 以attach方式进入到容器
docker attach 容器ID/容器名称

# 如果不想进入容器，直接获取相关指令的运行结果，可在后面填写相关操作指令
docker exec -it 容器ID/容器名称 相关命令
```

```ad-important
exec与attach的区别：
* exec：是在容器中打开新的终端，并且可以启动新的进程 (<font color="#f79646">推荐</font>)
* attach：是直接进入容器启动命令的终端，不会启动新的进程

当Docker容器在<font color="#c0504d">-d</font>守护态运行的时候，使用attach时就会一直卡着，因为此时容器运行的进程是ssh，而不是/bin/bash，所以是进入不到的。
```

那这里的<font color="#c0504d">-it</font>什么意思呢？

```
-i, --interactive          Keep STDIN open even if not attached
-t, --tty                  Allocate a pseudo-TTY
```

- -t：选项让Docker分配一个伪终端（pseudo-tty）并绑定到容器的标准输入上
- -i：则让容器的标准输入保持打开。
## 文件拷贝

```sh
# 从容器内拷贝文件到宿主机
docker cp 容器ID/容器名称:容器内目录/文件的绝对路径 宿主机目录/文件的绝对路径

# 从宿主机中拷贝文件到容器内
docker cp 宿主机目录/文件的绝对路径 容器ID/容器名称:容器内目录/文件的绝对路径
```


## 查看容器日志

```sh
docker logs -f -t 容器ID/容器名称
```