# 查看连接

查看MySQL服务端最大连接数：

```SQL
-- 查看最大连接数
show variables like '%max_connections%';
-- 查看实际最大连接数
show global status like 'Max_used_connections';
```

>默认MySQL的最大连接是100，一般是远远不够的~
>实际连接数是最大连接数的85%较为合适，所以最大连接数我们可以根据实际连接数去设置，如果你想设置最大连接数超过1024，还需要修改文件描述符的上限~

查看当前MySQL服务连接数：

```SQL
-- 如果是root帐号，你能看到所有用户的当前连接。如果是其它普通帐号，只能看到自己占用的连接。
-- show processlist; 只列出前100条
show processlist;
-- 如果想全列出请使用
show full processlist;
```

# 修改连接


## 方式一

修改连接数：

```SQL
-- 最大可以达到16384
set global max_connections=1000;
```

就是设置的最大连接数只在MySQL当前服务进程有效，一旦MySQL重启，又会恢复到初始状态。因为MySQL启动后的初始化工作是从其配置文件中读取数据的，而这种方式没有对其配置文件做更改。


## 方式二（修改配置文件）

这种方式说来很简单，只要修改MySQL配置文件my.ini或my.cnf的参数max_connections，将其改为max_connections=1000，然后重启MySQL即可。


# 参考资料

* [MySQL的最大连接数](https://www.jianshu.com/p/b51c4d5bdfc4)



