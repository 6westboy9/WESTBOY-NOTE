# synthetic关键字

[08-什么是synthetic_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1dy4y1V7ck?p=8&vd_source=401e9151ff5196d99069159680a48dbc)

synthetic：合成的，由Java编译器在编译阶段自动生成的。

>以下内容均为JDK 11之前~

## 字段

目标类：

```java
public class FieldDemo {

    public String hello() {
        return "Hello";
    }

    class FieldDemoInner {
        public void sayHello() {
            System.out.println(hello());
        }
    }
}
```

测试类：

```java
public class Main {
    public static void main(String[] args) {
        fieldDemo();
    }

    public static void fieldDemo() {
        Field[] fields = FieldDemo.FieldDemoInner.class.getDeclaredFields();
        for (Field field : fields) {
            System.out.println(field.getName() + " " + field.isSynthetic());
        }
    }
}
```

输出结果：

```
this$0 true
```

实际编译器的行为猜测：

>为啥说是猜测，只是觉得没有证实~

```java
public class FieldDemo {  
    public FieldDemo() {  
    }  
  
    public String hello() {  
        return "Hello";  
    }  
  
    class FieldDemoInner {
		
		// FieldDemo this$0;
		
        // FieldDemoInner(FieldDemo demo) {
        //    this.this$0 = demo;
        // }  
  
        public void sayHello() {  
	        // 根据Java语法要求，要调用某一个类的实例方法，就一定要持有该方法所在类的实例
            // System.out.println(this.this$0.hello()); 
            System.out.println(hello());
        }  
    }  
}
```

## 方法

目标类：

```java
public class MethodDemo {  
  
    class MethodDemoInner {  
        private String innerName;  
    }  
  
    public void setInnerName(String name) {  
        new MethodDemoInner().innerName = name;  
    }  
  
    public String getInnerName() {  
        return new MethodDemoInner().innerName;  
    }  
}
```

测试类：

```java
public class Main {
    public static void main(String[] args) {
        fieldDemo();
    }

	public static void methodDemo() {  
	    Method[] methods = MethodDemo.MethodDemoInner.class.getDeclaredMethods();  
	    for (Method method : methods) {  
	        System.out.println(method.getName() + " " + method.isSynthetic());  
	    }  
	}
}
```

输出结果：

```
access$000 true
access$002 true
```

实际编译器的行为猜测：

>为啥说是猜测，只是觉得没有证实~

```java
public class MethodDemo {  
  
    class MethodDemoInner {  
        private String innerName;  
    }

	// public void access$002(String name) {
	// 	  this.innerName = name;
	// }

    // public String access$000() {
    //    return this.innerName;
    // }
  
    public void setInnerName(String name) {
        // new MethodDemoInner().access$002(name);
        new MethodDemoInner().innerName = name;  
    }  
  
    public String getInnerName() {
        // new MethodDemoInner().access$000();
        return new MethodDemoInner().innerName;  
    }  
}
```

## 构造方法

目标类：

```java
public class ConstructorDemo {

    public ConstructorDemoInner inner = new ConstructorDemoInner();

    class ConstructorDemoInner {
        private ConstructorDemoInner() {
        }
    }
}
```

测试类：

```java
public class Main {  
    public static void main(String[] args) {  
        constructorDemo();  
    }
    
	public static void constructorDemo() {  
	    Constructor<?>[] declaredConstructors = ConstructorDemo.ConstructorDemoInner.class.getDeclaredConstructors();  
	    for (Constructor<?> constructor : declaredConstructors) {  
	        System.out.println(constructor.getName() + " " + constructor.isSynthetic());  
	        // 打印修饰符  
	        System.out.println(constructor.getModifiers() + " " + Modifier.toString(constructor.getModifiers()));  
	    }  
	}
}
```

输出结果：

```
org.westboy.temp.demo.ConstructorDemo$ConstructorDemoInner false
2 private
org.westboy.temp.demo.ConstructorDemo$ConstructorDemoInner true
4096 
```

