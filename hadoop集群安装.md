##### 集群状态查看

```
========= centos101 =======
7632 NodeManager
8338 Bootstrap
6935 NameNode
7964 RunJar
7087 DataNode
7487 ApplicationHistoryServer
8127 RunJar
========= centos102 =======
5266 NodeManager
4876 DataNode
5119 ResourceManager
========= centos103 =======
5762 SecondaryNameNode
5541 DataNode
5644 JobHistoryServer
5916 NodeManager
```

##### docker 参数说明

```
-d 后台启动

--hostname 指定主机名字
```

##### 文档

```
官网文档
http://hadoop.apache.org/docs/

底版本中文文档
http://hadoop.apache.org/docs/r1.0.4/cn/cluster_setup.html
```

## 使用 docker 安装 centos

##### 查看docker所有网络类型

```
$ docker network ls
bridge: 桥接网络, 每次启动容器ip变化(默认)
host: 主机网络, 使用主机的网络
none: 无指定网络, 不会分配局域网的IP
```

##### 创建网络环境, 设置固定ip

```
$ docker network create --subnet=172.20.0.0/16 hadoopnetwork
```

##### 创建 centos 容器基本环境

```bash
$ docker run --net hadoopnetwork --ip 172.20.0.101 -itd --name centosbase centos:centos7
```

##### docker 安装 centos 使用中的问题

```
问题1: (未解决, /usr/sbin/init 会影响xubuntu 系统本身)
使用systemctl命令管理进程，报以下错误错误信息: Failed to get D-Bus connection: Operation not permitted

原因:
Docker的设计理念是在容器里面不运行后台服务

解决方法：
创建容器增加参数 /usr/sbin/init
如果是已经创建好的容器，那你得重新把容器打包成镜像再启动了。把容器打包成镜像用的是docker commit这个命令
```

##### centos 需要的软件

```bash
# yum install -y wget
# wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
# yum install -y epel-release
# yum clean all
# yum makecache
# yum update
# yum install -y vim net-tools passwd sudo git zsh htop tree telnet telnet-server iotop
```

##### 安装 ssh 

- 安装

```
yum install -y openssl openssh-server openssh-clients
```

- 直接用启动

```bash
# /usr/sbin/sshd -D
直接运行会报下面错误: 
Could not load host key: /etc/ssh/ssh_host_rsa_key
Could not load host key: /etc/ssh/ssh_host_ecdsa_key
Could not load host key: /etc/ssh/ssh_host_ed25519_key

需要生成容器的公钥、私钥
# ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
# ssh-keygen -t rsa -f /etc/ssh/ssh_host_ecdsa_key
# ssh-keygen -t rsa -f /etc/ssh/ssh_host_ed25519_key
```

- 设置免密登录

```
创建 authorized_keys 文件, 添加公钥


如果仍然无法登录需要修改该文件权限
chmod 644 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

- 编写容器的服务启动脚本

  - 创建一个 /run.sh 的脚本, 添加如下内容

  ```shell
  #!/bin/bash
  /usr/sbin/sshd -D
  ```

  - 设置可执行权限

  ```bash
  chmod +x /run.sh
  ```

- 生成密钥对

```bash
ssh-keygen -t rsa 
```

- 会将本机的公钥发送到要访问计算机, 存储在 ~/.ssh/authorized_keys

```
ssh-copy-id centos101
```

##### 创建新用户

```bash
# adduser xxx
# passwd xxx
```

##### 关闭防火墙

```
sudo systemctl stop firewalld
sudo systemctl disable firewalld
```

##### 普通用户无法使用 sudo 命令

```
gladd is not in the sudoers file.  This incident will be reported

1. 添加sudoers文件的写权限, /etc/sudoers文件默认是只读的
chmod u+w /etc/sudoers


2. 编辑文件 /etc/sudoers
## Allow root to run any commands anywhere 
root    ALL=(ALL)       ALL
gong    ALL=(ALL)       ALL

## Same thing without a password
# %wheel        ALL=(ALL)       NOPASSWD: ALL
gong    ALL=(ALL)       NOPASSWD: ALL


