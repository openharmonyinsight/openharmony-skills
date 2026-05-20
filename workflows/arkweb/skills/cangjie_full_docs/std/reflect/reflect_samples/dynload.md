# 动态加载的使用

在项目根目录 `myProject` 下分别创建两个目录 `myModuleDirectory` 和 `myExecutableDirectory`，分别在其中使用 `cjpm` 构建仓颉动态库模块和可执行文件，该可执行文件将在动态加载该仓颉动态库模块后通过反射对动态库模块中的全局变量进行操作。

```bash
$ mkdir -p myProject && cd myProject
$ mkdir -p myPackage && cd myPackage
# 在 myPackage 目录下执行该命令初始化该仓颉动态库模块的目录结构，如此便可对 myPackage 下的仓颉功能进行动态编译。
$ cjpm init --type=dynamic --name myPackage
cjpm init success
$ cat << EOF > src/myPackage.cj
package myPackage

public var myPublicGlobalVariable0: Int64 = 2333
public let myPublicGlobalVariable1 = MyPublicType("Initializing myPublicGlobalVariable1 in myPackage")

public class MyPublicType {
    public MyPublicType(message: String) {
        println(message)
    }

    public static func myPublicStaticMemeberFunction() {
        println("myPackage.MyPublicType.myPublicStaticMemeberFunction is called.")
    }

    static let myStaticVariable = MyPublicType("Initializing myStaticVariable in myPackage.MyPublicType")
}
EOF
# 使用 cjpm 构建该仓颉动态库模块。
$ cjpm build
cjpm build success
$ cd .. && mkdir -p myExecutableDirectory && cd myExecutableDirectory
$ cjpm init
$ cat << EOF > src/main.cj
package myExecutableDirectory
import std.reflect.*

main(): Unit {
    // 加载仓颉动态库。
    let myPackage = PackageInfo.load("../myPackage/target/release/myPackage/libmyPackage")
    println(myPackage.name)
    TypeInfo.get("myPackage.MyPublicType") |> println

    let myPublicGlobalVariable0 = myPackage.getVariable("myPublicGlobalVariable0")
    (myPublicGlobalVariable0.getValue() as Int64).getOrThrow() |> println
    myPublicGlobalVariable0.setValue(666)
    (myPublicGlobalVariable0.getValue() as Int64).getOrThrow() |> println
}
EOF

# 构建并运行可执行程序。
$ cjpm run
Initializing myPublicGlobalVariable1 in myPackage
Initializing myStaticVariable in myPackage.MyPublicType
myPackage
myPackage.MyPublicType
2333
666

cjpm run finished
$ tree ..
..
├── myExecutableDirectory
│   ├── cjpm.lock
│   ├── cjpm.toml
│   ├── src
│   │   └── main.cj
│   └── target
│       └── release
│           ├── bin
│           │   ├── main
│           │   ├── myExecutableDirectory.bchir
│           │   └── myExecutableDirectory.cjo
│           ├── myExecutableDirectory
│           │   └── incremental-cache.json
│           └── myExecutableDirectory-cache.json
└── myPackage
    ├── cjpm.lock
    ├── cjpm.toml
    ├── src
    │   └── myPackage.cj
    └── target
        └── release
            ├── bin
            ├── myPackage
            │   ├── incremental-cache.json
            │   ├── libmyPackage.so
            │   ├── myPackage.bchir
            │   └── myPackage.cjo
            └── myPackage-cache.json

12 directories, 16 files
```

> **注意：**
>
> 由于当前 PackageInfo.load 函数根据文件名来判断包名，因此不允许修改该文件名，否则将抛出无法找到仓颉动态库模块文件的异常。
