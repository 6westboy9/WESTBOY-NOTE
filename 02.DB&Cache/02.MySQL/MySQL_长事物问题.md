* [MySQL-长事务详解](https://juejin.cn/post/6844903945920315405)

# 长事物实战演练



查询正在运行的事物SQL：

```sql
select t.*,to_seconds(now())-to_seconds(t.trx_started) idle_time from INFORMATION_SCHEMA.INNODB_TRX t;
```

结果：

| **trx\_id**                        | 5833                                                                                                                                                         |
| :--------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **trx\_state**                     | RUNNING                                                                                                                                                      |
| **trx\_started**                   | 2024-10-09 19:57:00                                                                                                                                          |
| **trx\_requested\_lock\_id**       | null                                                                                                                                                         |
| **trx\_wait\_started**             | null                                                                                                                                                         |
| **trx\_weight**                    | 2                                                                                                                                                            |
| **trx\_mysql\_thread\_id**         | 60                                                                                                                                                           |
| **trx\_query**                     | /\* ApplicationName=DataGrip 2024.2.2 \*/ select t.\*,to\_seconds\(now\(\)\)-to\_seconds\(t.trx\_started\) idle\_time from INFORMATION\_SCHEMA.INNODB\_TRX t |
| **trx\_operation\_state**          | null                                                                                                                                                         |
| **trx\_tables\_in\_use**           | 0                                                                                                                                                            |
| **trx\_tables\_locked**            | 1                                                                                                                                                            |
| **trx\_lock\_structs**             | 2                                                                                                                                                            |
| **trx\_lock\_memory\_bytes**       | 1136                                                                                                                                                         |
| **trx\_rows\_locked**              | 1                                                                                                                                                            |
| **trx\_rows\_modified**            | 0                                                                                                                                                            |
| **trx\_concurrency\_tickets**      | 0                                                                                                                                                            |
| **trx\_isolation\_level**          | REPEATABLE READ                                                                                                                                              |
| **trx\_unique\_checks**            | 1                                                                                                                                                            |
| **trx\_foreign\_key\_checks**      | 1                                                                                                                                                            |
| **trx\_last\_foreign\_key\_error** | null                                                                                                                                                         |
| **trx\_adaptive\_hash\_latched**   | 0                                                                                                                                                            |
| **trx\_adaptive\_hash\_timeout**   | 0                                                                                                                                                            |
| **trx\_is\_read\_only**            | 0                                                                                                                                                            |
| **trx\_autocommit\_non\_locking**  | 0                                                                                                                                                            |
| **trx\_schedule\_weight**          | null                                                                                                                                                         |
| **idle\_time**                     | 310                                                                                                                                                          |