3. 撤销sudoers文件写权限,命令:
chmod u-w /etc/sudoers
```

##### 安装 oh my zsh(影响环境变量, 不安装)

- 域名解析修改 hosts

```
1. https://www.ipaddress.com/ 查询域名 raw.githubusercontent.com 的 ip 为 185.199.108.133


2. 修改hosts文件 添加:
185.199.108.133 raw.githubusercontent.com
```

- 安装

```
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

##### 将容器 commit 为新的镜像

```bash
1. 停止容器


2. 查看容器进程找到刚才停止的容器
# docker ps -a


3. 创建新镜像
# docker commit e1501b5cd426 centos:glfadd_base


4. 查看创建好的镜像
```

##### 根据基础镜像安装centos

```bash
$ docker run --net hadoopnetwork --ip 172.20.0.101 -itd --name centos101 --hostname centos101 centos:glfadd_base /run.sh
$ docker run --net hadoopnetwork --ip 172.20.0.102 -itd --name centos102 --hostname centos102 centos:glfadd_base /run.sh
$ docker run --net hadoopnetwork --ip 172.20.0.103 -itd --name centos103 --hostname centos103 centos:glfadd_base /run.sh
```

##### 修改 hosts 文件

```
172.20.0.101 centos101
172.20.0.102 centos102
172.20.0.103 centos103
```

##### 安装 jdk 8 和 hadoop

```
1. 官网 https://www.oracle.com/java/technologies/javase-downloads.html 下载 jdk-8u291-linux-x64.tar.gz
wget https://download.oracle.com/otn/java/jdk/8u291-b10/d7fc238d0cbf4b0dac67be84580cfb4b/jdk-8u291-linux-x64.tar.gz?AuthParam=1622798508_591a13ca10b5a996d1b64f9623feadd5

2. 官网 https://hadoop.apache.org/releases.html 下载 hadoop https://mirrors.bfsu.edu.cn/apache/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz


3. 复制到docker
docker cp jdk-8u291-linux-x64.tar.gz centos101:/opt
docker cp hadoop-3.2.2.tar.gz centos101:/opt


4. 解压后设置环境变量, 编辑 /etc/profile.d/my_env.sh 文件, 添加如下内容
#HADOOP_HOME
export HADOOP_HOME=/opt/hadoop-3.2.2
export PATH=$PATH:$HADOOP_HOME/bin
export PATH=$PATH:$HADOOP_HOME/sbin
#JAVA_HOME
export JAVA_HOME=/opt/jdk1.8.0_291
export PATH=$PATH:$JAVA_HOME/bin


5. 使配置生效
source /etc/profile


6. 验证
java -version
hadoop version
```

##### hadoop目录

| 目录  | 说明                                            |
| ----- | ----------------------------------------------- |
| bin   | 存放对Hadoop相关服务（HDFS,YARN）进行操作的脚本 |
| sbin  | 存放启动或停止Hadoop相关服务的脚本              |
| etc   | Hadoop的配置文件目录，存放Hadoop的配置文件      |
| lib   | 存放Hadoop的本地库（对数据进行压缩解压缩功能）  |
| share | 存放Hadoop的依赖jar包、文档、和官方案例         |

## 配置 hadoop

> 目录 /opt/hadoop-3.2.2/etc/hadoop

##### 集群分配

- 原则

```
NameNode 和 SecondaryNameNode不要安装在同一台服务器
ResourceManager 也很消耗内存，不要和NameNode、SecondaryNameNode配置在同一台机器上。
```

##### core-site.xml (核心配置文件)

| 参数           | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| fs.defaultFS   | NameNode 的URI                                               |
| hadoop.tmp.dir | Hadoop的默认临时路径. hadoop.tmp.dir是hadoop文件系统依赖的基础配置，很多路径都依赖它。它默认的位置是在/tmp/{$user}下面，但是在/tmp路径下的存储是不安全的，因为linux一次重启，文件就可能被删除 |



````xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://centos101:8020</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/opt/hadoop-3.2.2/data</value>
    </property>
    <property>
        <name>hadoop.proxyuser.gong.hosts</name>
        <value>*</value>
    </property>
    <property>
        <name>hadoop.proxyuser.gong.groups</name>
        <value>*</value>
    </property>
    <property>
        <name>hadoop.http.staticuser.user</name>
        <value>gong</value>
    </property>
