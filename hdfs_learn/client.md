##### client 作用

```
1. 文件切分. 文件上传 HDFS 的时候, Client 将文件切分成一个一个的Block, 然后进行存储.
2. 与 NameNode 交互，获取文件元数据
3. 与 DataNode 交互，读取或者写入数据
4. Client 提供一些命令来管理 HDFS，比如启动或者关闭HDFS
5. Client 可以通过一些命令来访问 HDFS
```



