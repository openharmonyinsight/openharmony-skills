# AOP 开发示例

下面是使用 @InsertAtEntry 完成在指定函数入口插桩的示例代码：

<!-- compile -->

```cangjie
package AOP_demo1

import stdx.aspectCJ.*
import std.time.DateTime

@InsertAtEntry[packageName: "AOP_demo1", className: "", methodName: "printCurrentTime", isStatic: false, funcTypeStr: "()->Unit", recursive: false]
public func printCurrentTimeImpl() {
    println("----- ${DateTime.now()} -----")
}

public func printCurrentTime() {
    println("hi")
    println("bye")
}

main() {
    printCurrentTime()
    0
}
```

linux 平台编译命令：

```shell
cjc aop_demo1.cj -L $CANGJIE_STDX_PATH --import-path $CANGJIE_STDX_PATH -lstdx.aspectCJ --plugin=$CANGJIE_STDX_PATH/libcollect-aspects.so -o main # 第一次编译，收集切面
cjc aop_demo1.cj -L $CANGJIE_STDX_PATH --import-path $CANGJIE_STDX_PATH -lstdx.aspectCJ --plugin=$CANGJIE_STDX_PATH/libwave-aspects.so -o main # 第二次编译，织入切面
```

运行结果可能如下：

```text
----- 2025-06-03T00:00:18.994507-07:00 -----
hi
bye
```

下面是使用 @InsertAtExit 完成在指定函数退出前插桩的示例代码：

<!-- compile -->

```cangjie
package AOP_demo2

import stdx.aspectCJ.*
import std.time.DateTime

@InsertAtExit[packageName: "AOP_demo2", className: "", methodName: "printCurrentTime", isStatic: false, funcTypeStr: "()->std.core:String", recursive: false]
public func printCurrentTimeImpl() {
    println("----- ${DateTime.now()} -----")
}

public func printCurrentTime() {
    println("hi")
    println("bye")
    "done"
}

main() {
    println(printCurrentTime())
    0
}
```

linux 平台编译命令：

```shell
cjc aop_demo2.cj -L $CANGJIE_STDX_PATH --import-path $CANGJIE_STDX_PATH -lstdx.aspectCJ --plugin=$CANGJIE_STDX_PATH/libcollect-aspects.so -o main # 第一次编译，收集切面
cjc aop_demo2.cj -L $CANGJIE_STDX_PATH --import-path $CANGJIE_STDX_PATH -lstdx.aspectCJ --plugin=$CANGJIE_STDX_PATH/libwave-aspects.so -o main # 第二次编译，织入切面
```

运行结果可能如下：

```text
hi
bye
----- 2025-06-03T00:04:59.996469-07:00 -----
done
```

下面是使用 @ReplaceFuncBody 完成替换指定函数函数体的示例代码：

<!-- compile -->

```cangjie
package AOP_demo3

import stdx.aspectCJ.*
import std.time.DateTime

@ReplaceFuncBody[packageName: "AOP_demo3", className: "", methodName: "printCurrentTime", isStatic: false, recursive: false]
public func printCurrentTimeImpl(original: (String)->String) {
    println("----- ${DateTime.now()} -----")
    println(original("abc"))
    println("----- end -----")
    "def"
}

public func printCurrentTime(x: String): String {
    println(x)
    "456"
}

main() {
    println(printCurrentTime("123"))
    0
}
```

linux 平台编译命令：

```shell
cjc aop_demo3.cj -L $CANGJIE_STDX_PATH --import-path $CANGJIE_STDX_PATH -lstdx.aspectCJ --plugin=$CANGJIE_STDX_PATH/libcollect-aspects.so -o main # 第一次编译，收集切面
cjc aop_demo3.cj -L $CANGJIE_STDX_PATH --import-path $CANGJIE_STDX_PATH -lstdx.aspectCJ --plugin=$CANGJIE_STDX_PATH/libwave-aspects.so -o main # 第二次编译，织入切面
```

运行结果可能如下：

```text
----- 2025-06-03T00:04:59.996469-07:00 -----
abc
456
----- end -----
def
```
