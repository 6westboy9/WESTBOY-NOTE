# v1_快速安装

```
$ yum list | grep nginx
$ yum install nginx

# 查看安装目录
$ rpm -ql nginx

# 开机启动
$ systemctl enable nginx
$ systemctl disable nginx

$ systemctl status nginx

$ systemctl start nginx
$ systemctl stop nginx

$ systemctl restart nginx
$ systemctl reload nginx
```

# v2_编译安装

下载页面：https://nginx.org/en/download.html

* Mainline版本：是Nginx的最新版本，包含了最新的功能、改进和修复。它是由Nginx的开发团队发布的，通常是在每个大版本发布之前进行测试和验证。Mainline版本提供了最新的特性和性能优化，但<font color="#f79646">可能存在一些较新功能的稳定性问题</font>。
* Stable版本：是经过广泛测试和验证的版本，被认为是相对稳定和可靠的。它是适合生产环境使用的版本，具有较高的稳定性和兼容性。Stable版本通常会包含一些在Mainline版本中进行了验证和修复的功能和改进，以确保更高的稳定性。
* Legacy版本：是过去的发布版本，已经被新的Mainline和Stable版本所取代。Legacy版本可能不再接收新的功能更新和主要修复，而<font color="#f79646">只会接收严重的安全修复</font>。这些版本通常不建议在新项目中使用，而应该考虑升级到Mainline或Stable版本以获得更好的功能和性能。

>这里部署的是Stable版本：nginx-1.26.0

## 下载

```
$ tar -zxvf nginx-1.26.0.tar.gz
$ cd nginx-1.26.0
```

## 编译安装

```shell
# 1.生成Makefile
# 检查系统环境和依赖项，并生成适合当前系统的Makefile，Makefile是一个包含了编译和链接软件所需指令的脚本文件
$ ./configure

# 2.编译
# 根据Makefile文件进行编译，Makefile包含了构建软件的规则和指令。执行make命令将会执行Makefile中定义的编译操作，它会自动找到源代码文件，编译它们，并生成可执行文件或库文件
$ make

# 3.安装
# 将编译后的软件安装到系统中。执行该命令会将生成的可执行文件、库文件和其他必要的文件复制到指定的目录中，使得该软件可以在系统中被访问和使用
$ make install
```

### 存在问题

<font color="#f79646">1.生成Makefile</font>

```
$ ./configure
checking for OS
 + Linux 3.10.0-1160.114.2.el7.x86_64 x86_64
checking for C compiler ... not found

./configure: error: C compiler cc is not found
```

解决方案：

```bash
$ yum -y install gcc-c++
```

再次执行`./configure`即可~

<font color="#f79646">2.编译</font>

```
$ make
make: *** No rule to make target `build', needed by `default'.  Stop.
```

解决方案：

```
$ yum -y install pcre pcre-devel
$ yum -y install zlib zlib-devel
$ yum -y install openssl openssl-devel
```

需要重新执行`./configure`，然后再次执行`make`即可~

<font color="#f79646">3.安装</font>

```
$ make install
```

```
$ whereis nginx
nginx: /usr/local/nginx
```

## 启动


```
$ cd /usr/local/nginx/sbin
$ ./nginx
```

```
$ ps axo pid,cmd,psr,ni|grep nginx
 48191 nginx: master process ./ngi   1   0
 48192 nginx: worker process         3   0
 48199 grep --color=auto nginx       3   0
```

启动成功访问：服务器IP:80

![[Pasted image 20240524172741.png|600]]

## 常用命令

>前提：将nginx命令配置到系统变量中~

```
$ vim /etc/profile
# 最后一行配置
export PATH=$PATH:/usr/local/nginx/sbin
$ source /etc/profile
```


```bash
# 显示版本
$ nginx -v
nginx version: nginx/1.26.0

# 显示版本、编译器版本和参数
$ nginx -V
nginx version: nginx/1.26.0
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-44) (GCC) 
configure arguments:

# 重新加载配置
$ nginx -s reload

# 重新打开日志文件
$ nginx -s reopen

# 仅仅测试配置文件的正确性
$ nginx -t
```
