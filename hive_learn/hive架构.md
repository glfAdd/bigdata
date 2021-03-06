##### 是什么

```
Hive 是基于 Hadoop 的一个数据仓库工具，用来处理结构化数据, 可以将结构化的数据文件映射为一张数据库表, 并提供简单的sql查询功能，可以将sql语句转换为MapReduce任务进行运行, 并使得查询和分析方便

本质是：将 HQL 转化成 MapReduce 程序
```

##### 解决什么问题

```
直接使用hadoop 人员学习成本太高, MapReduce实现复杂查询逻辑开发难度太大

Hive 操作接口采用类SQL语法，提供快速开发的能力, 避免了去写MapReduce，减少开发人员的学习成本, 扩展功能很方便。
```

##### 特点

```
可扩展: Hive可以自由的扩展集群的规模，一般情况下不需要重启服务。
延展性: Hive支持用户自定义函数，用户可以根据自己的需求来实现自己的函数。
容错: 良好的容错性，节点出现问题SQL仍可完成执行

Hive不适用于在线事务处理。 它最适用于传统的数据仓库任务
Hive 不适合那些需要低延迟的应用
Hive 的最佳使用场合是大数据集的批处理作业，例如，网络日志分析

hadoop 和 mapreduce 是 hive 架构的基础
Hive处理的数据存储在HDFS
Hive分析数据底层的实现是MapReduce
执行程序运行在Yarn上
```

## 组建

<img src="/home/glfadd/Desktop/learn/bigdata/image/hive架构.png" alt="hive架构" style="zoom:60%;" />

##### Driver组件

```
包括Complier、Optimizer和Executor，它的作用是将我们写的HiveQL（类SQL）语句进行解析、编译优化，生成执行计划，然后调用底层的mapreduce计算框架


1. 解析器（SQL Parser）：将SQL字符串转换成抽象语法树AST，这一步一般都用第三方工具库完成，比如antlr；对AST进行语法分析，比如表是否存在、字段是否存在、SQL语义是否有误。
2. 编译器（Physical Plan）：将AST编译生成逻辑执行计划。
3. 优化器（Query Optimizer）：对逻辑执行计划进行优化。
4. 执行器（Execution）：把逻辑执行计划转换成可以运行的物理计划。对于Hive来说，就是MR/Spark。
```

##### Metastore组件

```
Metastore 组件存放 hive元数据. hive的元数据存储在关系数据库里

Metastore 组件包括两个部分: Metastore 服务和后台数据的存储

后台数据存储的介质就是关系数据库，例如hive默认的嵌入式磁盘数据库derby，还有mysql数据库。

Metastore服务是建立在后台数据存储介质之上，并且可以和hive服务进行交互的服务组件，默认情况下，metastore服务和hive服务是安装在一起的，运行在同一个进程当中。我也可以把metastore服务从hive服务里剥离出来，metastore独立安装在一个集群里，hive远程调用metastore服务，这样我们可以把元数据这一层放到防火墙之后，客户端访问hive服务，就可以连接到元数据这一层，从而提供了更好的管理性和安全保障。使用远程的metastore服务，可以让metastore服务和hive服务运行在不同的进程里，这样也保证了hive的稳定性，提升了hive服务的效率。
```

##### Thrift服务

```
thrift 是 facebook 开发的一个软件框架，它用来进行可扩展且跨语言的服务的开发，hive集成了该服务，能让不同的编程语言调用hive的接口。
```

##### CLI

````
command line interface，命令行接口
````

##### Thrift客户端

```
上面的架构图里没有写上Thrift客户端，但是hive架构的许多客户端接口是建立在thrift客户端之上，包括JDBC和ODBC接口
```

##### WEBGUI

```
hive客户端提供了一种通过网页的方式访问hive所提供的服务。这个接口对应hive的hwi组件（hive web interface），使用前要启动hwi服务
```

## 概念

##### Metastore (元数据)

```
包括：表名、表所属的数据库（默认是default）、表的拥有者、列/分区字段、表的类型（是否是外部表）、表的数据所在目录等

默认存储在自带的derby数据库中，推荐使用MySQL存储Metastore
```

##### 和关系型数据库比较

```


```

#####

```


```

##### 安装

```
1）Hive官网地址
http://hive.apache.org/
2）文档查看地址
https://cwiki.apache.org/confluence/display/Hive/GettingStarted
3）下载地址
http://archive.apache.org/dist/hive/
4）github地址
https://github.com/apache/hive


mysql 安装


```









