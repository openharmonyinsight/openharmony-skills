# 仓颉包兼容性检查

本章介绍从 0.59.4 版本开始引入的新特性**仓颉包兼容性检查**，在仓颉运行时加载仓颉包的过程中执行二进制兼容性检查，目的是帮助开发者识别兼容性问题，但无法拦截所有的二进制兼容性问题。

> **注意：**
>
> 该新特性仅适用于 0.59.4 及以后的版本。若运行时或标准库中存在 0.59.4 之前的版本，不保证兼容性，也无法确保正常运行。

## 检查规则

假设仓颉运行时的版本号为 `a.b.c`，待加载的仓颉包的版本号为 `x.y.z`。满足如下任一情况即为兼容：

- 当 `a` 和 `x` 均为 0 时，`a == x && b == y && c == z`。
- 当 `a` 和 `x` 均不为 0 时，`a == x`。

如果两个版本兼容，则继续执行后续包加载过程。如果不满足兼容性要求，则会出现以下两种报错场景：

- 场景一：被加载的是仓颉 core 包，则仓颉运行时终止执行，报错信息中包含仓颉运行时版本号和 core 包版本号。

    ```shell
    F executable cangjie file libcangjie-std-core.so version 0.59.3 is not compatible with deployed cangjie runtime version 0.59.5
    ```

- 场景二：被加载的包为仓颉 core 包以外的其他包，仓颉运行时报错并抛出 IncompatiblePackageException 异常，异常信息中包含仓颉运行时版本号和被加载包的版本号。

    ```shell
    E executable cangjie file liba.so version 0.59.5 is not compatible with deployed cangjie runtime version 0.59.3
    An exception has occurred:
    IncompatiblePackageException: executable cangjie file liba.so version 0.59.5 is not compatible with deployed cangjie runtime version 0.59.3
        at package_global_init(:0)
        at package_global_init(:0)
    ```
