# 执行事务控制语句示例

## 普通数据库事务

<!-- compile -->

```cangjie
import std.database.sql.*
import std.time.*

main() {
    let SQL_INSERT = "INSERT INTO EMPLOYEE (NAME, SALARY, CREATED_DATE) VALUES (?, ?, ?)"
    let drv = DriverManager.getDriver("opengauss") ?? return
    let db = drv.open("opengauss://localhost:5432/testdb")
    try (cn = db.connect()) {
        let psInsert = cn.prepareStatement(SQL_INSERT)

        // 创建事务对象
        let tx = cn.createTransaction()
        try {
            // 插入第一条数据
            psInsert.set<String>(0, "mkyong")
            psInsert.set<Array<Byte>>(1, Array<Byte>(1, repeat: 10))
            psInsert.set<DateTime>(2, DateTime.now())
            psInsert.update()

            // 插入第二条数据
            psInsert.set<String>(0, "kungfu")
            psInsert.set<Array<Byte>>(1, Array<Byte>(1, repeat: 20))
            psInsert.set<DateTime>(2, DateTime.now())
            psInsert.update()

            // 如果连接到数据库，测试回滚 SQLException：未为参数3指定值。
            psInsert.set<String>(0, "mkyong")
            psInsert.set<Array<Byte>>(1, Array<Byte>(5, {i => UInt8(i + 1)}))
            psInsert.update()

            // 提交事务
            tx.commit()
        } catch (e1: SqlException) {
            e1.printStackTrace()
            try {
                // 发生异常，回滚所有事务
                tx.rollback()
            } catch (e2: SqlException) {
                // 如果回滚失败
                e2.printStackTrace()
            }
        }
    } catch (e: SqlException) {
        // 如果连接失败
        e.printStackTrace()
    }
}
```

## 事务保存点

如果数据库事务支持保存点，可以参考如下样例：

<!-- compile -->

```cangjie
import std.database.sql.*
import std.time.*

main() {
    let SQL_INSERT = "INSERT INTO EMPLOYEE (NAME, SALARY, CREATED_DATE) VALUES (?, ?, ?)"
    let drv = DriverManager.getDriver("opengauss") ?? return
    let db = drv.open("opengauss://localhost:5432/testdb")
    try (cn = db.connect()) {
        let psInsert = cn.prepareStatement(SQL_INSERT)

        let tx = cn.createTransaction()
        try {
            // 创建保存点 1
            tx.save("save1")
            psInsert.set<String>(0, "mkyong")
            psInsert.set<Array<Byte>>(1, Array<Byte>(1, repeat: 10))
            psInsert.set<DateTime>(2, DateTime.now())
            psInsert.update()

            // 创建保存点 2
            tx.save("save2")
            psInsert.set<String>(0, "kungfu")
            psInsert.set<Array<Byte>>(1, Array<Byte>(1, repeat: 20))
            psInsert.set<DateTime>(2, DateTime.now())
            psInsert.update()

            // 创建保存点 3
            tx.save("save3")
            psInsert.set<String>(0, "mkyong")
            psInsert.set<Array<Byte>>(1, Array<Byte>(5, {i => UInt8(i + 1)}))
            psInsert.update()

            // 回滚到保存点 2
            tx.rollback("save2")

            // 提交事务
            tx.commit()
        } catch (e1: SqlException) {
            e1.printStackTrace()
            try {
                // 发生异常，回滚所有事务
                tx.rollback()
            } catch (e2: SqlException) {
                e2.printStackTrace()
            }
        }
    } catch (e: SqlException) {
        e.printStackTrace()
    }
}
```
