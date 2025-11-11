>Tomcat版本：9.0.14

# 工作原理



* <font color="#f79646">LimitLatch</font>是连接控制器，它负责控制最大连接数，<font color="#4bacc6">NIO模式下默认是10000</font>，达到这个阈值后，连接请求被拒绝。
	* SpringBoot Tomcat Config：<font color="#4bacc6">server.tomcat.max-connections</font>，默认10000。
* <font color="#f79646">Acceptor</font>在一个死循环里调用accept方法来接收新连接，一旦有新的连接请求到来，accept方法返回一个Channel对象，接着把Channel对象添加至Poller的PollerEvent类型的events队列。
* <font color="#f79646">Poller</font>的本质是一个Selector，也跑在单独线程里。Poller在内部维护一个PollerEvent队列，它在一个死循环里不断检测events队列里的Channel的数据就绪状态，一旦有Channel可读，就生成一个SocketProcessor任务对象扔给Executor去处理。
* <font color="#f79646">Executor</font>就是线程池，负责运行SocketProcessor任务，SocketProcessor#run方法会调用Http11Processor来读取和解析请求数据。
	* SpringBoot Tomcat Config：<font color="#4bacc6">server.tomcat.threads.min-spare</font>，最小工作线程数，默认10。
	* SpringBoot Tomcat Config：<font color="#4bacc6">server.tomcat.threads.max</font>，最大工作线程数，默认200。

借助Arthas查看Tomcat运行时相关参数信息：

```
$ vmtool --action getInstances --className org.apache.tomcat.util.net.AbstractEndpoint --express 'instances[0].maxConnections'
```

使用Arthas查看Tomcat当前连接数：

```shell
$ vmtool --action getInstances --className org.apache.coyote.AbstractProtocol$ConnectionHandler --express 'instances[0]'
$ vmtool --action getInstances --className org.apache.coyote.AbstractProtocol$ConnectionHandler --express 'instances[0].global'
```

## 线程池

查下工作线程池

```
$ vmtool --action getInstances --className org.apache.tomcat.util.net.AbstractEndpoint --express 'instances[0].executor'
$ vmtool --action getInstances --className org.apache.coyote.RequestGroupInfo --express 'instances[0]'

```


保存PojoEndpointServer和WsSession映射

org.apache.tomcat.websocket.WsWebSocketContainer#endpointSessionMap，类型为`Map<Endpoint, Set<WsSession>>`
org.apache.tomcat.websocket.WsWebSocketContainer#sessions 保存WsSession集合

