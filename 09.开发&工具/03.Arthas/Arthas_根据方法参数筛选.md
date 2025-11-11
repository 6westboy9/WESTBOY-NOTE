
# 异常

需求描述：针对一些偶发线上问题，需要持续监听并输出监听日志。

```sh
# -n 1000 表示满足条件的方法执行1000次
# -x 4 表示遍历的深度
# >> processWhiteboardItemsError.log 指定监听日志文件路径
# & 后台执行
watch com.lachesis.windranger.iwip.service.impl.WardOverviewService processWhiteboardItems {throwExp} 'throwExp != null' -n 1000 -x 4 >> processWhiteboardItemsError.log &
```

可见上述命令执行完成后，会运行一个后台任务，那如何查看呢？

```sh
jobs
```

其实这里主要应用到了Arthas的后台异步任务特性，详细说明参见：[Arthas后台异步任务](https://arthas.aliyun.com/doc/async.html)

# 集合筛选

目标方法

```java
public void get(List<UserInfo> list) {
	// ...
}
```

需求描述：筛选集合中指定元素（指定元素姓名为a2且年龄为18），如果存在，则输出该方法的请求上下文。

```
tt -t com.lachesis.puma.test.one.controller.UserController get 'params[0].{^ (#this.name == "a2" &&  #this.age > 18)}.size() != 0'
```


