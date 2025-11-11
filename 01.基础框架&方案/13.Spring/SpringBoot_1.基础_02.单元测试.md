# 版本差异

在SpringBoot应用中，JUnit4和JUnit5是两种常用的单元测试框架。它们在功能和使用上有一些显著的差异，选择合适的版本对于项目的成功至关重要。

* 注解：JUnit4使用`@Test`注解，而JUnit5引入了新的`@Test`注解，它来自`org.junit.jupiter.api`包。
* 运行器：在SpringBoot应用中，<font color="#c0504d">为了使测试类能够使用Spring的功能</font>，如@Autowired，JUnit4需要使用`@RunWith(SpringRunner.class)`注解。<font color="#c0504d">而JUnit5则不需要</font>，只需添加`@SpringBootTest`注解即可。
* MockMvc支持: 在service层测试中，JUnit5中的`@SpringBootTest`注解<font color="#c0504d">已经包含了MockMvc支持</font>，而JUnit4需要额外使用@RunWith(SpringJUnit4ClassRunner.class)和@WebAppConfiguration注解。


|           | JUnit4            | JUnit5                        |
| --------- | ----------------- | ----------------------------- |
| 注解        | `@org.junit.Test` | `@org.junit.jupiter.api.Test` |
| 运行器       |                   |                               |
| MockMvc支持 |                   |                               |
