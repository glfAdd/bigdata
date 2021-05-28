##### docker 参数说明

```
-d 后台启动

--hostname 指定主机名字
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
# yum install -y vim net-tools passwd
```

##### 安装 ssh 服务

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

##### 设置每个集群的 hosts 文件

```
172.20.0.101 centos101
172.20.0.102 centos102
172.20.0.103 centos103
```

##### docker创建快照

```

```

##### docker引用快照

```

```

##### 安装 jdk 8 和 hadoop

```
1. 官网 https://www.oracle.com/java/technologies/javase-downloads.html 下载 jdk-8u291-linux-x64.tar.gz


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


5. 是配置生效
source /etc/profile


6. 验证
java -version
hadoop version
```

##### hadoop目录

```
bin目录：存放对Hadoop相关服务（HDFS,YARN）进行操作的脚本
etc目录：Hadoop的配置文件目录，存放Hadoop的配置文件
lib目录：存放Hadoop的本地库（对数据进行压缩解压缩功能）
sbin目录：存放启动或停止Hadoop相关服务的脚本
share目录：存放Hadoop的依赖jar包、文档、和官方案例
```

