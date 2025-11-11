
# 查看所有索引

```
http://10.2.43.101:9200/_cat/indices

green  open sw_segment-20240320           BELlGqXxRmGtxLld8SZOGg 5 0 153384    0  83.5mb  83.5mb
green  open sw_browser_error_log-20240320 W-IPdZzVTy2loNQdxrNOxg 5 0      0    0     1kb     1kb
yellow open sw_ui_template                jBlECyzhRUKVt4qHu5rqdQ 1 1     57    0 233.1kb 233.1kb
green  open sw_zipkin_span-20240312       KBOiIp99SqC4m_p8Orkd3A 5 0      0    0     1kb     1kb
yellow open sw_metrics-all-20240320       wBoNy6NBQDCPW3N82C-Bww 1 1   7808 3862   1.9mb   1.9mb
green  open sw_log-20240320               e-pPUL6bSUi1FFAmQbXcEw 5 0      0    0     1kb     1kb
yellow open sw_records-all-20240320       VYkbr65yRq6wfMopDkEqpA 1 1     44    0    35kb    35kb
```

**响应说明**

| health | status | index                         | uuid                   | pri | rep | docs.count | docs.deleted | store.size | pri.store.size |
| ------ | ------ | ----------------------------- | ---------------------- | --- | --- | ---------- | ------------ | ---------- | -------------- |
| green  | open   | sw_segment-20240320           | BELlGqXxRmGtxLld8SZOGg | 5   | 0   | 153384     | 0            | 83.5mb     | 83.5mb         |
| green  | open   | sw_browser_error_log-20240320 | W-IPdZzVTy2loNQdxrNOxg | 5   | 0   | 0          | 0            | 1kb        | 1kb            |
| yellow | open   | sw_ui_template                | jBlECyzhRUKVt4qHu5rqdQ | 1   | 1   | 57         | 0            | 233.1kb    | 233.1kb        |
| green  | open   | sw_zipkin_span-20240312       | KBOiIp99SqC4m_p8Orkd3A | 5   | 0   | 0          | 0            | 1kb        | 1kb            |
| yellow | open   | sw_metrics-all-20240320       | wBoNy6NBQDCPW3N82C-Bww | 1   | 1   | 7808       | 3862         | 1.9mb      | 1.9mb          |
| green  | open   | sw_log-20240320               | e-pPUL6bSUi1FFAmQbXcEw | 5   | 0   | 0          | 0            | 1kb        | 1kb            |
| yellow | open   | sw_records-all-20240320       | VYkbr65yRq6wfMopDkEqpA | 1   | 1   | 44         | 0            | 35kb       | 35kb           |

1. **health**：索引健康状态，有以下可能的取值：
    - `green`：所有主分片和副本分片都可用。
    - `yellow`：所有主分片可用，但部分副本分片丢失。
    - `red`：部分主分片丢失，索引可能无法正常工作。
2. **status**：索引的状态，通常是 `open` 表示打开状态，也可能是 `closed` 表示关闭状态。
3. **index**：索引名称。
4. **uuid**：索引的唯一标识符。
5. **pri**：主分片数量。
6. **rep**：副本分片数量。
7. **docs.count**：索引中文档的数量。
8. **docs.deleted**：已删除的文档数量。
9. **store.size**：索引占用的磁盘存储空间大小。
10. **pri.store.size**：主分片占用的磁盘存储空间大小。



