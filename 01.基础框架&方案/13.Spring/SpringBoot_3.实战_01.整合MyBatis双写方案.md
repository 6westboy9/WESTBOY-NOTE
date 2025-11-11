# 需求

https://blog.csdn.net/weixin_43935927/article/details/111321547


旧的单表 -> 还是走SINGLE_DATASOURCE
新的分片表 -> 走SHARDING_DATASOURCE（主要需要思考一个问题，如果单表不走SHARDING_DATASOURCE，那对于关联查询怎么办？）

其实还是想后续然全部走SHARDING_DATASOURCE


# 联新实战方案

>Driaw图见分库分表附件~

![[Pasted image 20240207105649.png|1150]]
