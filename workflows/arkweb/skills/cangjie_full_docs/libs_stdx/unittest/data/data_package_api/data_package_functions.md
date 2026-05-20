# 函数

## func csv\<T>(String, Rune, Rune, Rune, Option\<Rune>, Option\<Array\<String>>, Array\<UInt64>, Array\<UInt64>, Bool) where T <: Serializable\<T>

```cangjie
public func csv<T>(
    fileName: String,
    delimiter!: Rune = ',',
    quoteChar!: Rune = '"',
    escapeChar!: Rune = '"',
    commentChar!: Option<Rune> = None,
    header!: Option<Array<String>> = None,
    skipRows!: Array<UInt64> = [],
    skipColumns!: Array<UInt64> = [],
    skipEmptyLines!: Bool = false
): CsvStrategy<T> where T <: Serializable<T>
```

功能：该函数可从 csv 文件中读取类型 T 的数据值，其中 T 必须可被序列化。该函数的返回值是参数化测试的一种参数源。

参数：

- fileName: String - CSV 格式的文件地址，可为相对地址，不限制后缀名。
- delimiter!: Rune - 一行中作为元素分隔符的符号。默认值为 `,` （逗号）。
- quoteChar!: Rune - 括住元素的符号。默认值为 `"` （双引号）。
- escapeChar!: Rune ：转义括住元素的符号。默认值为 `"` （双引号）。
- commentChar!: Option\<Rune> - 注释符号，跳过一行。必须在一行的最左侧。默认值是 `None`（不存在注释符号）。
- header!: Option\<Array\<String>> - 提供一种方式覆盖第一行。
    - 当 header 被指定时，文件的第一行将被作为数据行，指定的 header 将被使用。
    - 当 header 被指定，同时第一行通过指定 `skipRows` 被跳过时，第一行将被忽略，指定的 header 将被使用。
    - 当 header 未被指定时，即值为 `None` 时，文件的第一行将被作为表头。此为默认值。
- skipRows!: Array\<UInt64> - 指定需被跳过的数据行号，行号从 0 开始。默认值为空数组 `[]` 。
- skipColumns!: Array\<UInt64> - 指定需被跳过的数据列号，列号从 0 开始。当有数据列被跳过，并且用户指定了自定义的 header 时，该 header 将按照跳过后的实际数据列对应。默认值为空数据 `[]` 。
- skipEmptyLines!: Bool - 指定是否需要跳过空行。默认值为 `false` 。

返回值：

