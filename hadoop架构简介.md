##### hadoop  发行版本

- apache: 最基础版本, 适合入门学习
- cloudera(用的最多) 与 hortonworks 合并了

##### hadoop 架构

- HDFS 数据存储
- MapReduce 就按
- Common 辅助工具
- Yarn 资源调度

##### HDFS (hadoop分布式文件系统) 架构

- NameNode (nn)
  - 集群中只有一份
  - 管理HDFS命名空间(数据块存在哪个DataNode上由NameNode控制)
  - 配置副本策略
  - 管理数据块Block映射关系(记录文件存在哪些数据块中)
  - 处理客户端读写请求
- DataNode(dn)
  - 实际存储数据
  - 执行数据块读写操作
- Client
- SecondaryNameNode
  - 辅助NameData
  - 不是nn的热备份

##### yarn 架构

- 作用: 管理调度 cpu 和 内存资源
- ApplicationMaster (AM)
  - 位于Node Manager 上
  - 评估任务需要多少资源, 向 Resource Manager 申请资源
- Node Manager (NM)
  - 管理单个节点资源
  - 处理来自Resource Manager的指令
  - 处理来自ApplicationMaster的指令
- Resource Manager (RM)
  - 处理客户端请求
  - 监控	Node Manager 
  - 启动或监控ApplicationMaster
  - 总的资源的分配和调度
- container
  - yarn的资源管理器

##### MapReduce 架构

- 任务分发的过程叫做map
- 任务结束后汇总的过程叫做 reduce