</configuration>
````

##### hdfs-site.xml

 ```xml
 <configuration>
     <property>
         <name>dfs.namenode.name.dir</name>
         <value>file://${hadoop.tmp.dir}/name</value>
     </property>
     <property>
         <name>dfs.namenode.checkpoint.dir</name>
         <value>file://${hadoop.tmp.dir}/namesecondary</value>
     </property>
     <property>
         <name>dfs.datanode.name.dir</name>
         <value>file://${hadoop.data.dir}/data</value>
     </property>
     <property>
         <name>dfs.namenode.secondary.http-address</name>
         <value>centos103:9868</value>
     </property>
 </configuration>
 ```

##### yarn-site.xml

| 参数                                | 说明                                   |
| ----------------------------------- | -------------------------------------- |
| yarn.nodemanager.aux-services       | nomenodeManager获取数据的方式是shuffle |
| yarn.resourcemanager.hostname       | 指定Yarn的老大(ResourceManager)的地址  |
| yarn.log-aggregation-enable         | 开启日志聚集功能                       |
| yarn.log-aggregation.retain-seconds | 日志保存时间                           |
| yarn.log.server.url                 | 日志服务器地址                         |



```xml
<configuration>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.resourcemanager.hostname</name>
        <value>centos102</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
    </property>
    <property>
        <name>yarn.log-aggregation-enable</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.log.server.url</name>
        <value>http://centos101/jobhistory/logs</value>
    </property>
    <property>
        <name>yarn.log-aggregation.retain-seconds</name>
        <value>604800</value>
    </property>
    <property>
        <name>yarn.log-aggregation-enable</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.log.server.url</name>
        <value>http://${yarn.timeline-service.webapp.address}/applicationhistory/logs</value>
    </property>
    <property>
        <name>yarn.log-aggregation.retain-seconds</name>
        <value>604800</value>
    </property>
    <property>
        <name>yarn.timeline-service.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.timeline-service.hostname</name>
        <value>${yarn.resourcemanager.hostname}</value>
    </property>
    <property>
        <name>yarn.timeline-service.http-cross-origin.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.resourcemanager.system-metrics-publisher.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.timeline-service.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.timeline-service.hostname</name>
        <value>centos101</value>
    </property>
    <property>
        <name>yarn.timeline-service.http-cross-origin.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name> yarn.resourcemanager.system-metrics-publisher.enabled</name>
        <value>true</value>
    </property>
    <property>
        <name>yarn.timeline-service.generic-application-history.enabled</name>
        <value>true</value>
    </property>
    <property>
        <description>Address for the Timeline server to start the RPC server.</description>
        <name>yarn.timeline-service.address</name>
        <value>centos101:10201</value>
    </property>
    <property>
        <description>The http address of the Timeline service web application.</description>
        <name>yarn.timeline-service.webapp.address</name>
        <value>centos101:8188</value>
    </property>
    <property>
        <description>The https address of the Timeline service web application.</description>
        <name>yarn.timeline-service.webapp.https.address</name>
        <value>centos101:2191</value>
    </property>
    <property>
        <name>yarn.timeline-service.handler-thread-count</name>
        <value>24</value>
    </property>
</configuration>
```

##### mapres-site.xml

| 参数                                | 说明                |
| ----------------------------------- | ------------------- |
| mapreduce.jobhistory.address        | 历史服务器端地址    |
| mapreduce.jobhistory.webapp.address | 历史服务器web端地址 |



```xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <!-- 历史服务器端地址 -->
    <property>
        <name>mapreduce.jobhistory.address</name>
        <value>centos103:10020</value>
    </property>
    <!-- 历史服务器web端地址 -->
    <property>
        <name>mapreduce.jobhistory.webapp.address</name>
        <value>centos103:19888</value>
    </property>
</configuration>
```

##### workers

- /opt/hadoop-3.2.2/etc/hadoop/workers 添加如下内容, 文件中不允许有空行

```xml
centos101
centos102
centos103
```

##### 集群时间同步

```



```

##### xsync 集群分发脚本

