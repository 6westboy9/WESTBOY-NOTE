
asm-util.jar与asm-commons.jar有什么区别呢？
* 在asm-util.jar里，它提供的是通用性的功能，<font color="#f79646">没有特别明确的应用场景</font>；
* 在asm-commons.jar里，它提供的功能，都是为<font color="#f79646">解决某一种特定场景中出现的问题</font>而提出的解决思路。

>编程的习惯：在编写ASM代码的时候，如果写了一个类，它继承自ClassVisitor，那么就命名成XxxVisitor；如果写了一个类，它继承自MethodVisitor，那么就命名成XxxAdapter。通过类的名字，我就可以区分出哪些类是继承自ClassVisitor，哪些类是继承自MethodVisitor。其实，将MethodVisitor类的子类命名成XxxAdapter就是参考了GeneratorAdapter、AdviceAdapter、AnalyzerAdapter和InstructionAdapter类的名字。但是，CheckClassAdapter类是个例外，它是继承自ClassVisitor类。

# 1.asm-util

在asm-util.jar当中，主要介绍CheckClassAdapter和TraceClassVisitor类。在TraceClassVisitor类当中，会涉及到Printer、ASMifier和Textifier类。

![[Pasted image 20231122133644.png|500]]

* 其中，CheckClassAdapter类，主要负责检查（Check）生成的Class文件内容是否正确。
* 其中，TraceClassVisitor类，主要负责将.class文件的内容打印成文字输出。根据输出的文字信息，可以探索或追踪（Trace）Class文件的内部信息。
    
## 1.1.CheckClassAdapter

检查内容包括两部分：

1. 方法的调用顺序
2. 方法的调用参数

我们可以借助于CheckClassAdapter类来检查生成的字节码内容是否正确，主要有<font color="#f79646">两种使用方式</font>：
* 在生成类或转换类的<font color="#f79646">过程中</font>进行检查
* 在生成类或转换类的<font color="#f79646">结束后</font>进行检查

### 在过程中


### 在结束后


## 1.2.TraceClassVisitor


# 2.asm-commons

在asm-commons.jar当中，包括的类比较多，我们就不一一介绍每个类的作用了。但是，我们可以这些类可以分成两组，一组是ClassVisitor的子类，另一组是MethodVisitor的子类。

* 其中，ClassVisitor的子类有ClassRemapper、StaticInitMerger和SerialVersionUIDAdder类；
* 其中，MethodVisitor的子类有LocalVariablesSorter、GeneratorAdapter、AdviceAdapter、AnalyzerAdapter和InstructionAdapter类。

![[Pasted image 20231122133353.png|500]]
## 2.1.ClassRemapper


## 2.2.StaticInitMerger


## 2.3.SerialVersionUIDAdder


## 2.4.LocalVariablesSorter


## 2.5.GeneratorAdapter


## 2.6.AdviceAdapter


## 2.7.AnalyzerAdapter


## 2.8.InstructionAdapter

