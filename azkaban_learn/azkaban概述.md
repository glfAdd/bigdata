##### 是什么

```
一个批量工作流任务调度器。用于在一个工作流内以一个特定的顺序运行一组工作和流程
```

##### 架构

<img src="/home/glfadd/Desktop/learn/bigdata/azkaban_learn/image/关键组件构成.png" alt="关键组件构成" style="zoom:50%;" />





```
1、Relational Database(Mysql)
azkaban将大多数状态信息都存于MySQL中,Azkaban Web Server 和 Azkaban Executor Server也需要访问DB。

2、Azkaban Web Server
提供了Web UI，是azkaban的主要管理者，包括 project 的管理，认证，调度，对工作流执行过程的监控等。

3、Azkaban Executor Server
调度工作流和任务，纪录工作流活任务的日志
```

##### project, flow, job 关系

```
projects：工程. 所有 flows 将在工程中运行, 一个 projects 包含一个或多个 flows
flow: 一个flow包含多个job, 多个job和它们的依赖组成的图表叫做
job: 是你想在azkaban中运行的一个进程, 有多种类型
```

##### job类型

```
1.command：Linux shell命令行任务
2.gobblin：通用数据采集工具
3.hadoopJava：运行hadoopMR任务
4.java：原生java任务
5.hive：支持执行hiveSQL
6.pig：pig脚本任务
7.spark：spark任务
8.hdfsToTeradata：把数据从hdfs导入Teradata
9.teradataToHdfs：把数据从Teradata导入hdfs
```

