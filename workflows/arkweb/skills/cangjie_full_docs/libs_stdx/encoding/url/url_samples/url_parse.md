# URL 解析函数 parse 的使用

使用 parse 函数解析 URL 字符串，生成 URL 对象。示例中对一个地址进行了解析并获得了 URL 对象，并且打印该对象的各个属性。

示例：

<!-- verify -->
```cangjie
import stdx.encoding.url.*

main(): Int64 {
    /* 调用 URL 静态函数 parse 解析网址获得名为 url 的对象 */
    var url = URL.parse(
        "http://www.example.com:80/path%E4%BB%93%E9%A2%89?key=value%E4%BB%93%E9%A2%89#%E4%BD%A0%E5%A5%BD")

    /* 打印 url 的组件属性 */
    println("url.scheme = ${url.scheme}")
    println("url.opaque = ${url.opaque}")
    println("url.userInfo = ${url.userInfo}")
    println("url.rawUserInfo = ${url.rawUserInfo}")
    println("url.host = ${url.host}")
    println("url.hostName = ${url.hostName}")
    println("url.port = ${url.port}")
    println("url.path = ${url.path}")
    println("url.rawPath = ${url.rawPath}")
    println("url.query = ${url.query.getOrThrow()}")
    println("url.rawQuery = ${url.rawQuery.getOrThrow()}")
    println("url.fragment = ${url.fragment.getOrThrow()}")
    println("url.rawfragment = ${url.rawFragment.getOrThrow()}")
    println("url = ${url}")
    return 0
}
```

运行结果：

```text
url.scheme = http
url.opaque = 
url.userInfo = 
url.rawUserInfo = 
url.host = www.example.com:80
url.hostName = www.example.com
url.port = 80
url.path = /path仓颉
url.rawPath = /path%E4%BB%93%E9%A2%89
url.query = key=value仓颉
url.rawQuery = key=value%E4%BB%93%E9%A2%89
url.fragment = 你好
url.rawfragment = %E4%BD%A0%E5%A5%BD
url = http://www.example.com:80/path%E4%BB%93%E9%A2%89?key=value%E4%BB%93%E9%A2%89#%E4%BD%A0%E5%A5%BD
```
