##### 安装 4.0.0

```
可能版本太高, 失败
```

##### 安装 3.90.00

```bash
# 0. 参考
github: https://github.com/azkaban/azkaban/releases
文档: https://azkaban.github.io/azkaban/docs/latest/


# 1. 下载
$ wget https://codeload.github.com/azkaban/azkaban/zip/refs/tags/3.90.0


# 2. 修改使用的 maven 的源(可选)
编辑 build.gradle 文件, 将所有的 repositories 
maven {
	url 'https://plugins.gradle.org/m2/'
}
改为
maven {
	url 'http://maven.aliyun.com/nexus/content/groups/public/'
}
如果没有就添加(第一个 repositories 修改, 第二个 repositories 添加)


# 3.编译
$ ./gradlew distTar


# 4. /opt 下创建 azkaban


# 5. 拷贝目录
$ cp -r azkaban-*/build/distributions/* /opt/azkaban


# 6. 批量解压
$ ls *.tar.gz | xargs -n1 tar xzvf
```

##### 核心文件

```
├── azkaban-db # 创建库 sql
├── azkaban-exec-server # 进程任务处理
├── azkaban-solo-server # 单机模式运行
├── azkaban-web-server # web页面
```

##### mysql 设置

- 启动 mysql

  ```bash
  $ /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/bin/mysqld_safe --defaults-file=/opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/config/my.cnf &
  
  $ /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/bin/mysql -uroot -S /opt/mysql-8.0.25-linux-glibc2.17-x86_64-minimal/3306/mysql.sock -p
  ```

- myslq 创建库和表

  ```mysql
  -- 创建数据库
  create database azkaban;
  
  -- 使用库
  use azkaban;
  
  -- 从文件创建表
  source /opt/azkaban/azkaban-db-0.1.0-SNAPSHOT/create-all-sql-0.1.0-SNAPSHOT.sql;
  ```
  
- 修改 mysql 驱动

  ```bash
  # 0. 查看 mysql 驱动的版本和使用的数据库是否匹配, 如果不匹配下载
  https://mvnrepository.com/artifact/mysql/mysql-connector-java
  
  # 1. 数据库版本 mysql-8.0.25 , 下载对应 jar 文件, mysql-connector-java-8.0.25.jar
  
  # 3. 分别复制到 /opt/azkaban/azkaban-web-server-0.1.0-SNAPSHOT 和 /opt/azkaban/azkaban-exec-server-0.1.0-SNAPSHOT 删除版本不对的 mysql-connector-java 文件
  ```

##### exec 设置

```
/opt/azkaban/azkaban-exec-server-0.1.0-SNAPSHOT/conf/azkaban.properties

# 1. 修改 mysql 
mysql.user=root
mysql.password=123456
```

##### ssl 设置(未设置)

```
进入ssl文件夹：
cd /home/xindaqi/software/install/azkaban4/ssl

创建ssl
keytool -keystore keystore -alias jetty -genkey -keyalg RSA
```

##### web 设置

- /opt/azkaban/azkaban-web-server-0.1.0-SNAPSHOT/conf/azkaban.properties

  ```
  # 1. 修改 mysql 
  mysql.user=root
  mysql.password=123456
  ```

- /opt/azkaban/azkaban-web-server-3.91.0-207-g5f4b01d1/conf/azkaban-users.xml

  ```
  设置用户
  ```

##### 运行

- 启动 azkaban-exec-server

  ```
  # 启动executorServer时会将executorServer的host，port同步到mysql的executors表中
  
  /opt/azkaban/azkaban-exec-server-0.1.0-SNAPSHOT && ./bin/start-exec.sh
  ```

- 激活 executor

  ```bash
  # 1. 在数据库 azkaban.executors 表查看 port, 端口会一直变
  
  # 2. api 激活 azkaban.executors
  curl http://localhost:40409/executor?action=getStatus
  curl http://localhost:40409/executor?action=activate
  ```

- 启动 azkaban-web-server

  ```
  /opt/azkaban/azkaban-web-server-0.1.0-SNAPSHOT && ./bin/start-web.sh 
  ```

##### web UI

```
http://localhost:8081/

用户名/密码：azkaban/azkaban
```

##### 查看日志

```
/opt/azkaban/azkaban-exec-server-0.1.0-SNAPSHOT/logs
/opt/azkaban/azkaban-web-server-0.1.0-SNAPSHOT/logs
```

##### 问题1

```
问题:
azkaban-exec-server 启动以后 mysql 没有数据写入


原因:
azkaban-exec-server 和 azkaban-web-server 使用 mysql*.jar 包和数据库的版本不一致


解决办法:
1. 在 https://mvnrepository.com/artifact/mysql/mysql-connector-java 下载 jar 包
2. 分别复制到 /opt/azkaban/azkaban-web-server-0.1.0-SNAPSHOT 和 /opt/azkaban/azkaban-exec-server-0.1.0-SNAPSHOT 删除版本不对的 mysql-connector-java 文件
```

##### 问题2

```
问题: 
所有的任务都执行失败


原因:
启动服务时没有激活 executor


解决办法:
使用 api 激活
```







