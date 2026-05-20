# 日志打印示例

## 库开发场景记录日志

下面是开发仓颉库时，打印日志的示例。

代码如下：

<!-- run -->

```cangjie
import stdx.log.*
import stdx.logger.*
import std.env.*

public class PGConnection {
    let objId: Int64 = 1
    let logger = getGlobalLogger(("name", "PGConnection"))

    public func close(): Unit {
        logger.trace("driver conn closed", ("id", objId))
    }
}

main(): Unit {
    let tl = SimpleLogger(getStdOut())
    tl.level = LogLevel.TRACE
    setGlobalLogger(tl)
    var conn = PGConnection()
    conn.close()
}
```

运行结果可能如下：

```text
2024-11-21T20:16:43.33200773+08:00 TRACE driver conn closed name="PGConnection" id=1
```

## 应用程序开发场景日志打印

下面是 自定义 PasswordFilter 和 TextLogger 日志打印示例。

代码如下：

<!-- run -->

```cangjie
import std.time.*
import std.io.{OutputStream, ByteBuffer, BufferedOutputStream}
import std.env.*
import std.fs.*
import std.collection.{ArrayList, Map, HashMap}
import std.collection.concurrent.*
import std.sync.AtomicBool
import std.time.DateTime
import stdx.log.*

public class PasswordFilter <: Logger {
    var _level = LogLevel.INFO
    let processor: Logger
    public init(logger: Logger) {
        processor = logger
    }
    public mut prop level: LogLevel {
        get() {
            _level
        }
        set(v) {
            _level = v
        }
    }
    public func withAttrs(attrs: Array<Attr>): Logger {
        this
    }
    // log
    public func log(level: LogLevel, message: String, attrs: Array<Attr>): Unit {
        let record: LogRecord = LogRecord(DateTime.now(), level, message, attrs)
        log(record)
    }
    // lazy
    public func log(level: LogLevel, message: () -> String, attrs: Array<Attr>): Unit {
        let record: LogRecord = LogRecord(DateTime.now(), level, message(), attrs)
        log(record)
    }
    // 根据键值对的名字过滤，将密码值换成 "***"
    public func log(record: LogRecord): Unit {
        var attrs = record.attrs.clone()
        for (i in 0..attrs.size) {
            var attr = attrs[i]
            if (attr[0] == "password") {
                attrs[i] = (attr[0], "***")
            }
        }
        let r = LogRecord(record.time, record.level, record.message, attrs)
        processor.log(r)
    }
    public func isClosed(): Bool {
        false
    }
    public func close(): Unit {
    }
}

main() {
    let o = ByteBuffer()
    let tl = TextLogger(getStdOut())
    tl.level = LogLevel.TRACE
    let l = PasswordFilter(tl)
    setGlobalLogger(l)
    let logger = getGlobalLogger([("name", "main")])
    let user = User()
    // 普通记录信息日志
    logger.info("Hello, World!", ("k1", [[1, 4], [2, 5], [3]]), ("password", "v22222"))
    // 记录诊断日志，如果 DEBUG 级别未开启，直接返回，几乎无 cost
    logger.debug("Logging in user ${user.name} with birthday ${user.birthdayCalendar}")

    // lazy 方式记录耗时日志数据
    logger.log(LogLevel.ERROR, "long-running operation msg", ("k1", 100), ("k2", user.birthdayCalendar),
        ("oper", ToStringWrapper({=> "Some long-running operation returned"})))

    logger.log(LogLevel.ERROR, "long-running operation msg", ("sourcePackage", @sourcePackage()),
        ("sourceFile", @sourceFile()), ("sourceLine", @sourceLine()), ("birthdayCalendar", user.birthdayCalendar),
        ("oper", ToStringWrapper({=> "Some long-running operation returned"})))

    let m = HashMap<String, String>()
    m.add("k1", "1")
    m.add("k2", "2")
    m.add("k3", "3")
    logger.trace({=> "Some long-running operation returned"}, ("k1", m))
    let m2 = HashMap<String, LogValue>()
    m2.add("g1", m)

    // 如果 TRACE 级别没有开启，那么 lambda 表达式不会被执行
    logger.trace({=> "Some long-running operation returned"}, ("k2", m2))

    // Console.stdOut.write(o.bytes())
    // Console.stdOut.flush()
}

public class User {
    public prop name: String {
        get() {
            "foo"
        }
    }
    public prop birthdayCalendar: DateTime {
        get() {
            DateTime.now()
        }
    }
}

public class ToStringWrapper <: ToString & LogValue {
    let _fn: () -> String
    public init(fn: () -> String) {
        _fn = fn
    }
    public func toString(): String {
        return _fn()
    }
    public func writeTo(w: LogWriter): Unit {
        w.writeValue(_fn())
    }
}

public class TextLogger <: Logger {
    let w: TextLogWriter
    let opts = HashMap<String, String>()
    let _closed = AtomicBool(false)
    let queue = ConcurrentLinkedQueue<LogRecord>()
    let bo: BufferedOutputStream<OutputStream>
    let _attrs = ArrayList<Attr>()
    var _level = LogLevel.INFO
    public init(output: OutputStream) {
        bo = BufferedOutputStream<OutputStream>(output)
        w = TextLogWriter(bo)
    }

    public mut prop level: LogLevel {
        get() {
            _level
        }
        set(v) {
            _level = v
        }
    }
    public func withAttrs(attrs: Array<Attr>): Logger {
        if (attrs.size > 0) {
            let nl = TextLogger(w.out)
            nl._attrs.add(all: attrs)
            return nl
        }
        return this
    }
    // log
    public func log(level: LogLevel, message: String, attrs: Array<Attr>): Unit {
        if (this.enabled(level)) {
            let record: LogRecord = LogRecord(DateTime.now(), level, message, attrs)
            log(record)
        }
    }
    // lazy
    public func log(level: LogLevel, message: () -> String, attrs: Array<Attr>): Unit {
        if (this.enabled(level)) {
            let record: LogRecord = LogRecord(DateTime.now(), level, message(), attrs)
            log(record)
        }
    }
    public func log(record: LogRecord): Unit {
        // write time
        w.writeKey("time")
        w.writeValue(record.time)
        w.writeString(" ")
        // write level
        w.writeKey("level")
        w.writeString(record.level.toString())
        w.writeString(" ")
        // write message
        w.writeKey("msg")
        w.writeValue(record.message)
        w.writeString(" ")
        // write source

        // write attrs
        for (i in 0..record.attrs.size) {
            let attr = record.attrs[i]
            w.writeKey(attr[0])
            w.writeValue(attr[1])
            if (i < record.attrs.size - 1) {
                w.writeString(" ")
            }
        }
        w.writeString("\n")
        bo.flush()
    }
    public func isClosed(): Bool {
        _closed.load()
    }
    public func close(): Unit {
        if (isClosed()) {
            return
        }
        _closed.store(true)
    }
}

class TextLogWriter <: LogWriter {
    var out: OutputStream
    init(out: OutputStream) {
        this.out = out
    }
    public func writeNone(): Unit {
        out.write("None".toArray())
    }
    public func writeInt(v: Int64): Unit {
        out.write(v.toString().toArray())
    }
    public func writeUInt(v: UInt64): Unit {
        out.write(v.toString().toArray())
    }
    public func writeBool(v: Bool): Unit {
        out.write(v.toString().toArray())
    }
    public func writeFloat(v: Float64): Unit {
        out.write(v.toString().toArray())
    }
    public func writeString(v: String): Unit {
        out.write(v.toArray())
    }
    public func writeDateTime(v: DateTime): Unit {
        out.write(v.toString().toArray())
    }
    public func writeDuration(v: Duration): Unit {
        out.write(v.toString().toArray())
    }
    public func writeException(v: Exception): Unit {
        out.write(v.toString().toArray())
    }
    public func writeKey(v: String): Unit {
        out.write(v.toString().toArray())
        out.write("=".toArray())
    }
    public func writeValue(v: LogValue): Unit {
        match (v) {
            case vv: String =>
                out.write("\"".toArray())
                out.write(vv.toArray())
                out.write("\"".toArray())
            case vv: ToString =>
                out.write("\"".toArray())
                out.write(vv.toString().toArray())
                out.write("\"".toArray())
            case _ =>
                out.write("\"".toArray())
                v.writeTo(this)
                out.write("\"".toArray())
        }
    }
    public func startArray(): Unit {
        out.write("[".toArray())
    }
    public func endArray(): Unit {
        out.write("]".toArray())
    }
    public func startObject(): Unit {
        out.write("{".toArray())
    }
    public func endObject(): Unit {
        out.write("}".toArray())
    }
}
```

运行结果可能如下：

```text
time="2024-06-17T14:10:07.1861349Z" level=INFO msg="Hello, World!" k1="[[1, 4], [2, 5], [3]]" password="***"
time="2024-06-17T14:10:07.1864929Z" level=DEBUG msg="Logging in user foo with birthday 2024-06-17T14:10:07.1864802Z"
time="2024-06-17T14:10:07.1869579Z" level=ERROR msg="long-running operation msg" k1="100" k2="2024-06-17T14:10:07.186957Z" oper="Some long-running operation returned"
time="2024-06-17T14:10:07.18742Z" level=ERROR msg="long-running operation msg" sourcePackage="log" sourceFile="main.cj" sourceLine="77" birthdayCalendar="2024-06-17T14:10:07.1874188Z" oper="Some long-running operation returned"
time="2024-06-17T14:10:07.1879195Z" level=TRACE msg="Some long-running operation returned" k1="[(k1, 1), (k2, 2), (k3, 3)]"
time="2024-06-17T14:10:07.1881599Z" level=TRACE msg="Some long-running operation returned" k2="{g1="[(k1, 1), (k2, 2), (k3, 3)]"}"
```
