# 1.监听容器刷新完成扩展点




# 2.CommandLineRunner接口

>属于SpringBoot接口类~

当容器初始化完成之后会调用CommandLineRunner中的run方法，同样能够达到容器启动之后完成一些事情。这种方式和ApplicationListener相比更加灵活，如下：

- 不同的CommandLineRunner实现可以通过@Order注解指定执行顺序；
- 可以接收从控制台输入的参数。

```java
@Slf4j
@Component
public class CustomCommandLineRunner implements CommandLineRunner {
    @Override
    public void run(String... args) throws Exception {
        log.debug("从控制台接收参数:{}", Arrays.asList(args));
    }
}
```

```bash
java -jar demo.jar aaa bbb ccc
```

# 3.ApplicationRunner接口

>属于SpringBoot接口类~

相对于CommandLineRunner来说对于控制台传入的参数封装更好一些，可以通过键值对来获取指定的参数。

```bash
java -jar demo.jar --version=2.1.0 aaa bbb ccc
```

同样也可以通过@Order注解指定优先级。

```java
@Slf4j
@Component
public class CustomApplicationRunner implements ApplicationRunner {
    @Override
    public void run(ApplicationArguments args) throws Exception {
        log.debug("控制台接收的参数：{},{},{}",args.getOptionNames(),args.getNonOptionArgs(),args.getSourceArgs());
    }
}
```
