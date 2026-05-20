# 数组类型

## Array

可以使用 Array 类型来构造单一元素类型，有序序列的数据。

仓颉使用 `Array<T>` 来表示 Array 类型。T 表示 Array 的元素类型，T 可以是任意类型。

<!-- compile.error -array_example -->

```cangjie
var a: Array<Int64> = [0, 0, 0, 0] // Array whose element type is Int64
var b: Array<String> = ["a1", "a2", "a3"] // Array whose element type is String
```

元素类型不相同的 Array 是不相同的类型，所以它们之间不可以互相赋值。

因此以下例子是不合法的。

<!-- compile.error -array_example -->

```cangjie
b = a // Type mismatch
```

可以轻松使用字面量来初始化一个 Array，只需要使用方括号将逗号分隔的值列表括起来即可。

编译器会根据上下文自动推断 Array 字面量的类型。

<!-- compile -->

```cangjie
let a: Array<String> = [] // Created an empty Array whose element type is String
let b = [1, 2, 3, 3, 2, 1] // Created a Array whose element type is Int64, containing elements 1, 2, 3, 3, 2, 1
```

也可以使用构造函数的方式构造一个指定元素类型的 Array。其中， repeat 属于 Array 构造函数中的一个命名参数。

需要注意的是，当通过 repeat 指定的初始值初始化 Array 时，该构造函数不会拷贝 repeat，如果 repeat 是一个引用类型，构造后数组的每一个元素都将指向相同的引用。

<!-- compile -->

```cangjie
let a = Array<Int64>() // Created an empty Array whose element type is Int64
let c = Array<Int64>(3, repeat: 0) // Created an Array whose element type is Int64, length is 3 and all elements are initialized as 0
let d = Array<Int64>(3, {i => i + 1}) // Created an Array whose element type is Int64, length is 3 and all elements are initialized by the initialization function
```

示例中 `let d = Array<Int64>(3, {i => i + 1})` 使用了 [lambda 表达式](../function/lambda.md)作为初始化函数来初始化数组中的每一个元素，即 `{i => i + 1}`。

### 访问 Array 成员

当需要对 Array 的所有元素进行访问时，可以使用 for-in 循环遍历 Array 的所有元素。

Array 是按元素插入顺序排列的，因此对 Array 遍历的顺序总是恒定的。

<!-- verify -->

```cangjie
main() {
    let arr = [0, 1, 2]
    for (i in arr) {
        println("The element is ${i}")
    }
}
```

编译并执行上面的代码，会输出：

```text
The element is 0
The element is 1
The element is 2
```

当需要知道某个 Array 包含的元素个数时，可以使用 size 属性获得对应信息。

<!-- verify -->

```cangjie
main() {
    let arr = [0, 1, 2]
    if (arr.size == 0) {
        println("This is an empty array")
    } else {
        println("The size of array is ${arr.size}")
    }
}
```

编译并执行上面的代码，会输出：

```text
The size of array is 3
```

当想访问单个指定位置的元素时，可以使用下标语法访问（下标的类型必须是 Int64）。非空 Array 的第一个元素总是从位置 0 开始的。可以从 0 开始访问 Array 的任意一个元素，直到最后一个位置（Array 的 size - 1）。索引值不能使用负数或者大于等于 size，当编译器能检查出索引值非法时，会在编译时报错，否则会在运行时抛异常。

<!-- compile.error -->

```cangjie
main() {
    let arr = [0, 1, 2]
    let a = arr[0] // a == 0
    let b = arr[1] // b == 1
    let c = arr[-1] // array size is '3', but access index is '-1', which would overflow
}
```

如果想获取某一段 Array 的元素，可以在下标中传入 Range 类型的值，就可以一次性取得 Range 对应范围的一段 Array。

<!-- compile -->

```cangjie
let arr1 = [0, 1, 2, 3, 4, 5, 6]
let arr2 = arr1[0..5] // arr2 contains the elements 0, 1, 2, 3, 4
```

当 Range 字面量在下标语法中使用时，可以省略 start 或 end。

