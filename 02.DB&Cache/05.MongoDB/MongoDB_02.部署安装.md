# 版本选择

## 查看版本

<font color="#f79646">1.使用mongo shell查看</font>

```js
db.version()
"3.4.24"
```

<font color="#f79646">2.使用mongo查看</font>

```sh
./bin/mongo --version
MongoDB shell version v3.4.24
git version: 865b4f6a96d0f5425e39a18337105f33e8db504d
OpenSSL version: OpenSSL 1.0.1e-fips 11 Feb 2013
allocator: tcmalloc
modules: none
build environment:
    distmod: rhel70
    distarch: x86_64
    target_arch: x86_64
```

>mongo是命令行工具，用于连接一个特定的mongo实例。

```
mongo --host <host:port> -u <username> -p --authenticationDatabase <database>
```

```sh
mongo --host 10.2.3.157:27017 -u admin -p --authenticationDatabase coms
MongoDB shell version v3.4.24
Enter password: 输入密码
```

<font color="#f79646">3.使用mongod查看</font>

```sh
./bin/mongod --version
db version v3.4.24
git version: 865b4f6a96d0f5425e39a18337105f33e8db504d
OpenSSL version: OpenSSL 1.0.1e-fips 11 Feb 2013
allocator: tcmalloc
modules: none
build environment:
    distmod: rhel70
    distarch: x86_64
    target_arch: x86_64
```

>mongod是处理MongDB系统的主要进程。它处理数据请求，管理数据存储，以及后台管理操作。

## 版本差异

>截止到目前为止最新版本为7.0.7

在目前公司内部使用的是3.4.24版本，那么中间这些大版本有哪些差异呢？

* [阿里云MongDB大版本升级说明](https://www.alibabacloud.com/help/zh/mongodb/product-overview/upgrades-of-mongodb-major-versions)

