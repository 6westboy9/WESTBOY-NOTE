## 基础知识

![[Pasted image 20231219113145.png|500]]

在链路中首先要理解的概念是Segment，<font color="#f79646">Segment表示一个JVM进程内的所有操作</font>。上图中有6个Segment。Gateway Segment是Mall Segment的parent，通过parent关系就可以把多个Segment按顺序拼起来组装成一个链路。

>上述Segment表示的是逻辑概念，物理层面会存在多个Segment，物理层面的单个Segment表示一个JVM进程内一个线程中所有操作集合~

一个Segment里可能发生多个操作，比如操作1是查Redis，操作2是查MySQL，这就是两个Span，<font color="#f79646">Span表示一个具体的操作</font>。Span之间也是基于parent的关系构建起来的，而<font color="#f79646">Segment是Span的容器</font>。

多个Segment连接起来就组成了一个Trace，每个Trace都有一个全局唯一的ID。

```
Trace
	Segment1
		Span11
		Span12
		...
	Segment2
		Span21
		Span22
		Span23
		...
	Segment3
	...
```

> 在SkyWalking中是没有Trace这个概念的，所谓的Trace是将所有Segment串起来之后表示一个逻辑概念~

## 整体模型

![[Pasted image 20231220134621.png|900]]

说明：

1. 一个Trace由多个TraceSegment组成，TraceSegment使用TraceSegmentRef指向它的上一个TraceSegment。
2. 每个TraceSegment中有多个Span，每个Span都有spanId和parentSpanId，spanId从0开始，parentSpanId指向上一个span的Id。
3. 一个TraceSegment中第一个创建的Span叫<font color="#f79646">EntrySpan</font>，调用的本地方法对应<font color="#f79646">LocalSpan</font>，离开当前Segment对应<font color="#f79646">ExitSpan</font>。
4. 每个Span都有一个refs，每个TraceSegment的第一个Span（EntrySpan）的refs会指向它所在TraceSegment的上一个TraceSegment。
	1. 第一个TraceSegment的第一个Span（EntrySpan）的refs为空。--- 因为第一个TraceSegment没有父TraceSegment了嘛~
	2. 每个TraceSegment的LocalSpan和ExistSpan的refs均为空。
	3. 一个TraceSegment可以有多个父TraceSegment，所以TraceSegment的第一个Span（EntrySpan）的refs可能存在多个。

Segment是SkyWalking中提出的概念，表示一次请求在某个服务内的执行链路片段的合集，一个请求在多个服务中先后产生的Segment串起来构成一个完整的Trace，如下图所示：

![[Pasted image 20231221151437.png|700]]

**EntrySpan**
* TraceSegment<font color="#f79646">必须有EntrySpan</font>；
* 在一个TraceSegment中只能存在一个EntrySpan，后面的EntrySpan会复用前面EntrySpan，并会覆盖掉前一个EntrySpan设置的属性，所以<font color="#f79646">EntrySpan记录的信息永远是最靠近业务侧的信息</font>

**ExitSpan**
* 所谓ExitSpan和EntrySpan一样采用复用的机制，前提是在插件嵌套的情况下，<font color="#f79646">在一个RPC调用中，会有多层退出的点，而ExitSpan永远表示第一个</font>；
* 多个ExitSpan不存在嵌套关系，是平行存在的时候，是允许同时存在多个ExitSpan；
* 把ExitSpan简单理解为离开当前进程/线程的操作；
* TraceSegment<font color="#f79646">不一定非要有ExitSpan，也有可能会存在多个，且不会存在父子级关系</font>，也就是上面所说的嵌套情况下，只保留第一个；
* <font color="#f79646">ExitSpan不要把理解为TraceSegment的结束，可以理解为离开当前TraceSegment的操作</font>。

**LocalSpan**
* 通常记录本地方法调用；
* TraceSegment<font color="#f79646">不一定非要有LocalSpan，也有可能存在多个，没有严格的父子级关系限制</font>；

**案例**

![[Pasted image 20231221153533.png|900]]

Tomcat一进来就会创建EntrySpan，SpringMVC会复用Tomcat创建的EntrySpan。当访问Redis时会创建一个ExitSpan，peer会记录Redis地址。当访问MySQL时也会创建一个ExitSpan，peer会记录MySQL地址。
ExitSpan不要把理解为TraceSegment的结束，可以理解为离开当前TraceSegment的操作。

**对于上面所说的嵌套深入理解**

>其实个人认为，上面所说的嵌套关系，就是父子级关系，比如存在嵌套关系，意思就是存在父子级关系~

* 不会存在父子级关系的情况
	*  EntrySpan与EntrySpan
	* ExitSpan与ExitSpan
* 会存在父子级关系
	* LocalSpan与EntrySpan
	* LocalSpan与LocalSpan
	* ExitSpan与EntrySpan
	* ExitSpan与LocalSpan

从创建三者的方法中可以看到具体的关系：