当省略 start 时，Range 会从 0 开始；当省略 end 时，Range 的 end 会延续到最后一位。

<!-- compile -->

```cangjie
let arr1 = [0, 1, 2, 3, 4, 5, 6]
let arr2 = arr1[..3] // arr2 contains elements 0, 1, 2
let arr3 = arr1[2..] // arr3 contains elements 2, 3, 4, 5, 6
```

### 修改 Array

Array 是一种长度不变的 [Collection 类型](../../source_zh_cn/collections/collection_overview.md)，因此 Array 没有提供添加和删除元素的成员函数。

但是 Array 允许对其中的元素进行修改，同样使用下标语法。

<!-- verify -->

```cangjie
main() {
    let arr = [0, 1, 2, 3, 4, 5]
    arr[0] = 3
    println("The first element is ${arr[0]}")
}
```

编译并执行上面的代码，会输出：

```text
The first element is 3
```

Array 虽然是 struct 类型，但其内部持有的只是元素的引用，因此在作为表达式使用时不会拷贝副本，同一个 Array 实例的所有引用都会共享同样的元素数据。

因此对 Array 元素的修改会影响到该实例的所有引用。

<!-- compile -->

```cangjie
let arr1 = [0, 1, 2]
let arr2 = arr1
arr2[0] = 3
// arr1 contains elements 3, 1, 2
// arr2 contains elements 3, 1, 2
```

## VArray

除了引用类型的数组 Array，仓颉还引入了值类型数组 `VArray<T, $N>` ，其中 `T` 表示该值类型数组的元素类型，`$N` 是一个固定的语法。通过 `$` 加上一个 `Int64` 类型的数值字面量表示这个值类型数组的长度。需要注意的是，`VArray<T, $N>` 不能省略 `<T, $N>`，且使用类型别名时，不允许拆分 `VArray` 关键字与其泛型参数。

与频繁使用引用类型 Array 相比，使用值类型 VArray 可以减少堆上内存分配和垃圾回收的压力。但是需要注意的是，由于值类型本身在传递和赋值时的拷贝，会产生额外的性能开销，因此建议不要在性能敏感场景使用较大长度的 `VArray`。值类型和引用类型的特点请参见[值类型和引用类型变量](../basic_programming_concepts/program_structure.md#值类型和引用类型变量)。
<!-- compile.error -->

```cangjie
type varr1 = VArray<Int64, $3> // OK
type varr2 = VArray // Error
```

> **注意：**
>
> 由于运行时后端限制，当前 `VArray<T, $N>` 的元素类型 `T` 或 `T` 的成员不能包含引用类型、枚举类型、Lambda 表达式（`CFunc` 除外）以及未实例化的泛型类型。

`VArray` 可以由一个数组的字面量来进行初始化，左值 `a` 必须标识出 `VArray` 的实例化类型：

<!-- compile -->

```cangjie
var a: VArray<Int64, $3> = [1, 2, 3]
```

同时，它拥有两个构造函数：

<!-- compile -->

```cangjie
// VArray<T, $N>(initElement: (Int64) -> T)
let b = VArray<Int64, $5>({ i => i }) // [0, 1, 2, 3, 4]
// VArray<T, $N>(repeat!: T)
let c = VArray<Int64, $5>(repeat: 0) // [0, 0, 0, 0, 0]
```

除此之外，`VArray<T, $N>` 类型提供了两个成员方法：

- 用于下标访问和修改的 `[]` 操作符方法：

  <!-- compile -->

  ```cangjie
  var a: VArray<Int64, $3> = [1, 2, 3]
  let i = a[1] // i is 2
  a[2] = 4 // a is [1, 2, 4]
  ```

  下标访问的下标类型必须为 `Int64`。

- 用于获取 `VArray` 长度的 `size` 成员：

  <!-- compile -->

  ```cangjie
  var a: VArray<Int64, $3> = [1, 2, 3]
  let s = a.size // s is 3
  ```

  size 属性的类型为 `Int64`。

此外，`VArray` 还支持仓颉与 C 语言互操作场景使用，相关内容请参见[数组](../FFI/cangjie-c.md#数组)。
