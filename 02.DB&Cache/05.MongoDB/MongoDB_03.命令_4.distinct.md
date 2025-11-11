# 语法

```js
db.collection.distinct(
   field,
   query,
   options
)
```

# 使用

```js
// 1.基本使用
db.employees.distinct("salary")
// 2.带查询条件
db.employees.distinct("salary", { salary: { $gt: 5000 } })

// 3.控制查询结果中的字段
db.employees.distinct("department", {}, { projection: { _id: 0, department: 1 } })
// 4.指定字段排序查询结果
db.employees.distinct("salary", {}, { sort: { salary: 1 } })
```

# 存在问题

## 问题1.不包括不存在情况

>[!important] 注意distinct查询不会包括不存在的情况

<font color="#f79646">样例数据</font>

![[Pasted image 20240919141257.png|600]]

```js
db.nurseKnowledge.distinct("diseaseType", { "type" : { "$in" : ["309"] } })
```

结果

| result |
| :----- |
| 低血钾    |
| 测试乱码   |
| 低体温    |

<font color="#f79646">解决方案</font>

```js
db.nurseKnowledge.aggregate([
    { "$match": { "type": { "$in": ["309"] } } },
    { "$group": { "_id": { "diseaseType": "$diseaseType" } } }
])
```

| \_id                    |
| :---------------------- |
| {"diseaseType": "低体温"}  |
| {"diseaseType": "低血钾"}  |
| {"diseaseType": "测试乱码"} |
| {"diseaseType": null}   |

## 问题2.性能问题

https://blog.csdn.net/Awesome_py/article/details/126784370
