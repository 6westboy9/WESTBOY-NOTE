资料

* [Kettle变量和参数介绍系列文章1-变量的使用](https://blog.csdn.net/m0_69586799/article/details/126080483)
* [Kettle变量和参数介绍系列文章2-参数的使用](https://blog.csdn.net/m0_69586799/article/details/126377502)
* [Kettle变量和参数介绍系列文章3-循环的轻松实现](https://blog.csdn.net/m0_69586799/article/details/126978410)

# 参数

作业参数设置

转换参数设置

# 变量

## 变量的分类

在PDI中变量一共可以分为3类：

* 系统变量：即<font color="#4f81bd">用户目录/.kettle/kettle.properties</font>文件，修改配置<font color="#f79646">需要重启</font>才能生效 -- <font color="#f79646">全局变量</font>
* 自定义变量：对应<font color="#f79646">设置变量</font>组件 -- <font color="#f79646">局部变量</font>
* 环境变量：环境变量指的是当前脚本文件中出现的所有变量，包括系统变量、自定义变量以及环境变量自身定义的变量。

## 变量的使用

```shell
${var_name:default_value}
```

## 系统变量

系统变量说明

>用户目录/.kettle/kettle.properties

| 键                                     | 默认值 | 描述                                       |
| ------------------------------------- | --- | ---------------------------------------- |
| KETTLE_EMPTY_STRING_DIFFERS_FROM_NULL | N   | 设置为Y时，空字符串和null是独立的，N时，PDI会将空字符串当做null处理 |

## 自定义变量


### 设置变量组件


<font color="#f79646">变量的作用范围</font>

| 类型                                | 说明                 |
| --------------------------------- | ------------------ |
| Valid in the Java Virtual Machine | 凡是在一个JVM下运行的程序都受影响 |
| Valid in the parent job           | 当前作业下生效            |
| Valid in the grant-parent job     | 当前作业的父作业下生效        |
| Valid in the root job             | 凡是在根作业下运行的都生效      |

<font color="#f79646">使用注意</font>

* 变量的有效范围，超过使用范围后就无法使用了~
* <font color="#c0504d">在转换中定义的变量，在本次转换中不生效~</font>

<font color="#f79646">一般用法</font>

* 保存前一个步骤的结果值，在其它步骤中使用
* 在循环执行中通过对变量赋值实现遍历操作


### 获取变量组件


## 环境变量



# 流程


作业流程与转换流程


# 错误处理



# 脚本

## SQL脚本

## Java脚本


```java
// 获取记录中的字段值
String inhosCode = get(Fields.In, "inhos_code").getString(r);
// 日志中打印字段值
logBasic("inhosCode: " + inhosCode);
```

# Linux运行PDI程序


## 运行转换

运行`pan.sh`脚本即可，其底层实现为`spoon.sh`。

```sh
[root@localhost data-integration]# ./pan.sh -file:lachesis/order_out_202208.ktr 
#######################################################################
WARNING:  no libwebkitgtk-1.0 detected, some features will be unavailable
    Consider installing the package with apt-get or yum.
    e.g. 'sudo apt-get install libwebkitgtk-1.0-0'
#######################################################################
2024/04/08 09:27:46 - Pan - Start of run.
2024/04/08 09:27:47 - order_out_202208 - Dispatching started for transformation [order_out_202208]
2024/04/08 09:28:46 - pat_inhos_order_out_202208表数据抽取.0 - linenr 50000
2024/04/08 09:28:59 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 50000
2024/04/08 09:29:54 - pat_inhos_order_out_202208表数据抽取.0 - linenr 100000
2024/04/08 09:30:08 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 100000
2024/04/08 09:31:00 - pat_inhos_order_out_202208表数据抽取.0 - linenr 150000
2024/04/08 09:31:14 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 150000
2024/04/08 09:32:03 - pat_inhos_order_out_202208表数据抽取.0 - linenr 200000
2024/04/08 09:32:16 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 200000
2024/04/08 09:33:06 - pat_inhos_order_out_202208表数据抽取.0 - linenr 250000
2024/04/08 09:33:18 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 250000
2024/04/08 09:34:09 - pat_inhos_order_out_202208表数据抽取.0 - linenr 300000
2024/04/08 09:34:21 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 300000
2024/04/08 09:35:11 - pat_inhos_order_out_202208表数据抽取.0 - linenr 350000
2024/04/08 09:35:24 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 350000
2024/04/08 09:36:19 - pat_inhos_order_out_202208表数据抽取.0 - linenr 400000
2024/04/08 09:36:32 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 400000
2024/04/08 09:37:23 - pat_inhos_order_out_202208表数据抽取.0 - linenr 450000
2024/04/08 09:37:36 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 450000
2024/04/08 09:38:29 - pat_inhos_order_out_202208表数据抽取.0 - linenr 500000
2024/04/08 09:38:43 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 500000
2024/04/08 09:39:37 - pat_inhos_order_out_202208表数据抽取.0 - linenr 550000
2024/04/08 09:39:51 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 550000
2024/04/08 09:40:40 - pat_inhos_order_out_202208表数据抽取.0 - linenr 600000
2024/04/08 09:40:53 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 600000
2024/04/08 09:41:41 - pat_inhos_order_out_202208表数据抽取.0 - linenr 650000
2024/04/08 09:41:53 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 650000
2024/04/08 09:42:42 - pat_inhos_order_out_202208表数据抽取.0 - linenr 700000
2024/04/08 09:42:56 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 700000
2024/04/08 09:43:46 - pat_inhos_order_out_202208表数据抽取.0 - linenr 750000
2024/04/08 09:43:57 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 750000
2024/04/08 09:44:43 - pat_inhos_order_out_202208表数据抽取.0 - linenr 800000
2024/04/08 09:44:56 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 800000
2024/04/08 09:45:45 - pat_inhos_order_out_202208表数据抽取.0 - linenr 850000
2024/04/08 09:45:57 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 850000
2024/04/08 09:46:43 - pat_inhos_order_out_202208表数据抽取.0 - linenr 900000
2024/04/08 09:46:55 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 900000
2024/04/08 09:47:44 - pat_inhos_order_out_202208表数据抽取.0 - linenr 950000
2024/04/08 09:47:56 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 950000
2024/04/08 09:48:44 - pat_inhos_order_out_202208表数据抽取.0 - linenr 1000000
2024/04/08 09:48:55 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 1000000
2024/04/08 09:49:42 - pat_inhos_order_out_202208表数据抽取.0 - linenr 1050000
2024/04/08 09:49:54 - pat_inhos_order_outv2_202208插入或更新.0 - linenr 1050000
2024/04/08 09:49:57 - pat_inhos_order_out_202208表数据抽取.0 - Finished reading query, closing connection
2024/04/08 09:49:57 - pat_inhos_order_out_202208表数据抽取.0 - Finished processing (I=1061949, O=0, R=0, W=1061949, U=0, E=0)
2024/04/08 09:50:08 - pat_inhos_order_outv2_202208插入或更新.0 - Finished processing (I=1061949, O=1061949, R=1061949, W=1061949, U=0, E=0)
2024/04/08 09:50:08 - Pan - Finished!
2024/04/08 09:50:08 - Pan - Start=2024/04/08 09:27:47.282, Stop=2024/04/08 09:50:08.163
2024/04/08 09:50:08 - Pan - Processing ended after 22 minutes and 20 seconds (1340 seconds total).
2024/04/08 09:50:08 - order_out_202208 -  
2024/04/08 09:50:08 - order_out_202208 - Step pat_inhos_order_out_202208表数据抽取.0 ended successfully, processed 1061949 lines. ( 792 lines/s)
2024/04/08 09:50:08 - order_out_202208 - Step pat_inhos_order_outv2_202208插入或更新.0 ended successfully, processed 1061949 lines. ( 792 lines/s)
```

真正运行程序的脚本入口是`spoon.sh`，程序`main`方法对应的类：`org.pentaho.di.pan.Pan`。

```sh
[root@localhost data-integration]# cat pan.sh 
#!/bin/sh

# *****************************************************************************
#
# Pentaho Data Integration
#
# Copyright (C) 2005 - 2022 by Hitachi Vantara : http://www.hitachivantara.com
#
# *****************************************************************************
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# *****************************************************************************

INITIALDIR="`pwd`"
BASEDIR="`dirname $0`"
cd "$BASEDIR"
DIR="`pwd`"
cd - > /dev/null

if [ "$1" = "-x" ]; then
  set LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$BASEDIR/lib
  export LD_LIBRARY_PATH
  export OPT="-Xruntracer $OPT"
  shift
fi

"$DIR/spoon.sh" -main org.pentaho.di.pan.Pan -initialDir "$INITIALDIR/" "$@"
```

## 运行作业

><font color="#f79646">在Windows下设计好的作业，记得替换路径！</font>

```sh
nohup ./kitchen.sh -file:lachesis/job_order_out_all_v1/全量出院数据-医嘱表.kjb -logfile:logs/job_order_out_all_v1.log &
ps -ef | grep Kitchen
```






