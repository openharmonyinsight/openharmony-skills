目前无法判定 API 12 文档有错。`materials/` 目录为空，题面仅提供：

- API 12 文档：`open(path: string): number`
- API 13 SDK：`open(path: string): Promise<number>`

两者属于不同版本，签名差异只能说明所提供的返回类型不一致，不能据此认定 API 12 文档错误，也不能直接将其改为 `Promise<number>`。

需要取得同一接口的 API 12 SDK 声明、对应版本源码或官方版本变更记录，再核对。当前结论应为：**证据不足，API 12 文档是否有误尚待核实。**
