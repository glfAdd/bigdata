package com.glfadd.hdfs;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.net.URI;

public class HDFSClient {
    FileSystem file;

    @Before
    public void before() throws IOException, InterruptedException {
        System.out.println("before");
        // 设置属性
        Configuration config = new Configuration();
        // 分区个数2个
        config.set("dfs.replication", "2");


        // 1. 新建HDFS对象
        file = FileSystem.get(URI.create("hdfs://centos101:8020"), config, "gong");
    }

    @Test
    public void Test() throws IOException, InterruptedException {
        System.out.println("test");
        // 2. 操作集群
        file.copyFromLocalFile(new Path("/home/glfadd/Desktop/需要看得2"), new Path("/"));

        // 3. 关闭资源
        file.close();
    }

    @After
    public void after() throws IOException {
        System.out.println("after");
        file.close();
    }
}
