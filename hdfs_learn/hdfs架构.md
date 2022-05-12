##### 特点

```
分布式文件系统是什么
统一管理分布在集群上的文件系统, 跨机器存储, 解决海量存储问题, 提供统一的访问接口，能够像普通文件系统那样操作


分布式存储方案
将大文件拆分成多块分别放到不同服务器中


优点
    能够运行在廉价机器上，硬件出错常态，需要具备高容错性
    流式数据访问，而不是随机读写
    面向大规模数据集，能够进行批处理、能够横向扩展
    简单一致性模型，假定文件是一次写入、多次读取


缺点
    不支持低延迟数据访问
    不适合大量小文件存储（因为每条元数据占用空间是一定的）
    不支持并发写入，一个文件只能有一个写入者
    不支持文件随机修改，仅支持追加写入
```

##### 心跳机制

```
1. datanode 和 namenode 之间保持的心跳机制，datanode每隔3秒向namenode发送一次心跳包，证明自己还活着

2. 当datanode在一定时间内没发送心跳，等待10次，默认配置30秒未收到心跳，namenode会认定其为假死，由namenode主动每隔5秒向datanode发送一次检查，两次检查仍然没收到则认定为宕机。按默认配置共630断定datanode死亡。

3. 除此之外，datanode每隔六小时还会向namenode汇报自己的块信息

4. hdfs-default.xml中配置
```

##### 负载均衡

```
namenode要保证每个datanode上的块的数量大致相当

$ start-balancer.sh -t 10%
```

##### 副本机制

```
默认每个块3个副本，当发现某些块副本不足3个，会让指定节点创建副本，保证副本为3个，如果副本数据多于3个，会让指定的节点将多余副本删除。

如果无法处理副本(挂了一大半机子)，此时namenode会让hdfs进行安全模式，不许写入。 每一次刚启动hdfs默认都会先进入安全模式，各个datanode向namenode汇报块信息，namenode检测数据完整，退出安全模式
```

##### 命令

```
hadoop fs
或
hdfs dfs
```

- 本地上传到 HDFS

```bash
# 从本地剪切粘贴到HDFS
$ hadoop fs  -moveFromLocal  ./kongming.txt  /sanguo/shuguo

# 从本地文件系统中拷贝文件到HDFS
$ hadoop fs -copyFromLocal README.txt /

# 追加一个文件到已经存在的文件末尾
$ hadoop fs -appendToFile liubei.txt /sanguo/shuguo/kongming.txt

# 从本地文件系统中拷贝文件到HDFS
$ hadoop fs -put ./zaiyiqi.txt /user/atguigu/test/
```

- HDFS 操作

```bash
$ hadoop fs -ls /
$ hadoop fs -mkdir -p /sanguo/shuguo
$ hadoop fs -rmdir /test
$ hadoop fs -cat /sanguo/shuguo/kongming.txt
$ hadoop fs -chmod  666  /sanguo/shuguo/kongming.txt
$ hadoop fs -chown  atguigu:atguigu
$ hadoop fs -cp /sanguo/shuguo/kongming.txt /zhuge.txt
$ hadoop fs -mv /zhuge.txt /sanguo/shuguo/
$ hadoop fs -tail /sanguo/shuguo/kongming.txt
$ hadoop fs -rm /user/atguigu/test/jinlian2.txt
# 统计文件夹的大小信息
$ hadoop fs -du -s -h /user/atguigu/test
$ hadoop fs -du  -h /user/atguigu/test
# 设置HDFS中文件的副本数量
$ hadoop fs -setrep 10 /sanguo/shuguo/kongming.txt
```

- HDFS下载到本地

```
get
getmerge
copyTolocal
```



```
namenode (nn)
存储文件元数据, 如文件名, 文件目录结构, 文件属性(生成时间, 副本数, 权限), 以及每个文件的块列表和块所在的 datanode

datanode (dn)
存储文件块数据, 以及数据校验和

secondary namenode (2nn)
每隔一段时间对 namenode 备份


```

## block

```
将一个文件进行分块，通常是64M。写入后不能修改，但是可以追加
```



## MetaData

```
元数据
着文件系统树及整棵树内所有的文件和目录及分块信息
```



## NameNode

##### 作用

```
管理文件系统的命名空间，它维护 MetaData, 元数据有三种存储方式
内存元数据: 目的是提升性能，定期从磁盘加载一份镜像到内存中
命名空间镜像文件（fsImage）: 保存整个文件系统的目录树
编辑日志文件（edits）: 记录文件系统元数据发生的所有更改，如文件的删除或添加等操作信息



```

##### 单点故障

> 详细文章: https://juejin.cn/post/6844903990937796616



```
为了保证读写数据一致性，HDFS集群设计为只能有一个状态为Active的NameNode，但这种设计存在单点故障问题，官方提供了两种解决方案：

QJM（推荐）：通过同步编辑事务日志的方式备份命名空间数据，同时需要DataNode向所有NameNode上报块列表信息。还可以配置ZKFC组件实现故障自动转移。
NFS：将需要持久化的数据写入本地磁盘的同时写入一个远程挂载的网络文件系统做为备份。
通过增加一个Secondary NameNode节点，处于Standby的状态，与Active的NameNode同时运行。当Active的节点出现故障时，切换到Secondary节点。

为了保证Secondary节点能够随时顶替上去，Standby节点需要定时同步Active节点的事务日志来更新本地的文件系统目录树信息，同时DataNode需要配置所有NameNode的位置，并向所有状态的NameNode发送块列表信息和心跳。

同步事务日志来更新目录树由JournalNode的守护进程来完成，简称为QJM，一个NameNode对应一个QJM进程，当Active节点执行任何命名空间文件目录树修改时，它会将修改记录持久化到大多数QJM中，Standby节点从QJM中监听并读取编辑事务日志内容，并将编辑日志应用到自己的命名空间。发生故障转移时，Standby节点将确保在将自身提升为Active状态之前，从QJM读取所有编辑内容。

注意，QJM只是实现了数据的备份，当Active节点发送故障时，需要手工提升Standby节点为Active节点。如果要实现NameNode故障自动转移，则需要配套ZKFC组件来实现，ZKFC也是独立运行的一个守护进程，基于zookeeper来实现选举和自动故障转移。
```

## 















