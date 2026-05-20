# 宏包定义和导入

仓颉语言中宏的定义需要放在由 `macro package` 声明的包中，被 `macro package` 限定的包仅允许宏定义对外可见，其他声明包内可见。

> **说明：**
>
> 重导出的声明也允许对外可见，关于包管理和重导出的相关概念，请参见[包的导入](../package/import.md)章节。

<!-- compile.error -macro4 -->
<!-- cfg="--compile-macro" -->

```cangjie
// file define.cj
macro package define         // 编译 define.cjo 携带 macro 属性
import std.ast.*

public func A() {}          // Error, 宏包不允许定义外部可见的非宏定义，此处会报错

public macro M(input: Tokens): Tokens { // macro M 外部可见
    return input
}
```

需要特殊说明的是，在宏包中，允许其他宏包和非宏包的声明被重导出。在非宏包中仅允许非宏包的声明被重导出。

参考如下示例：

- 在宏包 A 中定义宏 `M1`

  <!-- compile -macro5 -->
  <!-- cfg="--compile-macro" -->

  ```cangjie
  macro package A
  import std.ast.*

  public macro M1(input: Tokens): Tokens {
      return input
  }
  ```

  编译命令如下：

  ```shell
  cjc A.cj --compile-macro
  ```

- 在非宏包 B 中定义一个 public 函数 `f1`。注意在非 `macro package` 中无法重导出 `macro package` 的符号

  <!-- compile -macro5 -->
  <!-- cfg="--output-type=dylib -o libB.so" -->

  ```cangjie
  package B
  // public import A.* // Error, it is not allowed to re-export a macro package in a package.

  public func f1(input: Int64): Int64 {
      return input
  }
  ```

  编译命令如下，这里选择使用 `--output-type` 选项将 B 包编译成动态库，关于 cjc 编译选项介绍可以参考 "附录 > cjc 编译选项" 章节。

  ```shell
  cjc B.cj --output-type=dylib -o libB.so
  ```

- 在宏包 C 中定义宏 `M2`，依赖了 A 包和 B 包的内容。可以看到 `macro package` 中可以重导出 `macro package` 和非 `macro package` 的符号

  <!-- compile -macro5 -->
  <!-- cfg="--compile-macro -L. -lB" -->

  ```cangjie
  macro package C
  public import A.* // correct: macro package is allowed to re-export in a macro package.
  public import B.* // correct: non-macro package is also allowed to re-export in a macro package.
  import std.ast.*

  public macro M2(input: Tokens): Tokens {
      return @M1(input) + Token(TokenKind.NL) + quote(f1(1))
  }
  ```

  编译命令如下，注意这里需要显式链接 B 包动态库：

  ```shell
  cjc C.cj --compile-macro -L. -lB
  ```

- 在 `main.cj` 中使用 `M2` 宏

  <!-- compile -macro5 -->
  <!-- cfg="--compile-macro -L. -lB" -->

  ```cangjie
  import C.*

  main() {
      @M2(let a = 1)
  }
  ```

  编译命令如下：

  ```shell
  cjc main.cj -o main -L. -lB
  ```

  `main.cj`中 `M2` 宏展开后的结果如下：

  <!-- code_no_check -->

  ```cangjie
  import C.*

  main() {
      let a = 1
      f1(1)
  }
  ```

可以看到 `main.cj` 中出现了来自于 B 包的符号 `f1`。宏的编写者可以在 C 包中重导出 B 包里的符号，这样宏的使用者仅需导入宏包，就可以正确地编译宏展开后的代码。如果在 `main.cj` 中仅使用 `import C.M2` 导入宏符号，则会报 `undeclared identifier 'f1'` 的错误信息。
