##### Maven jar 管理网站

```
https://mvnrepository.com/
```

##### Maven仓库分类

```
（1）本地仓库：Maven配置文件中指向的仓库目录，为当前电脑的所有maven工程服务。
（2）远程仓库：
　　　　公司私服：搭建在公司局域网中，为局域网范围内的所有maven工程服务。
　　　　中央仓库：搭建在Internet上，为全世界范围内的maven工程服务。
　　　　中央仓库镜像：为了分担中央仓库的压力，给访问分流，提升访问效率，比如阿里镜像、华为镜像。
（3）仓库保存的东西是什么？
　　　　保存maven执行构建命令时所需要的插件。
　　　　保存三方库（一方库指JDK，二方库指开发人员）框架或工具的jar包。
　　　　保存自己开发的maven工程。
　　　　即仓库保存的就是各种jar包。
　　　　
1. maven使用本地仓库存储的jar,所有项目都会公用仓库中的同一分jar
2. 会自动引入所需的兼容版本jar
```

##### 安装 - linux

- 下载

```bash
官网下载地址: https://maven.apache.org/download.cgi

$ wget https://mirrors.bfsu.edu.cn/apache/maven/maven-3/3.8.1/binaries/apache-maven-3.8.1-bin.tar.gz
$ tar zxvf apache-maven-3.8.1-bin.tar.gz -C /opt
```

- 创建本地仓库存储目录

```
1. 在 /opt/apache-maven-3.8.1 下创建目录ck

2. 修改该 settings.xml 文件
```

- 修改环境变量

```
1. 编辑/创建 /etc/profile.d/my_env.sh 文件, 添加
export MAVEN_HOME=/opt/apache-maven-3.8.1
export PATH=${MAVEN_HOME}/bin:${PATH}

2. 使环境变量立刻生效
source /etc/profile
```

- 修改该 maven 配置文件 /opt/apache-maven-3.8.1/conf/settings.xml

```xml
设置 mirror
<mirrors>
  <mirror>
    <id>nexus-aliyun</id>
    <mirrorOf>*,!jeecg,!jeecg-snapshots</mirrorOf>
    <name>Nexus aliyun</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
    </mirror>
</mirrors>



设置本地仓库存储目录
<localRepository>/opt/apache-maven-3.8.1/ck</localRepository>
```

- 验证安装, 检测配置是否有问题

```bash
mvn –v
或
mvn -version
```

##### 安装 windws

```
# 1. 下载 apache-maven-3.8.5-bin.zip

# 2. 设置环境变量
	新建系统变量：MAVEN_HOME，复制Maven的路径
	在系统变量：Path中复制粘贴：%MAVEN_HOME%\bin
```

![maven1](.\image\maven1.png)

![maven2](.\image\maven2.png)

## idea创建新项目

##### 创建标准的 maven 工程

```
new -> project -> 选择"Maven" -> next -> 设置name, Location, GroupID 等
```

##### 工程目录

```
├── pom.xml
└── src
    ├── main
    │   ├── java
    │   └── resources
    └── test
        └── java
```



| 目录      | 说明                           |
| --------- | ------------------------------ |
| src       | 源码                           |
| target    | 编译、打包后的文件             |
| pom.xml   | maven核心配置文件              |
| main      | 存放主程序                     |
| test      | 存放测试程序                   |
| class     | 编译的字节码文件               |
| java      | 存放java源文件                 |
| resources | 存放框架或者其他工具的配置文件 |

##### 修改项目 maven 的配置

- 使用Maven管理项目时，项目依赖的jar包将不再包含在项目内，默认情况下集中放置在用户目录下的.m2文件夹下

```
Build, Execution, Deployment -> Build Tools -> Maven

修改如下地方
Maven home directory: maven 解压后的目录
User settings file: 配置文件settings.xml路径
Local repository: 本地仓库路径
```

##### maven命令

```
mvn clean;			清理字节码文件
mvn compile; 		编译主程序文件
mvn test-compile;	编译测试程序
mvn test;  			执行测试junit
mvn package;  		将项目打包成jar包或者war包
mvn install;  		安装maven工程到本地仓库
mvn site;  			生成站点
```

## pom文件说明

##### 依赖解析过程

- 即解析 dependency 标签的内容时，会首先从本地仓库进行查找被依赖的jar包，没有则从远程仓库中找到被依赖的jar包，下载一份到本地仓库中
- 针对自己开发的Maven工程，进入含有pom.xml所在的目录，执行 mvn install命令后，可以将自己开发的Maven工程安装到本地仓库中 。

##### 使用GAV三个值唯一定位一个maven工程

- groupId: 组织的唯一标识，一般是公司域名(一级域名.二级域名.三级域名.四级域名.项目名) 
- artifactId: 项目的唯一标识 ,一般为模块名
- version: 项目的版本

