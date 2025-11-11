>接上节内容继续...
# 1.ClassVisitor

## 概述

ClassVisitor是一个抽象类，常见的子类有<font color="#f79646">ClassWriter（Core API）</font>和<font color="#f79646">ClassNode（Tree API）</font>。

![[Pasted image 20231115161948.png|300]]

### 字段

ClassVisitor类的字段

```java
public abstract class ClassVisitor {
	protected final int api;
	protected ClassVisitor cv;
}
```

* api字段：它是一个int类型的数据，指出了当前使用的ASM API版本，其取值有Opcodes.ASM4、Opcodes.ASM5、Opcodes.ASM6、Opcodes.ASM7、Opcodes.ASM8和Opcodes.ASM9。我们使用的ASM版本是9.0，因此我们在给api字段赋值的时候，选择Opcodes.ASM9就可以了。
* cv字段：它是一个ClassVisitor类型的数据，它的作用是将多个ClassVisitor串连起来。

![[Pasted image 20231115162753.png|350]]

### 方法

在ASM当中，使用到了Visitor Pattern（<font color="#f79646">访问者模式</font>），所以ClassVisitor当中许多的visitXxx方法。

虽然，在ClassVisitor类当中，有许多visitXxx方法，但是，<font color="#f79646">我们只需要关注这4个方法：visit、visitField、visitMethod和visitEnd</font>。为什么只关注这4个方法呢？<font color="#f79646">因为这4个方法是ClassVisitor类的精髓或骨架</font>，认识了这4个方法，其它的visitXxx都容易扩展；同时，我们将visitXxx方法缩小为4个，也能减少我们在学习ASM过程中的认知负担。

```java
public abstract class ClassVisitor {
    public void visit(
        final int version,
        final int access,
        final String name,
        final String signature,
        final String superName,
        final String[] interfaces);
    public FieldVisitor visitField( // 访问字段
        final int access,
        final String name,
        final String descriptor,
        final String signature,
        final Object value);
    public MethodVisitor visitMethod( // 访问方法
        final int access,
        final String name,
        final String descriptor,
        final String signature,
        final String[] exceptions);
    public void visitEnd();
    // ......
}
```

在ClassVisitor的visit、visitField和visitMethod方法中都带有signature参数。<font color="#f79646">这个signature参数与泛型密切相关</font>；换句话说，如果处理的是一个带有泛型信息的类、字段或方法，那么就需要给signature参数提供一定的值；如果处理的类、字段或方法不带有泛型信息，那么将signature参数设置为null就可以了。

## 方法调用顺序

在ClassVisitor类当中，定义了多个visitXxx方法。<font color="#f79646">这些visitXxx方法，遵循一定的调用顺序</font>。这个调用顺序，是参考自ClassVisitor类的API文档。

```
visit                                            <=== 重点关注
[visitSource][visitModule][visitNestHost][visitPermittedSubclass][visitOuterClass]
(
 visitAnnotation |
 visitTypeAnnotation |
 visitAttribute
)*
(
 visitNestMember |
 visitInnerClass |
 visitRecordComponent |
 visitField |                                    <=== 重点关注
 visitMethod                                     <=== 重点关注
)* 
visitEnd                                         <=== 重点关注
```

其中，涉及到一些符号，它们的含义如下：

* `[]`：表示最多调用一次，可以不调用，但最多调用一次。
* `()`和`|`：表示在多个方法之间，可以选择任意一个，并且多个方法之间不分前后顺序。
* `*`：表示方法可以调用0次或多次。

## 方法详述

### visit

<font color="#f79646">ClassVisitor#visit方法</font>

```java
public void visit(
    final int version,
    final int access,
    final String name,
    final String signature,
    final String superName,
    final String[] interfaces);
```

<font color="#f79646">ClassFile</font>

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

<font color="#f79646">映射关系</font>

| ClassVisitor方法 | 参数       | ClassFile                    |
| ---------------- | ---------- | ---------------------------- |
| visit            | version    | minor_version和major_version |
|                  | access     | access_flags                 |
|                  | name       | this_class                   |
|                  | signature  | attributes的一部分信息       |
|                  | superName  | super_class                  |
|                  | interfaces | interfaces_count和interfaces |
| visitField       |            | field_info                   |
| visitMethod      |            | method_info                  |

### visitField

<font color="#f79646">ClassVisitor#visitField方法</font>

```java
public FieldVisitor visitField( // 访问字段
    final int access,
    final String name,
    final String descriptor,
    final String signature,
    final Object value);
```

<font color="#f79646">field_info</font>

```
field_info {
    u2             access_flags;
    u2             name_index;
    u2             descriptor_index;
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
```

<font color="#f79646">映射关系</font>

| ClassVisitor方法 | 参数       | field_info             |
| ---------------- | ---------- | ---------------------- |
| visitField       | access     | access_flags           |
|                  | name       | name_index             |
|                  | descriptor | descriptor_index       |
|                  | signature  | attributes的一部分信息 |
|                  | value      | attributes的一部分信息 |

### visitMethod

<font color="#f79646">ClassVisitor#visitMethod方法</font>

```java
public MethodVisitor visitMethod( // 访问方法
    final int access,
    final String name,
    final String descriptor,
    final String signature,
    final String[] exceptions);
```

<font color="#f79646">method_info</font>

```
method_info {
    u2             access_flags;
    u2             name_index;
    u2             descriptor_index;
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
```

<font color="#f79646">映射关系</font>

| ClassVisitor方法 | 参数       | field_info             |
| ---------------- | ---------- | ---------------------- |
| visitMethod      | access     | access_flags           |
|                  | name       | name_index             |
|                  | descriptor | descriptor_index       |
|                  | signature  | attributes的一部分信息 |
|                  | exceptions | attributes的一部分信息 |


### visitEnd

visitEnd方法，它是这些visitXxx方法当中最后一个调用的方法。

为什么visitEnd()方法是最后一个调用的方法呢？是因为在ClassVisitor当中，定义了多个visitXxx方法，这些个visitXxx方法之间要遵循一个先后调用的顺序，而visitEnd方法是最后才去调用的。等到visitEnd方法调用之后，就表示说再也不去调用其它的visitXxx方法了，所有的工作已经做完了，到了要结束的时候了。

```java
public void visitEnd() {
    if (cv != null) {
        cv.visitEnd();
    }
}
```

# 2.ClassWriter

## 概述

ClassWriter的父类是ClassVisitor，因此ClassWriter类继承了visit、visitField、visitMethod和visitEnd等方法。

```java
public class ClassWriter extends ClassVisitor {
}
```

### 字段

```java
public class ClassWriter extends ClassVisitor {
    private int version;
    private final SymbolTable symbolTable;

    private int accessFlags;
    private int thisClass;
    private int superClass;
    private int interfaceCount;
    private int[] interfaces;

    private FieldWriter firstField;
    private FieldWriter lastField;

    private MethodWriter firstMethod;
    private MethodWriter lastMethod;

    private Attribute firstAttribute;

    //......
}
```

这些字段与ClassFile结构密切相关：

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

### 构造方法

ClassWriter定义的构造方法有两个，这里只关注其中一个，也就是只接收一个int类型参数的构造方法。在使用new关键字创建ClassWriter对象时，<font color="#f79646">推荐使用COMPUTE_FRAMES参数</font>。

```java
public class ClassWriter extends ClassVisitor {
    public static final int COMPUTE_MAXS = 1;
    public static final int COMPUTE_FRAMES = 2;
    public ClassWriter(final int flags) {
        this(null, flags);
    }
}
```

在创建ClassWriter对象的时候，要指定一个flags参数，它可以选择的值有三个：
* 第一个，可以选取的值是0。ASM不会自动计算max_stack和max_locals，也不会自动计算stack_map_frame。
* 第二个，可以选取的值是ClassWriter.COMPUTE_MAXS。ASM会自动计算max_stack和max_locals，但不会自动计算stack_map_frame。
* 第三个，可以选取的值是ClassWriter.COMPUTE_FRAMES（<font color="#f79646">推荐使用</font>）。ASM会自动计算max_stack和max_locals，也会自动计算stack_map_frame。

<font color="#f79646">为什么推荐使用COMPUTE_FRAMES？</font>

首先，来看一下max_stack和max_locals。在ClassFile结构中，每一个方法都用method_info来表示，而<font color="#f79646">方法里定义的代码则使用Code属性来表示</font>，其结构如下：

```
method_info {
    u2             access_flags;
    u2             name_index;
    u2             descriptor_index;
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}
```

Code属性结构：

```
Code_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 max_stack;     // 这里是max_stack
    u2 max_locals;    // 这里是max_locals
    u4 code_length;
    u1 code[code_length];
    u2 exception_table_length;
    {   u2 start_pc;
        u2 end_pc;
        u2 handler_pc;
        u2 catch_type;
    } exception_table[exception_table_length];
    u2 attributes_count;
    attribute_info attributes[attributes_count];
}
```

如果我们在创建ClassWriter对象的时候，将flags参数设置为ClassWriter.COMPUTE_MAXS或ClassWriter.COMPUTE_FRAMES，那么ASM会自动帮助我们计算Code结构中max_stack和max_locals的值。

接着，来看一下stack_map_frame。在Code结构里，可能有多个属性，其中一个可能就是StackMapTable。StackMapTable就是stack_map_frame具体存储格式，它的主要作用是对ByteCode进行类型检查。

属性结构

```
attribute_info {
    u2 attribute_name_index;
    u4 attribute_length;
    u1 info[attribute_length];
}
```

StackMapTable属性结构

```
StackMapTable_attribute {
    u2              attribute_name_index;
    u4              attribute_length;
    u2              number_of_entries;
    stack_map_frame entries[number_of_entries];
}
```

如果我们在创建ClassWriter对象的时候，将flags参数设置为ClassWriter.COMPUTE_FRAMES，那么ASM会自动帮助我们计算StackMapTable_attribute的内容。

![[Pasted image 20231115180556.png|700]]

我们推荐使用ClassWriter.COMPUTE_FRAMES。因为ClassWriter.COMPUTE_FRAMES这个选项，能够让ASM帮助我们自动计算max_stack、max_locals和stack_map_frame的具体内容。
* <font color="#f79646">如果将flags参数的取值为0，那么我们就必须要提供正确的max_stack、max_locals和stack_map_frame的值~</font>
* 如果将flags参数的取值为ClassWriter.COMPUTE_MAXS，那么ASM会自动帮助我们计算max_stack和max_locals，而我们则需要提供正确的stack_map_frame的值~

那么，<font color="#f79646">ASM为什么会提供0和ClassWriter.COMPUTE_MAXS这两个选项呢？</font>因为ASM在计算这些值的时候，要考虑各种各样不同的情况，所以它的算法相对来说就比较复杂，因而执行速度也会相对较慢。同时，ASM也鼓励开发者去研究更好的算法；如果开发者有更好的算法，就可以不去使用ClassWriter.COMPUTE_FRAMES，这样就能让程序的执行效率更高效。

但是，不得不说，要想计算max_stack、max_locals和stack_map_frame也不是一件容易的事情。出于方便的目的，就推荐大家使用ClassWriter.COMPUTE_FRAMES。

<font color="#4bacc6">在大多数情况下，ClassWriter.COMPUTE_FRAMES都能帮我们计算出正确的值。在少数情况下，ClassWriter.COMPUTE_FRAMES也可能会出错，比如说，有些代码经过混淆（obfuscate）处理，它里面的stack_map_frame会变更非常复杂，使用ClassWriter.COMPUTE_FRAMES就会出现错误的情况。针对这种少数的情况，我们可以在不改变原有stack_map_frame的情况下，使用ClassWriter.COMPUTE_MAXS，让ASM只帮助我们计算max_stack和max_locals。</font>

### 方法详述

#### visitXxx

在ClassWriter这个类当中，我们仍然是只关注其中的visit、visitField、visitMethod和visitEnd方法。这些visitXxx方法的调用，就是在为构建ClassFile提供原材料的过程。
#### toByteArray

在ClassWriter类当中，提供了一个toByteArray方法。这个方法的作用是将“所有的努力”（对visitXxx的调用）转换成字节数组，而这些字节数组的内容就遵循ClassFile结构。

在toByteArray方法的代码当中，通过三个步骤来得到字节数组：

* 第一步，计算size大小。这个size就是表示字节数组的最终的长度是多少。
* 第二步，将数据填充到字节数组当中。
* 第三步，将字节数组数据返回。


## 使用步骤

使用ClassWriter生成一个Class文件，可以大致分成三个步骤：

* 第一步，创建ClassWriter对象。
* 第二步，调用ClassWriter对象的visitXxx方法。
* 第三步，调用ClassWriter对象的toByteArray方法。

示例代码如下：

```java
import org.objectweb.asm.ClassWriter;

import static org.objectweb.asm.Opcodes.*;

public class HelloWorldGenerateCore {
    public static byte[] dump () throws Exception {
        // 1.创建ClassWriter对象
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);

        // 2.调用visitXxx方法
        cw.visit();
        cw.visitField();
        cw.visitMethod();
        cw.visitEnd();       // 注意，最后要调用visitEnd方法

        // 3.调用toByteArray方法
        byte[] bytes = cw.toByteArray();
        return bytes;
    }
}
```


## 示例1.生成接口（visit）

### 预期目标

```java
public interface HelloWorld {
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {  
  
    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";  
  
    public static void main(String[] args) throws Exception {  
        String relative_path = "sample/HelloWorld.class";  
        String filepath = PATH + relative_path;  
        byte[] bytes = dump();  
        FileUtil.writeBytes(bytes, filepath);  
    }  
  
    public static byte[] dump() throws Exception {  
        // 1.创建ClassWriter对象  
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);  
        // 2.调用visitXxx方法  
        cw.visit(  
            V1_8,                                        // version  
            ACC_PUBLIC + ACC_ABSTRACT + ACC_INTERFACE,   // access
            "sample/HelloWorld",                         // name  
            null,                                        // signature  
            "java/lang/Object",                          // superName  
            null                                         // interfaces  
        );  
        cw.visitEnd();  
        // 3.调用toByteArray方法  
        return cw.toByteArray();  
    }  
}
```

