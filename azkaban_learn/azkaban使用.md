##### 创建 project

##### 创建 job (flow 1.0 将弃用)

> 就是一个 .job 的文件

- test_1.job(没有依赖)

  ```
  type=command
  command=echo 'test_1'
  ```

- test_2.job(有依赖)

  ```
  type=command
  command=echo 'test_2'
  dependencies=test_1
  ```

- test_3.job

  ```
  type=command
  command=echo 'test_3'
  ```

##### 创建 job (flow 2.0 推荐)

>  flow 文件, 使用 YAML 格式
>
> 可以在一个流程中定义多个 job, job 支持嵌套



```
curl http://localhost:8081/executor?action=activate


```



```
nodes:
  - name: jobA
    type: command
    config:
      command: echo "Hello Azkaban Flow 2.0."
```





##### 打包成 .zip

```
zip aaa.zip test_1.job test_2.job 
```

##### 上传