```java
public AbstractSpan createEntrySpan(final String operationName) {  
    if (isLimitMechanismWorking()) {  
        NoopSpan span = new NoopSpan();  
        return push(span);  
    }  
    AbstractSpan entrySpan;  
    TracingContext owner = this;  
    final AbstractSpan parentSpan = peek();  
    final int parentSpanId = parentSpan == null ? -1 : parentSpan.getSpanId();  
    //  
    if (parentSpan != null && parentSpan.isEntry()) {  
        profilingRecheck(parentSpan, operationName);  
        parentSpan.setOperationName(operationName);  
        entrySpan = parentSpan;  
        return entrySpan.start();  
    } else {  
        entrySpan = new EntrySpan(  
            spanIdGenerator++, parentSpanId,  
            operationName, owner  
        );  
        entrySpan.start();  
        return push(entrySpan);  
    }  
}

```

```java
public AbstractSpan createLocalSpan(final String operationName) {  
    if (isLimitMechanismWorking()) {  
        NoopSpan span = new NoopSpan();  
        return push(span);  
    }  
    AbstractSpan parentSpan = peek();  
    final int parentSpanId = parentSpan == null ? -1 : parentSpan.getSpanId();  
    AbstractTracingSpan span = new LocalSpan(spanIdGenerator++, parentSpanId, operationName, this);  
    span.start();  
    return push(span);  
}
```

```java
public AbstractSpan createExitSpan(final String operationName, final String remotePeer) {  
    if (isLimitMechanismWorking()) {  
        NoopExitSpan span = new NoopExitSpan(remotePeer);  
        return push(span);  
    }  
  
    AbstractSpan exitSpan;  
    AbstractSpan parentSpan = peek();  
    TracingContext owner = this;  
    //  
    if (parentSpan != null && parentSpan.isExit()) {  
        exitSpan = parentSpan;  
    } else {  
        final int parentSpanId = parentSpan == null ? -1 : parentSpan.getSpanId();  
        exitSpan = new ExitSpan(spanIdGenerator++, parentSpanId, operationName, remotePeer, owner);  
        push(exitSpan);  
    }  
    exitSpan.start();  
    return exitSpan;  
}
```

## 组件设计

### TraceSegment

```java
public class TraceSegment {
    // 每个Segment的唯一id
    private String traceSegmentId;
	// 指向父Segment的引用对象
	// 大多数场景下，比如RPC请求时，只会存在一个父Segment的引用对象
	// 批处理场景时，会存在多个父Segment，这里只缓存第一个父Segment的引用对象
	// 它不会被序列化传输，只是辅助访问parent使用
    private TraceSegmentRef ref;
	// 属于当前Segment的所有Span
    private List<AbstractTracingSpan> spans;
	// 代表整个Trace的全局唯一id
	// 大多数场景下，只有会存在一个
	// 批处理场景时，存在多个父Segment，仅代表第一个Segment的id
    private DistributedTraceId relatedGlobalTraceId;

    private boolean ignore = false;
	// 当前线程内操作数超过配置，则丢弃
    private boolean isSizeLimited = false;

    private final long createTime;
    
    // ...
}
```


```java
public class TraceSegmentRef {  
    // SegmentRef的类型
    // - CROSS_PROCESS 跨进程
    // - CROSS_PROCESS 跨线程
    private SegmentRefType type;  
    // 
    private String traceId;  
    // 父Segment唯一id
    private String traceSegmentId;
    // 
    private int spanId;
    // Mall -> Order 对于Order服务来讲，parentService就是Mall
    private String parentService;
    // parentService的具体一个实例
    private String parentServiceInstance;
    // 进入parentService的那个请求
    private String parentEndpoint;  
    private String addressUsedAtClient;
}

public enum SegmentRefType {  
    CROSS_PROCESS, CROSS_THREAD  
}
```

### Span

* EntrySpan
* LocalSpan
* ExitSpan

### CarrierItem

```
CarrierItemHead -> SW8CarrierItem -> SW8CorrelationCarrierItem -> SW8ExtensionCarrierItem
```

### ContextCarrier

该类主要用于处理SkyWalking在<font color="#f79646">跨进程</font>间的数据传递。如：客户端A调用服务端B，那么会进行如下的步骤：
1. 客户端A调用前先创建ContextCarrier。
2. 通过ContextManager#inject将当前需要传递的数据放入新的ContextCarrier进行后续传递。
3. 使用ContextCarrier#items将步骤1的ContextCarrier内部的数据放入CarrierItemHead，用于后续在HTTP HEAD、Dubbo attachments 、MQ的HEAD中进行传递。
4. 服务端B接收到请求后提取信息存入自己创建的ContextCarrier中。
5. 通过ContextManager#createEntrySpan将ContextCarrier中的信息进行使用并做关联。
### ContextSnapshot

该类主要用于处理SkyWalking在<font color="#f79646">跨线程</font>间的数据传递。如：主线程调用中执行了子线程逻辑，那么会发生如下的步骤：
1. 调用子线程前会先执行ContextManager#capture用来创建一个ContextSnapshot。
2. 子线程执行前会执行ContextManager#continued将父线程给的ContextSnapshot传入自己的TraceSegmentRef中。
