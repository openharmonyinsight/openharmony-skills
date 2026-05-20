# 函数

## func handleError(HttpContext, UInt16)

```cangjie
public func handleError(ctx: HttpContext, code: UInt16): Unit
```

功能：便捷的 Http 请求处理函数，用于回复错误请求。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - Http 请求上下文。
- code: UInt16 - Http 响应码。

## func notFound(HttpContext)

```cangjie
public func notFound(ctx: HttpContext): Unit
```

功能：便捷的 Http 请求处理函数，用于回复 404 响应。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - Http 请求上下文。

## func upgrade(HttpContext)

```cangjie
public func upgrade(ctx: HttpContext): StreamingSocket
```

功能：在 handler 内获取 StreamingSocket，可用于支持协议升级和处理 CONNECT 请求。

> - 调用该函数时，将首先根据 ctx.responseBuilder 发送响应，仅发送状态码和响应头。
> - 调用该函数时，将把 ctx.request.body 置空，后续无法通过 body.read(...) 读数据，未读完的 body 数据将留存在返回的 StreamingSocket 中。

参数：

- ctx: [HttpContext](http_package_classes.md#class-httpcontext) - 请求上下文。

返回值：

- StreamingSocket - 底层连接（对于 HTTP/2 是一个 stream），可用于后续读写。

异常：

- [HttpException](http_package_exceptions.md#class-httpexception) - 获取底层连接（对于 HTTP/2 是一个 stream）失败。
