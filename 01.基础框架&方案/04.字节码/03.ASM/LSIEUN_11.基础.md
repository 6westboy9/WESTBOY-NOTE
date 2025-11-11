学习原始资料：

- [Java ASM系列一：Core API](https://blog.51cto.com/lsieun/2924583)
- [Java ASM系列二：OPCODE](https://blog.51cto.com/lsieun/3273965)
- [Java ASM系列三：Tree API](https://blog.51cto.com/lsieun/4034588)

# 1.介绍


## 版本

TODO

## 用途

* 生成新的Class（<font color="#f79646">generate</font>）
* 对已有的Class进行变换生成新的Class（<font color="#f79646">transform</font>）
* 对已有的Class进行分析不生成新的Class（<font color="#f79646">analyze</font>）

## 常见应用

### Spring AOP implemented with CGLib

Spring AOP可以通过JDK动态代理实现，也可以通过CGLib实现（已经不在维护了：[Github](https://github.com/cglib/cglib)）。其中CGLib是在ASM的基础上实现的。

### JDK Lambda

* 在rt.jar文件的jdk.internal.org.objectweb.asm包当中，就包含了JDK内置的ASM代码。在JDK 8版本当中，它所使用的ASM 5.0版本。
* 如果我们跟踪Lambda表达式的编码实现，就会找到InnerClassLambdaMetafactory#spinInnerClass方法。在这个方法当中，我们就会看到：<font color="#f79646">JDK会使用jdk.internal.org.objectweb.asm.ClassWriter来生成一个类，将lambda表达式的代码包装起来</font>。

* 第一步，找到这个方法：LambdaMetafactory#metafactory（可通过字节码指令查看到调用入口方法）
* 第二步，找到这个方法：InnerClassLambdaMetafactory#buildCallSite
* 第三步，找到这个方法：InnerClassLambdaMetafactory#spinInnerClass

简单写一个测试类：

```java
public class LambdaTest {
    public static void main(String[] args) {
        new Thread(() -> System.out.println("hello")).start();
    }
}
```

借助Byte Code Analyzer工具查看指令码：

![[Pasted image 20231115150054.png|400]]

# 2.组成部分

从组成结构上来说分为两部分：

* Core API
	* asm.jar
		* ClassReader
		* ClassVisitor
			* FieldVisitor
			* MethodVisitor
		* ClassWriter（父类ClassVisitor）
			* FieldWriter（父类FieldVisitor）
			* MethodWriter（父类MethodVisitorr）
	* asm-util.jar
	* asm-common.jar
* Tree API
	* asm-tree.jar、asm-analysis.jar

两者的关系，Core API是基础，而Tree API是在Core API的这个基础上构建起来的~

![[Pasted image 20231117205840.png|500]]

>MethodWriter的父类是MethodVisitor类，需要注意的是<font color="#f79646">MethodWriter类并不带有public修饰</font>，因此它的有效访问范围只局限于它所处package当中，不能像其它的public类一样被外部调用~

## Core API

### asm.jar

* <font color="#f79646">ClassReader</font>：负责读取Class文件里的内容，然后拆分成各个不同的部分。
* <font color="#f79646">ClassVisitor</font>：负责对Class文件中的某一个部分的信息进行修改。
* <font color="#f79646">ClassWriter</font>：负责将各个不同部分重新组合成一个完整的Class文件。

### asm-util.jar


### asm-commons.jar


## HelloWorld

编码实现

```java
public class HelloWorldDump {

    public static byte[] dump() {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);

        cw.visit(V1_8, ACC_PUBLIC | ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);

        {
            MethodVisitor mv1 = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
            mv1.visitCode();
            mv1.visitVarInsn(ALOAD, 0);
            mv1.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
            mv1.visitInsn(RETURN);
            mv1.visitMaxs(1, 1);
            mv1.visitEnd();
        }
        {
            MethodVisitor mv2 = cw.visitMethod(ACC_PUBLIC, "toString", "()Ljava/lang/String;", null, null);
            mv2.visitCode();
            mv2.visitLdcInsn("This is a HelloWorld object.");
            mv2.visitInsn(ARETURN);
            mv2.visitMaxs(1, 1);
            mv2.visitEnd();
        }
        cw.visitEnd();

        return cw.toByteArray();
    }
}
```

验证结果

```java
public class MyClassLoader extends ClassLoader {  
    @Override  
    protected Class<?> findClass(String name) throws ClassNotFoundException {  
        if ("sample.HelloWorld".equals(name)) {  
            byte[] bytes = HelloWorldDump.dump();  
            // File file = FileUtil.newFile("D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/sample/HelloWorld.class");  
            // FileUtil.writeBytes(bytes, file);  
            return defineClass(name, bytes, 0, bytes.length);  
        }  
        throw new ClassNotFoundException("Class Not Found: " + name);  
    }  
}
```

```java
public class HelloWorldRun {
    public static void main(String[] args) throws Exception {
        MyClassLoader classLoader = new MyClassLoader();
        Class<?> clazz = classLoader.loadClass("sample.HelloWorld");
        Object instance = clazz.newInstance();
        System.out.println(instance);
    }
}
```

运行后输出结果：

```
This is a HelloWorld object.
```


通过打开上述MyClassLoader中的注释代码，借助工具查看反编译后的源码如下：

```java
package sample;

public class HelloWorld {
    public HelloWorld() {
    }

    public String toString() {
        return "This is a HelloWorld object.";
    }
}
```


# 3.ASM与ClassFile

## ClassFile

参考[ Java Virtual Machine Specifications](https://docs.oracle.com/javase/specs/jvms/se8/html/index.html) 中的[Chapter 4. The class File Format (oracle.com)](https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html)定义：

```
ClassFile {
    u4             magic;
    u2             minor_version;
    u2             major_version;
    u2             constant_pool_count;
    cp_info        constant_pool[constant_pool_count-1];
    u2             access_flags;
    u2             this_class;
    u2             super_class;
    u2             interfaces_count;
    u2             interfaces[interfaces_count];
    u2             fields_count;
    field_info     fields[fields_count];
    u2             methods_count;
    method_info    methods[methods_count];
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
```

## 字节码类库

* [Apache Commons BCEL™ – Home](https://commons.apache.org/proper/commons-bcel/)
* [Javassist by jboss-javassist](http://www.javassist.org/)
* [ASM (ow2.io)](https://asm.ow2.io/)
* [Byte Buddy - runtime code generation for the Java virtual machine](https://bytebuddy.net/)

## ASM与ClassFile的关系

为了大家更直观的理解ASM与ClassFile之间关系，我们用下图来表示。其中，Java ClassFile相当于树根部分，ObjectWeb ASM相当于树干部分，而ASM的各种应用场景属于树枝或树叶部分。

![[Pasted image 20231115153246.png|350]]

## ASM学习层次

![[Pasted image 20231115153209.png|625]]


# 4.ClassFile

[[01.基础_ClassFile]]


# 5.ASMPrint工具-常用


在刚开始学习ASM的时候，编写ASM代码是不太容易的。或者，有些人原来对ASM很熟悉，但由于长时间不使用ASM，编写ASM代码也会有一些困难。在本文当中，我们介绍一个<font color="#f79646">ASMPrint</font>类，它能帮助我们将Class文件转换为ASM代码，这个功能非常实用。

```java
public class ASMPrint {
    public static void main(String[] args) throws IOException {
        // 1.设置参数
        String className = "org.asm.learn.l005.HelloWorld";
        int parsingOptions = ClassReader.SKIP_FRAMES | ClassReader.SKIP_DEBUG;
        boolean asmCode = true;

        // 2.打印结果
        Printer printer = asmCode ? new ASMifier() : new Textifier();
        PrintWriter printWriter = new PrintWriter(System.out, true);
        TraceClassVisitor traceClassVisitor = new TraceClassVisitor(null, printer, printWriter);
        new ClassReader(className).accept(traceClassVisitor, parsingOptions);
    }
}
```

说明：
* className设置为类的全限定名，可以是我们自己写的类，例如sample.HelloWorld，也可以是JDK自带的类，例如java.lang.Comparable。
* asmCode值设置为true或false。如果是true，可以打印出对应的ASM代码；如果是false，可以打印出方法对应的Instruction。
* parsingOptions值设置为ClassReader.SKIP_CODE、ClassReader.SKIP_DEBUG、ClassReader.SKIP_FRAMES、ClassReader.EXPAND_FRAMES的组合值，也可以设置为0，可以打印出详细程度不同的信息。

## ASMifier

>经过格式化后~

```java
package asm.org.asm.learn.l005;

import org.objectweb.asm.AnnotationVisitor;
import org.objectweb.asm.Attribute;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassWriter;
import org.objectweb.asm.ConstantDynamic;
import org.objectweb.asm.FieldVisitor;
import org.objectweb.asm.Handle;
import org.objectweb.asm.Label;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;
import org.objectweb.asm.RecordComponentVisitor;
import org.objectweb.asm.Type;
import org.objectweb.asm.TypePath;

public class HelloWorldDump implements Opcodes {

    public static byte[] dump () throws Exception {

        ClassWriter classWriter = new ClassWriter(0);
        FieldVisitor fieldVisitor;
        RecordComponentVisitor recordComponentVisitor;
        MethodVisitor methodVisitor;
        AnnotationVisitor annotationVisitor0;

        classWriter.visit(V1_8, ACC_PUBLIC | ACC_SUPER, "org/asm/learn/l005/HelloWorld", null, "java/lang/Object", null);

        {
            methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
            methodVisitor.visitCode();
            methodVisitor.visitVarInsn(ALOAD, 0);
            methodVisitor.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
            methodVisitor.visitInsn(RETURN);
            methodVisitor.visitMaxs(1, 1);
            methodVisitor.visitEnd();
        }
        {
            methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "toString", "()Ljava/lang/String;", null, null);
            methodVisitor.visitCode();
            methodVisitor.visitLdcInsn("This is a HelloWorld object.");
            methodVisitor.visitInsn(ARETURN);
            methodVisitor.visitMaxs(1, 1);
            methodVisitor.visitEnd();
        }
        classWriter.visitEnd();

        return classWriter.toByteArray();
    }
}
```

## Textifier

```
// class version 52.0 (52)
// access flags 0x21
public class org/asm/learn/l005/HelloWorld {


  // access flags 0x1
  public <init>()V
    ALOAD 0
    INVOKESPECIAL java/lang/Object.<init> ()V
    RETURN
    MAXSTACK = 1
    MAXLOCALS = 1

  // access flags 0x1
  public toString()Ljava/lang/String;
    LDC "This is a HelloWorld object."
    ARETURN
    MAXSTACK = 1
    MAXLOCALS = 1
}
```