可以看到有两个构造方法：

* 第一个不是synthetic，且修饰符是private；
* 第二个是synthetic，且修饰符为空（并不是我们一般认为的default，即没有任何修饰符时），且该修饰符编号为4096，即在JAVA语言规范中它标识的含义就是synthetic。
	* 按说ConstructorDemoInner中的构造方法是私有的，ConstructorDemo的成员变量inner中要new一个ConstructorDemoInner按说是不被允许的，那怎么实现的呢？就是借助synthetic构造方法。

## 总结

>上述不论是字段、方法或者构造方法，均是在内部类和外部类相互访问时，在语法层面解决正确性的一个问题，否则是不否和语法规范的。

用JavaScript来简单说明：Java编译器帮我们自动做了var that = this这个操作。

## 彩蛋


将JDK版本从1.8改为11版本之后，再运行上述案例，输出内容为空。

比如上述方法案例中，在JDK1.8版本下运行输出结果为：

```
access$000 true
access$002 true
```

改为JDK11之后：

```
```

其中的奥秘见JDK11 BNAC机制~

# JDK11 NBAC

Nested Based Access Control

[09-NBAC机制_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1dy4y1V7ck?p=9&spm_id_from=pageDriver&vd_source=401e9151ff5196d99069159680a48dbc)

>以下内容均为JDK 11之后~

## 背景

在内部类里面存在同一个方法的不同调用方式时，呈现不同结果的情况：

如果调用外部类的一个private方法：

* CASE1-反射调用 - 报错
* CASE2-直接调用 - 不会报错

>所以这里会产生一个困惑，明明是对同一个方法产生调用，为什么反射报错而直接调用不报错呢？内部类中不能通过反射方式调用外部类方法！JDK8之前，改为JDK11后就不会报错，源于NBAC机制，那么NBCA机制是怎么做到的呢？

**CASE1**

目标类：

```java
public class Outer {

    public void outerPublic() throws Exception {
        new Inner().reflectOuter(new Outer());
    }

    private void outerPrivate() {
    }

    class Inner {

        public void innerPublic() {
            outerPrivate();
        }

        private void reflectOuter(Outer outer) throws Exception {
            Method method = outer.getClass().getDeclaredMethod("outerPrivate");
            method.invoke(outer);
        }
    }
}

```

测试类：

```java
public class Main {
    public static void main(String[] args) throws Exception {
        new Outer().outerPublic();
    }
}
```

执行异常：

```
Exception in thread "main" java.lang.IllegalAccessException: Class org.westboy.temp.demo.Outer$Inner can not access a member of class org.westboy.temp.demo.Outer with modifiers "private"
	at sun.reflect.Reflection.ensureMemberAccess(Reflection.java:102)
	at java.lang.reflect.AccessibleObject.slowCheckMemberAccess(AccessibleObject.java:296)
	at java.lang.reflect.AccessibleObject.checkAccess(AccessibleObject.java:288)
	at java.lang.reflect.Method.invoke(Method.java:491)
	at org.westboy.temp.demo.Outer$Inner.reflectOuter(Outer.java:22)
	at org.westboy.temp.demo.Outer$Inner.access$000(Outer.java:14)
	at org.westboy.temp.demo.Outer.outerPublic(Outer.java:8)
	at org.westboy.temp.demo.Main.main(Main.java:13)
```

**CASE2**

目标类：

```java
public class Outer {

    public void outerPublic() throws Exception {
        // new Inner().reflectOuter(new Outer());
        new Inner().innerPublic();
    }

    private void outerPrivate() {
    }

    class Inner {

        public void innerPublic() {
            outerPrivate();
        }

        private void reflectOuter(Outer outer) throws Exception {
            Method method = outer.getClass().getDeclaredMethod("outerPrivate");
            method.invoke(outer);
        }
    }
}
```

测试类：

```java
public class Main {
    public static void main(String[] args) throws Exception {
        new Outer().outerPublic();
    }
}
```

执行成功~

## NBAC


