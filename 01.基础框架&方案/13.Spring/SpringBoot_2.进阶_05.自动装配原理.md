[一文搞懂SpringBoot自动配置原理](https://juejin.cn/post/7046554366068654094)



# 数据库自动装配



```java
@Bean(name = "newDataSource")  
@ConfigurationProperties(prefix = "spring.datasource.new")  
public DataSource newDataSource() {  
    return DataSourceBuilder.create().build();  
}
```

问题：`@ConfigurationProperties`使用在此的作用？这里无参配置，配置文件中的属性怎么跟代码绑定的呢？最后又怎么生成DataSource对象的呢？