- [CsvStrategy](data_package_classes.md#class-csvstrategy)\<T> 对象，T 可被序列化，数据值从 CSV 文件中读取。

异常：

- IllegalStateException - 如果 CSV 数据的结构不正确，则抛出该异常。

## func json\<T>(String) where T <: Serializable\<T>

```cangjie
public func json<T>(fileName: String): JsonStrategy<T> where T <: Serializable<T>
```

功能：该函数可从 JSON 文件中读取类型 T 的数据值，其中 T 必须可被序列化。该函数的返回值是参数化测试的一种参数源。

参数：

- fileName: String - JSON 格式的文件地址，可为相对地址。

返回值：

- [JsonStrategy](data_package_classes.md#class-jsonstrategy)\<T> - T 可被序列化，数据值从 JSON 文件中读取。

示例：

```cangjie
@Test[user in json("users.json")]
func test_user_age(user: User): Unit {
    @Expect(user.age, 100)
}
```

json 文件示例：

```json
[
    {
        "age": 100
    },
    {
        "age": 100
    }
]
```

创建一种被用作测试函数参数的类，该类实现接口 [Serializable](../../../serialization/serialization_package_api/serialization_package_interfaces.md#interface-serializable)。

<!--compile-->
```cangjie
import stdx.serialization.serialization.*
import std.convert.*

class User <: Serializable<User> {
    User(let age: Int64) {}

    public func serialize(): DataModel {
        DataModelStruct().add(Field("age", DataModelInt(age)))
    }

    public static func deserialize(dm: DataModel): User {
        if (let Some(dms) <- (dm as DataModelStruct)) {
            if (let Some(age) <- (dms.get("age") as DataModelInt)) {
                return User(age.getValue())
            }
        }

        throw Exception("Can't deserialize user.")
    }
}
```

任何实现 [Serializable](../../../serialization/serialization_package_api/serialization_package_interfaces.md#interface-serializable) 的类型都可以用作参数类型，包括默认值：

```cangjie
@Test[user in json("numbers.json")]
func test(value: Int64)
```

```cangjie
@Test[user in json("names.json")]
func test(name: String)
```

## func tsv\<T>(String, Rune, Rune, Option\<Rune>, Option\<Array\<String>>, Array\<UInt64>, Array\<UInt64>, Bool) where T <: Serializable\<T>

```cangjie
public func tsv<T>(
    fileName: String,
    quoteChar!: Rune = '"',
    escapeChar!: Rune = '"',
    commentChar!: Option<Rune> = None,
    header!: Option<Array<String>> = None,
    skipRows!: Array<UInt64> = [],
    skipColumns!: Array<UInt64> = [],
    skipEmptyLines!: Bool = false
): CsvStrategy<T> where T <: Serializable<T>
```

功能：该函数可从 tsv 文件中读取类型 T 的数据值，其中 T 必须可被序列化。该函数的返回值是参数化测试的一种参数源。

参数：

- fileName: String - TSV 格式的文件地址，可为相对地址，不限制后缀名。
- quoteChar!: Rune - 括住元素的符号。默认值为 `"` （双引号）。
- escapeChar!: Rune - 转义括住元素的符号。默认值为 `"` （双引号）。
- commentChar!: Option\<Rune> - 注释符号，跳过一行。必须在一行的最左侧。默认值是 `None`（不存在注释符号）。
- header!: Option\<Array\<String>> - 提供一种方式覆盖第一行。
    - 当 header 被指定时，文件的第一行将被作为数据行，指定的 header 将被使用。
    - 当 header 被指定，同时第一行通过指定 `skipRows` 被跳过时，第一行将被忽略，指定的 header 将被使用。
    - 当 header 未被指定时，即值为 `None` 时，文件的第一行（跳过后的实际数据）将被作为表头。此为默认值。
- skipRows!: Array\<UInt64> - 指定需被跳过的数据行号，行号从 0 开始。默认值为空数组 `[]` 。
- skipColumns!: Array\<UInt64> - 指定需被跳过的数据列号，列号从 0 开始。当有数据列被跳过，并且用户指定了自定义的 header 时，该 header 将按照跳过后的实际数据列对应。默认值为空数据 `[]` 。
- skipEmptyLines!: Bool - 指定是否需要跳过空行。默认值为 `false` 。

返回值：

- [CsvStrategy](data_package_classes.md#class-csvstrategy)\<T> - T 可被序列化，数据值从 TSV 文件中读取。

异常：

- IllegalStateException - 如果 TSV 数据的结构不正确，则抛出该异常。

示例：

在单元测试中，可以通过传入 csv/tsv 文件地址进行参数化测试。

CSV 文件每一行的数据应当被表示成一个 [Serializable](../../../serialization/serialization_package_api/serialization_package_interfaces.md#interface-serializable)\<T> 对象，它的成员名是文件每一列头的值，成员值是 [DataModelString](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodelstring) 类型的对应列号上的值。

举例来说，有一个 `testdata.csv` 文件，具有如下内容：

```csv
username,age
Alex Great,21
Donald Sweet,28
```

有几种方式可以序列化上述数据：

1. 将数据表示为 HashMap\<String, String> 类型。

    具体示例为：

    <!--compile-->
    ```cangjie
    import std.collection.HashMap
    import std.unittest.*
    import std.unittest.testmacro.*

    @Test[user in csv("testdata.csv")]
    func testUser(user: HashMap<String, String>) {
        @Assert(user["username"] == "Alex Great" || user["username"] == "Donald Sweet")
        @Assert(user["age"] == "21" || user["age"] == "28")
    }
    ```

2. 将数据表示为 [Serializable](../../../serialization/serialization_package_api/serialization_package_interfaces.md#interface-serializable)\<T> 类型数据，其 String 类型的数据可被反序列化为 [DataModelStruct](../../../serialization/serialization_package_api/serialization_package_classes.md#class-datamodelstruct) 格式对象。

    具体示例为：

    <!--compile-->
    ```cangjie
    import serialization.serialization.*
    import std.convert.*
    import std.unittest.*
    import std.unittest.testmacro.*

    public class User <: Serializable<User> {
        public User(let name: String, let age: UInt32) {}

        public func serialize(): DataModel {
            let dms = DataModelStruct()
            dms.add(Field("username", DataModelString(name)))
            dms.add(Field("age", DataModelString(age.toString())))
            return dms
        }

        public static func deserialize(dm: DataModel): User {
            var data: DataModelStruct = match (dm) {
                case dms: DataModelStruct => dms
                case _ => throw DataModelException("this data is not DataModelStruct")
            }

            let name = String.deserialize(data.get("username"))
            let age = String.deserialize(data.get("age"))
            return User(name, UInt32.parse(age))
        }
    }

    @Test[user in csv("testdata.csv")]
    func testUser(user: User) {
    @Assert(user.name == "Alex Great" || user.name == "Donald Sweet")
    @Assert(user.age == 21 || user.age == 28)
    }
    ```
