# 运行仓颉可执行程序

## 直接运行

### Linux / macOS

1. 首先请查阅[部署仓颉运行时](./runtime_deploy.md)章节完成运行时库的部署。

2. 将编译得到的可执行文件 `main` 拷贝至运行环境中，执行可执行文件即可。

    ```bash
    ./main
    ```

    **值得注意的是**，使用 `cjpm` 编译得到的可执行文件 `main` 在 `target/release/bin` 目录下。

### Windows

1. 首先请查阅[部署仓颉运行时](./runtime_deploy.md)章节，完成运行时库的部署。

2. 将编译得到的可执行文件 `main.exe` 拷贝至运行环境中，执行可执行文件即可。

    ```bash
    .\main.exe
    ```

    **值得注意的是**，使用 `cjpm` 编译得到的可执行文件 `main.exe` 在 `target\release\bin` 目录下。

## 使用 cjpm 运行

开发者常用 `cjpm` 来管理、编译、运行仓颉项目。

开发者可以根据[安装仓颉工具链](../first_understanding/install.md)章节，在运行环境上安装完整的仓颉工具链。 安装完成后，将整个仓颉项目拷贝至运行环境，使用 `cjpm run` 命令运行仓颉项目即可。
