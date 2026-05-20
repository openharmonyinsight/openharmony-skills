# ConcurrentLinkedQueue 使用示例

示例：

<!-- verify -->
```cangjie
import std.collection.*
import std.collection.concurrent.*
import std.sync.*

main() {
    let threads = 8
    let total: Int64 = 128
    let bq = ConcurrentLinkedQueue<Int64>(Array<Int64>(total, {i => i}))
    println("Total ${bq.size} after init")
    let jobs = Array<Future<Unit>>(threads, repeat: unsafe { zeroValue<Future<Unit>>() })
    for (t in 0..threads) {
        jobs[t] = spawn {
            for (i in t..total : threads) {
                bq.dequeue()
            }
        }
    }

    for (t in 0..threads) {
        jobs[t].get()
    }
    println("Total ${bq.size} after dequeue")
}
```

运行结果：

```text
Total 128 after init
Total 0 after dequeue
```
