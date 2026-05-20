# HashSet

使用 HashSet 类型需要导入 collection 包：

<!-- run -->

```cangjie
import std.collection.*
```

可以使用 HashSet 类型来构造只拥有不重复元素的 Collection。

仓颉使用 `HashSet<T>` 表示 HashSet 类型，T 表示 HashSet 的元素类型，T 必须是实现了 Hashable 和 `Equatable<T>` 接口的类型，例如数值或 String。

```cangjie
var a: HashSet<Int64> = ... // HashSet whose element type is Int64
var b: HashSet<String> = ... // HashSet whose element type is String
```

元素类型不相同的 HashSet 是不相同的类型，所以它们之间不可以互相赋值。

因此以下例子是不合法的。

```cangjie
b = a // Type mismatch
```

仓颉中可以使用构造函数的方式构造一个指定的 HashSet。

<!-- run -->

```cangjie
let a = HashSet<String>() // Created an empty HashSet whose element type is String
let b = HashSet<String>(100) // Created a HashSet whose capacity is 100
let c = HashSet<Int64>([0, 1, 2]) // Created a HashSet whose element type is Int64, containing elements 0, 1, 2
let d = HashSet<Int64>(c) // Use another Collection to initialize a HashSet
let e = HashSet<Int64>(10, {x: Int64 => (x * x)}) // Created a HashSet whose element type is Int64 and size is 10. All elements are initialized by specified rule function
```

## 访问 HashSet 成员

当需要对 HashSet 的所有元素进行访问时，可以使用 for-in 循环遍历 HashSet 的所有元素。

需要注意的是，HashSet 并不保证按插入元素的顺序排列，因此遍历的顺序和插入的顺序可能不同。

<!-- verify -->

```cangjie
import std.collection.*

main() {
    let mySet = HashSet<Int64>([0, 1, 2])
    for (i in mySet) {
        println("The element is ${i}")
    }
}
```

编译并执行上面的代码，有可能会输出：

```text
The element is 0
The element is 1
The element is 2
```

当需要知道某个 HashSet 包含的元素个数时，可以使用 size 属性获得对应信息。

<!-- verify -->

```cangjie
import std.collection.*

main() {
    let mySet = HashSet<Int64>([0, 1, 2])
    if (mySet.size == 0) {
        println("This is an empty hashset")
    } else {
        println("The size of hashset is ${mySet.size}")
    }
}
```

编译并执行上面的代码，会输出：

```text
The size of hashset is 3
```

当想判断某个元素是否被包含在某个 HashSet 中时，可以使用 contains 函数。如果该元素存在会返回 true，否则返回 false。

<!-- run -->

```cangjie
let mySet = HashSet<Int64>([0, 1, 2])
let a = mySet.contains(0) // a == true
let b = mySet.contains(-1) // b == false
```

## 修改 HashSet

HashSet 是一种可变的引用类型，HashSet 类型提供了添加元素、删除元素的功能。

HashSet 的可变性是一个非常有用的特征，可以让同一个 HashSet 实例的所有引用都共享同样的元素，并且对它们统一进行修改。

如果需要将单个元素添加到 HashSet 里，请使用 add 函数。如果希望同时添加多个元素，可以使用 `add(all!: Collection<T>)` 函数，这个函数可以接受另一个相同元素类型的 Collection 类型（例如 Array）。当元素不存在时，add 函数会执行添加的操作，当 HashSet 中存在相同元素时，add 函数将不会有效果。

<!-- run -->

```cangjie
let mySet = HashSet<Int64>()
mySet.add(0) // mySet contains elements 0
mySet.add(0) // mySet contains elements 0
mySet.add(1) // mySet contains elements 0, 1
let li = [2, 3]
mySet.add(all: li) // mySet contains elements 0, 1, 2, 3
```

HashSet 是引用类型，HashSet 在作为表达式使用时不会拷贝副本，同一个 HashSet 实例的所有引用都会共享同样的数据。

因此对 HashSet 元素的修改会影响到该实例的所有引用。

<!-- run -->

```cangjie
let set1 = HashSet<Int64>([0, 1, 2])
let set2 = set1
set2.add(3)
// set1 contains elements 0, 1, 2, 3
// set2 contains elements 0, 1, 2, 3
```

从 HashSet 中删除元素，可以使用 remove 函数，需要指定删除的元素。

<!-- run -->

```cangjie
let mySet = HashSet<Int64>([0, 1, 2, 3])
mySet.remove(1) // mySet contains elements 0, 2, 3
```
