
# 三种格式


binlog的三种格式：`statement`、`row`、`mixed`。

* `statement`：基于SQL语句的复制，每一条会修改数据的SQL语句会记录到binlog中。
	* 优点：不需要记录每一条SQL语句与每行的数据变化，这样子binlog的日志也会比较少，减少了磁盘IO，提高性能。
	* 缺点：可能导致<font color="#f79646">主备数据不一致</font>。
* `row`：基于行的复制格式，不记录每一条SQL语句的上下文信息，仅需记录哪条数据被修改了，修改成了什么样子了。
	* 优点：
	* 缺点：<font color="#f79646">占用空间</font>，比如你用一个delete语句删掉10万行数据，用statement的话就是一个SQL语句被记录到binlog中，占用几十个字节的空间。但如果用row格式的binlog，就要把这10万条记录都写到binlog中。这样做，不仅会占用更大的空间，同时写binlog也要耗费IO资源，影响执行速度。
* `mixed`：<font color="#f79646">折中方案</font>，mixed格式的意思是，MySQL自己会判断这条SQL语句是否可能引起主备不一致，如果有可能，就用row格式，否则就用statement格式。

也就是说，mixed格式可以利用statment格式的优点，同时又避免了数据不一致的风险。

因此，如果你的线上MySQL设置的binlog格式是statement的话，那基本上就可以认为这是一个不合理的设置。你至少应该把binlog的格式设置为mixed。

>但是，越来越多的场景要求把MySQL的binlog格式设置为row，这是为什么呢？


本段落推荐资料：[极客时间-MySQL45讲第24讲 - MySQL是怎么保证主备一致的？](https://time.geekbang.org/column/article/76446)



