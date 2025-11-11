# 线程基础
## 1.线程状态（线程生命周期）

Java中线程状态总共6种，在给定某一时刻，线程只能处于其中一个状态。--- 源码参见：`Thread$State`类

![[Pasted image 20250205174548.png|800]]

>[!danger] 要注意的一点是，Java线程将操作系统中的<font color="#ff0000">就绪</font>和<font color="#ff0000">运行</font>两种状态笼统地称作<font color="#ff0000">运行中</font>！

![[Pasted image 20250205174529.png|1000]]

> 我们可以在网上通常见到会将WAITING、TIME_WAITING和BLOCKED统称为阻塞状态！
> 关于LockSupport及Unsafe类详细介绍参见：[并发工具类-LockSupport](https://www.yuque.com/westboy/xk1bf0/bvwbco)

+ <font style="color:#E8323C;">NEW</font>（初始状态）：使用new关键字创建了一个线程后，该线程处于NEW状态，此时仅由JVM为其分配内存，并初始化其成员变量的值。
+ <font style="color:#E8323C;">BLOCKED</font>（阻塞状态）：阻塞状态是线程阻塞进入synchronized关键字修饰的方法或代码块（获取锁的时候）时的状态，但是<u>阻塞在java.concurrent包中的Lock接口的线程状态却是等待状态</u>，因为java.concurrent包中的Lock接口对于阻塞的实现均使用了LockSupport类中的相关方法。（<u>阻塞状态是synchronized关键字场景才会遇到的</u>）
+ BLOCKED和WAITING有什么区别？
    - 虽然`BLOCKED`和`WAITING`都有等待的含义，但二者有着本质的区别，首先它们状态形成的调用方法不同，其次`BLOCKED`可以理解为当前线程还处于活跃状态，<font style="color:#E8323C;">只是在阻塞等待其他线程使用完某个锁资源</font>；
    - 而`WAITING`则是因为自身调用了`Object.wait()`/`Thread.join()`/`LockSupport.park()` 而进入等待状态，<font style="color:#E8323C;">只能等待其他线程执行某个特定的动作才能被继续唤醒</font>，比如当线程因为调用了`Object.wait()`而进入`WAITING`状态之后，则需要等待另一个线程执行`Object.notify()`或`Object.notifyAll()`才能被唤醒。--- 出自拉钩教育《Java源码剖析》
    - 疑问：那`Thread.join()`又是在等待其他线程的什么动作呢？--- <font style="color:#E8323C;">在等待其他线程执行完成！见其他知识点-</font>[Thread#join方法](#J1UCC)

---

+ Thread#start和Thread#run方法区别
    - start方法来启动线程，真正实现了多线程运行。这时无需等待run方法体代码执行完毕，可以直接继续执行下面的代码。
    - 通过调用start方法来启动一个线程，这时此线程是处于<font style="color:#E8323C;">就绪状态</font>，并没有运行。
    - run称为线程体，它包含了要执行的这个线程的内容，线程就进入了运行中状态，开始运行run方法中代码。
+ Thread#start和Runnable#run方法区别
    - 从源码角度看，start属于Thread的方法，并使用synchronized来保证线程安全。run为Runnable的抽象方法，一般都是需要重写该方法。
    - 从执行效果看，start可以开启多线程，将线程从NEW状态转换成RUNNABLE状态，而run方法只是一个普通的方法。

## 2.线程调度算法

+ <font style="color:#E8323C;">抢占式调度</font>指的是每条线程执行的时间、线程的切换都由系统控制，系统控制指的是在系统某种运行机制下，可能每条线程都分同样的执行时间片，也可能是某些线程执行的时间片较长，甚至某些线程得不到执行的时间片。在这种机制下，一个线程的堵塞不会导致整个进程堵塞。
+ <font style="color:#E8323C;">协同式调度</font>指某一线程执行完后主动通知系统切换到另一线程上执行，这种模式就像接力赛一样，一个人跑完自己的路程就把接力棒交接给下一个人，下个人继续往下跑。线程的执行时间由线程本身控制，线程切换可以预知，不存在多线程同步问题，但它有一个致命弱点：如果一个线程编写有问题，运行到一半就一直堵塞，那么可能导致整个系统崩溃。

![[Pasted image 20250205174720.png|600]]

>[!danger] <font style="color:#E8323C;">Java使用的线程调使用抢占式调度</font>，Java中线程会按优先级分配CPU时间片运行，且优先级越高越优先执行，但优先级高并不代表能独自占用执行时间片，可能是优先级高得到越多的执行时间片，反之，优先级低的分到的执行时间少但不会分配不到执行时间。
## 3.进程调度算法

TODO

## 4.线程与进程区别

TODO

## 5.守护线程

```java
public class DaemonThread implements Runnable {

    @Override
    public void run() {
        try {
            TimeUnit.SECONDS.sleep(5);
            System.out.println("thread run...");
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        } finally {
            System.out.println("thread run finally");
        }
    }

    public static void main(String[] args) {
        DaemonThread myThread = new DaemonThread();
        Thread thread = new Thread(myThread);
        // 默认等待线程执行完任务才退出
        // 设置为true时，不会等执行完任务直接退出（因为Java虚拟机中已经没有非Daemon线程了，虚拟机需要退出）
        thread.setDaemon(true);
        thread.start();
    }
}
```

注意事项：

+ 守护线程需要在启动线程之前设置，不能在启动线程之后设置。
+ <font style="color:#E8323C;">在守护线程中产生的新的线程也是守护线程</font>。
+ <font style="color:#E8323C;">当JVM中所有的线程都是守护线程的时候，JVM就可以退出了。反之，如果还有一个或以上的非守护线程则JVM不会退出</font>。
    - 垃圾回收线程就是经典的守护线程，当我们的程序中不再有任何的线程时，程序就不会再产生垃圾，垃圾回收器就无事可做，所以当垃圾回收线程是JVM上仅剩的线程时，垃圾回收线程会自动离开。
+ 在JVM退出时，守护线程中的finally块并不一定会执行，所以<font style="color:#E8323C;">在构建守护线程的时候，不能依靠finally块中的内容来确保关闭或清理资源的逻辑</font>。

# 创建线程的方式

## 1.继承Thread类

```java
public class ThreadCreationOne extends Thread {

    @Override
    public void run() {
        System.out.println("thread run...");
    }

    public static void main(String[] args) {
        ThreadCreationOne thread = new ThreadCreationOne();
        thread.start();
    }
}
```

## 2.实现Runnable接口

```java
public class ThreadCreationTwo implements Runnable {

    @Override
    public void run() {
        System.out.println("thread run...");
    }

    public static void main(String[] args) {
        ThreadCreationTwo myThread = new ThreadCreationTwo();
        Thread thread = new Thread(myThread);
        thread.start();
    }
}
```

>**方式一与方式二比较**

继承Thread类与实现Runnable接口方式，在实现Runnable接口中，都会将Runnable接口实现类当做参数设置到Thread类的构造方法中去，赋值给Thread类的target属性，该属性类型为Runnable，最终这两种方式都会去调用Thread类的start方法，而start方法是一个native方法，最终会调用Thread类的run方法（源码见下）。

```java
public void run() {
    if (target != null) {
        target.run();
    }
}
```

+ 对于方式一，会直接执行重写的run方法。
+ 对于方式二，由于在创建Thread时，设置了target，因此会直接执行target的run方法。
+ 本质上，这两种方式都是通过创建一个Thread类对象实现。

## 3.实现Callable接口并结合Future实现

```java
public class ThreadCreationThree {

    public static void main(String[] args) {
        FutureTask<Integer> futureTask = new FutureTask<>(new Task());
        new Thread(futureTask).start();
        try {
            Integer result = futureTask.get();
            System.out.println(result);
        } catch (InterruptedException | ExecutionException e) {
            throw new RuntimeException(e);
        }
    }

    static class Task implements Callable<Integer> {
        @Override
        public Integer call() throws Exception {
            return new Random().nextInt(100);
        }
    }
}
```

+ 首先定义一个Callable接口的实现类，并实现call方法，且call方法是有返回值的。
+ 然后通过FutureTask的构造方法，包装该实现类。
+ 再把FutureTask作为Thread类的target参数，创建Thread对象，调用start方法启动线程。
+ 最后通过FutureTask的get方法获取线程的执行结果。

**<font style="color:#E8323C;">工作原理</font>**



TODO



## 4.线程池创建线程

+ 方式一
    - 首先，定义个Runnable接口实现类，重写run方法。
    - 然后，创建一个线程池ExecutorService对象。
    - 通过线程池ExecutorService对象的execute方法传入Runnable接口实现类对象。
+ 方式二
    - 首先，定义一个Callable接口实现类，重写call方法。
    - 然后，创建一个线程池ExecutorService对象。
    -  通过线程池ExecutorService对象的submit方法传入Callable接口实现类对象。

> 这里要注意的一点是，ExecutorService对于Callable接口实现类对象的处理方法是submit，而不是execute，关于submit和execute方法的区别见。

```java
public class ThreadCreationFour {

    public static void main(String[] args) {
        ExecutorService executorService = Executors.newFixedThreadPool(3);
        for (int i = 0; i < 10; i++) {
            executorService.execute(new Task());
        }
        executorService.shutdown();
    }

    static class Task implements Runnable {
        @Override
        public void run() {
            try {
                TimeUnit.SECONDS.sleep(1);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
            System.out.println(Thread.currentThread().getName() + " thread run...");
        }
    }
}
```

在线程池中，我们其实是把创建和管理线程的任务都交给了线程池。而创建线程是通过线程工厂类Executors$DefaultThreadFactory来创建的（也可以自定义工厂类）。我们看下这个工厂类的具体实现。

![[Pasted image 20250205174929.png|800]]

> [!danger] 因此，综上所述。在回答这个问题的时候，我们可以说本质上创建线程就只有一种方式，就是构造一个`Thread`类。

## 5.总结

虽然归根结底只有一个种方式 --- 构造一个`Thread`类，但是要回答问题的话，不推荐！

<font style="color:#F5222D;">个人认为，如果你要说有1种、2种、3种、4种其实也是可以的。重要的是，你要能说出你的依据，讲出它们各自的不同点和共同点。</font>

就好比创建`ArrayList`对象一样，我们一般有以下几种方式：

1. 通过构造方法，`List list = new ArrayList();`
2. 通过`Arrays.asList("a", "b");`
3. 通过`Java8`提供的`Stream API`，如`List list = Stream.of("a", "b").collect(Collectors.toList());`
4. 通过`guava`第三方包，`List list3 = Lists.newArrayList("a", "b");`

等等，现在，我告诉你创建`ArrayList`就只有一种方式，即构造一个`ArrayList`类，有点不太合适。

## 6.扩展

问：一个类实现了`Runnable`接口就会执行`Thread`默认的`run`方法（因为单`Runnble`接口实现类的对象是不能开启线程运行的，只有构建一个`Thread`对象并调用`start`方法才会启动一个线程），然后判断`target`不为空，最后执行在`Runnable`接口中实现的`run`方法。而继承`Thread`类，就会执行重写后的`run`方法。那么，现在我既继承`Thread`类，又实现`Runnable`接口，如下程序，应该输出什么结果呢？

示例

```java
public class TestThread {
    public static void main(String[] args) {
        Thread thread = new Thread(new Runnable() {
            // 实现Runnable接口的run方法
            @Override
            public void run() {
                System.out.println("runnable");
            }
        }) {
            // 继承自Thread类的run方法
            @Override
            public void run() {
                System.out.println("Thread run");
            }
        };
        thread.start();
    }
}
```

> 接口与类的某个方法同名，但是又不同功能的写法（第一次见）参见：[不同功能的接口与类的同名方法](https://www.yuque.com/westboy/xk1bf0/cumq0t)

![[Pasted image 20250205175103.png|600]]

<font style="color:rgb(33, 37, 41);">子类重写了父类的方法就会优先执行子类重写的方法！</font>

那如何做到既执行了`Thread#run`方法也执行了`Runnble#run`方法呢？

```java
public class TestThread {
    public static void main(String[] args) {
        Thread thread = new Thread(new Runnable() {
            // 实现Runnable接口的run方法
            @Override
            public void run() {
                System.out.println("runnable");
            }
        }) {
            // 继承自Thread类的run方法
            @Override
            public void run() {
                System.out.println("Thread run");
                super.run(); // 只需要再此调用父类的run方法即可
            }
        };
        thread.start();
    }
}
```

惊不惊喜，没想到与并发本身没多大关系吧，而是继承的问题！

# 终止线程的方式


## 1.正常运行结束

程序运行结束，线程自动结束。

## 2.使用退出标志位（不推荐）

为什么不推荐使用呢？让我们看一个示例就会明白。

生产者

```java
class Producer implements Runnable {
    public volatile boolean canceled = false; // 使用volatile变量
    BlockingQueue<Integer> storage;

    public Producer(BlockingQueue<Integer> storage) {this.storage = storage;}

    @Override
    public void run() {
        int num = 0;
        try {
            while (num <= 100000 && !canceled) {
                if (num % 50 == 0) {
                    storage.put(num);
                    System.out.println(Thread.currentThread().getName() 
                                       + ": " + num + "是50的倍数,被放到仓库中了");
                }
                num++;
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            System.out.println("生产者结束运行"); // 如果线程被中断将打印此日志
        }
    }
}
```

测试方法

```java
public static void main(String[] args) throws InterruptedException {
    ArrayBlockingQueue<Integer> storage = new ArrayBlockingQueue<>(8);
    
    Producer producer = new Producer(storage);
    Thread producerThread = new Thread(producer);
    producerThread.setName("生产者");
    producerThread.start();
    
    Thread.sleep(500);

    // main线程在消费（充当消费者）
    while (Math.random() < 0.97) {
        System.out.println(storage.take() + "被消费了");
        Thread.sleep(100);
    }

    System.out.println("消费者不需要更多数据了");
    // 一旦消费不需要更多数据了，我们应该让生产者也停下来，但是实际情况却停不下来
    producer.canceled = true;
    System.out.println(producer.canceled);
}
```

运行发现线程迟迟不能结束

![](https://cdn.nlark.com/yuque/0/2022/png/301383/1663469038912-a0d99b5e-2be4-49e2-80f2-718be06ae201.png)

通过`arthas`的`thread`命令发现生产者线程并没有结束运行，而是一直处于`WAITTING`状态。

![](https://cdn.nlark.com/yuque/0/2022/png/301383/1663469251381-44203f8f-0288-4005-8018-a65a051e2a5c.png)

原因分析：当消费者不再需要数据，就会将`canceled`的标记位设置为`true`，理论上此时生产者会跳出`while`循环，并打印输出“生产者运行结束”。然而结果却不是我们想象的那样，尽管已经把`canceled`设置成`true`，但生产者仍然没有停止，这是因为在这种情况下，生产者在执行`storage.put(num)`时发生阻塞（队列已满，阻塞等待消费，但是消费者已经不再消费了，所以就会一直阻塞等待状态中），在它被叫醒之前是没有办法进入下一次循环判断`canceled`的值的，所以在这种情况下用`volatile`是没有办法让生产者停下来的。--- <font style="color:#F5222D;">重要原因（标志位不能唤醒阻塞等待中的线程）</font>

<font style="color:#2F54EB;">使用线程中断的方式改进</font>

生产者改进

```java
class Producer implements Runnable {
    public volatile boolean canceled = false; // 使用volatile变量
    BlockingQueue<Integer> storage;

    public Producer(BlockingQueue<Integer> storage) {this.storage = storage;}

    @Override
    public void run() {
        int num = 0;
        try {
            while (num <= 100000 && !canceled 
                   && !Thread.currentThread().isInterrupted()) {
                if (num % 50 == 0) {
                    storage.put(num);
                    System.out.println(Thread.currentThread().getName() 
                                       + ": " + num + "是50的倍数,被放到仓库中了");
                }
                num++;
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            System.out.println("生产者结束运行"); // 如果线程被中断将打印此日志
        }
    }
}
```

测试方法改进

```java
public static void main(String[] args) throws InterruptedException {
    ArrayBlockingQueue<Integer> storage = new ArrayBlockingQueue<>(8);
    
    Producer producer = new Producer(storage);
    Thread producerThread = new Thread(producer);
    producerThread.setName("生产者");
    producerThread.start();
    
    Thread.sleep(500);

    // main线程在消费（充当消费者）
    while (Math.random() < 0.97) {
        System.out.println(storage.take() + "被消费了");
        Thread.sleep(100);
    }

    System.out.println("消费者不需要更多数据了");
    // 一旦消费不需要更多数据了，我们应该让生产者也停下来，但是实际情况却停不下来
    producer.canceled = true;
    System.out.println(producer.canceled);
    producerThread.interrupt();
}
```

## 3.线程中断（推荐）

对于`Java`而言，最正确的停止线程的方式是使用`interrupt`。但`<font style="color:#E8323C;">interrupt</font>`<font style="color:#E8323C;">仅仅起到通知被停止线程的作用</font>。而对于被停止的线程而言，它拥有完全的自主权，它既可以选择立即停止，也可以选择一段时间后停止，也可以选择压根不停止。<font style="color:#E8323C;">那么为什么</font>`<font style="color:#E8323C;">Java</font>`<font style="color:#E8323C;">不提供强制停止线程的能力呢？</font>

事实上，`Java`希望程序间能够相互通知、相互协作地管理线程，因为如果不了解对方正在做的工作，贸然强制停止线程就可能会造成一些安全的问题，为了避免造成问题就需要给对方一定的时间来整理收尾工作。比如：线程正在写入一个文件，这时收到终止信号，它就需要根据自身业务判断，是选择立即停止，还是将整个文件写入成功后停止，而如果选择立即停止就可能造成数据不完整，不管是中断命令发起者，还是接收者都不希望数据出现问题。

_**<font style="color:#2F4BDA;">中断相关方法</font>**_

```java
// 线程中断方法，中断目标线程，给目标线程发一个中断信号，线程被标记为中断状态
public void interrupt() 

// 静态方法，判断的是调用线程当前线程的中断状态，测试当前线程是否已被中断，通过此方法可以清除线程的中断状态
// 当第一次调用时，返回当前线程状态，并同时将该线程的中断标志位复位为false（默认为false）
    
// 换句话说，如果连续两次调用此方法，则第二次调用将返回false
// 除非当前线程在第一次调用清除其中断状态之后且在第二次调用检查其状态之前再次中断
// 如果当前线程已被中断，则为true；否则为false
public static boolean interrupted() {
    return currentThread().isInterrupted(true);
}

// 与interrupted不同，使用该方法判断中断状态时，线程的中断状态不受该方法的影响
public boolean isInterrupted() {
    return isInterrupted(false);
}

// 测试某些线程是否已被中断。根据传递的ClearInterrupted的值重置或不重置中断状态
private native boolean isInterrupted(boolean ClearInterrupted);
```

_**<font style="color:#2F54EB;">使用方式</font>**_

```java
while (!Thread.currentThread().isInterrupted() && more work to do) {
    do more work
}
```

_**<font style="color:#2F54EB;">正常运行被中断</font>**_

```java
public class ThreadInterruptDemo02 {

    static class StopThread implements Runnable {
        @Override
        public void run() {
            int count = 0;
            while (!Thread.currentThread().isInterrupted() && count < 1000) {
                System.out.println("count = " + count++);
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(new StopThread());
        thread.start();
        Thread.sleep(5); // 5ms
        thread.interrupt();
    }
}
```

运行结果：

```plain
count = 0
count = 1
count = 2
...    
count = 154
count = 155
count = 156
```

_**<font style="color:#2F54EB;">处于休眠状态线程被中断</font>**_

```java
public class ThreadInterruptDemo03 {

    static class StopThread implements Runnable {
        @Override
        public void run() {
            int count = 0;
            while (!Thread.currentThread().isInterrupted() && count < 1000) {
                System.out.println("count = " + count++);
                try {
                    TimeUnit.SECONDS.sleep(5);
                } catch (InterruptedException e) {
                    throw new RuntimeException(e); // 抛出异常并将中断标记设置成false
                }
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(new StopThread());
        thread.start();
        Thread.sleep(5); // 5ms
        thread.interrupt();
    }
}
```

![](https://cdn.nlark.com/yuque/0/2022/png/301383/1663466617715-b6c52bcd-2c95-4e18-97e3-5da78cb22d47.png)

如果`sleep`、`wait`等可以让线程进入阻塞的方法使线程休眠了，而处于休眠中的线程被中断，那么线程是可以感受到中断信号的，并且会抛出一个`InterruptedException`异常，同时清除中断信号，将中断标记位设置成 `false`。

_**<font style="color:#2F54EB;">最佳的两种处理方式</font>**_

方式一：抛异常（如上）

```java
try {
    TimeUnit.SECONDS.sleep(5);
} catch (InterruptedException e) {
    throw new RuntimeException(e);
}
```

方式二：再次中断

```java
try {
    TimeUnit.SECONDS.sleep(5);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    // 打印异常日志
}
```

## 4.stop方法终止线程（线程不安全）

程序中可以直接使用`thread.stop()`来强行终止线程，但是stop方法是很危险的，就象突然关闭计算机电源，而不是按正常程序关机一样，可能会产生不可预料的结果，不安全主要是：调用`thread.stop()`之后，创建子线程的线程就会抛出`ThreadDeatherror`的错误，并且会释放子线程所持有的所有锁。一般任何进行加锁的代码块，都是为了保护数据的一致性，如果在调用`thread.stop()`后导致了该线程所持有的所有锁的突然释放（不可控制），那么被保护数据就有可能呈现不一致性，其他线程在使用这些被破坏的数据时，有可能导致一些很奇怪的应用程序错误。因此，并不推荐使用stop方法来终止线程。

# 线程间通信
## 1.Object#wait/notify

等待/通知的相关方法是任意Java对象具备的，因为这些方法被定义在所有对象的超类java.lang.Object上。

![[Pasted image 20250205175221.png|800]]

![[Pasted image 20250205175232.png|600]]

示例

```java
public class ThreadWaitNotifyMain {

    private static final Object LOCK = new Object();
    private static boolean flag = true;

    public static void main(String[] args) {
        Thread waitThread = new Thread(new Wait(), "WaitThread");
        waitThread.start();
        sleepMs(1000);
        Thread notifyThread = new Thread(new Notify(), "NotifyThread");
        notifyThread.start();
    }

    static class Wait implements Runnable {
        @Override
        public void run() {
            synchronized (LOCK) {
                while (flag) {
                    try {
                        System.out.println(getCurThreadName() + " flag is true. wait@ " + getCurTime()); // ①
                        LOCK.wait();
                    } catch (InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                }
                System.out.println(getCurThreadName() + " flag is false. running@ " + getCurTime()); // ④
            }
        }
    }

    static class Notify implements Runnable {
        @Override
        public void run() {
            synchronized (LOCK) {
                System.out.println(getCurThreadName() + " hold lock. notify@ " + getCurTime()); // ②
                LOCK.notifyAll();
                flag = false;
                sleepMs(5000);
            }

            synchronized (LOCK) {
                System.out.println(getCurThreadName() + " hold lock again. sleep@ " + getCurTime()); // ③
                sleepMs(5000);
            }
        }
    }

    // 在此省略了一些getCurThreadName()、getCurTime()、sleepMs(5000)方法，见名知意~
}
```

运行结果只会出现以下两种

```plain
WaitThread flag is true. wait@ 23:57:28
NotifyThread hold lock. notify@ 23:57:29
NotifyThread hold lock again. sleep@ 23:57:34
WaitThread flag is false. running@ 23:57:39
```

分析（点击放大看）

![[Pasted image 20250205175328.png|1100]]

```plain
WaitThread flag is true. wait@ 23:57:28
NotifyThread hold lock. notify@ 23:57:29
WaitThread flag is false. running@ 23:57:35
NotifyThread hold lock again. sleep@ 23:57:40
```

分析（点击放大看）

![[Pasted image 20250205175339.png|1100]]

> 上述两个图中虚线前面部分因为`WaitThread`先`start`并`sleep`了`1s`后才调用的`NotifyThread`的`start`方法，保证了`WaitThread`先执行`NotifyThread`后执行！
> 结果不同主要是在虚线后部分线程调度问题导致！

总结

+ 使用wait/notify/notifyAll时，必须先调用对象加锁。
+ 调用wait方法后，线程状态由RUNNING变为WAITING，并将当前线程放置到<font style="color:#F5222D;">对象的等待队列（注意是对象的等待队列），会释放锁</font>。
+ notify/notifyAll方法调用后，等待线程依旧不会从wait返回，需要等调用notify/notifyAll方法的线程释放锁之后，等待线程才有机会从wait返回。--- ❓有点不是很理解，等待线程不是在等待队列么？这里说从wait返回是什么意思呢？
+ notify是将等待队列中的一个等待线程从等待队列中移到同步队列中，而notifyAll是将所有线程全部移至同步队列，被移动的线程状态<font style="color:#F5222D;">由WAITTING变为BLOCKED</font>。--- <font style="color:#F5222D;">重要</font>
+ 从wait方法返回的前提是获取得了调用对象的锁。

**注意事项**

+ 为什么wait方法必须在synchronized保护的同步代码中使用？
+ 为什么wait/notify/notifyAll被定义在Object类中，而sleep定义在Thread类中？
+ wait/notify和sleep方法的异同？

接下来挨个看上面三个问题。

第一个问题：为什么wait方法必须在synchronized保护的同步代码中使用？

wait方法源码注释：

![[Pasted image 20250205175449.png|700]]

左侧内容大概意思：

锁对象记作：O

当前线程记作：T

线程T调用对象O的wait方法会使当前线程T处于等待状态，直到另外一个线程调用对象O的notify/notifyAll方法，或者等到超时。

当前线程T必须拥有对象O的monitor。

此方法使当前线程T将自己置于对象O的等待集中，然后放弃对对象O的所有同步声明。线程T因为线程调度目的处于休眠状态，直到发生以下四种情况之一：

+ 其他一些线程调用对象O的notify方法，恰好线程T被随意地选择为要被唤醒的线程。
+ 其他一些线程调用对象O的notifyAll方法。
+ 其他一些线程中断线程T。
+ 等待超时。

然后将线程T从对象O的等待集中移除，并重新启用线程调度。然后与其他线程竞争对象O的monitor，一旦线程T获取到了monitor，就会恢复到线程T调用等待方法时的状态。

线程也可以在没有被通知、中断或超时的情况下被唤醒，即所谓的<font style="color:#F5222D;">虚假唤醒</font>。虽然在实践中很少发生，所以<font style="color:#E8323C;background-color:#FADB14;">一般编码时都会加以循环条件判断防止虚假唤醒</font>，如果条件不满足则继续等待。

在使用wait方法时，必须把wait方法写在synchronized保护的while代码块中，并始终判断执行条件是否满足，如果满足就往下继续执行，如果不满足就执行wait方法，而在执行wait方法之前，必须先持有对象的monitor锁，也就是通常所说的synchronized锁。那么设计成这样有什么好处呢？



假设不使用synchronized关键字时的一个生产者-消费者模型示例。

![|575](https://cdn.nlark.com/yuque/0/2022/png/301383/1663299739401-39fa8720-76ca-4e0f-9eb5-fc5b14eabfb7.png)

![|625](https://cdn.nlark.com/yuque/0/2022/png/301383/1663341564033-dd505ff6-bc4b-4fdc-886f-26dfe9fdce46.png)



_<font style="color:#08979C;background-color:#D3F5F0;">第二个问题：为什么wait/notify/notifyAll被定义在Object类中，而sleep定义在Thread类中？</font>_

<font style="color:#2F54EB;"></font>

+ 因为Java中每个对象都有一把称之为monitor监视器的锁，由于每个对象都可以上锁，这就要求在对象头中有一个用来保存锁信息的位置。这个<font style="color:#F5222D;">锁是对象级别的，而非线程级别的</font>，wait/notify/notifyAll也都是锁级别的操作，它们的锁属于对象，所以把它们定义在Object类中是最合适，因为Object类是所有对象的父类。
+ 因为如果把wait/notify/notifyAll方法定义在Thread类中，会带来很大的<font style="color:#F5222D;">局限性</font>，比如一个线程可能持有多把锁，以便实现相互配合的复杂逻辑，假设此时wait方法定义在Thread类中，如何实现让一个线程持有多把锁呢？又如何明确线程等待的是哪把锁呢？<font style="color:#F5222D;">既然我们是让当前线程去等待某个对象的锁，自然应该通过操作对象来实现，而不是操作线程</font>。



_<font style="color:#08979C;background-color:#D3F5F0;">第三个问题：wait/notify和sleep方法的异同？</font>_



+ 相同点
    - 它们都可以让线程阻塞。
    - 它们都可以响应interrupt中断：在等待的过程中如果收到中断信号，都可以进行响应，并抛出InterruptedException异常。
+ 不同点
    - wait/notify是Object类的方法，而sleep是Thread类的方法。
    - wait方法必须在synchronized保护的代码中使用，而sleep方法并没有这个要求。
    - 在同步代码中执行sleep方法时，并不会释放monitor锁，但执行wait方法时会主动释放monitor锁。
    - sleep方法中会要求必须定义一个时间，时间到期后会主动恢复，而对于没有参数的wait方法而言，意味着永久等待，直到被中断或被唤醒才能恢复，它并不会主动恢复。

## 2.Condtion#await/signal

TODO

## 3.Thread#join

如果一个线程A执行了thread.join()语句，其含义是：当前线程A等待thread线程执行完成之后才从thread.join()返回。

示例

```java
public class ThreadJoinDemo {
    public static void main(String[] args) throws InterruptedException {
        Thread t = new Thread(() -> {
            CommonUtil.printWithMs("执行开始");
            CommonUtil.sleepMs(3000);
            CommonUtil.printWithMs("执行完成");
        });
        t.start();
        t.join();
    }
}
// [2022-10-19 11:07:29.742][Thread-0] 执行开始
// [2022-10-19 11:07:32.781][Thread-0] 执行完成
```

在Thread类中有三个关于join的重载方法源码如下：

```java
public final void join() throws InterruptedException {
    join(0);
}

// 最核心方法
public final synchronized void join(long millis) throws InterruptedException {
    long base = System.currentTimeMillis();
    long now = 0;

    if (millis < 0) {
        throw new IllegalArgumentException("timeout value is negative");
    }

    if (millis == 0) {
        // isAlive是Thread类的native方法 --- 作用就是判断当前线程是否还活着
        while (isAlive()) {
            // wait是Object类的native方法
            wait(0);
        }
    } else {
        while (isAlive()) {
            long delay = millis - now;
            if (delay <= 0) {
                break;
            }
            wait(delay);
            now = System.currentTimeMillis() - base;
        }
    }
}

public final synchronized void join(long millis, int nanos) throws InterruptedException {
    if (millis < 0) {
        throw new IllegalArgumentException("timeout value is negative");
    }

    if (nanos < 0 || nanos > 999999) {
        throw new IllegalArgumentException(
            "nanosecond timeout value out of range");
    }

    if (nanos >= 500000 || (nanos != 0 && millis == 0)) {
        millis++;
    }

    join(millis);
}

```

那上面的示例结合源码如何理解呢？(注意点：join是Thread类的方法，isAlive是Thread类的native方法，wait是Object方法，这几点将有助于理解join方法逻辑)

+ 主线程执行`t.join()`时，join方法是一个synchronized方法，需要加锁，那锁对象是谁呢？顾名思义是t，<font style="color:#E8323C;">即该线程对象t是被当做锁对象</font>。
+ 主线程尝试加锁成功了，调用`isAlive()`方法，判断是线程t是否存活，显然是存活的。然后调用锁对象t的wait方法，此时主线程移至锁对象t的等待队列里去（主线程的状态从RUNNABLE变更为WAITTING状态）
+ 等待t线程执行完任务后，主线程会被唤醒，且需要再次获取到锁，主线程继续执行`t.join()`后的逻辑。--- <font style="color:#F5222D;">重要</font>

# 线程安全
## 1.活跃性问题

**死锁**

死锁是指两个线程之间相互等待对方资源，但同时又互不相让。

**活锁**

活锁与死锁非常相似，也是程序一直等不到结果，但对比于死锁，活锁是活的，什么意思呢？因为正在运行的线程并没有阻塞，它<font style="color:#E8323C;">始终在运行中，却一直得不到结果</font>。

举一个例子，假设有一个消息队列，队列里放着各种各样需要被处理的消息，而某个消息由于自身被写错了导致不能被正确处理，执行时会报错，可是队列的重试机制会重新把它放在队列头进行优先重试处理，但这个消息本身无论被执行多少次，都无法被正确处理，每次报错后又会被放到队列头进行重试，周而复始，最终导致线程一直处于忙碌状态，但程序始终得不到结果，便发生了活锁问题。

**饥饿**

饥饿是指线程需要某些资源时始终得不到，尤其是`CPU`资源，就会导致线程一直不能运行而产生的问题。

## 2.线程安全的实现方法

+ 互斥同步：`synchronized`和`ReentrantLock`
+ 非阻塞同步：`CAS`+`AtomicXXX`（其底层实现为`CAS`+`volatile`）
+ 无同步方案：栈封闭（即局部变量），本地存储`ThreadLocal`

# 面试问题

## 1.Thread.sleep与Object.wait的区别

参见线程间通信-`[Object#wait/notify](#L0PqS)`部分内容的重要事项的第三个问题！

## 2.实现生产者与消费者模型实现方式

+ 使用`Object#wait/notify`实现
+ 使用`LockSupport#park/unpark`实现
+ 使用`Condition#await/signal`实现
+ 使用`BlockingQueue`实现