- 创建脚本 xsync.sh

```shell
#!/bin/bash
#1. 判断参数个数
if [ $# -lt 1 ]
then
	echo Not Enough Arguement!
	exit;
fi
#2. 遍历集群所有机器
for host in centos101 centos102 centos103
do
	echo ====================  $host  ====================
	#3. 遍历所有目录，挨个发送
	for file in $@
	do
		#4 判断文件是否存在
		if [ -e $file ]
		then
			#5. 获取父目录
			pdir=$(cd -P $(dirname $file); pwd)
			#6. 获取当前文件的名称
			fname=$(basename $file)
			ssh $host "mkdir -p $pdir"
			rsync -av $pdir/$fname $host:$pdir
		else
			echo $file does not exists!
		fi
	done
done
```

- 使用

```bash
# 修改权限
chmod +x xsync

# 将脚本移动到/bin中，以便全局调用
sudo mv xsync /bin/

# 测试脚本
sudo xsync /bin/xsync

# 使用
xsync /opt/a.txt
```

##### 查看集群 jps 脚本

```shell
#!/bin/bash
for i in centos101 centos102 centos103; do
	echo "========= $i =========="
	ssh $i "jps" | grep -v Jps
done
```

##### 集群启动方式1

> 需要配置好ssh

- 如果集群是第一次启动需要先格式化 NameNode (使用centos101 NN)
- 格式化之前，一定要先停止上次启动的所有namenode和datanode进程，然后再删除data和log数据

```bash
/opt/hadoop-3.2.2/sbin/stop-all.sh

# 集群中的所有机器都会启动

1. 格式化 (centos101配置了namenode的节点上运行)
hdfs namenode -format

2. 启动HDFS (centos101配置了namenode的节点上运行)
/opt/hadoop-3.2.2/sbin/start-dfs.sh

3. 在配置了ResourceManager的节点（centos102）启动YARN
/opt/hadoop-3.2.2/sbin/start-yarn.sh

5. 启动历史服务器 (centos103)
mapred --daemon start historyserver

6. 启动 Timelineserver (centos101)
yarn --daemon start timelineserver

```

##### 集群启动方式2

```bash
1. 各个服务组件逐一启动/停止
# 分别启动/停止HDFS组件
$ hdfs --daemon start/stop namenode/datanode/secondarynamenode
# 启动/停止YARN
$ yarn --daemon start/stop  resourcemanager/nodemanager
```

##### 集群状态查看

- 使用web

```
yarn的web管理界面
http://centos102:8088/cluster


hdfs的web管理页面
http://centos101:9870


查看日志
http://centos103:19888/jobhistory


Web端查看SecondaryNameNode(不好用)
http://centos103:9868/status.html


日志服务器地址
http://centos103:19888/jobhistory



```

- 使用命令

```
[gong@centos101 ~]$ hdfs fsck /
Connecting to namenode via http://centos101:9870/fsck?ugi=gong&path=%2F
FSCK started by gong (auth:SIMPLE) from /172.20.0.101 for path / at Sun May 30 02:45:08 UTC 2021


Status: HEALTHY //集群状态健康
 Number of data-nodes:	3 //集群有多少数据节点
 Number of racks:		1 //集群有多少机架
 Total dirs:			1 //集群有多少个目录
 Total symlinks:		0 //集群有多少链接

Replicated Blocks:
 Total size:	0 B //集群总共文件大小
 Total files:	0 //集群有多少个文件
 Total blocks (validated):	0  //多少个数据块  通过验证的有2块  平均块大小是27xxx
 Minimally replicated blocks:	0 //最少复制的块数
 Over-replicated blocks:	0 //超过预计复制数目的块有几个（比如说 多备份了1个副本）
 Under-replicated blocks:	0 // 少于预计复制数目的块有几个（比如说 3副本少备份了1个副本）
 Mis-replicated blocks:		0 //没备份的块有几个
 Default replication factor:	3 //备份因子为1  每个数据块给1个备份
 Average block replication:	0.0  //平均备份数目，1个备份
 Missing blocks:		0
 Corrupt blocks:		0
 Missing replicas:		0

Erasure Coded Block Groups:
 Total size:	0 B
 Total files:	0
 Total block groups (validated):	0
 Minimally erasure-coded block groups:	0
 Over-erasure-coded block groups:	0
 Under-erasure-coded block groups:	0
 Unsatisfactory placement block groups:	0
 Average block group size:	0.0
 Missing block groups:		0
 Corrupt block groups:		0
 Missing internal blocks:	0
FSCK ended at Sun May 30 02:45:08 UTC 2021 in 9 milliseconds


The filesystem under path '/' is HEALTHY
```

