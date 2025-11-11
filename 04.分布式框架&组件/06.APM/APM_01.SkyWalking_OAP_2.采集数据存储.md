## 采集存储流程

![[Pasted image 20231221113900.png|1400]]

TraceSegment

SegmentObject

TraceAnalyzer

从Agent端采集的Segment数据在OAP中的存储内容如下：

![[Pasted image 20231220154747.png|1500]]


## 页面数据展示

![[Pasted image 20231221161649.png|1200]]

>在Span中的OpName就是前端所显示的端点~

点击展开端点Mysql/JDBC/PreparedStatement/execute查看明细：

![[Pasted image 20231221161845.png|1200]]

接口响应数据：

```json
{
    "data": {
        "trace": {
            "spans": [
                {
                    "traceId": "471fb99104a347c099c99c9b542b511d.233.17031462873150001",
                    "segmentId": "471fb99104a347c099c99c9b542b511d.233.17031462873150000",
                    "spanId": 0,
                    "parentSpanId": -1,
                    "refs": [],
                    "serviceCode": "datasync",
                    "serviceInstanceName": "d3118563a1ee42688de18e4bf0fc11eb@192.168.172.1",
                    "startTime": 1703146287317,
                    "endTime": 1703146288418,
                    "endpointName": "GET:/sysTableSyncConfig",
                    "type": "Entry",
                    "peer": "",
                    "component": "SpringMVC",
                    "isError": false,
                    "layer": "Http",
                    "tags": [
                        {
                            "key": "url",
                            "value": "http://10.2.43.39:9098/data-sync/sysTableSyncConfig"
                        },
                        {
                            "key": "http.method",
                            "value": "GET"
                        },
                        {
                            "key": "http.status_code",
                            "value": "200"
                        }
                    ],
                    "logs": [],
                    "attachedEvents": []
                },
                {
                    "traceId": "471fb99104a347c099c99c9b542b511d.233.17031462873150001",
                    "segmentId": "471fb99104a347c099c99c9b542b511d.233.17031462873150000",
                    "spanId": 1,
                    "parentSpanId": 0,
                    "refs": [],
                    "serviceCode": "datasync",
                    "serviceInstanceName": "d3118563a1ee42688de18e4bf0fc11eb@192.168.172.1",
                    "startTime": 1703146288178,
                    "endTime": 1703146288184,
                    "endpointName": "HikariCP/Connection/getConnection",
                    "type": "Local",
                    "peer": "",
                    "component": "HikariCP",
                    "isError": false,
                    "layer": "Unknown",
                    "tags": [],
                    "logs": [],
                    "attachedEvents": []
                },
                {
                    "traceId": "471fb99104a347c099c99c9b542b511d.233.17031462873150001",
                    "segmentId": "471fb99104a347c099c99c9b542b511d.233.17031462873150000",
                    "spanId": 2,
                    "parentSpanId": 0,
                    "refs": [],
                    "serviceCode": "datasync",
                    "serviceInstanceName": "d3118563a1ee42688de18e4bf0fc11eb@192.168.172.1",
                    "startTime": 1703146288184,
                    "endTime": 1703146288203,
                    "endpointName": "Mysql/JDBC/PreparedStatement/execute",
                    "type": "Exit",
                    "peer": "10.2.6.43:3306",
                    "component": "mysql-connector-java",
                    "isError": false,
                    "layer": "Database",
                    "tags": [
                        {
                            "key": "db.type",
                            "value": "Mysql"
                        },
                        {
                            "key": "db.instance",
                            "value": "windranger_sync"
                        },
                        {
                            "key": "db.statement",
                            "value": "select seq_id, table_name, channel, data_source, table_sql, call_method, table_parameter, \n    table_node, cron, status, query_by_patient, product_code, create_time, create_person, \n    update_time, update_person, description, data_format, base64, direct_search, direct_sql, \n    direct_table_parameter, redis_key, fail_strategy\n    from sys_table_sync_config"
                        }
                    ],
                    "logs": [],
                    "attachedEvents": []
                },
                {
                    "traceId": "471fb99104a347c099c99c9b542b511d.233.17031462873150001",
                    "segmentId": "471fb99104a347c099c99c9b542b511d.233.17031462873150000",
                    "spanId": 3,
                    "parentSpanId": 0,
                    "refs": [],
                    "serviceCode": "datasync",
                    "serviceInstanceName": "d3118563a1ee42688de18e4bf0fc11eb@192.168.172.1",
                    "startTime": 1703146288208,
                    "endTime": 1703146288208,
                    "endpointName": "HikariCP/Connection/close",
                    "type": "Local",
                    "peer": "",
                    "component": "HikariCP",
                    "isError": false,
                    "layer": "Unknown",
                    "tags": [],
                    "logs": [],
                    "attachedEvents": []
                },
                {
                    "traceId": "471fb99104a347c099c99c9b542b511d.233.17031462873150001",
                    "segmentId": "471fb99104a347c099c99c9b542b511d.233.17031462873150000",
                    "spanId": 4,
                    "parentSpanId": 0,
                    "refs": [],
                    "serviceCode": "datasync",
                    "serviceInstanceName": "d3118563a1ee42688de18e4bf0fc11eb@192.168.172.1",
                    "startTime": 1703146288208,
                    "endTime": 1703146288215,
                    "endpointName": "HikariCP/Connection/getConnection",
                    "type": "Local",
                    "peer": "",
                    "component": "HikariCP",
                    "isError": false,
                    "layer": "Unknown",
                    "tags": [],
                    "logs": [],
                    "attachedEvents": []
                },
                {
                    "traceId": "471fb99104a347c099c99c9b542b511d.233.17031462873150001",
                    "segmentId": "471fb99104a347c099c99c9b542b511d.233.17031462873150000",
                    "spanId": 5,
                    "parentSpanId": 0,
                    "refs": [],
                    "serviceCode": "datasync",
                    "serviceInstanceName": "d3118563a1ee42688de18e4bf0fc11eb@192.168.172.1",
                    "startTime": 1703146288215,
                    "endTime": 1703146288224,
                    "endpointName": "Mysql/JDBC/PreparedStatement/execute",
                    "type": "Exit",
                    "peer": "10.2.3.114:3306",
                    "component": "mysql-connector-java",
                    "isError": false,
                    "layer": "Database",
                    "tags": [
                        {
                            "key": "db.type",
                            "value": "Mysql"
                        },
                        {
                            "key": "db.instance",
                            "value": "windranger_foundation"
                        },
                        {
                            "key": "db.statement",
                            "value": "select * from sys_dic where 1=1 \n     \n     \n     \n     \n      and dic_type = ?"
                        }
                    ],
                    "logs": [],
                    "attachedEvents": []
                },
                {
                    "traceId": "471fb99104a347c099c99c9b542b511d.233.17031462873150001",
                    "segmentId": "471fb99104a347c099c99c9b542b511d.233.17031462873150000",
                    "spanId": 6,
                    "parentSpanId": 0,
                    "refs": [],
                    "serviceCode": "datasync",
                    "serviceInstanceName": "d3118563a1ee42688de18e4bf0fc11eb@192.168.172.1",
                    "startTime": 1703146288225,
                    "endTime": 1703146288225,
                    "endpointName": "HikariCP/Connection/close",
                    "type": "Local",
                    "peer": "",
                    "component": "HikariCP",
                    "isError": false,
                    "layer": "Unknown",
                    "tags": [],
                    "logs": [],
                    "attachedEvents": []
                }
            ]
        }
    }
}
```
