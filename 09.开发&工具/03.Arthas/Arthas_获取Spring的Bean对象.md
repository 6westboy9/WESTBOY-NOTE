https://www.cnblogs.com/cdfive2018/p/16085896.html

项目一般都是基于Spring/SpringBoot来构建，如果我们能获取Spring的`ApplicationContext`，就能方便获取Spring容器的Bean，然后调用里面的方法。

# 1.借助Dubbo的SpringExtensionFactory

```shell
sc -d com.alibaba.dubbo.config.spring.extension.SpringExtensionFactory
```

获取结果里的`classLoaderHash`值。

通过`ognl`命令，`-c`参数指定ClassLoader的hash值，即上一步的`classLoaderHash`值。

```shell
ognl -c 6b884d57 '@com.alibaba.dubbo.config.spring.extension.SpringExtensionFactory@contexts.iterator.next'
```

观察输出结果，此时已成功获取到Spring的`ApplicationContext`，接下来可以根据场景和需要灵活使用了。

```shell
# 调用某service方法
ognl -c 6b884d57 '#context=@com.alibaba.dubbo.config.spring.extension.SpringExtensionFactory@contexts.iterator.next,#context.getBean("songService").findRandomSongList(5)'
```
# 2.自己实现ApplicationContextAware接口

其实与上述Dubbo类似，只是自己提供了实现而已~