## mysql (二进制安装)

> 官网: https://dev.mysql.com/downloads/mysql/

##### 创建用户

```
groupadd mysql
useradd mysql -g mysql -s /sbin/nologin
```

#####  下载

```
选择最小安装
$ wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.25-linux-glibc2.17-x86_64-minimal.tar.xz
$ tar -Jxvf mysql-8.0.25-linux-glibc2.17-x86_64-minimal.tar.xz
$ cd mysql-8.0.25-linux-glibc2.17-x86_64-minimal
```

##### 创建文件修改该权限

```bash
$ mkdir data
$ mkdir 3306
$ chmod 755 -R data 
$ chmod 755 -R 3306 
$ sudo chown -R mysql:mysql data
$ sudo chown -R mysql:mysql 3306 
```

##### 设置配置文件

- 创建文件

  ```bash
  $ mkdir config && cd config
  ```

- config 下创建 my.cnf 文件

  ```
  [client]
  port = 3306
  socket = /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.sock
  default-character-set=utf8mb4
  
  [mysql]
  disable-auto-rehash #允许通过TAB键提示
  default-character-set = utf8mb4
  connect-timeout = 10
  socket = /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.sock
  
  [mysqld]
  user=mysql
  server-id = 3306
  port = 3306
  socket = /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.sock
  pid-file = /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.pid
  basedir = /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal
  datadir = /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/data
  #bind_address = 10.10.10.11
  autocommit = 1
  
  default_authentication_plugin=mysql_native_password
  character-set-server=utf8mb4
  explicit_defaults_for_timestamp=true
  lower_case_table_names=1
  back_log=103
  max_connections=10000
  max_connect_errors=100000
  table_open_cache=512
  external-locking=FALSE
  max_allowed_packet=32M
  sort_buffer_size=2M
  join_buffer_size=2M
  thread_cache_size=51
  transaction_isolation=READ-COMMITTED
  tmp_table_size=96M
  max_heap_table_size=96M
  
  
  #logs
  long_query_time = 10
  slow_query_log = 1
  slow_query_log_file=/opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/slow.log
  
  #log-warnings = 1
  log_error_verbosity=3
  
  log-error = /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.err
  log_output = FILE #参数log_output指定了慢查询输出的格式，默认为FILE，你可以将它设为TABLE，然后就可以查询mysql架构下的slow_log表了
  
  
  #log-queries-not-using-indexes
  #log-slow-slave-statements
  max_binlog_size = 1G
  #max_relay_log_size = 1G
  
  # replication
  log-bin=/opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql-bin
  #server-id=1
  #binlog_format= ROW
  #gtid_mode = on
  #enforce_gtid_consistency = 1
  #log_slave_updates   = 1
  #master-info-repository=TABLE
  #relay-log-info-repository=TABLE
  
  # innodb storage engine parameters
  innodb_buffer_pool_size=500M
  innodb_data_file_path=ibdata1:100M:autoextend:max:5G #redo
  innodb_temp_data_file_path = ibtemp1:100M:autoextend:max:10G
  #innodb_file_io_threads=4 #默认的是4
  innodb_log_buffer_size=16M
  innodb_log_file_size=256M #undo
  innodb_log_files_in_group=2
  innodb_lock_wait_timeout=50
  innodb_file_per_table=1 #独立表空间
  ```

##### 初始化

```
方式1: 使用配置文件, 文件中生成随机密码
$ bin/mysqld --defaults-file=config/my.cnf --user=mysql --initialize

密码在 3306/mysql.err 文件中
2021-06-21T07:58:23.251821Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: 2p<hp3:CHjXj


方式2: 参数 --initialize-insecure 设置空密码 (使用这个)
$ bin/mysqld --defaults-file=config/my.cnf --user=mysql --initialize-insecure 


方式3: 参数设置目录
$ bin/mysqld --user=mysql  --initialize --basedir=/opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal --datadir=/opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/data
```

