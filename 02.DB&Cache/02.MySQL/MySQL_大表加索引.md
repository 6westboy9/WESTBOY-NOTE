https://segmentfault.com/a/1190000040570831#item-3-4
## 方案一

>出自《高性能MySQL》一书

```sql
-- tb有接近3千万数据
-- 1.创建一张与原表结构相同的新表
create table tb_new like tb;
-- 2.在新表上创建索引
alter table tb_new add index idx_col_name (col_name);
-- 3.重命名原表为其它表名：tb => tb_tmp
--   新表重命名为原表名： tb_new => tb
--   此时新表承担业务（tb_new）
rename table tb to tb_tmp, tb_new to tb;
-- 4.为原表新增索引
alter table tb_tmp add index idx_col_name (col_name);
-- 5.交换表：
--   新表改回最初的名称：tb => tb_new
--   原表改回最初的名称：tb_tmp => tb
--   原表重新承担业务（tb）
rename table tb to tb_new, tb_tmp => tb;
-- 6.把新表数据导入原表（即把新表承担业务期间产生的数据和到原表中）
insert into tb (col_name1, col_name2) select col_name1, col_name2 from tb_new;
```



## 方案二

