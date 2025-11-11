SpEL即Spring Expression Language，<font color="#f79646">Spring3</font>开始引入的功能丰富强大的表达式语言。类似于OGNL和JSF EL的表达式语言，能够在运行时构建复杂表达式，存取对象属性、对象方法调用等。

* [官网](https://docs.spring.io/spring-framework/reference/core/expressions.html)
# 设置默认值

SpEl表达式中支持`a?:b`这样的语法来设置默认值。其表示如果a不为null时其结果为a，否则就为b。

```java
@Test
public void test24 () {
	ExpressionParser parser = new SpelExpressionParser();
	Assert.assertTrue(parser.parseExpression("#abc?:123").getValue().equals(123)); // 变量abc不存在
	Assert.assertTrue(parser.parseExpression("1?:123").getValue().equals(1));      // 数字1不为null
}
```

我们可能经常会使用类似于`a.b.c`这样的用法，表示a的b属性的c属性，但如果a为null或者a的b属性为null时都会出现空指针。为了避免此种情况发生，我们可以在SpEl表达式中使用安全导航，这样当a为null或a的b属性为null时将直接返回null，而不抛出空指针异常。SpEl表达式中安全导航的语法是将点`.`替换为`?.`，即不使用`a.b.c`，而是使用`a?.b?.c`。

```java
@Test
public void test25 () {
	ExpressionParser parser = new SpelExpressionParser();
	Assert.assertNull(parser.parseExpression("null?.abc").getValue());
	Assert.assertNull(parser.parseExpression("T(System)?.getProperty('abc')?.length()").getValue());
}
```

# 获取bean对象

在SpEL表达式里面也可以直接访问bean对象，前提是指定了一个BeanResolver。

