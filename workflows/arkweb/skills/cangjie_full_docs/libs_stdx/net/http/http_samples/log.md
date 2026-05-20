# log

示例：

<!-- compile -->
```cangjie
import stdx.log.*
import stdx.net.http.*

main() {
    // 1. 构建 Server 实例
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()
    // 2. 注册 HttpRequestHandler
    server.distributor.register("/index", {
        httpContext => httpContext.responseBuilder.body("Hello 仓颉!")
    })
    // 3. 开启日志
    server.logger.level = LogLevel.DEBUG
    // client 端通过 client.logger.level = DEBUG 开启
    // 4. 启动服务
    server.serve()
}
```

运行结果：

```text
2025-05-24T23:55:12.779407244+08:00 DEBUG [thread#1] [Server#serve] bindAndListen(127.0.0.1, 8080)
```
