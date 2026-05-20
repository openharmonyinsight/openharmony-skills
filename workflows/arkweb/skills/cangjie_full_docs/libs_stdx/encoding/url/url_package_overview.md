# stdx.encoding.url

## 功能介绍

url 包提供了 URL 相关的能力，包括解析 URL 的各个组件，对 URL 进行编解码，合并 URL 或路径等。

URL（Uniform Resource Locator）是统一资源定位符的缩写，它是用来标识互联网上资源位置的一种地址。通常包含协议、主机名、路径和查询参数等信息，其中协议是指访问资源所使用的协议（如 HTTP、FTP 等），主机名是指资源所在的服务器的域名或 IP 地址，路径是指资源所在的具体位置，查询参数是指用于传递参数的字符串。URL 是互联网上标识资源的唯一方式，通过 URL 可以访问网页、图片、视频等各种类型的资源。

URL 一般是以下格式：

```text
scheme://host[:port]/path[?query][#fragment]
```

其中：

- `scheme`：协议，例如 `http`、`https`、`ftp` 等；
- `host`：主机名或 IP 地址；
- `port`：端口号，可选，默认为协议默认端口；
- `path`：资源路径，例如 `/index.html`、`/blog/post/123` 等；
- `query`：查询参数，例如 `?page=2&sort=desc` 等，可选；
- `fragment`：文档片段标识符，例如 `#section-1`，可选。

例如，网址 `https://www.example.com/blog/post/123?page=2&sort=desc#section-1` 的 URL 格式为：

- scheme: https
- host: `www.example.com`
- path: /blog/post/123
- query: ?page=2&sort=desc
- fragment: #section-1

URL 编码的原因和基本过程：

URL 编码是将 URL 中的非 ASCII 字符转换为一种可读性更好的 ASCII 字符的过程。这是因为 URL 中只允许包含 ASCII 字符，而非 ASCII 字符可能会导致 URL 解析错误或传输失败。

URL 编码的基本过程如下：

1. 将 URL 字符串转换为字节数组。
2. 对于每个非 `ASCII` 字符，将其转换为 `UTF-8` 编码的字节序列。
3. 对于每个字节，将其转换为两个十六进制数字。
4. 在每个十六进制数字前添加一个百分号（%）。
5. 将所有编码后的字符连接起来形成编码后的 URL 字符串。

例如，将字符串“你好，世界！”进行 URL 编码，结果为“%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81”。

## API 列表

### 类

|                 类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [Form](./url_package_api/url_package_classes.md#class-form) | Form 以 key-value 键值对形式存储 http 请求的参数，同一个 key 可以对应多个 value，value 以数组形式存储。   |
| [URL](./url_package_api/url_package_classes.md#class-url) |该类提供解析 URL 的函数以及其他相关函数。  |
| [UserInfo](./url_package_api/url_package_classes.md#class-userinfo) |UserInfo 表示 URL 中用户名和密码信息。  |

### 异常类

|                 异常类名              |                功能                 |
| --------------------------------- | ---------------------------------- |
| [UrlSyntaxException](./url_package_api/url_package_exceptions.md#class-urlsyntaxexception) | url 解析异常类。 |
