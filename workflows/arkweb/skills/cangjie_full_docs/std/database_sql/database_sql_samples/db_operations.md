# 执行数据库操作语句示例

## 插入数据

<!-- compile -->

```cangjie
import std.database.sql.*

main() {
    // 获取数据库连接示例
    let drv = DriverManager.getDriver("opengauss") ?? return
    let ds = drv.open("opengauss://testuser:testpwd@localhost:5432/testdb", [])
    let conn = ds.connect()

    // 插入数据 1
    var stmt = conn.prepareStatement("INSERT INTO test VALUES(?, ?)")
    stmt.set<String>(0, "li lei")
    stmt.set<Int32>(1, 12)
    var ur = stmt.update()
    println("Update Result: ${ur.rowCount} ${ur.lastInsertId}")

    // 插入数据 2
    stmt.set<String>(0, "han meimei")
    stmt.set<Int32>(1, 13)
    ur = stmt.update()
    println("Update Result: ${ur.rowCount} ${ur.lastInsertId}")

    // 如果需要在插入数据后返回插入的 id 值，可以参考如下方式：
    let sql = "INSERT INTO test (name, age) VALUES (?,?) RETURNING id, name"
    try (stmt = conn.prepareStatement(sql)) {
        stmt.set<String>(0, "li lei")
        stmt.set<Int32>(1, 12)
        let qr = stmt.query()
        while (qr.next()) {
            println("id = ${qr.get<Int32>(0)}, name=${qr.get<String>(1)}")
        }
    } catch (e: Exception) {
        e.printStackTrace()
    }
    stmt.close()
}
```

## 查询数据

<!-- compile -->

```cangjie
import std.database.sql.*

main() {
    // 获取数据库连接示例
    let drv = DriverManager.getDriver("opengauss") ?? return
    let ds = drv.open("opengauss://testuser:testpwd@localhost:5432/testdb", [])
    let conn = ds.connect()

    // 查询操作示例
    var stmt = conn.prepareStatement("select * from test where name = ?")
    stmt.set<String>(0, "li lei")
    let qr = stmt.query()
    while (qr.next()) {
        println("id = ${qr.get<Int32>(0)}, name = ${qr.get<String>(1)}, age=${qr.get<Int32>(2)}")
    }
    stmt.close()
}
```

## 更新数据

<!-- compile -->

```cangjie
import std.database.sql.*

main() {
    // 获取数据库连接示例
    let drv = DriverManager.getDriver("opengauss") ?? return
    let ds = drv.open("opengauss://testuser:testpwd@localhost:5432/testdb", [])
    let conn = ds.connect()

    // 更新操作示例
    var stmt = conn.prepareStatement("update test set age = ? where name = ?")
    stmt.set<Int32>(0, 15)
    stmt.set<String>(1, "li lei")
    var ur = stmt.update()
    println("Update Result: ${ur.rowCount} ${ur.lastInsertId}")
    stmt.close()
}
```

## 删除数据

<!-- compile -->

```cangjie
import std.database.sql.*

main() {
    // 获取数据库连接示例
    let drv = DriverManager.getDriver("opengauss") ?? return
    let ds = drv.open("opengauss://testuser:testpwd@localhost:5432/testdb", [])
    let conn = ds.connect()

    // 删除操作示例
    var stmt = conn.prepareStatement("delete from test where name = ?")
    stmt.set<String>(0, "li lei")
    var ur = stmt.update()
    println("Update Result: ${ur.rowCount} ${ur.lastInsertId}")
    stmt.close()
}
```