在上述代码中，我们调用了visit方法、visitEnd方法和toByteArray方法。由于sample.HelloWorld这个接口中，并没有定义任何的字段和方法，因此，在上述代码中没有调用visitField方法和visitMethod方法。

### 小结

在这里，我们重点介绍一下visit方法的各个参数：

* version: 表示当前类的版本信息。在上述示例代码中，其取值为Opcodes.V1_8，表示使用Java 8版本。
* access: 表示当前类的访问标识信息。在上面的示例中，access的取值是ACC_PUBLIC + ACC_ABSTRACT + ACC_INTERFACE，也可以写成ACC_PUBLIC | ACC_ABSTRACT | ACC_INTERFACE。
* name: 表示当前类的名字，它采用的格式是<font color="#f79646">Internal Name</font>的形式。
* signature: 表示当前类的泛型信息。因为在这个接口当中不包含任何的泛型信息，因此它的值为null。
* superName: 表示当前类的父类信息，它采用的格式是Internal Name的形式。
* interfaces: 表示当前类实现了哪些接口信息。

<font color="#f79646">Fully Qualified Class Name&Internal Name</font>

在Java文件中，我们使用Java语言来编写代码，使用类名的形式是Fully Qualified Class Name，例如java.lang.String；将Java文件编译之后，就会生成Class文件；在Class文件中，类名的形式会发生变化，称之为Internal Name，例如java/lang/String。因此，将Fully Qualified Class Name转换成Internal Name的方式就是，将`.`字符转换成`/`字符。

|          | Java Language              | Java ClassFile   |
| -------- | -------------------------- | ---------------- |
| 文件格式 | .java                      | .class           |
| 类名     | Fully Qualified Class Name | Internal Name    |
| 类名示例 | java.lang.String           | java/lang/String |

## 示例2.生成接口+字段+方法（visitField & visitMethod）

### 预期目标

```java
public interface HelloWorld extends Cloneable {
    int LESS = -1;
    int EQUAL = 0;
    int GREATER = 1;
    int compareTo(Object o);
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {  
  
    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";  
  
    public static void main(String[] args) throws Exception {  
        String relative_path = "sample/HelloWorld.class";  
        String filepath = PATH + relative_path;  
        byte[] bytes = dump();  
        FileUtil.writeBytes(bytes, filepath);  
    }  
  
    public static byte[] dump() throws Exception {  
        // 1.创建ClassWriter对象  
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);  
        // 2.调用visitXxx方法  
        cw.visit(V1_8, ACC_PUBLIC + ACC_ABSTRACT + ACC_INTERFACE, "sample/HelloWorld",  null, "java/lang/Object", new String[]{"java/lang/Cloneable"});  
        {  
            FieldVisitor fv1 = cw.visitField(ACC_PUBLIC + ACC_FINAL + ACC_STATIC, "LESS", "I", null, -1);  
            fv1.visitEnd();  
        }  
        {  
            FieldVisitor fv2 = cw.visitField(ACC_PUBLIC + ACC_FINAL + ACC_STATIC, "EQUAL", "I", null, 0);  
            fv2.visitEnd();  
        }  
        {  
            FieldVisitor fv3 = cw.visitField(ACC_PUBLIC + ACC_FINAL + ACC_STATIC, "GREATER", "I", null, 1);  
            fv3.visitEnd();  
        }  
        {  
            MethodVisitor mv1 = cw.visitMethod(ACC_PUBLIC + ACC_ABSTRACT, "compareTo", "(Ljava/lang/Object;)I", null, null);  
            mv1.visitEnd();  
        }  
        cw.visitEnd();  
        // 3.调用toByteArray方法  
        return cw.toByteArray();  
    }  
}
```

### 反编译结果

```java
package sample;

public interface HelloWorld extends Cloneable {
    int LESS = -1;
    int EQUAL = 0;
    int GREATER = 1;

    int compareTo(Object var1);
}
```


### 小结

在这里，我们重点说一下visitField方法和visitMethod方法的各个参数：

* visitField(access, name, descriptor, signature, value)
* visitMethod(access, name, descriptor, signature, exceptions)

这两个方法的前4个参数是相同的，不同的地方只在于第5个参数。

* access：表示当前字段或方法带有的访问标识信息，例如ACC_PUBLIC、ACC_STATIC和ACC_FINAL等。
* name：表示当前字段或方法的名字。
* descriptor：表示当前字段或方法的描述符。这些描述符，与我们平时使用的Java类型是有区别的。
* signature：表示当前字段或方法是否带有泛型信息。换句话说，如果不带有泛型信息，提供一个null就可以了；如果带有泛型信息，就需要给它提供某一个具体的值。
* value：是visitField方法的第5个参数。这个参数的取值，<font color="#f79646">与当前字段是否为常量有关系</font>。如果当前字段是一个常量，就需要给value参数提供某一个具体的值；如果当前字段不是常量，那么使用null就可以了。
* exceptions：是visitMethod方法的第5个参数。这个参数的取值，<font color="#f79646">与当前方法声明中是否具有throws XxxException相关</font>。

我们可以使用ASMPrint类来查看下面的sample.HelloWorld类的ASM代码，从而观察value参数和exceptions参数的取值。

源码：

```java
package org.asm.learn.l008_02;

import java.io.FileNotFoundException;
import java.io.IOException;

public class HelloWorld {
    // 这是一个常量字段，使用static、final关键字修饰
    public static final int constant_field = 10;
    // 这是一个非常量字段
    public int non_constant_field;

    public void test() throws FileNotFoundException, IOException {
        // do nothing
    }
}
```

工具类：

```java
public class ASMPrint {
    public static void main(String[] args) throws IOException {
        // 1.设置参数
        String className = "org.asm.learn.l008_02.HelloWorld";
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

生成的ASM代码：

```java
package asm.org.asm.learn.l008_02;
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

    public static byte[] dump() throws Exception {

        ClassWriter classWriter = new ClassWriter(0);
        FieldVisitor fieldVisitor;
        RecordComponentVisitor recordComponentVisitor;
        MethodVisitor methodVisitor;
        AnnotationVisitor annotationVisitor0;

        classWriter.visit(V1_8, ACC_PUBLIC | ACC_SUPER, "org/asm/learn/l008_02/HelloWorld", null, "java/lang/Object", null);

        {
            fieldVisitor = classWriter.visitField(ACC_PUBLIC | ACC_FINAL | ACC_STATIC, "constant_field", "I", null, new Integer(10)); // 观察常量最后一个value参数
            fieldVisitor.visitEnd();
        }
        {
            fieldVisitor = classWriter.visitField(ACC_PUBLIC, "non_constant_field", "I", null, null); // 观察非常量最后一个value参数（同常量的访问标志也不同）
            fieldVisitor.visitEnd();
        }
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
            methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "test", "()V", null, new String[]{"java/io/FileNotFoundException", "java/io/IOException"}); // 方法声明的异常信息
            methodVisitor.visitCode();
            methodVisitor.visitInsn(RETURN);
            methodVisitor.visitMaxs(0, 1);
            methodVisitor.visitEnd();
        }
        classWriter.visitEnd();

        return classWriter.toByteArray();
    }
}
```


## 示例3.生成类


### 预期目标

```java
public class HelloWorld {
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtil.writeBytes(bytes, filepath);
    }

    public static byte[] dump() throws Exception {
        // 1.创建ClassWriter对象
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        // 2.调用visitXxx方法
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);

        MethodVisitor mv = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
        mv.visitCode();
        mv.visitVarInsn(ALOAD, 0);
        mv.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
        mv.visitInsn(RETURN);
        mv.visitMaxs(1, 1);
        mv.visitEnd();

        cw.visitEnd();

        // 3.调用toByteArray方法
        return cw.toByteArray();
    }
}
```

### 与接口实现区别

![[Pasted image 20231116103952.png|1000]]

>注意：如果不加上述2部分的代码，就不会生成默认的构造方法，因而就不能实例化~

==测试验证==

1.注释掉上述2部分代码

2.自定义类加载器

```java
public class MyClassLoader extends ClassLoader {
    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        if ("sample.HelloWorld".equals(name)) {
            File file = FileUtil.newFile("D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/sample/HelloWorld.class");
            byte[] bytes = FileUtil.readBytes(file);
            return defineClass(name, bytes, 0, bytes.length);
        }
        throw new ClassNotFoundException("Class Not Found: " + name);
    }
}
```

3.使用

```java
public class HelloWorldRun {
    public static void main(String[] args) throws Exception {
        MyClassLoader classLoader = new MyClassLoader();
        Class<?> clazz = classLoader.loadClass("sample.HelloWorld");
        System.out.println(clazz);
        Object instance = clazz.newInstance();
        System.out.println(instance);
    }
}
```

输出结果：

```
class sample.HelloWorld                                                              # 可以加载
Exception in thread "main" java.lang.InstantiationException: sample.HelloWorld       # 但是不能实例化
	at java.lang.Class.newInstance(Class.java:427)
	at org.asm.learn.l008_03.HelloWorldRun.main(HelloWorldRun.java:8)
Caused by: java.lang.NoSuchMethodException: sample.HelloWorld.<init>()               # 指明原因没有默认构造方法
	at java.lang.Class.getConstructor0(Class.java:3082)
	at java.lang.Class.newInstance(Class.java:412)
	... 1 more
