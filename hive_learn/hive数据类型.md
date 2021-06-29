##### 基本数据类型

- Hive的String类型相当于数据库的varchar类型，该类型是一个可变的字符串，不过它不能声明其中最多能存储多少个字符，理论上它可以存储2GB的字符数

| Hive数据类型 | Java数据类型 | 长度                                               | 例子           |
| ------------ | ------------ | -------------------------------------------------- | -------------- |
| TINYINT      | byte         | 1byte有符号整数                                    | 20             |
| SMALINT      | short        | 2byte有符号整数                                    | 20             |
| INT          | int          | 4byte有符号整数                                    | 20             |
| BIGINT       | long         | 8byte有符号整数                                    | 20             |
| BOOLEAN      | boolean      | 布尔类型，true或者false                            | TRUE  FALSE    |
| FLOAT        | float        | 单精度浮点数                                       | 3.14159        |
| DOUBLE       | double       | 双精度浮点数                                       | 3.14159        |
| STRING       | string       | 字符系列。可以指定字符集。可以使用单引号或者双引号 | 'hello' "word" |
| TIMESTAMP    |              | 时间类型                                           |                |
| BINARY       |              | 字节数组                                           |                |

##### 集合数据类型

- Hive有三种复杂数据类型ARRAY、MAP 和 STRUCT。ARRAY和MAP与Java中的Array和Map类似，而STRUCT与C语言中的Struct类似，它封装了一个命名字段集合，复杂数据类型允许任意层次的嵌套。

| 数据类型 | 描述                                                         |
| -------- | ------------------------------------------------------------ |
| STRUCT   | 和c语言中的struct类似，都可以通过“点”符号访问元素内容。例如，如果某个列的数据类型是STRUCT{first 		STRING, last STRING},那么第1个元素可以通过字段.first来引用。 |
| MAP      | MAP是一组键-值对元组集合，使用数组表示法可以访问数据。例如，如果某个列的数据类型是MAP，其中键->值对是’first’->’John’和’last’->’Doe’，那么可以通过字段名[‘last’]获取最后一个元素 |
| ARRAY    | 数组是一组具有相同类型和名称的变量的集合。这些变量称为数组的元素，每个数组元素都有一个编号，编号从零开始。例如，数组值为[‘John’, 		‘Doe’]，那么第2个元素可以通过数组名[1]进行引用。 |

##### 类型转换

- 隐式类型转换规则

  ```
  1. 任何整数类型都可以隐式地转换为一个范围更广的类型，如TINYINT可以转换成INT，INT可以转换成BIGINT。
  2. 所有整数类型、FLOAT和STRING类型都可以隐式地转换成DOUBLE。
  3. TINYINT、SMALLINT、INT都可以转换为FLOAT。
  4. BOOLEAN类型不可以转换为任何其它的类型。
  ```

- 使用CAST操作显示进行数据类型转换

  ```
  CAST('1' AS INT)将把字符串'1' 转换成整数1
  如果强制类型转换失败，如执行CAST('X' AS INT)，表达式返回空值 NULL
  
  0: jdbc:hive2://hadoop102:10000> select '1'+2, cast('1'as int) + 2;
  +------+------+--+
  | _c0  | _c1  |
  +------+------+--+
  | 3.0  | 3    |
  +------+------+--+
  ```

##### 数据库操作

> 创建数据库文件在 /usr/hive/warehouse 目录下

| 命令                                   | 说明                         |
| -------------------------------------- | ---------------------------- |
| show databases;                        | 显示数据库                   |
| show databases like 'db_hive*';        | 过滤显示查询的数据库         |
| desc database db_hive;                 | 显示数据库信息               |
| desc database extended db_hive;        | 显示数据库详细信息，extended |
| use db_hive;                           |                              |
| drop database db_hive2;                |                              |
| drop database if exists db_hive2;      |                              |
| create database if not exists db_hive; |                              |

##### 表操作

```
CREATE [EXTERNAL] TABLE [IF NOT EXISTS] table_name 
[(col_name data_type [COMMENT col_comment], ...)] 
[COMMENT table_comment] 
[PARTITIONED BY (col_name data_type [COMMENT col_comment], ...)] 
[CLUSTERED BY (col_name, col_name, ...) 
[SORTED BY (col_name [ASC|DESC], ...)] INTO num_buckets BUCKETS] 
[ROW FORMAT row_format] 
[STORED AS file_format] 
[LOCATION hdfs_path]
[TBLPROPERTIES (property_name=property_value, ...)]
[AS select_statement]
```





| 命令 | 说明 |
| ---- | ---- |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |
|      |      |







































































