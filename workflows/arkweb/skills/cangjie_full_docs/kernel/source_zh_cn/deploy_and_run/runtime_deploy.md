# 部署仓颉运行时

为了使仓颉可执行程序能够在不同的操作系统环境中正常运行，仓颉语言提供了一套运行时（`runtime`）环境。该运行时环境为仓颉可执行程序提供了对内存和其他系统资源的访问，例如在运行过程中依赖的仓颉动态库。

安装完整的仓颉工具链包含了仓颉代码编译环境和仓颉运行时的安装（详情请参见[安装仓颉工具链](../first_understanding/install.md)章节）。如果不需要编译代码，仅仅是运行可执行程序，也可以在环境中独立部署运行时。

本节介绍仓颉运行时的部署。

**值得注意的是**，编译时使用[全静态链接](../Appendix/compile_options.md#--static)仓颉库，运行时模块已在编译时嵌入到可执行文件中，因此无需在运行环境额外部署运行时，可直接在运行环境中运行编译所得的可执行文件。

## Linux

1. 首先请前往仓颉官方发布渠道，下载适配平台架构的安装包：

    - `cangjie-sdk-linux-x64-x.y.z.tar.gz`：适用于 x86_64 架构 Linux 系统的仓颉工具链。
    - `cangjie-sdk-linux-aarch64-x.y.z.tar.gz`：适用于 aarch64 架构 Linux 系统的仓颉工具链。

2. 请将下载的安装包解压到合适的目录。

    解压完成后，可以在当前工作路径下看到一个名为 `cangjie` 的目录，其中存放了仓颉工具链的全部内容。

    `cangjie` 目录下的 `runtime` 目录，即为运行时库，存放了仓颉 `runtime` 的全部动态库。

3. 请在运行环境执行如下命令完成 `runtime` 的部署（其中 `${CANGJIE_HOME}` 请修改为 `cangjie` 目录所在的路径，`${hw_arch}` 请修改为对应的硬件架构）：

    ```bash
    export LD_LIBRARY_PATH=${CANGJIE_HOME}/runtime/lib/linux_${hw_arch}_cjnative:${LD_LIBRARY_PATH}
    ```

## macOS

1. 首先请前往仓颉官方发布渠道，下载适配平台架构的安装包：

    - `cangjie-sdk-mac-aarch64-x.y.z.tar.gz`：适用于 aarch64/arm64 架构 macOS 系统的仓颉工具链。

2. 请将下载的安装包解压到合适的目录。

    解压完成后，可以在当前工作路径下看到一个名为 `cangjie` 的目录，其中存放了仓颉工具链的全部内容。

    `cangjie` 目录下的 `runtime` 目录，即为运行时库，存放了仓颉 `runtime` 的全部动态库。

3. 请在运行环境执行如下命令完成 `runtime` 的部署（其中 `${CANGJIE_HOME}` 请修改为 `cangjie` 目录所在的路径，`${hw_arch}` 请修改为对应的硬件架构）：

    ```bash
    export DYLD_LIBRARY_PATH=${CANGJIE_HOME}/runtime/lib/darwin_${hw_arch}_cjnative:${DYLD_LIBRARY_PATH}
    ```

## Windows

1. 首先请前往仓颉官方发布渠道，下载适配平台架构的安装包：

    - `cangjie-sdk-windows-x64-x.y.z.zip`：适用于 x86_64 架构 Windows 系统的仓颉工具链。

2. 请将下载的安装包解压到合适的目录。

    解压完成后，可以在当前工作路径下看到一个名为 `cangjie` 的目录，其中存放了仓颉工具链的全部内容。

    `cangjie` 目录下的 `runtime` 目录，即为运行时库，存放了仓颉 `runtime` 的全部动态库。

3. 此处为开发者提供三种环境下部署 `runtime` 的方法，可以根据使用习惯及环境配置，选择一种执行（其中 `${CANGJIE_HOME}` 请修改为 `cangjie` 目录所在的路径，`${hw_arch}` 请修改为对应的硬件架构）：

    - 若使用 Windows 命令提示符（CMD）环境，请执行：

        ```bash
        set "PATH=${CANGJIE_HOME}\runtime\lib\windows_x86_64_cjnative;%PATH%;"
        ```

    - 若使用 PowerShell 环境，请执行：

        ```bash
        $env:PATH = "${CANGJIE_HOME}\runtime\lib\windows_x86_64_cjnative;" + $env:Path
        ```

    - 若使用 MSYS shell、bash 等环境，请执行：

        ```bash
        export PATH=${CANGJIE_HOME}/runtime/lib/windows_x86_64_cjnative
        ```
