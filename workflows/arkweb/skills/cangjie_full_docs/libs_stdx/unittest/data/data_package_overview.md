# stdx.unittest.data

## 功能介绍

unittest.data 库用于在编写仓颉项目单元测试代码时提供输入序列化格式的测试数据的能力，当前支持 json/csv/tsv 等格式。

标准测试能力可参考标准库 API 文档。

## API 列表

### 函数

|              函数名          |           功能           |
| --------------------------- | ------------------------ |
| [csv\<T>(String, Rune, Rune, Rune, Option\<Rune>, Option\<Array\<String>>, Array\<UInt64>, Array\<UInt64>, Bool)](./data_package_api/data_package_functions.md#func-csvtstring-rune-rune-rune-optionrune-optionarraystring-arrayuint64-arrayuint64-bool-where-t--serializablet) | 该函数可从 csv 文件中读取类型 T 的数据值，其中 T 必须可被序列化。该函数的返回值是参数化测试的一种参数源。 |
| [json\<T>(String)](./data_package_api/data_package_functions.md#func-jsontstring-where-t--serializablet) | 该函数可从 JSON 文件中读取类型 T 的数据值，其中 T 必须可被序列化。该函数的返回值是参数化测试的一种参数源。 |
| [tsv\<T>(String, Rune, Rune, Option\<Rune>, Option\<Array\<String>>, Array\<UInt64>, Array\<UInt64>, Bool)](./data_package_api/data_package_functions.md#func-tsvtstring-rune-rune-optionrune-optionarraystring-arrayuint64-arrayuint64-bool-where-t--serializablet) | 该函数可从 tsv 文件中读取类型 T 的数据值，其中 T 必须可被序列化。该函数的返回值是参数化测试的一种参数源。 |

### 类

|              类名          |           功能           |
| --------------------------- | ------------------------ |
| [CsvStrategy](./data_package_api/data_package_classes.md#class-csvstrategy) | `DataStrategy` 对 CSV 数据格式的序列化实现。 |
| [JsonStrategy](./data_package_api/data_package_classes.md#class-jsonstrategy) | `DataStrategy` 对 JSON 数据格式的序列化实现。 |
| [SerializableProvider](./data_package_api/data_package_classes.md#class-serializableprovider) | 获取序列化数据 DataProvider 接口的实现。 |
