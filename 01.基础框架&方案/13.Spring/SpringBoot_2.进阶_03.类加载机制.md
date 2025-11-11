# 包结构比对

``` xml
<build>  
    <!-- 默认包名: boot-web-1.0-SNAPSHOT -->  
    <finalName>boot-web</finalName>
</build>
```

```
mvn clean package
```

打包如下：

![[Pasted image 20231101213940.png|200]]

加入插件`spring-boot-maven-plugin`插件：

```xml
<build>
	<!-- 默认包名: boot-web-1.0-SNAPSHOT -->
	<finalName>boot-web</finalName>
	<plugins>
		<plugin>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-maven-plugin</artifactId>
			<version>2.7.14</version>
			<configuration>
				<mainClass>com.learn.boot.web.BootWebApplication</mainClass>
			</configuration>
			<executions>
				<execution>
					<id>repackage</id>
					<goals>
						<goal>repackage</goal>
					</goals>
				</execution>
			</executions>
		</plugin>
	</plugins>
</build>
```

重新打包如下：

![[Pasted image 20231101214027.png|200]]

这里可以看到生成了两个jar相关文件，其中boot-web.jar是spring-boot-maven-plugin插件重新打包后生成的可执行jar，即可以通过java -jar boot-web.jar命令启动。boot-web.jar.original这个则是mvn package打包的原始jar，<font color="#f79646">在spring-boot-maven-plugin插件repackage命令操作时重命名为xxx.original</font>，这个是一个普通的jar，可以被引用在其他服务中。

## 内部结构比对


```
boot-web
├ com
│  └ learn
│      └ boot
│          └ web
│             └ BootWebApplication.class
└ META-INF
    └ maven
        └ com.learn
            └ boot-web
```

需要说明的是，Spring Boot使用了FatJar技术将所有依赖放在一个最终的jar包文件BOOT-INF/lib中，当前项目的Class全部放在BOOT-INF/classes目录中。

```
xxx.jar
├ BOOT-INF
│  ├ classes                        <=== 当前项目的class文件和配置文件
│  │  └ com
│  │      └ learn
│  │          └ boot
│  │              └ web
│  └ lib                            <=== 当前项目所依赖的jar包
├ META-INF
│  └ maven
│      └ com.learn
│          └ boot-web
└ org
    └ springframework
        └ boot
            └ loader
                ├ archive
                ├ data
                ├ jar
                ├ jarmode
                └ util
```

从这个目录结构中，你可以看到Tomcat的启动包（tomcat-embedcore-9.2.62.jar）就在`BOOT-INF\lib`目录下。而FatJar的启动Main函数就是JarLauncher，它负责创建LaunchedURLClassLoader来加载`BOOT-INF\lib`下面的所有jar包。下面是Spring Boot应用的Manifest文件内容。

```
Manifest-Version: 1.0
Spring-Boot-Classpath-Index: BOOT-INF/classpath.idx
Archiver-Version: Plexus Archiver
Built-By: pengbo.wang
Spring-Boot-Layers-Index: BOOT-INF/layers.idx
Start-Class: org.lachesis.springboot.web.BootWebApplication
Spring-Boot-Classes: BOOT-INF/classes/
Spring-Boot-Lib: BOOT-INF/lib/
Spring-Boot-Version: 2.7.7
Created-By: Apache Maven 3.8.8
Build-Jdk: 1.8.0_202
Main-Class: org.springframework.boot.loader.JarLauncher
```

# 资源加载


看网上说资源加载不到，也没复现该问题~

### 使用IDEA调用main方法


```java
public class FooTest {

    public static void main(String[] args) throws IOException {  
        ClassLoader classLoader = FooTest.class.getClassLoader();  
        System.out.println(classLoader);  
        URL resource = classLoader.getResource("json/test.json");  
        System.out.println(resource);  
        System.out.println(ReaderUtil.read(resource.openStream()));  
    }  
}
```

通过IDEA调用FooTest#main方法输出结果：