```


## 示例4.生成注解类

### 预期目标

```java
public @interface MyTag {
    String name();
    int age();
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/MyTag.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtil.writeBytes(bytes, filepath);
    }

    public static byte[] dump() throws Exception {
        ClassWriter classWriter = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        MethodVisitor methodVisitor;
        classWriter.visit(V1_8, ACC_PUBLIC | ACC_ANNOTATION | ACC_ABSTRACT | ACC_INTERFACE, "sample/MyTag", null, "java/lang/Object", new String[]{"java/lang/annotation/Annotation"});

        {
            methodVisitor = classWriter.visitMethod(ACC_PUBLIC | ACC_ABSTRACT, "name", "()Ljava/lang/String;", null, null);
            methodVisitor.visitEnd();
        }
        {
            methodVisitor = classWriter.visitMethod(ACC_PUBLIC | ACC_ABSTRACT, "age", "()I", null, null);
            methodVisitor.visitEnd();
        }
        classWriter.visitEnd();

        return classWriter.toByteArray();
    }
}
```

# 3.FieldVisitor

### 概述

TODO

## 示例1.字段常量


### 预期目标

```java
public interface HelloWorld {
    int intValue = 100;
    String strValue = "ABC";
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {  
  
    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";  
  
    public static void main(String[] args) throws Exception {  
        String relative_path = "sample/HelloWorld.class";  
        String filepath = PATH + relative_path;  
        byte[] bytes = dump();  
        FileUtil.writeBytes(bytes, filepath);  
    }  
  
    public static byte[] dump() throws Exception {  
        // 1.创建ClassWriter对象  
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);  
  
        // 2.调用visitXxx方法  
        cw.visit(V1_8, ACC_PUBLIC + ACC_ABSTRACT + ACC_INTERFACE, "sample/HelloWorld", null, "java/lang/Object", null);  
  
        {  
            FieldVisitor fv1 = cw.visitField(ACC_PUBLIC | ACC_FINAL | ACC_STATIC, "intValue", "I", null, 100);  
            fv1.visitEnd();  
        }  
  
        {  
            FieldVisitor fv2 = cw.visitField(ACC_PUBLIC + ACC_FINAL + ACC_STATIC, "strValue", "Ljava/lang/String;", null, "ABC");  
            fv2.visitEnd();  
        }  
  
        cw.visitEnd();  
  
        // 3.调用toByteArray方法  
        return cw.toByteArray();  
    }  
}
```

>在得到一个FieldVisitor对象之后，要<font color="#f79646">记得调用它的visitEnd方法</font>~

## 示例2.字段注解

###  预期目标

```java
public interface HelloWorld {
    @MyTag(name = "tomcat", age = 10)
    int intValue = 100;
}
```

其中MyTag定义如下：

```java
public @interface MyTag {
    String name();
    int age();
}
```

该注解类如何生成可以参考：[[LSIEUN_12.CORE_API_生成新的类#2.ClassWriter#示例4：生成注解类]]

### 编码实现

```java
public class HelloWorldGenerateCore {
    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtil.writeBytes(bytes, filepath);
    }

    public static byte[] dump() throws Exception {
        // 1.创建ClassWriter对象
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        // 2.调用visitXxx方法
        cw.visit(V1_8, ACC_PUBLIC | ACC_ABSTRACT | ACC_INTERFACE, "sample/HelloWorld", null, "java/lang/Object", null);

        {
            FieldVisitor fv1 = cw.visitField(ACC_PUBLIC | ACC_FINAL | ACC_STATIC, "intValue", "I", null, 100);

            {
                AnnotationVisitor anno = fv1.visitAnnotation("Lsample/MyTag;", false);
                anno.visit("name", "tomcat");
                anno.visit("age", 10);
                anno.visitEnd();
            }

            fv1.visitEnd();
        }

        cw.visitEnd();

        // 3.调用toByteArray方法
        return cw.toByteArray();
    }
}
```

# 4.FieldWriter

## 概述

TODO

# 5.MethodVisitor

通过调用ClassVisitor#visitMethod方法，会返回一个MethodVisitor类型的对象。

## 概述


## 方法的调用顺序

在MethodVisitor类当中，定义了许多的visitXxx方法，这些方法的调用，也要遵循一定的顺序。

```
(visitParameter)*
[visitAnnotationDefault]
(visitAnnotation | visitAnnotableParameterCount | visitParameterAnnotation | visitTypeAnnotation | visitAttribute)*
[
    visitCode
    (
        visitFrame |
        visitXxxInsn |
        visitLabel |
        visitInsnAnnotation |
        visitTryCatchBlock |
        visitTryCatchAnnotation |
        visitLocalVariable |
        visitLocalVariableAnnotation |
        visitLineNumber
    )*
    visitMaxs
]
visitEnd
```

其中，涉及到一些符号，它们的含义如下：

* `[]`：表示最多调用一次，可以不调用，但最多调用一次。
* `()`和`|`：表示在多个方法之间，可以选择任意一个，并且多个方法之间不分前后顺序。
* `*`：表示方法可以调用0次或多次。

我们可以把这些visitXxx方法分成三组：

* 第一组，在visitCode方法之前的方法。这一组的方法，主要负责parameter、annotation和attributes等内容；在当前我们暂时不去考虑这些内容，可以忽略这一组方法。
* 第二组，在visitCode方法和visitMaxs方法之间的方法。这一组的方法，主要负责当前方法的方法体内的opcode内容。其中，<font color="#f79646">visitCode方法，标志着方法体的开始，而visitMaxs方法，标志着方法体的结束~</font>
* 第三组，是visitEnd方法。这个visitEnd方法，是最后一个进行调用的方法。

对这些visitXxx方法进行精简之后，内容如下：

```
[
    visitCode
    (
        visitFrame |
        visitXxxInsn |
        visitLabel |
        visitTryCatchBlock
    )*
    visitMaxs
]
visitEnd
```

## 方法详述

>此处梳理的MethodVisitor中的方法对应ASM版本：TODO
>参考方法的调用顺序，将所有方法分为5个部分~

| 序号 | 部分 | 方法名称                     | 描述                                                                                                       |
| ---- | ---- | ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 1    | P1   | visitParameter               | 用于访问方法的参数信息                                                                                     |
| 2    | P1   | visitAnnotationDefault       | 用于访问注解的默认值信息                                                                                   |
| 3    | P1   | visitAnnotation              | 用于访问方法上的注解信息                                                                                   |
| 4    | P1   | visitTypeAnnotation          | 访问在方法上定义的类型注解                                                                                 |
| 5    | P1   | visitAnnotableParameterCount | 用于访问方法中参数上的注解信息（用于表示方法中可添加注解的参数数目）                                       |
| 6    | P1   | visitParameterAnnotation     | 用于访问方法中参数上的注解信息（用于访问方法参数上的注解内容）                                             |
| 7    | P1   | visitAttribute               | 用于访问方法中定义的非标准属性                                                                             |
| 8    | P2   | visitCode                    | 此方法表示开始访问方法中的内容，如果方法是抽象方法，即没有方法体内容，就不需调用此方法~                    |
| 9    | P3   | visitInsn                    | 用于访问<font color="#f79646">没有操作数</font>的指令                                                      |
| 10   | P3   | visitIntInsn                 | 用于访问<font color="#f79646">有操作数为int类型</font>的指令                                               |
| 11   | P3   | visitVarInsn                 | 用于访问<font color="#f79646">操作局部变量表</font>的指令                                                  |
| 12   | P3   | visitTypeInsn                | 用于访问<font color="#f79646">类型相关</font>的指令                                                        |
| 13   | P3   | visitFieldInsn               | 用于访问<font color="#f79646">与操作字段相关</font>的指令                                                  |
| 14   | P3   | visitMethodInsn              | 用于访问<font color="#f79646">与操作方法相关</font>的指令                                                  |
| 15   | P3   | visitInvokeDynamicInsn       | 访问invokedynamic指令                                                                                      |
| 16   | P3   | visitLabel                   | 用于在指定位置生成锚记点（也叫标记位置）                                                                   |
| 17   | P3   | visitJumpInsn                | 用于访问或创建跳转指令                                                                                     |
| 18   | P3   | visitLdcInsn                 | 此方法用于访问或者将常量压入操作数栈中                                                                     |
| 19   | P3   | visitIincInsn                | 用于访问或将IINC指令压入栈顶                                                                               |
| 20   | P3   | visitTableSwitchInsn         | 用于访问或者将tableswitch指令压入栈顶                                                                      |
| 21   | P3   | visitLookupSwitchInsn        | 用于访问或者将lookupswitch指令压入栈顶                                                                     |
| 22   | P3   | visitTryCatchBlock           | 用于实现try-catch语句块                                                                                    |
| 23   | P3   | visitLocalVariable           | 用于设定Code属性中的LocalVariableTable表中的某一项的值，调试器可以使用它来确定方法执行期间给定局部变量的值 |
| 24   | P3   | visitLineNumber              | 用于设置行号信息，调试器可以使用它来确定代码的哪一部分对应于源文件中的给定行号                             |
| 25   | P3   | visitFrame                   | 用于访问栈中信息                                                                                           |
| 26   | P4   | visitMaxs                    | 用于访问或设置方法的操作数栈和局部变量表的最大值                                                           |
| 27   | P5   | visitEnd                     |                                                                                                            |

### visitInsn

此方法用于访问<font color="#f79646">没有操作数</font>的指令。

### visitIntInsn

此方法用于访问有操作数为int类型的指令
###  visitVarInsn

此方法用于访问操作局部变量表的指令。

### visitLdcInsn

此方法用于访问或者将常量压入操作数栈中。

### visitLineNumber

visitLineNumber则用于设置行号信息。

## 示例1.生成<init\>方法

### 预期目标


```java
public class HelloWorld {
}
```

或者：

```java
public class HelloWorld {
    public HelloWorld() {
        super();
    }
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {  

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";  
  
    public static void main(String[] args) throws Exception {  
        String relative_path = "sample/HelloWorld.class";  
        String filepath = PATH + relative_path;  
        byte[] bytes = dump();  
        FileUtils.writeBytes(filepath, bytes);  
    }  
  
    public static byte[] dump() throws Exception {  
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);  
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);  
        {  
            MethodVisitor mv1 = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);  
            mv1.visitCode();  
            mv1.visitVarInsn(ALOAD, 0);  
            mv1.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);  
            mv1.visitInsn(RETURN);  
            mv1.visitMaxs(1, 1);  
            mv1.visitEnd();  
        }  
        cw.visitEnd();  
        return cw.toByteArray();  
    }  
}
```

### Frame变化

>关于Frame变化请先掌握[[LSIEUN_12.CORE_API_生成新的类#7.Frame]]

```
javap -c sample.HelloWorld      
public class sample.HelloWorld {
  public sample.HelloWorld();
    Code:
       0: aload_0
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return
}
```

使用Frame部分的HelloWorldFrameCore工具类输出Frame变化信息：

```
<init>()V
[uninitialized_this] []                     # 初始状态
[uninitialized_this] [uninitialized_this]   # aload_0
[sample/HelloWorld] []                      # invokespecial
[] []                                       # return
```

在这里，我们看到一个很“不一样”的变量，就是<font color="#f79646">uninitialized_this</font>，它就是一个“引用”，它指向的内存空间还没有初始化；等经过初始化之后，uninitialized_this变量就变成this变量。

## 示例2.生成<clinit\>方法


### 预期目标

```java
public class HelloWorld {
    static {
        System.out.println("class initialization method");
    }
}
```

或者：

```java
public class HelloWorld {
    public HelloWorld() {
    }

    static {
        System.out.println("class initialization method");
    }
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);
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
            MethodVisitor mv2 = cw.visitMethod(ACC_STATIC, "<clinit>", "()V", null, null);
            mv2.visitCode();
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("class initialization method");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            mv2.visitInsn(RETURN);
            mv2.visitMaxs(2, 0);
            mv2.visitEnd();
        }
        cw.visitEnd();
        return cw.toByteArray();
    }
}
```

### Frame变化

>关于Frame变化需要先掌握[[LSIEUN_12.CORE_API_生成新的类#7.Frame]]

```
javap -c sample.HelloWorld
public class sample.HelloWorld {
  public sample.HelloWorld();
    Code:
       0: aload_0
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return

  static {};
    Code:
       0: getstatic     #15                 // Field java/lang/System.out:Ljava/io/PrintStream;
       3: ldc           #17                 // String class initialization method
       5: invokevirtual #23                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
       8: return
}
```


```
<init>()V
[uninitialized_this] []
[uninitialized_this] [uninitialized_this]
[sample/HelloWorld] []
[] []

<clinit>()V
[] []                                            # 初始状态
[] [java/io/PrintStream]                         # getstatic       <= 获取System类的静态成员变量out，类型为PrintStream
[] [java/io/PrintStream, java/lang/String]       # ldc             <= Push item from run-time constant pool
[] []                                            # invokevirtual   <= 调用对象的实例方法
[] []                                            # return
```

>因为是静态方法，所以局部变量表第0个并没有this变量~

## 示例3.方法中创建对象

### 预期目标

假如有一个GoodChild类，内容如下：

```java
public class GoodChild {
    public String name;
    public int age;

    public GoodChild(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

我们的预期目标是生成一个HelloWorld类：

```java
public class HelloWorld {
    public void test() {
        GoodChild child = new GoodChild("Lucy", 8);
    }
}
```
### 编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);
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
            MethodVisitor mv2 = cw.visitMethod(ACC_PUBLIC, "test", "()V", null, null);
            mv2.visitCode();
            mv2.visitTypeInsn(NEW, "sample/GoodChild");
            mv2.visitInsn(DUP);
            mv2.visitLdcInsn("Lucy");
            mv2.visitIntInsn(BIPUSH, 8);
            mv2.visitMethodInsn(INVOKESPECIAL, "sample/GoodChild", "<init>", "(Ljava/lang/String;I)V", false);
            mv2.visitVarInsn(ASTORE, 1);
            mv2.visitInsn(RETURN);
            mv2.visitMaxs(4, 2);
            mv2.visitEnd();
        }
        cw.visitEnd();
        return cw.toByteArray();
    }
}
```

### Fram变化

>关关于Frame变化需要先掌握[[LSIEUN_12.CORE_API_生成新的类#7.Frame]]

```
javap -c sample.HelloWorld
public class sample.HelloWorld {
  public sample.HelloWorld();
    Code:
       0: aload_0
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return

  public void test();
    Code:
       0: new           #11                 // class sample/GoodChild
       3: dup
       4: ldc           #13                 // String Lucy
       6: bipush        8
       8: invokespecial #16                 // Method sample/GoodChild."<init>":(Ljava/lang/String;I)V
      11: astore_1
      12: return
}
```


```
<init>()V
[uninitialized_this] []
[uninitialized_this] [uninitialized_this]
[sample/HelloWorld] []
[] []

test()V
[sample/HelloWorld] []                                                                                       # 初始状态
[sample/HelloWorld] [uninitialized_sample/GoodChild]                                                         # new            <= 创建类实例的指令
[sample/HelloWorld] [uninitialized_sample/GoodChild, uninitialized_sample/GoodChild]                         # dup            <= 复制操作数栈栈顶的值并压入栈顶
[sample/HelloWorld] [uninitialized_sample/GoodChild, uninitialized_sample/GoodChild, java/lang/String]       # ldc            <= 将字符串常量（"Lucy"）加载至操作数栈
[sample/HelloWorld] [uninitialized_sample/GoodChild, uninitialized_sample/GoodChild, java/lang/String, int]  # bipush         <= 将byte常量（8）加载至操作数栈
[sample/HelloWorld] [sample/GoodChild]                                                                       # invokespecial  <= 调用GoodChild类的初始化，在这个过程中会消耗掉索引为1,2,3的操作数栈元素，索引为0变量一直没有变指向实例化对象
[sample/HelloWorld, sample/GoodChild] []                                                                     # astore_1       <= 将操作数栈栈顶元素存储到局部变量表
[] []                                                                                                        # return
```

>new指令后面跟了dup和invokespecial两个指令，其中dup指令的作用是复制操作数栈栈顶的值并压入栈顶。invokespecial在此处的作用是调用实例的构造函数。

<font color="#f79646">一般我们看到new+dup+invokespecial就可以立马想到是创建一个对象，且是通过无参构造方法创建的对象。如果有参的话，会在new和dup之间插入其它指令，用于加载参数至操作数栈~</font>

## 示例4.方法中调用其他方法

### 预期目标

```java
public class HelloWorld {
    public void test(int a, int b) {
        int val = Math.max(a, b); // 对static方法进行调用
        System.out.println(val);  // 对non-static方法进行调用
    }
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {
    
    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);
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
            MethodVisitor mv2 = cw.visitMethod(ACC_PUBLIC, "test", "(II)V", null, null);
            mv2.visitCode();
            mv2.visitVarInsn(ILOAD, 1);
            mv2.visitVarInsn(ILOAD, 2);
            mv2.visitMethodInsn(INVOKESTATIC, "java/lang/Math", "max", "(II)I", false);
            mv2.visitVarInsn(ISTORE, 3);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitVarInsn(ILOAD, 3);
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(I)V", false);
            mv2.visitInsn(RETURN);
            mv2.visitMaxs(2, 4);
            mv2.visitEnd();
        }
        cw.visitEnd();
        return cw.toByteArray();
    }
}
```

### Frame变化

>关于Frame变化需要先掌握[[LSIEUN_12.CORE_API_生成新的类#7.Frame]]

```
javap -c sample.HelloWorld
public class sample.HelloWorld {
  public sample.HelloWorld();
    Code:
       0: aload_0
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return

