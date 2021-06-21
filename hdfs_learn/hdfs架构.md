##### 分布式文件系统是什么

```

```

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