```
sun.misc.Launcher$AppClassLoader@18b4aac2
file:/D:/IdeaProjects/mine/westboy-hub/spring-boot-labs/spring-boot-loader/target/classes/json/test.json
{"name": "xw"}
```


```java
public class BootLoaderApplication {  
  
    public static void main(String[] args) throws IOException {  
        ClassLoader contextClassLoader = Thread.currentThread().getContextClassLoader();  
        System.out.println(contextClassLoader);
          
        ClassLoader classLoader = BootLoaderApplication.class.getClassLoader();  
        System.out.println(classLoader);  
        
        URL resource = classLoader.getResource("json/test.json");  
        System.out.println(resource);  
        System.out.println(ReaderUtil.read(resource.openStream()));  
  
        ClassPathResource classPathResource = new ClassPathResource("json/test.json");  
        System.out.println(classPathResource);  
        System.out.println(ReaderUtil.read(classPathResource.getInputStream()));  
    }  
}
```

两者

通过IDEA调用BootWebApplication#main方法输出结果：

```
sun.misc.Launcher$AppClassLoader@18b4aac2
sun.misc.Launcher$AppClassLoader@18b4aac2
file:/D:/IdeaProjects/mine/westboy-hub/spring-boot-labs/spring-boot-loader/target/classes/json/test.json
{"name": "xw"}
class path resource [json/test.json]
{"name": "xw"}
```

可以看到通过IDEA启动时，输出结果是一样的。

## 使用spring-boot-maven-plugin打包后执行

项目结构

```sh
spring-boot-loader
└─ src
│	└─ main
│	  ├─ java
│	  │    └─ com
│	  │        └─ lachesis
│	  │            └─ springboot
│	  │                └─ loader
│	  │	                  └─ BootLoaderApplication.java
│     └─ resources
│          └─ json
│              └─ test.json
└─ pom.xml
```

其中pom.xml中的插件配置如下：

```xml
<build>
	<plugins>
		<plugin>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-maven-plugin</artifactId>
			<version>${spring-boot.version}</version>
			<executions>
				<execution>
					<goals>
						<goal>repackage</goal>
					</goals>
				</execution>
			</executions>
		</plugin>
	</plugins>
</build>
```

使用maven打包：

```
mvn clean package
```

使用java命令运行程序：

```sh
cd D:\IdeaProjects\mine\westboy-hub\spring-boot-labs\spring-boot-loader\target
java -jar .\spring-boot-loader-1.0-SNAPSHOT.jar
```

输出结果：

```
org.springframework.boot.loader.LaunchedURLClassLoader@6433a2
org.springframework.boot.loader.LaunchedURLClassLoader@6433a2
jar:file:/D:/IdeaProjects/mine/westboy-hub/spring-boot-labs/spring-boot-loader/target/spring-boot-loader-1.0-SNAPSHOT.jar!/BOOT-INF/classes!/json/test.json
{"name": "xw"}
class path resource [json/test.json]
{"name": "xw"}

```

为了方便我们将上述的输出结果放在一起对比下：

```sh
# 使用IDEA调用main方法输出结果：
sun.misc.Launcher$AppClassLoader@18b4aac2
sun.misc.Launcher$AppClassLoader@18b4aac2
file:/D:/IdeaProjects/mine/westboy-hub/spring-boot-labs/spring-boot-loader/target/classes/json/test.json
{"name": "xw"}
class path resource [json/test.json]
{"name": "xw"}


# 使用spring-boot-maven-plugin打包后执行输出结果：
org.springframework.boot.loader.LaunchedURLClassLoader@6433a2
org.springframework.boot.loader.LaunchedURLClassLoader@6433a2
jar:file:/D:/IdeaProjects/mine/westboy-hub/spring-boot-labs/spring-boot-loader/target/spring-boot-loader-1.0-SNAPSHOT.jar!/BOOT-INF/classes!/json/test.json
{"name": "xw"}
class path resource [json/test.json]
{"name": "xw"}

```