```xml
<groupId>junit</groupId>
<artifactId>junit</artifactId>
<version>4.12</version>
会对应到本地仓库中：
junit\junit\4.12\junit-4.12.jar
即 groupId\artifactId\version\artifactId-version.jar


<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-web</artifactId>
<version>2.3.8.RELEASE</version>
会对应到本地仓库中：
org\springframework\boot\spring-boot-starter-web\2.3.8.RELEASE\spring-boot-starter-web-2.3.8.RELEASE.jar
```

##### 依赖的作用域 scope 标签 

- compile作用域的依赖：默认的依赖作用范围，开发时需要，部署时也需要（运行时servlet容器不会提供），一般的就是这样。
- test作用域的依赖：主程序（main）是无法依赖test范围的jar的，开发时就不可以使用（那些jar主程序也是用不到的，主要是测试框架），只有测试程序可以依赖。要知道，测试程序常规是不参与打包的，test范围的依赖也不参与打包，只是在开发阶段会用到，或者maven编译（compile）时会执行测试程序。
  如果开发时主程序可以依赖test范围的jar，那么打包时由于test范围的jar不参与打包，所以打成的包运行时肯定就会报错。
- provided作用域的依赖：开发时，由于没有运行时环境，有些jar我们需要暂时依赖（不依赖有些方法就会找不到，用不了），但是项目打包部署运行时，由于运行时环境（servlet容器，比如：tomcat）会提供一些jar包，所以开发时那些暂时依赖的jar包就不能参与打包了，否则会发生冲突导致报错。

|  作用域  | 对主程序是否有效 | 对测试程序有效 | 是否参与打包（部署） |    典型例子     |
| :------: | :--------------: | :------------: | :------------------: | :-------------: |
| compile  |       有效       |      有效      |         参与         |   spring-core   |
|   test   |       无效       |      有效      |        不参与        |      junit      |
| provided |       有效       |      有效      |        不参与        | servlet-api.jar |

##### 依赖的传递性

- 当一个模块工程A在pom.xml中配置了相关依赖信息，则其他模块工程B使用这个模块工程A时，不需要再额外的配置依赖的信息了，其会从A中传递到B中。
- 只有compile与runtime范围的依赖才能进行传递。test、provided、system范围的依赖需要在每个工程中手动配置
- 传递依赖的原则
  - 作用：解决多个模块工程间的jar包冲突问题。
    - 传递依赖发生时，优先选择距离(指引用jar包的深度更浅的)该工程最近的jar包。
    - 路径相同时，先声明(上下位置关系在上面的)的先。即标签先声明的jar包被使用。
    - 非传递依赖时（即直接依赖），以最后的标签声明的jar包为主。

##### 依赖的删除 exclusion 标签

- 删除不希望出现的jar包

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-web</artifactId>
        <version>5.1.8.RELEASE</version>
        <scope>compile</scope>
        <exclusions>
            <exclusion>
                <groupId>org.springframework</groupId>
                <artifactId>spring-jcl</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
</dependencies>
```

##### 统一管理jar包的版本号

- 可以使引用这个变量的所有jar包的版本快速修改
- 使用标签，并自定义标签来声明版本号
- 在标签中，使用${自定义标签名}来引用

```xml
<properties>
    <jar.version>5.1.7.RELEASE</jar.version>
</properties>
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-web</artifactId>
        <version>${jar.version}</version>
    </dependency>
</dependencies>
```

## 依赖继承

##### 作用

- 对于非compile范围作用域范围的依赖，由于不能进行依赖传递，所以需要在每个模块工程中单独定义，可能造成各个模块工程间的jar版本不一致。所以需要使用一个父工程，并定义好管理这些依赖的信息，令每个模块继承父工程，即可获得非compile范围的依赖信息。对依赖版本修改时，只需修改父工程即可
- 每个子工程中相关的非compile范围的依赖仍需写，只是不需要再写版本号了。由父工程统一管理版本号
- 使用继承后，在执行maven安装工程的命令时（maven install），必须先安装父工程，再安装子工程。若直接安装子工程，会由于没有找不到依赖的版本号而报错

##### 创建

```
创建一个父工程，并添加相关的非compile范围的依赖

由于父工程一般只起到聚合子工程的作用，并无java代码，所以父工程创建时的打包方式需要选择 <packaging>pom</packaging>, POM是最简单的打包类型
```

## 标签说明

```xml
<project xmlns = "http://maven.apache.org/POM/4.0.0"
    xmlns:xsi = "http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation = "http://maven.apache.org/POM/4.0.0
    http://maven.apache.org/xsd/maven-4.0.0.xsd">
 
    <!-- 模型版本 -->
    <modelVersion>4.0.0</modelVersion>
    <!-- 公司或者组织的唯一标志，并且配置时生成的路径也是由此生成， 如com.companyname.project-group，maven会将该项目打成的jar包放本地路径：/com/companyname/project-group -->
    <groupId>com.companyname.project-group</groupId>
 
    <!-- 项目的唯一ID，一个groupId下面可能多个项目，就是靠artifactId来区分的 -->
    <artifactId>project</artifactId>
 
    <!-- 工程的版本号. 在 artifact 的仓库中，它用来区分不同的版本 -->
    <version>1.0</version>
</project>
```