##### 启动服务

```
$ /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/bin/mysqld_safe --defaults-file=/opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/config/my.cnf &
```

##### 首次登录修改密码

```
$ bin/mysql -uroot -S /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.sock

# 修改密码
alter user 'root'@'localhost' identified by '123456';
```

##### 登录

```
$ bin/mysql -uroot -S /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.sock -p
```

##### 允许外网访问

```
use mysql;
select host,user from user;
update user set host='%' where user='root';
flush privileges;
select host,user from user;
```

##### 使用中问题

- 问题: 初始化问题

  ```
  错误信息:
  ./mysqld: error while loading shared libraries: libaio.so.1: cannot open shared object file: No such file or directory
  
  解决办法:
  centos: yum install numactl
  ubuntu: aptitude install libaio1 libaio-dev
  ```
  
- 问题: mysql 启动问题

  ```
  错误信息:
  ./mysql: error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory
  
  解决办法:
  ubuntu
  aptitude install libncurses5
  ```
  
- 问题: 客户端服务链接mysql

  ```
  错误信息:
  ERROR 1045 (28000): Access denied for user 'glfadd'@'localhost' (using password: NO)
  
  解决办法:
  $ bin/mysql -uroot -S /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.sock
  ```

##### 生成软链接 (未使用)

```bash
$ cd /usr/local
$ ln -s /opt/mysql-8.0.20-linux-x86_64-minimal mysql
```

## Hive

> hive 元数据存储在 mysql 中, mysql 必须先运行

##### hive 安装

```bash
1. 下载解压到docker /opt目录下
$ wget https://mirrors.bfsu.edu.cn/apache/hive/hive-3.1.2/apache-hive-3.1.2-bin.tar.gz


2. 设置环境变量, 编辑 /etc/profile.d/my_env.sh 文件
export HIVE_HOME=/opt/apache-hive-3.1.2-bin
export PATH=$PATH:$HIVE_HOME/bin


3. 使配置生效
source /etc/profile


4. 解决日志Jar包冲突
$ mv $HIVE_HOME/lib/log4j-slf4j-impl-2.10.0.jar $HIVE_HOME/lib/log4j-slf4j-impl-2.10.0.jar.bak
```

##### hive 元数据配置到MySql

- 下载 MySQL 对应版本的 JDBC 

```bash
官网: https://dev.mysql.com/downloads/connector/j/
选择 "Platform Independent (Architecture Independent), Compressed TAR Archive"

$ wget https://cdn.mysql.com//Downloads/Connector-J/mysql-connector-java-8.0.25.tar.gz

将版本对应的JDBC驱动 mysql-connector-java-8.0.25.jar 拷贝到 $HIVE_HOME/lib 目录下
```

- 数据在hdfs中的存储位置

```bash
$ hdfs dfs -mkdir -p /usr/hive/warehouse
$ hdfs dfs -mkdir -p /usr/hive/tmp
$ hdfs dfs -mkdir -p /usr/hive/log
$ hdfs dfs -chmod g+w /usr/hive/warehouse
$ hdfs dfs -chmod g+w /usr/hive/tmp
$ hdfs dfs -chmod g+w /usr/hive/log
```

- 在 $HIVE_HOME/conf 目录下新建 hive-site.xml 文件

