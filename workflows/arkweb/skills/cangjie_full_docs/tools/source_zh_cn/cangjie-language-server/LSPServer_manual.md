# 语言服务器工具

## 功能简介

`Cangjie Language Server` 仓颉语言服务器基于仓颉语言提供定义跳转，查找引用和补全等语言服务功能。

## 使用说明

仓颉语言服务器是在 IDE 上提供仓颉语言服务的服务器后端，需要搭配 IDE 客户端使用。开发者可以搭配仓颉发布的 VSCode 插件，或自行开发适配 LSP 协议的 IDE 客户端使用。

`Cangjie Language Server` 启动参数如下：

```shell
-V                    可选参数，使能 LSPServer 崩溃日志生成能力
--enable-log=<value>  可选参数，控制是否开启日志打印，若不设置，默认设值为 true，开启日志打印功能
--log-path=<value>    可选参数，设置日志文件和崩溃日志文件生成位置，若不设置，默认在 LSPServer 所在目录生成日志文件
--disableAutoImport   可选参数，禁用代码补全时的自动包导入功能
--test                可选参数，启动测试模式，配合运行 LSPServer 测试用例
```

## 使用示例

```shell
LSPServer.exe --enable-log=true --log-path=D:/CangjieLSPLog -V --disableAutoImport
```

表示启动 LSPServer，使能 LSPServer 日志和崩溃日志生成，并将日志文件生成位置设置在 `D:/CangjieLSPLog` 目录下；同时禁用代码补全时的自动包导入功能。