  public void test(int, int);
    Code:
       0: iload_1
       1: iload_2
       2: invokestatic  #16                 // Method java/lang/Math.max:(II)I
       5: istore_3
       6: getstatic     #22                 // Field java/lang/System.out:Ljava/io/PrintStream;
       9: iload_3
      10: invokevirtual #28                 // Method java/io/PrintStream.println:(I)V
      13: return
}
```

```
<init>()V
[uninitialized_this] []
[uninitialized_this] [uninitialized_this]
[sample/HelloWorld] []
[] []

test(II)V
[sample/HelloWorld, int, int] []                                     # 初始状态（因为不是静态方法调用，所以在局部变量表索引0处有个this）
[sample/HelloWorld, int, int] [int]                                  # iload_1
[sample/HelloWorld, int, int] [int, int]                             # iload_2
[sample/HelloWorld, int, int] [int]                                  # invokestatic（调用静态方法Math.max）
[sample/HelloWorld, int, int, int] []                                # istore_3
[sample/HelloWorld, int, int, int] [java/io/PrintStream]             # getstatic
[sample/HelloWorld, int, int, int] [java/io/PrintStream, int]        # iload_3
[sample/HelloWorld, int, int, int] []                                # invokevirtual
[] []                                                                # return
```

<font color="#f79646">注意</font>

![[Pasted image 20231118160746.png|900]]

## 示例5.不同MethodVisitor交叉使用

### 预期目标

```java
package sample;

import java.util.Date;

public class HelloWorld {
    public HelloWorld() {
    }

    public void test() {
        System.out.println("This is a test method.");
    }

    public void printDate() {
        Date var1 = new Date();
        System.out.println(var1);
    }
}
```

### 1.顺序编码实现

```java
public class HelloWorldGenerateCore {  
  
    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";  
  
    public static void main(String[] args) throws Exception {  
        String relative_path = "sample/HelloWorld.class";  
        String filepath = PATH + relative_path;  
        byte[] bytes = dump();  
        FileUtils.writeBytes(filepath, bytes);  
    }  
  
    public static byte[] dump() throws Exception {  
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);  
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);  
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
            MethodVisitor mv2 = cw.visitMethod(ACC_PUBLIC, "test", "()V", null, null);  
            mv2.visitCode();  
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");  
            mv2.visitLdcInsn("This is a test method.");  
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);  
            mv2.visitInsn(RETURN);  
            mv2.visitMaxs(2, 1);  
            mv2.visitEnd();  
        }  
        {  
            MethodVisitor mv3 = cw.visitMethod(ACC_PUBLIC, "printDate", "()V", null, null);  
            mv3.visitCode();  
            mv3.visitTypeInsn(NEW, "java/util/Date");  
            mv3.visitInsn(DUP);  
            mv3.visitMethodInsn(INVOKESPECIAL, "java/util/Date", "<init>", "()V", false);  
            mv3.visitVarInsn(ASTORE, 1);  
            mv3.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");  
            mv3.visitVarInsn(ALOAD, 1);  
            mv3.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/Object;)V", false);  
            mv3.visitInsn(RETURN);  
            mv3.visitMaxs(2, 2);  
            mv3.visitEnd();  
        }  
        cw.visitEnd();  
        return cw.toByteArray();  
    }  
}
```

### 2.交叉编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);
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
            MethodVisitor mv2 = cw.visitMethod(ACC_PUBLIC, "test", "()V", null, null);
            MethodVisitor mv3 = cw.visitMethod(ACC_PUBLIC, "printDate", "()V", null, null);

            // mv3
            mv3.visitCode();
            mv3.visitTypeInsn(NEW, "java/util/Date");
            mv3.visitInsn(DUP);
            mv3.visitMethodInsn(INVOKESPECIAL, "java/util/Date", "<init>", "()V", false);

            // mv2
            mv2.visitCode();
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("This is a test method.");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);

            // mv3
            mv3.visitVarInsn(ASTORE, 1);
            mv3.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv3.visitVarInsn(ALOAD, 1);
            mv3.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/Object;)V", false);

            // mv2
            mv2.visitInsn(RETURN);
            mv2.visitMaxs(2, 1);
            mv2.visitEnd();

            // mv3
            mv3.visitInsn(RETURN);
            mv3.visitMaxs(2, 2);
            mv3.visitEnd();
        }
        cw.visitEnd();
        return cw.toByteArray();
    }
}
```

## 使用经验

### 推荐使用COMPUTE_FRAMES

<font color="#f79646">为什么我们不推荐调用MethodVisitor#visitFrame方法呢？</font>原因是计算frame本身就很麻烦，还容易出错。

我们在创建ClassWriter对象的时候，使用了ClassWriter.COMPUTE_FRAMES参数：

```java
ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
```

使用ClassWriter.COMPUTE_FRAMES后，ASM会自动计算max_stacks、max_locals和stack_map_frames的具体值。

从代码的角度来说，<font color="#f79646">使用ClassWriter.COMPUTE_FRAMES，会忽略我们在代码中visitMaxs方法和visitFrame方法传入的具体参数值</font>；换句话说，无论我们传入的参数值是否正确，ASM会帮助我们从新计算一个正确的值，代替我们在代码中传入的参数。

需要注意的是，在创建ClassWriter对象时，flags参数使用ClassWriter.COMPUTE_FRAMES值时：
* <font color="#f79646">我们可以给visitMaxs方法传入一个错误的值，但是不能省略对于visitMaxs方法的调用</font>，如果我们省略掉对于visitMaxs方法的调用，生成的Class文件就会出错。
* <font color="#f79646">如果我们省略掉visitCode和visitEnd方法，生成的Class文件也不会出错</font>，当然，并不建议这么做。

### 不同MethodVisitor交叉使用

假如我们有两个MethodVisitor对象mv1和mv2，如下所示：

```java
MethodVisitor mv1 = cw.visitMethod(...);
MethodVisitor mv2 = cw.visitMethod(...);
```

同时，我们也知道MethodVisitor类里的visitXxx方法需要遵循一定的调用顺序：

* 第一步，调用visitCode方法，调用一次
* 第二步，调用visitXxxInsn方法，可以调用多次
* 第三步，调用visitMaxs方法，调用一次
* 第四步，调用visitEnd方法，调用一次

对于mv1和mv2这两个对象来说，它们的visitXxx方法的调用顺序是彼此独立的、不会相互干扰。

一般情况下，我们可以如下写代码，这样逻辑比较清晰：

```java
MethodVisitor mv1 = cw.visitMethod(...);
mv1.visitCode(...);
mv1.visitXxxInsn(...)
mv1.visitMaxs(...);
mv1.visitEnd();

MethodVisitor mv2 = cw.visitMethod(...);
mv2.visitCode(...);
mv2.visitXxxInsn(...)
mv2.visitMaxs(...);
mv2.visitEnd();
```

但是，我们也可以这样来写代码：

```java
MethodVisitor mv1 = cw.visitMethod(...);
MethodVisitor mv2 = cw.visitMethod(...);

mv1.visitCode(...);
mv2.visitCode(...);

mv2.visitXxxInsn(...)
mv1.visitXxxInsn(...)

mv1.visitMaxs(...);
mv1.visitEnd();
mv2.visitMaxs(...);
mv2.visitEnd();
```

在上面的代码中，mv1和mv2这两个对象的visitXxx方法交叉调用，这是可以的。换句话说，<font color="#f79646">只要每一个MethodVisitor对象在调用visitXxx方法时，遵循了调用顺序，那结果就是正确的</font>；不同的MethodVisitor对象，是相互独立的、不会彼此影响。

那么，可能有的同学会问：<font color="#f79646">MethodVisitor对象交叉使用有什么作用呢？有没有什么场景下的应用呢？回答是有的</font>。在ASM当中，有一个org.objectweb.asm.commons.StaticInitMerger类，类当中有一个MethodVisitor mergedClinitVisitor，它就是一个很好的示例，在后续内容中，我们会介绍到这个类。

org.objectweb.asm.commons.StaticInitMerger#visitMethod源码：

![[Pasted image 20231118164930.png|600]]

