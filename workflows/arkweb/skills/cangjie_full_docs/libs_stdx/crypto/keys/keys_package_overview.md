# stdx.crypto.keys

## 功能介绍

keys 包提供非对称加密和签名算法，包括 RSA 和 SM2 非对称加密算法以及 ECDSA 签名算法。

使用本包需要外部依赖 OpenSSL 3 的 crypto 动态库文件，故使用前需安装相关工具。

- 对于 Linux 操作系统，可参考以下方式：
    - 如果系统的包管理工具支持安装 OpenSSL 3 开发工具包，可通过这个方式安装，并确保系统安装目录下含有 libcrypto.so 和 libcrypto.so.3 这两个动态库文件，例如 Ubuntu 22.04 系统上可使用 sudo apt install libssl-dev 命令安装 libssl-dev 工具包；
    - 如果无法通过上面的方式安装，可自行下载 OpenSSL 3.x.x 源码编译安装软件包，并确保安装目录下含有 libcrypto.so 和 libcrypto.so.3 这两个动态库文件，然后可选择下面任意一种方式来保证系统链接器可以找到这些文件：
        - 在系统未安装 OpenSSL 的场景，安装时选择直接安装到系统路径下；
        - 安装在自定义目录的场景，将这些文件所在目录设置到环境变量 LD_LIBRARY_PATH 以及 LIBRARY_PATH 中。

- 对于 Windows 操作系统，可按照以下步骤：
    - 自行下载 OpenSSL 3.x.x 源码编译安装 x64 架构软件包或者自行下载安装第三方预编译的供开发人员使用的 OpenSSL 3.x.x 软件包；
    - 确保安装目录下含有 libcrypto.dll.a（或 libcrypto.lib）、libcrypto-3-x64.dll 这两个库文件；
    - 将 libcrypto.dll.a（或 libcrypto.lib）所在的目录路径设置到环境变量 LIBRARY_PATH 中，将 libcrypto-3-x64.dll 所在的目录路径设置到环境变量 PATH 中。

- 对于 macOS 操作系统，可参考以下方式：
    - 使用 brew install openssl@3 安装，并确保系统安装目录下含有 libcrypto.dylib 和 libcrypto.3.dylib 这两个动态库文件；
    - 如果无法通过上面的方式安装，可自行下载 OpenSSL 3.x.x 源码编译安装软件包，并确保安装目录下含有 libcrypto.dylib 和 libcrypto.3.dylib 这两个动态库文件，然后可选择下面任意一种方式来保证系统链接器可以找到这些文件：
        - 在系统未安装 OpenSSL 的场景，安装时选择直接安装到系统路径下；
        - 安装在自定义目录的场景，将这些文件所在目录设置到环境变量 DYLD_LIBRARY_PATH 以及 LIBRARY_PATH 中。

> **说明：**
>
> 如果未安装 OpenSSL 3 软件包或者安装低版本的软件包，程序可能无法使用并抛出相关异常 CryptoException：Can not load openssl library or function xxx。

## API 列表

### 类

| 类名                                                                                    | 功能                           |
| --------------------------------------------------------------------------------------- | ------------------------------ |
| [ECDSAPrivateKey](./keys_package_api/keys_package_classes.md#class-ecdsaprivatekey)     | ECDSA 私钥类。                  |
| [ECDSAPublicKey](./keys_package_api/keys_package_classes.md#class-ecdsapublickey)       | ECDSA 公钥类。                  |
| [RSAPrivateKey](./keys_package_api/keys_package_classes.md#class-rsaprivatekey)         | RSA 私钥类。                    |
| [RSAPublicKey](./keys_package_api/keys_package_classes.md#class-rsapublickey)           | RSA 公钥类。                    |
| [SM2PrivateKey](./keys_package_api/keys_package_classes.md#class-sm2privatekey)         | SM2 私钥类。                    |
| [SM2PublicKey](./keys_package_api/keys_package_classes.md#class-sm2publickey)           | SM2 公钥类。                    |

### 枚举

| 枚举名                                                               | 功能                                                         |
| -------------------------------------------------------------------- | ------------------------------------------------------------ |
| [Curve](./keys_package_api/keys_package_enums.md#enum-curve)         | 枚举类型 Curve 用于选择生成 ECDSA 密钥时使用的椭圆曲线类型。 |
| [PadOption](./keys_package_api/keys_package_enums.md#enum-padoption) | 用于设置 RSA 的填充模式。                                    |

### 结构体

| 结构体名                                                                   | 功能                 |
| -------------------------------------------------------------------------- | -------------------- |
| [OAEPOption](./keys_package_api/keys_package_structs.md#struct-oaepoption) | 最优非对称加密填充。 |
| [PSSOption](./keys_package_api/keys_package_structs.md#struct-pssoption)   | 概率签名方案。       |
