>源码版本8.7.0

# 1.默认配置修改

## 1.1.根pom.xml修改

去除maven-checkstyle-plugin插件，因为在研究源码的过程中可能会进行一个代码修改操作，不满足该插件要求的代码风格时，在编译期间会报错。

## 1.2.apm-webapp模块的pom.xml修改

> 解决办法一

去除frontend-maven-plugin插件，即不编译前端模块。

> 解决办法二

另外一种解决方法，不去除该插件。

# 2.拉取代码并执行相关操作

```shell
git clone https://github.com/apache/skywalking.git
cd skywalking/
git submodule init
git submodule update
```

>使用git submodule允许用户将一个Git仓库作为另一个Git仓库的子目录。 它能让你将另一个仓库克隆到自己的项目中，同时还保持提交的独立性。

# 3.编译项目

>需要注意的SkyWalking使用到Protocol Buffers进行网络通信，因此在编译过程会通过相应插件将Proto文件编译生成Class文件~

执行编译：

```
mvn clean package -Dmaven.test.skip=true
mvn clean package -DskipTests
```

为了让源码中使用到生成的类，需要将其标记为Source Root，那么这些类就会加入到ClassPath，访问就不会报错了~

![[Pasted image 20231124192311.png|325]]


# 4.推荐资料

* [官方本地构建说明文档](https://github.com/apache/skywalking/blob/v8.7.0/docs/en/guides/How-to-build.md) 




