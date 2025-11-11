


### 嵌套使用

```properties
spring.application.name=datasync
user=${spring.application.name}
```

如上配置，在SpringBoot配置文件中，可以使用`${spring.application.name}`获取当前上下文中的其它配置属性值。那么当使用Java代码进行配置时，在`@Value`注解中如何使用呢？

```java
@Value("${user:${spring.application.name:}}")  
private String user;
```

