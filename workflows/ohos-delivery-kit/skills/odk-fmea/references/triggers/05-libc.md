# libc / libc++ 故障模式 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../05-libc.md](../05-libc.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| C-01 | 内存分配失败未判空 | malloc/strdup/new(nothrow) 返回值未判空直接解引用；无低内存降级路径 |
| C-02 | 缓冲区溢出 / 越界读写 | 使用 strcpy/strcat/sprintf 等不限长函数；memcpy 长度来自外部数据未校验；数组下标无边界检查 |
| C-03 | use-after-free / double free | 释放与使用存在多线程竞争；错误路径重复释放；智能指针与裸指针混用 |
| C-04 | 字符串未以 '\0' 结尾 | strncpy 拷贝后未显式补终止符；从网络/文件读入的缓冲区直接作 C 字符串使用 |
| C-05 | 整数溢出 | 长度计算（a*b+c）无溢出检查即用于分配；size_t 与 int 混用符号转换 |
| C-06 | 格式化字符串误用 | printf/日志接口直接以用户输入作格式串；格式串与参数个数/类型不匹配 |
| C-07 | STL 使用错误 | erase/push_back 后继续使用失效迭代器；vector 用 [] 而非 at 访问边界敏感下标；遍历中修改容器 |
| C-08 | 异常跨边界传播 | 异常可穿过 C 接口/NAPI 边界；noexcept 函数内可抛异常（触发 std::terminate） |
| C-09 | errno / 系统调用返回值未检查 | read/write/open/pthread_* 返回值未检查；只判 -1 不处理短读短写与 EINTR 重试 |
| C-10 | 崩溃信号特征（用于故障注入后的日志识别） | 分析对象为崩溃 faultlog（按 Reason:Signal 反查根因模式）；代码存在递归无出口、向已关闭 pipe/socket 写入（SIGPIPE）等信号敏感形态 |