交叉使用示例代码见：[[LSIEUN_12.CORE_API_生成新的类#5.MethodVisitor#示例5.不同MethodVisitor交叉使用]]

# 6.MethodWriter

## 概述

### 字段

对应关系

![[Pasted image 20231117210802.png|500]]

# 7.Frame

## 概述

JVM Architecture组成

![[Pasted image 20231117212954.png|775]]

本节研究对象是Runtime Data Areas部分的Stack Frame~

![[Pasted image 20231117213807.png|1000]]

>在Runtime Data Area中，每个线程对应一个属于自己的Stack，当一个新线程开始时，就会在内存上分配一个属于自己的Stack；当线程结束时，相应的Stack就会被回收~


![[Pasted image 20231116153347.png|400]]

<font color="#f79646">在编译的时候，就决定了local_variables和operand_stack的大小~</font>

## 方法的初始Frame

<font color="#4bacc6">在方法刚开始的时候，operand_stack为空，不需要存储任何的数据，而local_variables的初始状态，则需要考虑三个因素：</font>

1. <font color="#4bacc6">当前方法是否为static方法？</font>
	* <font color="#f79646">如果当前方法是non-static方法，则需要在local_variables索引为0的位置存在一个this变量</font>
	* <font color="#f79646">如果当前方法是static方法，则不需要存储this</font>
2. <font color="#4bacc6">当前方法是否接收参数？</font>
	- 方法接收的参数会按照参数的声明顺序放到local_variables当中
3. <font color="#4bacc6">方法参数是否包含long或double类型？</font>
	- 如果方法的参数是long或double类型，那么它在local_variables当中占用两个位置

### static方法

```java
public class HelloWorld {
    public static int add(int a, int b) {
        return a + b;
    }
}
```

#### 打印Frame变化

运行HelloWorldFrameCore类

```java
public class HelloWorldFrameCore {  
  
    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/target/classes/";  
  
    public static void main(String[] args) {  
        String relative_path = "org/asm/learn/l013_02/HelloWorld.class";  
        String filepath = PATH + relative_path;  
        byte[] bytes = FileUtil.readBytes(filepath);  
  
        ClassReader cr = new ClassReader(bytes);  
        ClassVisitor cv = new MethodStackMapFrameVisitor(Opcodes.ASM9, null);  
        int parsingOptions = ClassReader.EXPAND_FRAMES; // 注意，这里使用了EXPAND_FRAMES  
        cr.accept(cv, parsingOptions);  
    }  
}
```

核心实现

```java
public class MethodStackMapFrameVisitor extends ClassVisitor {
    private String owner;

    public MethodStackMapFrameVisitor(int api, ClassVisitor classVisitor) {
        super(api, classVisitor);
    }

    @Override
    public void visit(int version, int access, String name, String signature, String superName, String[] interfaces) {
        super.visit(version, access, name, signature, superName, interfaces);
        this.owner = name;
    }

    @Override
    public MethodVisitor visitMethod(int access, String name, String descriptor, String signature, String[] exceptions) {
        MethodVisitor mv = super.visitMethod(access, name, descriptor, signature, exceptions);
        return new MethodStackMapFrameAdapter(api, owner, access, name, descriptor, mv);
    }

    private static class MethodStackMapFrameAdapter extends AnalyzerAdapter {
        private final String methodName;
        private final String methodDesc;

        public MethodStackMapFrameAdapter(int api, String owner, int access, String name, String descriptor, MethodVisitor methodVisitor) {
            super(api, owner, access, name, descriptor, methodVisitor);
            this.methodName = name;
            this.methodDesc = descriptor;
        }

        @Override
        public void visitCode() {
            super.visitCode();
            System.out.println();
            System.out.println(methodName + methodDesc);
            printStackMapFrame();
        }

        @Override
        public void visitInsn(int opcode) {
            super.visitInsn(opcode);
            printStackMapFrame();
        }

        @Override
        public void visitIntInsn(int opcode, int operand) {
            super.visitIntInsn(opcode, operand);
            printStackMapFrame();
        }

        @Override
        public void visitVarInsn(int opcode, int var) {
            super.visitVarInsn(opcode, var);
            printStackMapFrame();
        }

        @Override
        public void visitTypeInsn(int opcode, String type) {
            super.visitTypeInsn(opcode, type);
            printStackMapFrame();
        }

        @Override
        public void visitFieldInsn(int opcode, String owner, String name, String descriptor) {
            super.visitFieldInsn(opcode, owner, name, descriptor);
            printStackMapFrame();
        }

        @Override
        public void visitMethodInsn(int opcode, String owner, String name, String descriptor, boolean isInterface) {
            super.visitMethodInsn(opcode, owner, name, descriptor, isInterface);
            printStackMapFrame();
        }

        @Override
        public void visitInvokeDynamicInsn(String name, String descriptor, Handle bootstrapMethodHandle, Object... bootstrapMethodArguments) {
            super.visitInvokeDynamicInsn(name, descriptor, bootstrapMethodHandle, bootstrapMethodArguments);
            printStackMapFrame();
        }

        @Override
        public void visitJumpInsn(int opcode, Label label) {
            super.visitJumpInsn(opcode, label);
            printStackMapFrame();
        }

        @Override
        public void visitLdcInsn(Object value) {
            super.visitLdcInsn(value);
            printStackMapFrame();
        }

        @Override
        public void visitIincInsn(int var, int increment) {
            super.visitIincInsn(var, increment);
            printStackMapFrame();
        }

        @Override
        public void visitTableSwitchInsn(int min, int max, Label dflt, Label... labels) {
            super.visitTableSwitchInsn(min, max, dflt, labels);
            printStackMapFrame();
        }

        @Override
        public void visitLookupSwitchInsn(Label dflt, int[] keys, Label[] labels) {
            super.visitLookupSwitchInsn(dflt, keys, labels);
            printStackMapFrame();
        }

        @Override
        public void visitMultiANewArrayInsn(String descriptor, int numDimensions) {
            super.visitMultiANewArrayInsn(descriptor, numDimensions);
            printStackMapFrame();
        }

        private void printStackMapFrame() {
            String locals_str = locals == null ? "[]" : list2Str(locals);
            String stack_str = stack == null ? "[]" : list2Str(stack);
            String line = String.format("%s %s", locals_str, stack_str);
            System.out.println(line);
        }

        private String list2Str(List<Object> list) {
            if (list == null || list.size() == 0) return "[]";
            int size = list.size();
            String[] array = new String[size];
            for (int i = 0; i < size; i++) {
                Object item = list.get(i);
                array[i] = item2Str(item);
            }
            return Arrays.toString(array);
        }

        private String item2Str(Object obj) {
            if (obj == Opcodes.TOP) {
                return "top";
            }
            else if (obj == Opcodes.INTEGER) {
                return "int";
            }
            else if (obj == Opcodes.FLOAT) {
                return "float";
            }
            else if (obj == Opcodes.DOUBLE) {
                return "double";
            }
            else if (obj == Opcodes.LONG) {
                return "long";
            }
            else if (obj == Opcodes.NULL) {
                return "null";
            }
            else if (obj == Opcodes.UNINITIALIZED_THIS) {
                return "uninitialized_this";
            }
            else if (obj instanceof Label) {
                Object value = uninitializedTypes.get(obj);
                if (value == null) {
                    return obj.toString();
                }
                else {
                    return "uninitialized_" + value;
                }
            }
            else {
                return obj.toString();
            }
        }
    }
}
```

>这里涉及AnalyzerAdapter的内容，在后续进行深究~ <font color="#f79646">TODO</font>

输出结果：

```
<init>()V
[uninitialized_this] []
[uninitialized_this] [uninitialized_this]
[org/asm/learn/l013_02/HelloWorld] []
[] []

add(II)I
[int, int] []
[int, int] [int]
[int, int] [int, int]
[int, int] [int]
[] []
```

><font color="#4bacc6">在上面的结果中，第一对中括号中存放的是local_variables的数据，在第二对中括号中存放的是operand_stack的数据~</font>

#### 分析Frame变化


来查看add方法的<font color="#4bacc6">初始Frame</font>：

```
[int, int] []
```

```
javap -c org.asm.learn.l013_02.HelloWorld
Compiled from "HelloWorld.java"
public class org.asm.learn.l013_02.HelloWorld {
  public org.asm.learn.l013_01.HelloWorld();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public static int add(int, int);
    Code:
       0: iload_0
       1: iload_1
       2: iadd
       3: ireturn
```

其中add方法整体的Frame变化如下：

```
add(II)I
[int, int] []            # 初始状态
[int, int] [int]         # iload_0
[int, int] [int, int]    # iload_1
[int, int] [int]         # iadd    将操作数栈中两个整数弹出，进行加法运算，得到结果，再进行入栈~
[] []                    # ireturn 将整数值从方法的操作数栈中弹出（栈顶），并将其作为返回值返回~
```

<font color="#f79646">为什么最后一行打印为空呢？</font>

查看上述工具类MethodStackMapFrameVisitor调用visitMethod时，创建了一个MethodStackMapFrameAdapter对象，MethodStackMapFrameAdapter类继承自AnalyzerAdapter，AnalyzerAdapter属于asm-common.jar中的内容，后续进行深究补充~

查看AnalyzerAdapter的visitInsn方法就会发现其中的奥秘，因为在遇到ireturn、return和areturn时，会将局部变量表变量locals和操作数栈变量stack设置为null。

![[Pasted image 20231118112506.png|600]]

### non-static方法

```java
public class HelloWorld {
    public int add(int a, int b) {
        return a + b;
    }
}
```

```
javap -c org.asm.learn.l013_02.HelloWorld
Compiled from "HelloWorld.java"
public class org.asm.learn.l013_02.HelloWorld {
  public org.asm.learn.l013_02.HelloWorld();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public int add(int, int);
    Code:
       0: iload_1
       1: iload_2
       2: iadd
       3: ireturn
}
```

对比与静态方法的区别：

![[Pasted image 20231118113623.png|500]]

这是因为local_variables索引为0的位置存在一个this变量，因此其他参数变量都要向后移动。

使用上面HelloWorldFrameCore工具打印Fram变化过程：

```
<init>()V
[uninitialized_this] []
[uninitialized_this] [uninitialized_this]
[org/asm/learn/l013_02/HelloWorld] []
[] []

add(II)I
[org/asm/learn/l013_02/HelloWorld, int, int] []            # 初始状态
[org/asm/learn/l013_02/HelloWorld, int, int] [int]         # iload_0
[org/asm/learn/l013_02/HelloWorld, int, int] [int, int]    # iload_1
[org/asm/learn/l013_02/HelloWorld, int, int] [int]         # iadd
[] []                                                      # ireturn
```

如果当前方法是non-static方法，则需要在local_variables索引为0的位置存在一个this变量~

### long&double类型

```java
public class HelloWorld {
    public long add(long a, long b) {
        return a + b;
    }
}
```


```
javap -c org.asm.learn.l013_02.HelloWorld
Compiled from "HelloWorld.java"
public class org.asm.learn.l013_02.HelloWorld {
  public org.asm.learn.l013_02.HelloWorld();
    Code:
       0: aload_0
       1: invokespecial #1                  // Method java/lang/Object."<init>":()V
       4: return

  public long add(long, long);
    Code:
       0: lload_1
       1: lload_3
       2: ladd
       3: lreturn
}
```


```
<init>()V
[uninitialized_this] []
[uninitialized_this] [uninitialized_this]
[org/asm/learn/l013_02/HelloWorld] []
[] []

add(JJ)J
[org/asm/learn/l013_02/HelloWorld, long, top, long, top] []                      # 初始状态，这里将long和top放在一起表示一个long类型，占用2个位置
[org/asm/learn/l013_02/HelloWorld, long, top, long, top] [long, top]             # lload_1
[org/asm/learn/l013_02/HelloWorld, long, top, long, top] [long, top, long, top]  # lload_3
[org/asm/learn/l013_02/HelloWorld, long, top, long, top] [long, top]             # ladd
[] []                                                                            # lreturn
```


## 进阶1_ClassFile中的StackMapTable

视频地址：
* [Java ASM系列：（038）StackMapTable的由来_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV19B4y1K7gi/?spm_id_from=333.788&vd_source=401e9151ff5196d99069159680a48dbc)
* [Java ASM系列：（039）不推荐使用visitFrame方法_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV13q4y1s7Pg/?spm_id_from=333.788&vd_source=401e9151ff5196d99069159680a48dbc)
* [Java ASM系列：（040）StackMapTable进一步解释_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1HV411x7wT/?spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source=401e9151ff5196d99069159680a48dbc)
官方文档：https://docs.oracle.com/javase/specs/jvms/se8/html/jvms-4.html#jvms-4.7.4

![[Pasted image 20231120140521.png]]

```java
public class HelloWorld {
    public void test(boolean flag) {
        if (flag) {
            System.out.println("value is true");
        } else {
            System.out.println("value is false");
        }
    }
}
```

### 查看Instruction

```
public void test(boolean);
  Code:
     0: iload_1
     1: ifeq          15
     4: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
     7: ldc           #3                  // String value is true
     9: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
    12: goto          23
    15: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
    18: ldc           #5                  // String value is false
    20: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
    23: return
```

### 查看Frame

```
test(Z)V
[sample/HelloWorld, int] []                                             # 初始状态
[sample/HelloWorld, int] [int]                                          # iload_1
[sample/HelloWorld, int] []                                             # ifeq
[sample/HelloWorld, int] [java/io/PrintStream]                          # getstatic
[sample/HelloWorld, int] [java/io/PrintStream, java/lang/String]        # ldc
[sample/HelloWorld, int] []                                             # invokevirtual
[] []                                                                   # goto
[sample/HelloWorld, int] [java/io/PrintStream]                          # getstatic
[sample/HelloWorld, int] [java/io/PrintStream, java/lang/String]        # ldc
[sample/HelloWorld, int] []                                             # invokevirtual
[] []                                                                   # return
```

严格的来说，每一条Instruction都对应两个frame，一个是instruction执行之前的frame，另一个是instruction执行之后的frame。但是，当多个instruction放到一起的时候来说，第n个instruction执行之后的frame，就成为第n+1个instruction执行之前的frame，所以也可以理解成：每一条instruction对应一个frame。

这些frames是要存储起来的。我们知道，<font color="#f79646">每一个instruction对应一个frame，如果都要存储起来，那么在Class文件中就会占用非常多的空间</font>；而Class文件设计的一个主要目标就是尽量占用较小的存储空间，那么就需要对这些frames进行压缩。

### 压缩Frame

为了让Class文件占用的存储空间尽可能的小，因此要对frames进行压缩。对frames进行压缩，从本质上来说，就是忽略掉一些不重要的frames，而只留下一些重要的frames。

那么，怎样区分哪些frames重要，哪些frames不重要呢？我们从instruction执行顺序的角度来看待这个问题。

如果说，instruction是按照一个挨一个向下顺序执行的，那么它们对应的frames就不重要；相应的，instruction在执行过程时，它是从某个地方跳转过来的，那么对应的frames就重要。为什么说instruction是按照“一个挨一个向下顺序执行”的，那么它们对应的frames就不重要呢？因为这些instruction对应的frame可以很容易的推导出来。<font color="#f79646">如果当前的instruction是从某个地方跳转过来的，就必须要记录它执行之前的frame的情况，否则就没有办法计算它执行之后的frame的情况。当然，我们这里讲的只是大体的思路，而不是具体的判断细节~</font>

<font color="#f79646">经过压缩之后的frames，就存放在ClassFile的StackMapTable结构中~</font>

## 进阶2_如何使用visitFrame方法

### 预期目标

```java
public class HelloWorld {
    public void test(boolean flag) {
        if (flag) {
            System.out.println("value is true");
        } else {
            System.out.println("value is false");
        }
    }
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);

        {
            MethodVisitor mv1 = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
            mv1.visitCode();
            mv1.visitVarInsn(ALOAD, 0);
            mv1.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
            mv1.visitInsn(RETURN);
            mv1.visitMaxs(0, 0);
            mv1.visitEnd();
        }

        {
            MethodVisitor mv2 = cw.visitMethod(ACC_PUBLIC, "test", "(Z)V", null, null);
            Label elseLabel = new Label();
            Label returnLabel = new Label();

            // 第1段
            mv2.visitCode();
            mv2.visitVarInsn(ILOAD, 1);
            mv2.visitJumpInsn(IFEQ, elseLabel);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("value is true");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            mv2.visitJumpInsn(GOTO, returnLabel);

            // 第2段
            mv2.visitLabel(elseLabel);
            mv2.visitFrame(F_SAME, 0, null, 0, null); // 调用visitFrame方法
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("value is false");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);

            // 第3段
            mv2.visitLabel(returnLabel);
            mv2.visitFrame(F_SAME, 0, null, 0, null); // 调用visitFrame方法
            mv2.visitInsn(RETURN);
            mv2.visitMaxs(2, 2);
            mv2.visitEnd();
        }

        cw.visitEnd();
        return cw.toByteArray();
    }
}
```

![[Pasted image 20231120142839.png|600]]

在上面的代码中，我们创建ClassWriter对象时，使用了<font color="#f79646">ClassWriter.COMPUTE_MAXS</font>参数，这样ASM就会只计算max_locals和max_stack的值；在实现test方法的时候，就需要明确的调用MethodVisitor#visitFrame方法来添加相应的frame信息。

同时，我们也要注意到：MethodVisitor#visitLabel方法的调用在前，MethodVisitor#visitFrame方法的调用在后。因为MethodVisitor#visitLabel方法是放置了一个潜在的跳转label目标，程序在跳转之后，就需要使用MethodVisitor#visitFrame方法给出跳转之后Frame的具体情况。

<font color="#f79646">为什么第一个Frame不需要记录呢？因为初始的Frame可以通过方法的描述符计算出来~</font>

<font color="#f79646">每个Frame是依赖于前一个Frame的，也就是当前Frame记录的是与上一个Frame的差异，也就是说③处的Frame和②是一样的（局部变量表与操作数栈是相同的）②与①是一样的~</font>

![[Pasted image 20231121200017.png|800]]

局部变量表和操作数栈数据类型：

```
union verification_type_info {
    Top_variable_info;
    Integer_variable_info;
    Float_variable_info;
    Long_variable_info;
    Double_variable_info;
    Null_variable_info;
    UninitializedThis_variable_info;
    Object_variable_info;
    Uninitialized_variable_info;
}
```

StackMapTable属性结构：

![[Pasted image 20231120144133.png|400]]

1.借助[java8-classfile-tutorial/src/main/java/run/I_Attributes_Code.java at 9cf868d6db1943d492f2b43a6fcfd88c860e2d3f · lsieun/java8-classfile-tutorial (github.com)](https://github.com/lsieun/java8-classfile-tutorial/blob/9cf868d6db1943d492f2b43a6fcfd88c860e2d3f/src/main/java/run/I_Attributes_Code.java#L15)工具类查看：

```
--->|002| StackMapTable:
HexCode: 00130000000400020F07
attribute_name_index     = '0013' (#19)
attribute_length         = '00000004' (4)
number_of_entries        = '0002' (2)
stack_map_frame[0]@15 {
    same_frame {
        frame_type               = '0F' (15)
    }
}
stack_map_frame[1]@23 {
    same_frame {
        frame_type               = '07' (7)
    }
}
```

2.借助IDEA的插件查看：

![[Pasted image 20231120143655.png|800]]

3.查看Instruction：

```
public void test(boolean);
  Code:
     0: iload_1
     1: ifeq          15
     4: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
     7: ldc           #3                  // String value is true
     9: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
    12: goto          23
    15: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
    18: ldc           #5                  // String value is false
    20: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
    23: return
```

>其实我对于StackMapTable我还是懵懂的，仅知道其主要用于提高JVM在加载类时对局部变量表中的类型验证效率，但是具体的原理还是模糊的~


>此块的知识了解即可~


## 进阶3_不推荐使用visitFrame方法

为什么我们不推荐调用MethodVisitor.visitFrame方法呢？原因是计算frame本身就很麻烦，还容易出错。

我们在创建ClassWriter对象的时候，使用了<font color="#f79646">ClassWriter.COMPUTE_FRAMES</font>参数：

```java
ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
```

在使用了ClassWriter.COMPUTE_FRAMES参数之后，ASM会忽略代码当中对于MethodVisitor#visitFrame方法的调用，并且自动帮助我们计算stack_map_frame的具体内容。

# 8.Label

## 概述

所属范畴

![[Pasted image 20231118170333.png|800]]

由上图可见Label是属于MethodVisitor范畴的，那Label类到底是作甚的呢？

在程序中，有三种基本控制结构：顺序、选择和循环。

* 如果没有Label类的参与，那么MethodVisitor类只能生成顺序结构的代码；
* 如果有Label类的参与，MethodVisitor类就能生成选择和循环结构的代码。

如果查看Label类的API文档，就会发现下面的描述，分成了三个部分。

* A position in the bytecode of a method.
* Labels are used for jump, goto, and switch instructions, and for try catch blocks.
* A label designates the instruction that is just after. Note however that there can be other elements between a label and the instruction it designates (such as other labels, stack map frames, line numbers, etc.).

* 第一部分，Label类上是什么（What）；
* 第二部分，在哪些用到Label类（Where）；
* 第三部分，在编写ASM代码过程中，如何使用Label类（How），或者说，Label类与Instruction的关系。

如果是刚刚接触Label类，那么可能对于上面的三部分英文描述没有太多的感受或“理解；但是，如果接触Label类一段时间之后，就会发现它描述的内容很精髓。本节的内容也是围绕着这三部分来展开的。

## 1.Label类

在Label类当中，定义了很多的字段和方法。为了方便，将Label类简化一下，内容如下：

```java
public class Label {
    int bytecodeOffset;

    public Label() {
        // Nothing to do.
    }

    public int getOffset() {
        return bytecodeOffset;
    }
}
```

经过这样简化之后，<font color="#f79646">Label类当中就只包含一个bytecodeOffset字段，那么这个字段代表什么含义呢？</font>bytecodeOffset字段就是a position in the bytecode of a method。

举例子来说明一下。假如有一个test方法，它包含的Instruction内容如下：

```java
public class HelloWorld {
    public void test(boolean flag) {
        if (flag) {
            System.out.println("value is true");
        } else {
            System.out.println("value is false");
        }
    }
}
```

工具类

https://github.com/lsieun/java8-classfile-tutorial/blob/9cf868d6db1943d492f2b43a6fcfd88c860e2d3f/src/main/java/run/K_Code_Locals.java#L17

>注意使用时，需要修改

```java
// 修改前：因为原始项目中test方法是无参的
String name_and_type = "test:()V";
// 修改后：而现在我们的项目中test方法是含有一个boolean类型的参数
String name_and_type = "test:(Z)V";
```

<font color="#f79646">TODO 补充工具类</font>

输出结果：

```
constant_pool_count='0026' (38)
constant_pool
    |001| CONSTANT_Methodref {Value='java/lang/Object.<init>:()V', HexCode='0A00070017'}
    |002| CONSTANT_Fieldref {Value='java/lang/System.out:Ljava/io/PrintStream;', HexCode='0900180019'}
    |003| CONSTANT_String {Value='value is true', HexCode='08001A'}
    |004| CONSTANT_Methodref {Value='java/io/PrintStream.println:(Ljava/lang/String;)V', HexCode='0A001B001C'}
    |005| CONSTANT_String {Value='value is false', HexCode='08001D'}
    |006| CONSTANT_Class {Value='sample/HelloWorld', HexCode='07001E'}
    |007| CONSTANT_Class {Value='java/lang/Object', HexCode='07001F'}
    |008| CONSTANT_Utf8 {Value='<init>', HexCode='0100063C696E69743E'}
    |009| CONSTANT_Utf8 {Value='()V', HexCode='010003282956'}
    |010| CONSTANT_Utf8 {Value='Code', HexCode='010004436F6465'}
    |011| CONSTANT_Utf8 {Value='LineNumberTable', HexCode='01000F4C696E654E756D6265725461626C65'}
    |012| CONSTANT_Utf8 {Value='LocalVariableTable', HexCode='0100124C6F63616C5661726961626C655461626C65'}
    |013| CONSTANT_Utf8 {Value='this', HexCode='01000474686973'}
    |014| CONSTANT_Utf8 {Value='Lsample/HelloWorld;', HexCode='0100134C73616D706C652F48656C6C6F576F726C643B'}
    |015| CONSTANT_Utf8 {Value='test', HexCode='01000474657374'}
    |016| CONSTANT_Utf8 {Value='(Z)V', HexCode='010004285A2956'}
    |017| CONSTANT_Utf8 {Value='flag', HexCode='010004666C6167'}
    |018| CONSTANT_Utf8 {Value='Z', HexCode='0100015A'}
    |019| CONSTANT_Utf8 {Value='StackMapTable', HexCode='01000D537461636B4D61705461626C65'}
    |020| CONSTANT_Utf8 {Value='MethodParameters', HexCode='0100104D6574686F64506172616D6574657273'}
    |021| CONSTANT_Utf8 {Value='SourceFile', HexCode='01000A536F7572636546696C65'}
    |022| CONSTANT_Utf8 {Value='HelloWorld.java', HexCode='01000F48656C6C6F576F726C642E6A617661'}
    |023| CONSTANT_NameAndType {Value='<init>:()V', HexCode='0C00080009'}
    |024| CONSTANT_Class {Value='java/lang/System', HexCode='070020'}
    |025| CONSTANT_NameAndType {Value='out:Ljava/io/PrintStream;', HexCode='0C00210022'}
    |026| CONSTANT_Utf8 {Value='value is true', HexCode='01000D76616C75652069732074727565'}
    |027| CONSTANT_Class {Value='java/io/PrintStream', HexCode='070023'}
    |028| CONSTANT_NameAndType {Value='println:(Ljava/lang/String;)V', HexCode='0C00240025'}
    |029| CONSTANT_Utf8 {Value='value is false', HexCode='01000E76616C75652069732066616C7365'}
    |030| CONSTANT_Utf8 {Value='sample/HelloWorld', HexCode='01001173616D706C652F48656C6C6F576F726C64'}
    |031| CONSTANT_Utf8 {Value='java/lang/Object', HexCode='0100106A6176612F6C616E672F4F626A656374'}
    |032| CONSTANT_Utf8 {Value='java/lang/System', HexCode='0100106A6176612F6C616E672F53797374656D'}
    |033| CONSTANT_Utf8 {Value='out', HexCode='0100036F7574'}
    |034| CONSTANT_Utf8 {Value='Ljava/io/PrintStream;', HexCode='0100154C6A6176612F696F2F5072696E7453747265616D3B'}
    |035| CONSTANT_Utf8 {Value='java/io/PrintStream', HexCode='0100136A6176612F696F2F5072696E7453747265616D'}
    |036| CONSTANT_Utf8 {Value='println', HexCode='0100077072696E746C6E'}
    |037| CONSTANT_Utf8 {Value='(Ljava/lang/String;)V', HexCode='010015284C6A6176612F6C616E672F537472696E673B2956'}
=== === ===  === === ===  === === ===
Method test:(Z)V
=== === ===  === === ===  === === ===
max_stack = 2
max_locals = 2
code_length = 24
code = 1B99000EB200021203B60004A7000BB200021205B60004B1
=== === ===  === === ===  === === ===
0000: iload_1              // 1B
0001: ifeq            14   // 99000E
0004: getstatic       #2   // B20002     || java/lang/System.out:Ljava/io/PrintStream;
0007: ldc             #3   // 1203       || value is true
0009: invokevirtual   #4   // B60004     || java/io/PrintStream.println:(Ljava/lang/String;)V
0012: goto            11   // A7000B
0015: getstatic       #2   // B20002     || java/lang/System.out:Ljava/io/PrintStream;
0018: ldc             #5   // 1205       || value is false
0020: invokevirtual   #4   // B60004     || java/io/PrintStream.println:(Ljava/lang/String;)V
0023: return               // B1
=== === ===  === === ===  === === ===
LocalVariableTable:
index  start_pc  length  name_and_type
    0         0      24  this:Lsample/HelloWorld;
    1         0      24  flag:Z
```

详细说明

![[Pasted image 20231118175612.png|1000]]

那么，这个bytecodeOffset字段是做什么用的呢？<font color="#4bacc6">它用来计算一个</font><font color="#f79646">相对偏移量</font>。比如说，bytecodeOffset字段的值是15，它标识了getstatic指令的位置，而在索引值为1的位置是ifeq指令，ifeq后面跟的14，这个14就是一个相对偏移量。换一个角度来说，由于ifeq的索引位置是1，相对偏移量是14，那么1+14＝15，也就是说，如果ifeq的条件成立，那么下一条执行的指令就是索引值为15的getstatic指令了。

<font color="#f79646">方法体字节码所处位置</font>

![[Pasted image 20231118181737.png|1000]]
## 2.Label类能做什么

在ASM当中，Label类可以用于实现选择（if、switch）、循环（for、while）和try-catch语句。

在编写ASM代码的过程中，我们所要表达的是一种代码的跳转逻辑，就是从一个地方跳转到另外一个地方；在这两者之间，可以编写其它的代码逻辑，可能长一些，也可能短一些，所以，Instruction所对应的索引值还不确定。<font color="#f79646">Label类的出现，就是代表一个抽象的位置，也就是将来要跳转的目标。当我们调用ClassWriter.toByteArray()方法时，这些ASM代码会被转换成字节数组，在这个过程中，需要计算出Label对象中bytecodeOffset字段的值到底是多少，从而再进一步计算出跳转的相对偏移量</font>。

## 3.Label类如何使用

### 预期目标

```java
public class HelloWorld {
    public void test(boolean flag) {
        if (flag) {
            System.out.println("value is true");
        } else {
            System.out.println("value is false");
        }
    }
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {  
  
    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";  
  
    public static void main(String[] args) throws Exception {  
        String relative_path = "sample/HelloWorld.class";  
        String filepath = PATH + relative_path;  
        byte[] bytes = dump();  
        FileUtils.writeBytes(filepath, bytes);  
    }  
  
    public static byte[] dump() throws Exception {  
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);  
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);  
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
            MethodVisitor mv = cw.visitMethod(ACC_PUBLIC, "test", "(Z)V", null, null);  
            Label elseLabel = new Label();    // 首先，准备两个Label对象  
            Label returnLabel = new Label();  
  
            // 第1段  
            mv.visitCode();  
            mv.visitVarInsn(ILOAD, 1);  
            mv.visitJumpInsn(IFEQ, elseLabel);  
            mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");  
            mv.visitLdcInsn("value is true");  
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);  
            mv.visitJumpInsn(GOTO, returnLabel);  
  
            // 第2段  
            mv.visitLabel(elseLabel);         // 将第一个Label放到这里  
            mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");  
            mv.visitLdcInsn("value is false");  
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);  
  
            // 第3段  
            mv.visitLabel(returnLabel);       // 将第二个Label放到这里  
            mv.visitInsn(RETURN);  
            mv.visitMaxs(2, 2);  
            mv.visitEnd();  
        }  
        cw.visitEnd();  
        return cw.toByteArray();  
    }  
}
```


![[Pasted image 20231120090854.png|600]]

![[Pasted image 20231120091335.png|550]]

### 使用总结

如何使用Label类：

* 首先，定义Label类的实例label；
* 其次，通过MethodVisitor.visitLabel方法确定label的位置；
* 最后，在条件合适的情况下，通过MethodVisitor类跳转相关的方法（例如，visitJumpInsn方法）与label建立联系。

## 4.Frame的变化


```
javap -c sample.HelloWorld

  public void test(int, int);
    Code:
       0: iload_1
       1: iload_2
       2: invokestatic  #16                 // Method java/lang/Math.max:(II)I
    Code:
       0: aload_0
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return

  public void test(boolean);
    Code:
       0: iload_1
       1: ifeq          15
       4: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
       7: ldc           #18                 // String value is true
       9: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      12: goto          23
      15: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      18: ldc           #26                 // String value is false
      20: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      23: return
}
```


```
<init>()V
[uninitialized_this] []
[uninitialized_this] [uninitialized_this]
[sample/HelloWorld] []
[] []

test(Z)V
[sample/HelloWorld, int] []                                              # 初始状态（非静态方法，所以左侧局部变量索引为0处需要放置this变量）
[sample/HelloWorld, int] [int]                                           # iload_1
[sample/HelloWorld, int] []                                              # ifeq                <--- 默认与0进行比较
[sample/HelloWorld, int] [java/io/PrintStream]                           # getstatic
[sample/HelloWorld, int] [java/io/PrintStream, java/lang/String]         # ldc                 <--- 将"value is true"入栈
[sample/HelloWorld, int] []                                              # invokevirtual
[] []                                                                    # goto
[sample/HelloWorld, int] [java/io/PrintStream]                           # getstatic           <--- 注意这里是非线性的变化
[sample/HelloWorld, int] [java/io/PrintStream, java/lang/String]         # ldc                 <--- 将"value is false"入栈
[sample/HelloWorld, int] []                                              # invokevirtual
[] []                                                                    # return
```

![[Pasted image 20231120110308.png|750]]

>可以看到上面的boolean类型，指令为iload_1，对于boolean、byte、short、char和int这5种类型，均会转换成int类型（统一处理）~

通过上面的输出结果，我们希望大家能够看到：<font color="#f79646">由于程序代码逻辑发生了跳转，那么相应的local_variables和operand_stack结构也发生了非线性的变化</font>。这部分内容与MethodVisitor.visitFrame方法有关系。

<font color="#4bacc6">为什么上述goto打印结果为空数组呢？</font>

查看我们打印工具中MethodStackMapFrameAdapter的父类AnalyzerAdapter中的visitJumpInsn方法，便可得知其原因。

![[Pasted image 20231120092609.png|500]]

类似的情况在AnalyzerAdapter有四个方法：

* visitInsn
	* (opcode >= Opcodes.IRETURN && opcode <= Opcodes.RETURN) || opcode == Opcodes.ATHROW时
* visitJumpInsn
	* 对应跳转指令有
		* IFEQ
		* IFNE
		* IFLT
		* IFGE
		* IFGT
		* IFLE
		* IF_ICMPEQ
		* IF_ICMPNE
		* IF_ICMPLT
		* IF_ICMPGE
		* IF_ICMPGT
		* IF_ICMPLE
		* IF_ACMPEQ
		* IF_ACMPNE
		* GOTO
		* JSR
		* IFNULL
		* IFNONNULL
* visitTableSwitchInsn
	* 对应Java语法中的switch语句
* visitLookupSwitchInsn
	* 对应Java语法中的switch语句
	* 用于分支比较松散的情况，使用方式与visitTableSwitchInsn类似


## 示例1.if语句

### 预期目标

```java
package sample;  
  
public class HelloWorld {  
    public HelloWorld() {  
    }  
  
    public void test(int var1) {  
        if (var1 == 0) {  
            System.out.println("value is 0");  
        } else {  
            System.out.println("value is not 0");  
        }  
  
    }  
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);
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
            MethodVisitor mv = cw.visitMethod(ACC_PUBLIC, "test", "(I)V", null, null);
            Label elseLabel = new Label();
            Label returnLabel = new Label();

            // 第1段
            mv.visitCode();
            mv.visitVarInsn(ILOAD, 1);
            mv.visitJumpInsn(IFNE, elseLabel);
            mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv.visitLdcInsn("value is 0");
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            mv.visitJumpInsn(GOTO, returnLabel);

            // 第2段
            mv.visitLabel(elseLabel);
            mv.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv.visitLdcInsn("value is not 0");
            mv.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);

            // 第3段
            mv.visitLabel(returnLabel);
            mv.visitInsn(RETURN);
            mv.visitMaxs(2, 2);
            mv.visitEnd();
        }
        cw.visitEnd();
        return cw.toByteArray();
    }
}
```

## 示例2.switch语句

### 预期目标

```java
public class HelloWorld {
    public void test(int val) {
        switch (val) {
            case 1:
                System.out.println("val = 1");
                break;
            case 2:
                System.out.println("val = 2");
                break;
            case 3:
                System.out.println("val = 3");
                break;
            case 4:
                System.out.println("val = 4");
                break;
            default:
                System.out.println("val is unknown");
        }
    }
}
```

扩展：从Instruction的角度来说，实现switch语句可以使用lookupswitch或tableswitch指令~

<font color="#f79646">tableswitch</font>

上述预期目标使用的就是tableswitch指令：

```
javap -c sample.HelloWorld
public class sample.HelloWorld {
  public sample.HelloWorld();
    Code:
       0: aload_0
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return

  public void test(int);
    Code:
       0: iload_1
       1: tableswitch   { // 1 to 4
                     1: 32
                     2: 43
                     3: 54
                     4: 65
               default: 76
          }
      32: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      35: ldc           #18                 // String val = 1
      37: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      40: goto          84
      43: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      46: ldc           #26                 // String val = 2
      48: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      51: goto          84
      54: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      57: ldc           #28                 // String val = 3
      59: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      62: goto          84
      65: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      68: ldc           #30                 // String val = 4
      70: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      73: goto          84
      76: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      79: ldc           #32                 // String val is unknown
      81: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      84: return
}
```

如果将上述预期目标改为：

```java
public class HelloWorld {
    public void test(int val) {
        switch (val) {
            case 10:
                System.out.println("val = 1");
                break;
            case 20:
                System.out.println("val = 2");
                break;
            case 30:
                System.out.println("val = 3");
                break;
            case 40:
                System.out.println("val = 4");
                break;
            default:
                System.out.println("val is unknown");
        }
    }
}
```

将连续的1~4改为非连续的10，20，30和40时，将使用的是lookupswitch指令：

<font color="#f79646">lookupswitch</font>

```
javap -c sample.HelloWorld
public class sample.HelloWorld {
  public sample.HelloWorld();
    Code:                    
       0: aload_0                                                                  
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return                                                                   
                                                                                   
  public void test(int);                                                           
    Code:                                                                          
       0: iload_1                                                                  
       1: lookupswitch  { // 4                                                     
                    10: 44                                                         
                    20: 55                                                         
                    30: 66                                                         
                    40: 77
               default: 88
          }
      44: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      47: ldc           #18                 // String val = 1
      49: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      52: goto          96
      55: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      58: ldc           #26                 // String val = 2
      60: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      63: goto          96
      66: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      69: ldc           #28                 // String val = 3
      71: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      74: goto          96
      77: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      80: ldc           #30                 // String val = 4
      82: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      85: goto          96
      88: getstatic     #16                 // Field java/lang/System.out:Ljava/io/PrintStream;
      91: ldc           #32                 // String val is unknown
      93: invokevirtual #24                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      96: return
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);

        {
            MethodVisitor mv1 = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
            mv1.visitCode();
            mv1.visitVarInsn(ALOAD, 0);
            mv1.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
            mv1.visitInsn(RETURN);
            mv1.visitMaxs(0, 0);
            mv1.visitEnd();
        }

        {
            MethodVisitor mv2 = cw.visitMethod(ACC_PUBLIC, "test", "(I)V", null, null);
            Label caseLabel1 = new Label();
            Label caseLabel2 = new Label();
            Label caseLabel3 = new Label();
            Label caseLabel4 = new Label();
            Label defaultLabel = new Label();
            Label returnLabel = new Label();

            // 第1段
            mv2.visitCode();
            mv2.visitVarInsn(ILOAD, 1);
            mv2.visitTableSwitchInsn(1, 4, defaultLabel, caseLabel1, caseLabel2, caseLabel3, caseLabel4);

            // 第2段
            mv2.visitLabel(caseLabel1);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("val = 1");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            mv2.visitJumpInsn(GOTO, returnLabel);

            // 第3段
            mv2.visitLabel(caseLabel2);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("val = 2");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            mv2.visitJumpInsn(GOTO, returnLabel);

            // 第4段
            mv2.visitLabel(caseLabel3);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("val = 3");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            mv2.visitJumpInsn(GOTO, returnLabel);

            // 第5段
            mv2.visitLabel(caseLabel4);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("val = 4");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            mv2.visitJumpInsn(GOTO, returnLabel);

            // 第6段
            mv2.visitLabel(defaultLabel);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("val is unknown");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            // 此处就不需要添加GOTO指令了~

            // 第7段
            mv2.visitLabel(returnLabel);
            mv2.visitInsn(RETURN);
            mv2.visitMaxs(0, 0);
            mv2.visitEnd();
        }

        cw.visitEnd();

        return cw.toByteArray();
    }
}
```


## 示例3.for语句

### 预期目标

```java
public class HelloWorld {
    public void test() {
        for (int i = 0; i < 10; i++) {
            System.out.println(i);
        }
    }
}
```

### 编码实现

```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);

        {
            MethodVisitor mv1 = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
            mv1.visitCode();
            mv1.visitVarInsn(ALOAD, 0);
            mv1.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
            mv1.visitInsn(RETURN);
            mv1.visitMaxs(0, 0);
            mv1.visitEnd();
        }

        {
            MethodVisitor methodVisitor = cw.visitMethod(ACC_PUBLIC, "test", "()V", null, null);
            Label conditionLabel = new Label();
            Label returnLabel = new Label();

            // 第1段
            methodVisitor.visitCode();
            methodVisitor.visitInsn(ICONST_0);
            methodVisitor.visitVarInsn(ISTORE, 1);

            // 第2段
            methodVisitor.visitLabel(conditionLabel);
            methodVisitor.visitVarInsn(ILOAD, 1);
            methodVisitor.visitIntInsn(BIPUSH, 10);
            methodVisitor.visitJumpInsn(IF_ICMPGE, returnLabel);
            methodVisitor.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            methodVisitor.visitVarInsn(ILOAD, 1);
            methodVisitor.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(I)V", false);
            methodVisitor.visitIincInsn(1, 1);
            methodVisitor.visitJumpInsn(GOTO, conditionLabel);

            // 第3段
            methodVisitor.visitLabel(returnLabel);
            methodVisitor.visitInsn(RETURN);
            methodVisitor.visitMaxs(0, 0);
            methodVisitor.visitEnd();
        }

        cw.visitEnd();

        return cw.toByteArray();
    }
}
```

## 示例4.try-catch语句

### 预期目标

```java
public class HelloWorld {
    public void test() {
        try {
            System.out.println("Before Sleep");
            Thread.sleep(1000);
            System.out.println("After Sleep");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

### 编码实现


```java
public class HelloWorldGenerateCore {

    private static final String PATH = "D:/IdeaProjects/mine/westboy-hub/base-asm/generated-classes/";

    public static void main(String[] args) throws Exception {
        String relative_path = "sample/HelloWorld.class";
        String filepath = PATH + relative_path;
        byte[] bytes = dump();
        FileUtils.writeBytes(filepath, bytes);
    }

    public static byte[] dump() throws Exception {
        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_FRAMES);
        cw.visit(V1_8, ACC_PUBLIC + ACC_SUPER, "sample/HelloWorld", null, "java/lang/Object", null);
        {
            MethodVisitor mv1 = cw.visitMethod(ACC_PUBLIC, "<init>", "()V", null, null);
            mv1.visitCode();
            mv1.visitVarInsn(ALOAD, 0);
            mv1.visitMethodInsn(INVOKESPECIAL, "java/lang/Object", "<init>", "()V", false);
            mv1.visitInsn(RETURN);
            mv1.visitMaxs(0, 0);
            mv1.visitEnd();
        }
        {
            MethodVisitor mv2 = cw.visitMethod(ACC_PUBLIC, "test", "()V", null, null);
            Label startLabel = new Label();
            Label endLabel = new Label();
            Label handlerLabel = new Label();
            Label returnLabel = new Label();

            // 第1段
            mv2.visitCode();
            // visitTryCatchBlock可以在这里访问
            mv2.visitTryCatchBlock(startLabel, endLabel, handlerLabel, "java/lang/InterruptedException");

            // 第2段
            mv2.visitLabel(startLabel);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("Before Sleep");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);
            mv2.visitLdcInsn(1000L);
            mv2.visitMethodInsn(INVOKESTATIC, "java/lang/Thread", "sleep", "(J)V", false);
            mv2.visitFieldInsn(GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            mv2.visitLdcInsn("After Sleep");
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V", false);

            // 第3段
            mv2.visitLabel(endLabel);
            mv2.visitJumpInsn(GOTO, returnLabel);

            // 第4段
            mv2.visitLabel(handlerLabel);
            mv2.visitVarInsn(ASTORE, 1);
            mv2.visitVarInsn(ALOAD, 1);
            mv2.visitMethodInsn(INVOKEVIRTUAL, "java/lang/InterruptedException", "printStackTrace", "()V", false);

            // 第5段
            mv2.visitLabel(returnLabel);
            mv2.visitInsn(RETURN);

            // 第6段
            // visitTryCatchBlock也可以在这里访问
            // mv2.visitTryCatchBlock(startLabel, endLabel, handlerLabel, "java/lang/InterruptedException");
            mv2.visitMaxs(0, 0);
            mv2.visitEnd();
        }
        cw.visitEnd();
        return cw.toByteArray();
    }
}
```

```
javap -c sample.HelloWorld      
public class sample.HelloWorld {
  public sample.HelloWorld();
    Code:                    
       0: aload_0                                                                  
       1: invokespecial #8                  // Method java/lang/Object."<init>":()V
       4: return                                                                   
                                                                                   
  public void test();                                                              
    Code:                                                                          
       0: getstatic     #17                 // Field java/lang/System.out:Ljava/io/PrintStream;
       3: ldc           #19                 // String Before Sleep
       5: invokevirtual #25                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
       8: ldc2_w        #26                 // long 1000l
      11: invokestatic  #33                 // Method java/lang/Thread.sleep:(J)V
      14: getstatic     #17                 // Field java/lang/System.out:Ljava/io/PrintStream;
      17: ldc           #35                 // String After Sleep
      19: invokevirtual #25                 // Method java/io/PrintStream.println:(Ljava/lang/String;)V
      22: goto          30
      25: astore_1
      26: aload_1
      27: invokevirtual #38                 // Method java/lang/InterruptedException.printStackTrace:()V
      30: return
    Exception table:
       from    to  target type
           0    22    25   Class java/lang/InterruptedException
}
```

### 小结

有一个问题，visitTryCatchBlock方法为什么可以在后边的位置调用呢？这与Code属性的结构有关系：

```
Code_attribute {
    u2 attribute_name_index;
    u4 attribute_length;
    u2 max_stack;
    u2 max_locals;
    u4 code_length;
    u1 code[code_length];
    u2 exception_table_length;
    {   u2 start_pc;
        u2 end_pc;
        u2 handler_pc;
        u2 catch_type;
    } exception_table[exception_table_length];
    u2 attributes_count;
    attribute_info attributes[attributes_count];
}
```

因为instruction的内容（对应于visitXxxInsn方法的调用）存储于Code结构当中的codes数组内，<font color="#f79646">而try-catch的内容（对应于visitTryCatchBlock方法的调用），存储在Code结构当中的exception_table数组内</font>，所以visitTryCatchBlock方法的调用时机，可以早一点，也可以晚一点，只要整体上遵循MethodVisitor类对就于visitXxx方法调用的顺序要求就可以了。

# 9.Opcodes

Opcodes是一个接口，它定义了许多字段。这些字段主要是在ClassVisitor.visitXxx和MethodVisitor.visitXxx方法中使用。
## 1.在ClassVisitor中的应用

### 1.1.ASM Version

字段含义：Opcodes.ASM4~Opcodes.ASM9标识了ASM的版本信息。

应用场景：用于创建具体的ClassVisitor实例，例如ClassVisitor(int api, ClassVisitor classVisitor)中的api参数。

```java
public interface Opcodes {
    // ASM API versions.
    int ASM4 = 4 << 16 | 0 << 8;
    int ASM5 = 5 << 16 | 0 << 8;
    int ASM6 = 6 << 16 | 0 << 8;
    int ASM7 = 7 << 16 | 0 << 8;
    int ASM8 = 8 << 16 | 0 << 8;
    int ASM9 = 9 << 16 | 0 << 8;
}
```

### 1.2.Java Version

字段含义：Opcodes.V1_1~Opcodes.V16标识了.class文件的版本信息。

应用场景：用于ClassVisitor.visit(int version, int access, ...)的version参数。

```java
public interface Opcodes {
    // Java ClassFile versions
    // (the minor version is stored in the 16 most significant bits, and the major version in the 16 least significant bits).
    int V1_1 = 3 << 16 | 45;
    int V1_2 = 0 << 16 | 46;
    int V1_3 = 0 << 16 | 47;
    int V1_4 = 0 << 16 | 48;
    int V1_5 = 0 << 16 | 49;
    int V1_6 = 0 << 16 | 50;
    int V1_7 = 0 << 16 | 51;
    int V1_8 = 0 << 16 | 52;

    int V9  = 0 << 16 | 53;
    int V10 = 0 << 16 | 54;
    int V11 = 0 << 16 | 55;
    int V12 = 0 << 16 | 56;
    int V13 = 0 << 16 | 57;
    int V14 = 0 << 16 | 58;
    int V15 = 0 << 16 | 59;
    int V16 = 0 << 16 | 60;
}
```

### 1.3.Access Flags

字段含义：Opcodes.ACC_PUBLIC~Opcodes.ACC_MODULE标识了Class、Field、Method的访问标识（Access Flag）。

应用场景：

* ClassVisitor.visit(int version, int access, ...)的access参数。
* ClassVisitor.visitField(int access, String name, ...)的access参数。
* ClassVisitor.visitMethod(int access, String name, ...)的access参数。

>注释部分为应用级别，class表示类，field表示字段，method表示方法

```java
public interface Opcodes {
    int ACC_PUBLIC = 0x0001;       // class, field, method
    int ACC_PRIVATE = 0x0002;      // class, field, method
    int ACC_PROTECTED = 0x0004;    // class, field, method
    int ACC_STATIC = 0x0008;       // field, method
    int ACC_FINAL = 0x0010;        // class, field, method, parameter
    int ACC_SUPER = 0x0020;        // class
    int ACC_SYNCHRONIZED = 0x0020; // method
    int ACC_OPEN = 0x0020;         // module
    int ACC_TRANSITIVE = 0x0020;   // module requires
    int ACC_VOLATILE = 0x0040;     // field
    int ACC_BRIDGE = 0x0040;       // method
    int ACC_STATIC_PHASE = 0x0040; // module requires
    int ACC_VARARGS = 0x0080;      // method
    int ACC_TRANSIENT = 0x0080;    // field
    int ACC_NATIVE = 0x0100;       // method
    int ACC_INTERFACE = 0x0200;    // class
    int ACC_ABSTRACT = 0x0400;     // class, method
    int ACC_STRICT = 0x0800;       // method
    int ACC_SYNTHETIC = 0x1000;    // class, field, method, parameter, module *
    int ACC_ANNOTATION = 0x2000;   // class
    int ACC_ENUM = 0x4000;         // class(?) field inner
    int ACC_MANDATED = 0x8000;     // field, method, parameter, module, module *
    int ACC_MODULE = 0x8000;       // class
}
```

## 2.在MethodVisitor中的应用

### 2.1.frame

![[Pasted image 20231121203234.png|1000]]
### 2.2.opcodes

字段含义：Opcodes.NOP~Opcodes.IFNONNULL表示opcode的值。

应用场景：在MethodVisitor.visitXxxInsn(opcode)方法中的opcode参数中使用。

>注释部分表示其应用的方法名~

```java
public interface Opcodes {
    int NOP = 0; // visitInsn
    int ACONST_NULL = 1; // - 同上
    int ICONST_M1 = 2; // -
    int ICONST_0 = 3; // -
    int ICONST_1 = 4; // -
    int ICONST_2 = 5; // -
    int ICONST_3 = 6; // -
    int ICONST_4 = 7; // -
    int ICONST_5 = 8; // -
    int LCONST_0 = 9; // -
    int LCONST_1 = 10; // -
    int FCONST_0 = 11; // -
    int FCONST_1 = 12; // -
    int FCONST_2 = 13; // -
    int DCONST_0 = 14; // -
    int DCONST_1 = 15; // -
    int BIPUSH = 16; // visitIntInsn
    int SIPUSH = 17; // -
    int LDC = 18; // visitLdcInsn
    int ILOAD = 21; // visitVarInsn
    int LLOAD = 22; // -
    int FLOAD = 23; // -
    int DLOAD = 24; // -
    int ALOAD = 25; // -
    int IALOAD = 46; // visitInsn
    int LALOAD = 47; // -
    int FALOAD = 48; // -
    int DALOAD = 49; // -
    int AALOAD = 50; // -
    int BALOAD = 51; // -
    int CALOAD = 52; // -
    int SALOAD = 53; // -
    int ISTORE = 54; // visitVarInsn
    int LSTORE = 55; // -
    int FSTORE = 56; // -
    int DSTORE = 57; // -
    int ASTORE = 58; // -
    int IASTORE = 79; // visitInsn
    int LASTORE = 80; // -
    int FASTORE = 81; // -
    int DASTORE = 82; // -
    int AASTORE = 83; // -
    int BASTORE = 84; // -
    int CASTORE = 85; // -
    int SASTORE = 86; // -
    int POP = 87; // -
    int POP2 = 88; // -
    int DUP = 89; // -
    int DUP_X1 = 90; // -
    int DUP_X2 = 91; // -
    int DUP2 = 92; // -
    int DUP2_X1 = 93; // -
    int DUP2_X2 = 94; // -
    int SWAP = 95; // -
    int IADD = 96; // -
    int LADD = 97; // -
    int FADD = 98; // -
    int DADD = 99; // -
    int ISUB = 100; // -
    int LSUB = 101; // -
    int FSUB = 102; // -
    int DSUB = 103; // -
    int IMUL = 104; // -
    int LMUL = 105; // -
    int FMUL = 106; // -
    int DMUL = 107; // -
    int IDIV = 108; // -
    int LDIV = 109; // -
    int FDIV = 110; // -
    int DDIV = 111; // -
    int IREM = 112; // -
    int LREM = 113; // -
    int FREM = 114; // -
    int DREM = 115; // -
    int INEG = 116; // -
    int LNEG = 117; // -
    int FNEG = 118; // -
    int DNEG = 119; // -
    int ISHL = 120; // -
    int LSHL = 121; // -
    int ISHR = 122; // -
    int LSHR = 123; // -
    int IUSHR = 124; // -
    int LUSHR = 125; // -
    int IAND = 126; // -
    int LAND = 127; // -
    int IOR = 128; // -
    int LOR = 129; // -
    int IXOR = 130; // -
    int LXOR = 131; // -
    int IINC = 132; // visitIincInsn
    int I2L = 133; // visitInsn
    int I2F = 134; // -
    int I2D = 135; // -
    int L2I = 136; // -
    int L2F = 137; // -
    int L2D = 138; // -
    int F2I = 139; // -
    int F2L = 140; // -
    int F2D = 141; // -
    int D2I = 142; // -
    int D2L = 143; // -
    int D2F = 144; // -
    int I2B = 145; // -
    int I2C = 146; // -
    int I2S = 147; // -
    int LCMP = 148; // -
    int FCMPL = 149; // -
    int FCMPG = 150; // -
    int DCMPL = 151; // -
    int DCMPG = 152; // -
    int IFEQ = 153; // visitJumpInsn
    int IFNE = 154; // -
    int IFLT = 155; // -
    int IFGE = 156; // -
    int IFGT = 157; // -
    int IFLE = 158; // -
    int IF_ICMPEQ = 159; // -
    int IF_ICMPNE = 160; // -
    int IF_ICMPLT = 161; // -
    int IF_ICMPGE = 162; // -
    int IF_ICMPGT = 163; // -
    int IF_ICMPLE = 164; // -
    int IF_ACMPEQ = 165; // -
    int IF_ACMPNE = 166; // -
    int GOTO = 167; // -
    int JSR = 168; // -
    int RET = 169; // visitVarInsn
    int TABLESWITCH = 170; // visiTableSwitchInsn
    int LOOKUPSWITCH = 171; // visitLookupSwitch
    int IRETURN = 172; // visitInsn
    int LRETURN = 173; // -
    int FRETURN = 174; // -
    int DRETURN = 175; // -
    int ARETURN = 176; // -
    int RETURN = 177; // -
    int GETSTATIC = 178; // visitFieldInsn
    int PUTSTATIC = 179; // -
    int GETFIELD = 180; // -
    int PUTFIELD = 181; // -
    int INVOKEVIRTUAL = 182; // visitMethodInsn
    int INVOKESPECIAL = 183; // -
    int INVOKESTATIC = 184; // -
    int INVOKEINTERFACE = 185; // -
    int INVOKEDYNAMIC = 186; // visitInvokeDynamicInsn
    int NEW = 187; // visitTypeInsn
    int NEWARRAY = 188; // visitIntInsn
    int ANEWARRAY = 189; // visitTypeInsn
    int ARRAYLENGTH = 190; // visitInsn
    int ATHROW = 191; // -
    int CHECKCAST = 192; // visitTypeInsn
    int INSTANCEOF = 193; // -
    int MONITORENTER = 194; // visitInsn
    int MONITOREXIT = 195; // -
    int MULTIANEWARRAY = 197; // visitMultiANewArrayInsn
    int IFNULL = 198; // visitJumpInsn
    int IFNONNULL = 199; // -
}
```

### 2.3.opcode_newarray

![[Pasted image 20231121204421.png|1000]]

示例1

```java
public class HelloWorld {
    public void test() {
        byte[] bytes = new byte[10];
    }
}
```

对应test方法ASM编码：

```java
{
	methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "test", "()V", null, null);
	methodVisitor.visitCode();
	methodVisitor.visitIntInsn(BIPUSH, 10);
	methodVisitor.visitIntInsn(NEWARRAY, T_BYTE); // T_BYTE
	methodVisitor.visitVarInsn(ASTORE, 1);
	methodVisitor.visitInsn(RETURN);
	methodVisitor.visitMaxs(1, 2);
	methodVisitor.visitEnd();
}
```

示例2

```java
public class HelloWorld {
    public void test() {
        long[] bytes = new long[10];
    }
}
```

对应test方法ASM编码：

```java
{
	methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "test", "()V", null, null);
	methodVisitor.visitCode();
	methodVisitor.visitIntInsn(BIPUSH, 10);
	methodVisitor.visitIntInsn(NEWARRAY, T_LONG); // T_LONG
	methodVisitor.visitVarInsn(ASTORE, 1);
	methodVisitor.visitInsn(RETURN);
	methodVisitor.visitMaxs(1, 2);
	methodVisitor.visitEnd();
}
```
### 2.4.opcode_invokedynamic

![[Pasted image 20231121204359.png|1000]]

```java
public class HelloWorld {
    public void test() {
        BiFunction<Integer, Integer, Integer> func = Math::max;
    }
}
```

```java
{
	methodVisitor = classWriter.visitMethod(ACC_PUBLIC, "test", "()V", null, null);
	methodVisitor.visitCode();
	methodVisitor.visitInvokeDynamicInsn("apply", "()Ljava/util/function/BiFunction;", 
		new Handle(Opcodes.H_INVOKESTATIC, "java/lang/invoke/LambdaMetafactory", "metafactory", 
			"(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;", false), 
			new Object[]{ Type.getType("(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;"), 
				new Handle(Opcodes.H_INVOKESTATIC, "java/lang/Math", "max", "(II)I", false), 
				Type.getType("(Ljava/lang/Integer;Ljava/lang/Integer;)Ljava/lang/Integer;")});
	methodVisitor.visitVarInsn(ASTORE, 1);
	methodVisitor.visitInsn(RETURN);
	methodVisitor.visitMaxs(1, 2);
	methodVisitor.visitEnd();
}
```

## 3.总结

本文主要对Opcodes接口里定义的字段进行介绍，内容总结如下：

* 第一点，在Opcodes类定义的字段，主要应用于ClassVisitor和MethodVisitor类的visitXxx方法。
* 第二点，记忆方法。由于Opcodes类定义的字段很多，我们可以<font color="#f79646">分成不同的批次和类别来进行理解</font>，慢慢去掌握。

# 10.总结

https://blog.51cto.com/lsieun/2949920
