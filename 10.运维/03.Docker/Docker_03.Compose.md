https://juejin.cn/post/7154451839964938254

Docker Compose的yaml文件包含4个一级key：version、services、networks、volumes。

- version：是必须指定的，而且总是位于文件的第一行。它定义了Compose文件格式的版本。注意，<font color="#f79646">并非定义DockerCompose或Docker引擎的版本号</font>。
- services：用于定义不同的应用服务。Docker Compose会将每个服务部署在各自的容器中。
- networks：用于指引Docker创建新的网络。默认情况下，Docker Compose会创建bridge网络。这是一种单主机网络，只能够实现同一主机上容器的连接。当然，也可以使用driver属性来指定不同的网络类型。
- volumes：用于指引Docker来创建新的卷。

```yml
version: '3'
services:
  mysql:
    build:
      context: ./mysql
    environment:
      MYSQL_ROOT_PASSWORD: admin
    restart: always
    container_name: mysql
    volumes:
    - /data/edu-bom/mysql/test:/var/lib/mysql
    image: mysql/mysql:5.7
    ports:
      - 3306:3306
    networks:
      net:
  eureka:
    build:
      context: ./edu-eureka-boot
    restart: always
    ports:
      - 8761:8761
    container_name: edu-eureka-boot
    hostname: edu-eureka-boot
    image: edu/edu-eureka-boot:1.0
    depends_on:
      - mysql
    networks:
      net:
networks:
    net:
volumes:
    vol:
```