```xml
<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration> 
  <property> 
    <name>javax.jdo.option.ConnectionURL</name>  
    <value>jdbc:mysql://centos101:3306/metastore?useSSL=false</value> 
  </property>  
  <property> 
    <name>javax.jdo.option.ConnectionDriverName</name>  
    <value>com.mysql.jdbc.Driver</value> 
  </property>  
  <property> 
    <name>javax.jdo.option.ConnectionUserName</name>  
    <value>root</value> 
  </property>  
  <property> 
    <name>javax.jdo.option.ConnectionPassword</name>  
    <value>123456</value> 
  </property>  
  <property> 
    <name>hive.metastore.warehouse.dir</name>  
    <value>/usr/hive/warehouse</value> 
  </property>  
  <property> 
    <name>hive.metastore.schema.verification</name>  
    <value>false</value> 
  </property>  
  <property> 
    <name>hive.metastore.uris</name>  
    <value>thrift://centos101:9083</value> 
  </property>  
  <property> 
    <name>hive.server2.thrift.port</name>  
    <value>10000</value> 
  </property>  
  <property> 
    <name>hive.server2.thrift.bind.host</name>  
    <value>centos101</value> 
  </property>  
  <property> 
    <name>hive.metastore.event.db.notification.api.auth</name>  
    <value>false</value> 
  </property> 
</configuration>
```

## 安装 tez 引擎

> hive有三种引擎：mapreduce、spark、tez，默认引擎为MapReduce，但MapReduce的计算效率非常低，而Spark和Tez引擎效率高，公司一般会使用Spark或Tez作为hive的引擎。
>
> 官网: http://tez.apache.org/
> 下载地址: https://mirrors.bfsu.edu.cn/apache/tez/

##### 下载

```bash
1. 下载解压到 centos101
$ wget https://mirrors.bfsu.edu.cn/apache/tez/0.10.0/apache-tez-0.10.0-bin.tar.gz
$ tar zxvf apache-tez-0.10.0-bin.tar.gz

2. 上传到 hdfs 中
$ hadoop fs -mkdir /tez
$ hadoop fs -put /opt/apache-tez-0.10.0-bin.tar.gz /tez
```

##### tez-site.xml

> 新建 $HADOOP_HOME/etc/hadoop/tez-site.xml 文件

```xml
<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<configuration> 
  <!--指明hdfs集群上的tez的tar包，使Hadoop可以自动分布式缓存该jar包-->
  <property> 
    <name>tez.lib.uris</name>  
    <value>${fs.defaultFS}/tez/apache-tez-0.10.0-bin.tar.gz</value> 
  </property>  
  <property> 
    <name>tez.use.cluster.hadoop-libs</name>  
    <value>true</value> 
  </property>  
  <property> 
    <name>tez.am.resource.memory.mb</name>  
    <value>1024</value> 
  </property>  
  <property> 
    <name>tez.am.resource.cpu.vcores</name>  
    <value>1</value> 
  </property>  
  <property> 
    <name>tez.container.max.java.heap.fraction</name>  
    <value>0.4</value> 
  </property>  
  <property> 
    <name>tez.task.resource.memory.mb</name>  
    <value>1024</value> 
  </property>  
  <property> 
    <name>tez.task.resource.cpu.vcores</name>  
    <value>1</value> 
  </property> 
</configuration>
```

##### tez.sh

> 新建 $HADOOP_HOME/etc/hadoop/shellprofile.d/tez.sh 添加Tez的Jar包相关信息

```
hadoop_add_profile tez
function _tez_hadoop_classpath
{
    hadoop_add_classpath "$HADOOP_HOME/etc/hadoop" after
    hadoop_add_classpath "/opt/apache-tez-0.10.0-bin/*" after
    hadoop_add_classpath "/opt/apache-tez-0.10.0-bin/lib/*" after
}
```

##### hive-site.xml

> 修改Hive的计算引擎, 编辑 $HIVE_HOME/conf/hive-site.xml 添加

```xml
<property>
    <name>hive.execution.engine</name>
    <value>tez</value>
</property>
<property>
    <name>hive.tez.container.size</name>
    <value>1024</value>
</property>
```

##### 解决日志Jar包冲突

```
$ mv /opt/apache-tez-0.10.0-bin/lib/slf4j-log4j12-1.7.10.jar /opt/apache-tez-0.10.0-bin/lib/slf4j-log4j12-1.7.10.jar.bak
```

##### 初始化元数据库

```bash
1. 登陆MySQL


2. 新建Hive元数据库
mysql> create database metastore;
mysql> quit;


3. 初始化Hive元数据库
$ schematool -initSchema -dbType mysql -verbose
```

##### 设置 hive log

> 日志默认放在  /tmp/gong/hive.log

