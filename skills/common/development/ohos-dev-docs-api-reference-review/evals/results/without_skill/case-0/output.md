materials/ 为空，以下根据题面提供的文档内容和匹配版本 SDK 核对：

| 文档位置 | 问题 | 应修改为 |
|---|---|---|
| 第 7 行 | “从 API 10 支持”与 `@since 12` 不符 | 从 API 12 开始支持 |
| 第 9 行 | 参数顺序和返回类型错误，且缺少可选标记 | `open(path: string, flags?: number): number` |
| 第 10 行 | “flags 必填”与 `flags?` 不符 | flags 为可选参数，类型为 number |

正确声明：

```ts
/** @since 12 */
export function open(path: string, flags?: number): number;
```

SDK 声明未提供 flags 的默认值，文档不应据此推断。未修改文件。
