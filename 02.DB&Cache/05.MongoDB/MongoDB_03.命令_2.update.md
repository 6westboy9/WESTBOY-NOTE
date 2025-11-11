
>需求：往文档对象数组属性中添加对象

```js
use coms
db.sysConfigFile.update({ 'key': 'orderExecutionConfig' }, { "$pull": { 'children': { 'key': 'enableSkinTestMedicinePrepare' } } })
db.sysConfigFile.update({ 'key': 'orderExecutionConfig' }, {
    "$push": {
        "children":
            {
			"_id" : "65095ee1cf1fe2309d010848-Thu May 23 2024 13:17:45 GMT+0800",
			"wardCode" : "",
			"key" : "enableSkinTestMedicinePrepare",
			"pattern" : {
				"componentType" : "Switch",
				"label" : "是否启用皮试（备配药）流程"
			},
			"value" : false
		}
    }
})
```

