##### 执行 sql 语句方式

- 直接执行语句

  ```bash
  # 进入 hive 交互模式
  $ hive
  
  
  # 查hdfs目录
  > show databases;
  > use default;
  > dfs -ls /;
  
  
  # 退出交互模式
  > exit;
  或
  > quit;
  或
  ctrl + C
  ```

- -e 不进入hive的交互窗口执行sql语句

  ```
  $ hive -e "show databases;"
  ```

- -f 执行脚本中sql语句

  ```bash
  1. 创建hivef.sql文件, 文件中写入正确的sql语句
  show databases;
  
  
  2. 执行文件中的sql语句
  $ hive -f hivef.sql
  
  
  3. 执行文件中的sql语句并将结果写入文件中
  $ hive -f hivef.sql  > aaa.txt
  ```

##### 查看 hive 执行命令历史

```
在 ~/.hivehistory 文件内
```

##### 查看当前所有配置信息

```
> set;
```

##### hive 设置方式

- 优先级

  ```
  配置文件 < 命令行参数 < 参数声明
  
  注意: 某些系统级的参数，例如log4j相关的设定，必须用前两种方式设定，因为那些参数的读取在会话建立以前已经完成了。
  ```

- 配置文件

  ```
  1. 默认配置文件：hive-default.xml 
  2. 用户自定义配置文件：hive-site.xml
  3. 用户自定义配置会覆盖默认配置。
  4. Hive也会读入Hadoop的配置，因为Hive是作为Hadoop的客户端启动的，Hive的配置会覆盖Hadoop的配置
  5. 配置文件的设定对本机启动的所有Hive进程都有效。
  ```

- 命令行参数(仅对本次hive启动有效)

  ```
  启动Hive时，可以在命令行添加 -hiveconf param=value 来设定参数
  
  $ bin/hive -hiveconf mapred.reduce.tasks=10;
  
  查看参数设置：
  hive (default)> set mapred.reduce.tasks;
  ```

- 参数声明(仅对本次hive启动有效)

  ```
  可以在HQL中使用SET关键字设定参数
  
  
  hive (default)> set mapred.reduce.tasks=100;
  hive (default)> set mapred.reduce.tasks;
  ```

##### 简单使用

- 写入的数据结构类似

  ```json
  {
  	"name": "songsong",
  	"friends": ["bingbing", "lili"],
  	"children": {
  		"xiao song": 18,
  		"xiaoxiao song": 19
  	},
  	"address": {
  		"street": "hui long guan",
  		"city": "beijing"
  	}
  }
  ```

- 基于结构, 将数据写入 /home/gong/hive_test.txt 文件

  ```
  songsong,bingbing_lili,xiao song:18_xiaoxiao song:19,hui long guan_beijing
  yangyang,caicai_susu,xiao yang:18_xiaoxiao yang:19,chao yang_beijing
  ```

- hive 中创建表

  > 在 /usr/hive/warehouse 下创建数据库文件

  ```
  create table test(
  name string,
  friends array<string>,
  children map<string, int>,
  address struct<street:string, city:string>
  )
  -- 列分隔符
  row format delimited fields terminated by ','
  --MAP STRUCT 和 ARRAY 的分隔符(数据分割符号)
  collection items terminated by '_'
  -- MAP中的key与value的分隔符
  map keys terminated by ':'
  -- 行分隔符
  lines terminated by '\n';
  ```

- 导入数据

  ```
  load data local inpath '/home/gong/hive_test.txt' into table test; 
  ```

- 访问数据

  ```
  select friends[1],children['xiao song'],address.city from test
  where name="songsong";
  ```

##### 查看数据库

```
desc database g_test;
desc database extended g_test;
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+
| db_name  | comment  |                      location                      | owner_name  | owner_type  | parameters  |
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+
| g_test   |          | hdfs://centos101:8020/usr/hive/warehouse/g_test.db | gong        | USER        |             |
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+

```









