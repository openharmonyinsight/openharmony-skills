# ArrayList

使用 ArrayList 类型需要导入 collection 包：

<!-- run -->

```cangjie
import std.collection.*
```

仓颉使用 `ArrayList<T>` 表示 ArrayList 类型，T 表示 ArrayList 的元素类型，T 可以是任意类型。

ArrayList 具备非常好的扩容能力，适合于需要频繁增加和删除元素的场景。

相比 Array，ArrayList 既可以原地修改元素，也可以原地增加和删除元素。

ArrayList 的可变性是一个非常有用的特征，可以让同一个 ArrayList 实例的所有引用都共享同样的元素，并且对它们统一进行修改。

```cangjie
var a: ArrayList<Int64> = ... // ArrayList whose element type is Int64
var b: ArrayList<String> = ... // ArrayList whose element type is String
```

元素类型不相同的 ArrayList 是不相同的类型，所以它们之间不可以互相赋值。

因此以下例子是不合法的。

```cangjie
b = a // Type mismatch
```

仓颉中可以使用构造函数的方式构造一个指定的 ArrayList。

<!-- run -->

```cangjie
let a = ArrayList<String>() // Created an empty ArrayList whose element type is String
let b = ArrayList<String>(100) // Created an ArrayList whose element type is String, and allocate a space of 100
let c = ArrayList<Int64>([0, 1, 2]) // Created an ArrayList whose element type is Int64, containing elements 0, 1, 2
let d = ArrayList<Int64>(c) // Use another Collection to initialize an ArrayList
let e = ArrayList<String>(2, {x: Int64 => x.toString()}) // Created an ArrayList whose element type is String and size is 2. All elements are initialized by specified rule function
```

## 访问 ArrayList 成员

当需要对 ArrayList 的所有元素进行访问时，可以使用 for-in 循环遍历 ArrayList 的所有元素。

<!-- verify -->

```cangjie
import std.collection.ArrayList

main() {
    let list = ArrayList<Int64>([0, 1, 2])
    for (i in list) {
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

当需要知道某个 ArrayList 包含的元素个数时，可以使用 size 属性获得对应信息。

<!-- verify -->

```cangjie
import std.collection.ArrayList

main() {
    let list = ArrayList<Int64>([0, 1, 2])
    if (list.size == 0) {
        println("This is an empty arraylist")
    } else {
        println("The size of arraylist is ${list.size}")
    }
}
```

编译并执行上面的代码，会输出：

```text
The size of arraylist is 3
```

当想访问单个指定位置的元素时，可以使用下标语法访问（下标的类型必须是 Int64）。非空 ArrayList 的第一个元素总是从位置 0 开始的。可以从 0 开始访问 ArrayList 的任意一个元素，直到最后一个位置（ArrayList 的 size - 1）。使用负数或大于等于 size 的索引会触发运行时异常。

```cangjie
let a = list[0] // a == 0
let b = list[1] // b == 1
let c = list[-1] // Runtime exceptions
```

ArrayList 也支持下标中使用 Range 的语法，详见 [Array](../basic_data_type/array.md#array) 章节。

## 修改 ArrayList

可以使用下标语法对某个位置的元素进行修改。

<!-- run -->

```cangjie
let list = ArrayList<Int64>([0, 1, 2])
list[0] = 3
```

ArrayList 是引用类型，ArrayList 在作为表达式使用时不会拷贝副本，同一个 ArrayList 实例的所有引用都会共享同样的数据。

因此对 ArrayList 元素的修改会影响到该实例的所有引用。

<!-- run -->

```cangjie
let list1 = ArrayList<Int64>([0, 1, 2])
let list2 = list1
list2[0] = 3
// list1 contains elements 3, 1, 2
// list2 contains elements 3, 1, 2
```

如果需要将单个元素添加到 ArrayList 的末尾，请使用 add 函数。如果希望同时添加多个元素到末尾，可以使用 `add(all!: Collection<T>)` 函数，这个函数可以接受其他相同元素类型的 Collection 类型，如 Array。Collection 类型详见[基础 Collection 类型概述](collection_overview.md)。

<!-- run -->

```cangjie
import std.collection.ArrayList

main() {
    let list = ArrayList<Int64>()
    list.add(0) // list contains element 0
    list.add(1) // list contains elements 0, 1
    let li = [2, 3]
    list.add(all: li) // list contains elements 0, 1, 2, 3
}
```

可以通过 `add(T, at!: Int64)` 和 `add(all!: Collection<T>, at!: Int64)` 函数将指定的单个元素或相同元素类型的 Collection 值插入到指定索引的位置。该索引处的元素和后面的元素会被挪后以腾出空间。

<!-- run -->

```cangjie
let list = ArrayList<Int64>([0, 1, 2]) // list contains elements 0, 1, 2
list.add(4, at: 1) // list contains elements 0, 4, 1, 2
```

从 ArrayList 中删除元素，可以使用 remove 函数，需要指定删除的索引。该索引处后面的元素会前移以填充空间。

<!-- run -->

```cangjie
let list = ArrayList<String>(["a", "b", "c", "d"]) // list contains the elements "a", "b", "c", "d"
list.remove(at: 1) // Delete the element at subscript 1, now the list contains elements "a", "c", "d"
```

## 增加 ArrayList 的大小

每个 ArrayList 都需要特定数量的内存来保存其内容。当向 ArrayList 添加元素并且该 ArrayList 开始超出其保留容量时，该 ArrayList 会分配更大的内存区域并将其所有元素复制到新内存中。这种增长策略意味着触发重新分配内存的添加操作具有性能成本，但随着 ArrayList 的保留内存变大，它们发生的频率会越来越低。

如果知道大约需要添加多少个元素，可以在添加之前预备足够的内存以避免中间重新分配，这样可以提升性能表现。

<!-- run -->

```cangjie
import std.collection.ArrayList

main() {
    let list = ArrayList<Int64>(100) // Allocate space at once
    for (i in 0..100) {
        list.add(i) // Does not trigger reallocation of space
    }
    list.reserve(100) // Prepare more space
    for (i in 0..100) {
        list.add(i) // Does not trigger reallocation of space
    }
}
```