```
1. 创建日志目录 
$ mkdir logs


2. 备份文件
$ cp $HIVE_HOME/conf/hive-log4j2.properties.template $HIVE_HOME/conf/hive-log4j2.properties


3. 修改 $HIVE_HOME/conf/hive-log4j2.properties 设置目录
property.hive.log.dir = /opt/apache-hive-3.1.2-bin/logs
```

##### 启动

```bash
1. 启动metastore
nohup hive --service metastore > $HIVE_HOME/logs/metastore.log 2>&1 &


2. 启动hiveserver2
nohup hive --service hiveserver2 > $HIVE_HOME/logs/hiveServer2.log2>&1 &
```

##### 验证是否安装成功

```
验证hive 是否成功
hive --help

查看是否使用tez
hive> set hive.execution.engine;
hive.execution.engine=tez
```

##### beeline 客户端

> 可以自动补全命令

```bash
$ beeline -u jdbc:hive2://centos101:10000 -n gong


链接成功显示
Connecting to jdbc:hive2://centos101:10000
Connected to: Apache Hive (version 3.1.2)
Driver: Hive JDBC (version 3.1.2)
Transaction isolation: TRANSACTION_REPEATABLE_READ
Beeline version 3.1.2 by Apache Hive
0: jdbc:hive2://centos101:10000>
```

## tez ui

> https://blog.csdn.net/sinat_37690778/article/details/80594571
>
> https://www.jianshu.com/p/ed2675c10b94

##### 下载

```
1. 下载 tomcat
官网: https://tomcat.apache.org/download-10.cgi
$ wget https://downloads.apache.org/tomcat/tomcat-10/v10.0.7/bin/apache-tomcat-10.0.7.zip


2. 下载 tez-ui
官网: https://repository.apache.org/content/repositories/releases/org/apache/tez/tez-ui/
$ wget https://repository.apache.org/content/repositories/releases/org/apache/tez/tez-ui/0.10.0/tez-ui-0.10.0.war


3. 在 /opt/apache-tomcat-10.0.7/webapps 下新建tez目录
$ mkdir -p /opt/apache-tomcat-10.0.7/webapps/tez


4. 将 tez-ui 解压到该目录下
$ unzip tez-ui-0.9.2.war
```

##### configs.env

> 编辑 /opt/apache-tomcat-10.0.7/webapps/tez/config/configs.env 文件, 去掉下面两行的注释

```bash
timeline: "http://centos101:8188",
rm: "http://centos101:8088",
```

##### tez-site.xml

> 编辑 $HADOOP_HOME/etc/hadoop/tez-site.xml 文件, 添加如下内容

```xml
<property>
    <name>tez.history.logging.service.class</name>
    <value>org.apache.tez.dag.history.logging.ats.ATSHistoryLoggingService</value>
</property>
<property>
    <name>tez.tez-ui.history-url.base</name>
    <value>http://centos101:8880/tez-ui/</value>
</property>
```

##### 启动 (centos101)

```
1. 启动tomcat
# 修改权限
$ chmod +x -R /opt/apache-tomcat-10.0.7/bin
$ /opt/apache-tomcat-10.0.7/bin/startup.sh


访问界面
http://centos101:8080/tez
```

##### 切换 hive 的引擎(临时生效)

```
# hive 的引擎切换为 MapReduce
hive> set hive.execution.engine=mr;

# hive 的引擎切换为 tez
hive> set hive.execution.engine=tez;

# 查看 hive 引擎
hive> set hive.execution.engine;
```

##### 问题1: 启动时报错

```
报错信息:
Exception in thread "main" java.lang.NoSuchMethodError: com.google.common.base.Preconditions.checkArgument(ZLjava/lang/String;Ljava/lang/Object;)


原因:
是系统找不到相关jar包或同一类型的jar包有不同版本存在，系统无法决定使用哪一个。


解决办法:
删除hive中低版本的guava包，把hadoop里的复制到hive的lib目录下即可。


$ cd $HIVE_HOME/lib
$ mv guava-19.0.jar guava-19.0.jar.bak
$ cp $HADOOP_HOME/share/hadoop/common/lib/guava-27.0-jre.jar .
```











