* [Spring Boot循环依赖的症状和解决方案](https://blog.csdn.net/m0_37996629/article/details/129972669?ydreferer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8%3D)

## 构造方法循环依赖

>使用版本：<font color="#ffc000">2.1.2.RELEASE</font>

```java
@Component
public class ServiceA1 {

    private ServiceB1 serviceB1;

    public ServiceA1(ServiceB1 serviceB1) {
        this.serviceB1 = serviceB1;
    }
}

@Component
public class ServiceB1 {

    private ServiceA1 serviceA1;

    public ServiceB1(ServiceA1 serviceA1) {
        this.serviceA1 = serviceA1;
    }
}
```

```
2025-06-30 15:31:21.916 [main] ERROR o.s.b.diagnostics.LoggingFailureAnalysisReporter - 

***************************
APPLICATION FAILED TO START
***************************

Description:

The dependencies of some of the beans in the application context form a cycle:

┌─────┐
|  serviceA1 defined in file [D:\Projects\Idea\P2\mnis\windranger-controller\target\classes\com\lachesis\windranger\controller\test\ServiceA1.class]
↑     ↓
|  serviceB1 defined in file [D:\Projects\Idea\P2\mnis\windranger-controller\target\classes\com\lachesis\windranger\controller\test\ServiceB1.class]
└─────┘
```

* ! 在2.6.0之前，Spring Boot会自动处理循环依赖的问题，在2.6.0及之后的版本会默认检查循环依赖，存在该问题则会报错

| 版本                  | 默认是否允许循环依赖 | 备注             |
| ------------------- | ---------- | -------------- |
| Spring Boot < 2.6.0 | 是          | 自动尝试解决，尤其是属性注入 |
| Spring Boot ≥ 2.6.0 | 否          | 默认禁止，需显式开启配置   |

```yaml
# 2.6.0+版本默认为false
spring.main.allow-circular-references: false
```

* ! 很明显在上述场景中是无法自动处理循环依赖问题的，那自动处理循环依赖能处理哪些场景呢？

>Spring容器默认是按照字母序创建Bean的，所以ServiceA1创建永远在ServiceB1前面


### 解1.使用@Lazy注解

```java
@Component
public class ServiceA1 {

    private ServiceB1 serviceB1;

	@Lazy
	@Autowired // 这里的注解可以省略，什么情况下不能省略呢？见下说明
    public ServiceA1(ServiceB1 serviceB1) {
        this.serviceB1 = serviceB1;
    }
}

@Component
public class ServiceB1 {

    private ServiceA1 serviceA1;

    public ServiceB1(ServiceA1 serviceA1) {
        this.serviceA1 = serviceA1;
    }
}
```

* ! 如果只有一个构造函数，可以不加@Autowired，但有多个构造函数的时候就必须指定使用哪个
* ! <font color="#ff0000">@Lazy不能解决构造函数循环依赖！！！</font>
* ! <font color="#ff0000">@Lazy可以推迟Bean的加载，但无法解决循环依赖的根本问题！！！</font>
* ! <font color="#ff0000">@Lazy主要是为了优化Bean加载时机，提高性能，而不是用来处理循环依赖！！！</font>

推荐资料：

* [Spring中的@Lazy懒加载能否解决循环依赖问题?](https://blog.csdn.net/zzzzzengjf/article/details/141953708)

### 解2.改为非构造方法

```java
@Component
public class ServiceA1 {

    @Autowired
    private ServiceB1 serviceB1;

}
```


## 循环依赖问题的解决方案

推荐资料：[一篇文章带你彻底搞懂Spring解决循环依赖的底层原理](https://blog.csdn.net/cy973071263/article/details/132676795)

### 1.重新设计

当你面临一个循环依赖问题时，有可能是你对JavaBean的设计有问题，没有将各自的依赖做到很好的分离。你应该尽量正确地重新设计JavaBean，以保证它们的层次是精心设计的，避免没有必要的循环依赖。

如果不能重新设计组件（可能有很多的原因：遗留代码，已经被测试并不能修改代码，没有足够的时间或资源来完全重新设计等等原因），但有一些变通方法可以解决这个问题。

### 2.使用Setter/Field注入


### 3.使用@Lazy注解


### 4.使用@PostConstruct注解


## 5.实现ApplicationContextAware和InitializingBean接口


