# Linux 版本工具链的支持与安装

仓颉工具链当前基于以下 Linux 发行版进行了完整功能测试：

- Ubuntu 18.04
- Ubuntu 20.04
- UnionTech OS Server 20
- Kylin Linux Advanced Server Release V10

## 适用于各 Linux 发行版的仓颉工具链依赖安装命令

> **注意：**
>
> 当前仓颉工具链依赖的某些工具在一些 Linux 发行版上可能无法通过系统默认软件源直接安装。可参考下一节[编译安装依赖工具](./linux_toolchain_install.md#编译安装依赖工具)进行手动安装。

### Ubuntu 18.04

```shell
$ apt-get install \
          binutils \
          libc-dev \
          libc++-dev \
          libgcc-7-dev
```

此外，还需要安装 OpenSSL 3，安装方法请参见[编译安装依赖工具](./linux_toolchain_install.md#编译安装依赖工具)。

### Ubuntu 20.04

```shell
$ apt-get install \
          binutils \
          libc-dev \
          libc++-dev \
          libgcc-9-dev
```

此外，还需要安装 OpenSSL 3，安装方法请参见[编译安装依赖工具](./linux_toolchain_install.md#编译安装依赖工具)。

### UnionTech OS Server 20

```shell
$ yum install \
      binutils \
      glibc-devel \
      libstdc++-devel \
      gcc \
```

此外，还需要安装 OpenSSL 3，安装方法请参见[编译安装依赖工具](./linux_toolchain_install.md#编译安装依赖工具)。

### Kylin Linux Advanced Server release V10

```shell
$ yum install \
      binutils \
      glibc-devel \
      libstdc++-devel \
      gcc \
```

此外，还需要安装 OpenSSL 3，安装方法请参见[编译安装依赖工具](./linux_toolchain_install.md#编译安装依赖工具)。

### 其他 Linux 发行版

根据使用的 Linux 发行版的不同，可能需要参考以上系统的依赖安装命令，使用系统包管理工具安装对应依赖。若使用的系统没有提供相关软件包，可能需要自行安装链接工具、C 语言开发工具、C++ 开发工具、GCC 编译器、以及 OpenSSL 3 以正常使用仓颉工具链。

## 编译安装依赖工具

当前仓颉工具链中的部分标准库（以及部分工具）使用了 OpenSSL 3 开源软件。对于系统包管理工具未提供 OpenSSL 3 的场景，用户可能需要源码编译安装 OpenSSL 3，本节提供了 OpenSSL 3 源码编译的方法和步骤。

### OpenSSL 3

从以下链接可以下载到 OpenSSL 3 的源码：

- <https://www.openssl.org/source/>
- <https://www.openssl.org/source/old/>

建议使用 OpenSSL 3.0.7 或更高版本。

> **注意：**
>
> 请在执行以下编译和安装命令前仔细阅读注意事项，并根据实际情况调整命令。不正确的配置和安装可能会导致系统其他软件不可用。如果在编译安装过程中遇到问题或希望进行额外的安装配置，请参见 OpenSSL 源码中的 `INSTALL` 文件或 OpenSSL 的 [FAQ](https://www.openssl.org/docs/faq.html)。

此处以 OpenSSL 3.0.7 为例，下载后使用以下命令解压压缩包：

```shell
$ tar xf openssl-3.0.7.tar.gz
```

解压完成后进入目录：

```shell
$ cd openssl-3.0.7
```

编译 OpenSSL：

> **注意：**
>
> 如果系统已经安装了 OpenSSL，建议使用 `--prefix=<path>` 选项指定一个自定义安装路径，例如 `--prefix=/usr/local/openssl-3.0.7` 或开发者的个人目录。在系统目录已经存在 OpenSSL 的场景下直接使用以下命令编译安装可能会使系统 OpenSSL 被覆盖，并导致依赖系统 OpenSSL 的应用不可用。

```shell
$ ./Configure --libdir=lib
$ make
```

测试 OpenSSL：

```shell
$ make test
```

将 OpenSSL 安装至系统目录（或先前指定的 `--prefix` 目录），可能需要提供 root 权限以成功执行以下命令：

```shell
$ make install
```

或

```shell
$ sudo make install
```

如果先前编译 OpenSSL 时没有通过 `--prefix` 设置自定义安装路径，则 OpenSSL 安装已经完成了。如果先前通过 `--prefix` 指定了自定义的安装路径，还需要设置以下变量，以使仓颉工具链可以找到 OpenSSL 3。

> **注意：**
>
> 如果系统中原先存在其他版本的 OpenSSL，通过以下方式配置后，除了仓颉工具链外，其他编译开发工具默认使用的 OpenSSL 版本也可能受到影响。如果使用其他编译开发工具时出现 OpenSSL 不兼容的情况，请仅为仓颉开发环境配置以下变量。

*请将 `<prefix>` 替换为指定的自定义安装路径。*

```shell
$ export LIBRARY_PATH=<prefix>/lib:$LIBRARY_PATH
$ export LD_LIBRARY_PATH=<prefix>/lib:$LD_LIBRARY_PATH
```

通过以上方式所配置的环境变量仅在当前执行命令的 `shell` 会话窗口有效。若希望 `shell` 每次启动时都自动配置，可以在 `$HOME/.bashrc`、`$HOME/.zshrc` 或其他 `shell` 配置文件（依开发者的 `shell` 种类而定）加入以上命令。

若希望配置可以默认对所有用户生效，可以执行以下命令：

*请将 `<prefix>` 替换为指定的自定义安装路径。*

```shell
$ echo "export LIBRARY_PATH=<prefix>/lib:$LIBRARY_PATH" >> /etc/profile
$ echo "<prefix>/lib" >> /etc/ld.so.conf
$ ldconfig
```

执行完毕后重新打开 `shell` 会话窗口即可生效。

至此，OpenSSL 3 已经成功安装，可以回到原来的章节继续阅读或尝试运行仓颉编译器了。
