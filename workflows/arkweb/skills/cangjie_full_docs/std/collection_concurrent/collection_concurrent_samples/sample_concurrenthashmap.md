# ConcurrentHashMap 使用示例

示例：

<!-- verify -->
```cangjie
import std.collection.*
import std.collection.concurrent.*
import std.sync.*

main() {
    let threads = 8
    let M = 1024

    let cmap = ConcurrentHashMap<Int64, Int64>(concurrencyLevel: 64)
    let jobs = Array<Future<Unit>>(threads, repeat: unsafe { zeroValue<Future<Unit>>() })
    for (t in 0..threads) {
        jobs[t] = spawn {
            for (i in t..M : threads) {
                cmap.put(i, i + 3)
            }
        }
    }

    for (t in 0..threads) {
        jobs[t].get()
    }

    println("Size after put: ${cmap.size}")

    for (t in 0..threads) {
        jobs[t] = spawn {
            for (i in t..M : threads) {
                cmap.remove(i, {v => v % 2 == 0})
            }
        }
    }

    for (t in 0..threads) {
        jobs[t].get()
    }

    println("Size after remove first: ${cmap.size}")

    for (t in 0..threads) {
        jobs[t] = spawn {
            for (i in t..M : threads) {
                cmap.remove(i)
            }
        }
    }

    for (t in 0..threads) {
        jobs[t].get()
    }

    println("Size after remove second: ${cmap.size}")
}
```

运行结果：

```text
Size after put: 1024
Size after remove first: 512
Size after remove second: 0
```
