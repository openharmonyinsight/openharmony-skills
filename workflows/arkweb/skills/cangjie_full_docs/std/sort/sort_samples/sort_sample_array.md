# 对 Array 和 List 进行排序

## 对 Array 进行排序

创建无序 Array，并对这个 Array 进行排序。

示例：

<!-- verify -->
```cangjie
import std.sort.*

class Student <: ToString {
    public var name: String
    public var age: Int64
    public init(name: String, age: Int64) {
        this.name = name
        this.age = age
    }
    public func toString(): String {
        return "{name: ${name} age: ${age}}"
    }
}

main() {
    /* 对 Int64 数组升序排序 */
    var a = [1, 3, 5, 2, 4]
    sort(a)
    println(a)

    /* 按照年龄升序排序 */
    var b = [Student("A", 8), Student("B", 7), Student("C", 3), Student("D", 4), Student("E", 6)]
    let comparator = {l: Student, r: Student => l.age.compare(r.age)}
    sort(b, by: comparator)
    println(b)

    /* 按照年龄降序排序 */
    var c = [Student("A", 8), Student("B", 7), Student("C", 3), Student("D", 4), Student("E", 6)]
    let lessThan = {l: Student, r: Student => l.age < r.age}
    sort(c, lessThan: lessThan, descending: true)
    println(c)

    /* 按照年龄升序排序，并且是稳定排序 */
    var d = [Student("A", 8), Student("B", 7), Student("C", 7), Student("D", 4), Student("E", 7)]
    let key = {i: Student => i.age}
    sort(d, key: key, stable: true)
    println(d)
    return 0
}
```

运行结果：

```text
[1, 2, 3, 4, 5]
[{name: C age: 3}, {name: D age: 4}, {name: E age: 6}, {name: B age: 7}, {name: A age: 8}]
[{name: A age: 8}, {name: B age: 7}, {name: E age: 6}, {name: D age: 4}, {name: C age: 3}]
[{name: D age: 4}, {name: B age: 7}, {name: C age: 7}, {name: E age: 7}, {name: A age: 8}]
```

## 对 List 进行排序

创建无序 List，并对这个 List 进行排序。

示例：

<!-- verify -->
```cangjie
import std.sort.*
import std.collection.*

class Student <: ToString {
    public var name: String
    public var age: Int64
    public init(name: String, age: Int64) {
        this.name = name
        this.age = age
    }
    public func toString(): String {
        return "{name: ${name} age: ${age}}"
    }
}

main() {
    /* 对 Int64 的 List 进行升序排序 */
    var a = ArrayList<Int64>([1, 3, 5, 2, 4])
    sort(a)
    println(a)

    /* 按照年龄升序排序 */
    var b = ArrayList<Student>([Student("A", 8), Student("B", 7), Student("C", 3), Student("D", 4), Student("E", 6)])
    let comparator = {l: Student, r: Student => l.age.compare(r.age)}
    sort(b, by: comparator)
    println(b)

    /* 按照年龄降序排序 */
    var c = ArrayList<Student>([Student("A", 8), Student("B", 7), Student("C", 3), Student("D", 4), Student("E", 6)])
    let lessThan = {l: Student, r: Student => l.age < r.age}
    sort(c, lessThan: lessThan, descending: true)
    println(c)

    /* 按照年龄升序排序，并且是稳定排序 */
    var d = ArrayList<Student>([Student("A", 8), Student("B", 7), Student("C", 7), Student("D", 4), Student("E", 7)])
    let key = {i: Student => i.age}
    sort(d, key: key, stable: true)
    println(d)
    return 0
}
```

运行结果：

```text
[1, 2, 3, 4, 5]
[{name: C age: 3}, {name: D age: 4}, {name: E age: 6}, {name: B age: 7}, {name: A age: 8}]
[{name: A age: 8}, {name: B age: 7}, {name: E age: 6}, {name: D age: 4}, {name: C age: 3}]
[{name: D age: 4}, {name: B age: 7}, {name: C age: 7}, {name: E age: 7}, {name: A age: 8}]
```
