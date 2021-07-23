import org.apache.hadoop.conf.Configuration;
// 通用文件系统 api,
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;


public class HandleFile {

    public static void main(String[] args) throws Exception {
        URI uri = new URI("hdfs://centos101:8020");
        // Configuration 封装了服务器或客户端的配置, 通过路径指定配置文件, 如 etc/hadoop/core-site.xml
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(uri, conf, "gong");

        // 上传文件
        InputStream in = new FileInputStream("/home/glfadd/Desktop/logs/aaaaaa.log");
        OutputStream out = fs.create(new Path("/java_test/aaaaaa.log"));
        IOUtils.copyBytes(in, out, 4096, true);

//        // 删除文件
//        path = new Path("hdfs://centos101:80");
//        Boolean flag = fs.delete();


    }
}
