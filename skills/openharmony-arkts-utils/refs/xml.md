# XML API 精简参考

> 源文档: js-apis-xml.md (1300+ 行)

## 导入模块

```typescript
import { xml } from '@kit.ArkTS';
```

---

## XML 生成

### XmlSerializer (固定缓冲区)

```typescript
// 创建序列化器
const arrayBuffer = new ArrayBuffer(4096);
const serializer = new xml.XmlSerializer(arrayBuffer, "utf-8");

// 写入 XML 声明
serializer.setDeclaration();  // <?xml version="1.0" encoding="utf-8"?>

// 写入元素
serializer.startElement("root");
serializer.setAttributes("id", "1");
serializer.startElement("child");
serializer.setText("Hello World");
serializer.endElement();  // </child>
serializer.endElement();  // </root>

// 获取结果
const result = new Uint8Array(arrayBuffer);
const decoder = new util.TextDecoder();
const xmlString = decoder.decodeToString(result);
```

### XmlDynamicSerializer (动态扩容, API 18+)

```typescript
const serializer = new xml.XmlDynamicSerializer("utf-8");

serializer.setDeclaration();
serializer.startElement("root");
serializer.setText("content");
serializer.endElement();

// 获取结果
const arrayBuffer = serializer.getOutput();
```

### 序列化方法

| 方法 | 说明 |
|------|------|
| `setDeclaration()` | 写入 XML 声明 |
| `startElement(name)` | 开始元素 |
| `endElement()` | 结束元素 |
| `setAttributes(name, value)` | 设置属性 |
| `setText(text)` | 设置文本内容 |
| `addEmptyElement(name)` | 添加空元素 |
| `setComment(comment)` | 添加注释 |
| `setCDATA(data)` | 添加 CDATA |
| `setDocType(docType)` | 设置文档类型 |
| `setNamespace(prefix, uri)` | 设置命名空间 |

### 生成示例

```typescript
const buffer = new ArrayBuffer(2048);
const serializer = new xml.XmlSerializer(buffer);

serializer.setDeclaration();
serializer.startElement("bookstore");
  serializer.startElement("book");
    serializer.setAttributes("category", "COOKING");
    serializer.startElement("title");
      serializer.setAttributes("lang", "en");
      serializer.setText("Everyday Italian");
    serializer.endElement();
    serializer.startElement("author");
      serializer.setText("Giada De Laurentiis");
    serializer.endElement();
    serializer.startElement("price");
      serializer.setText("30.00");
    serializer.endElement();
  serializer.endElement();
serializer.endElement();

// 输出:
// <?xml version="1.0" encoding="utf-8"?>
// <bookstore>
//   <book category="COOKING">
//     <title lang="en">Everyday Italian</title>
//     <author>Giada De Laurentiis</author>
//     <price>30.00</price>
//   </book>
// </bookstore>
```

---

## XML 解析

### XmlPullParser

```typescript
// 从字符串创建
const parser = new xml.XmlPullParser(xmlString, "utf-8");

// 从 ArrayBuffer 创建
const parser = new xml.XmlPullParser(arrayBuffer, "utf-8");
```

### 解析配置

```typescript
interface ParseOptions {
  supportDoctype?: boolean;      // 支持 DOCTYPE
  ignoreNameSpace?: boolean;     // 忽略命名空间
  tagValueCallbackFunction?: (name: string, value: string) => boolean;
  attributeValueCallbackFunction?: (name: string, value: string) => boolean;
  tokenValueCallbackFunction?: (eventType: EventType, value: ParseInfo) => boolean;
}
```

### 解析方法

```typescript
// 使用回调解析
parser.parseXml(options: ParseOptions): void
```

### EventType 事件类型

| 类型 | 值 | 说明 |
|------|----|----|
| `START_DOCUMENT` | 0 | 文档开始 |
| `END_DOCUMENT` | 1 | 文档结束 |
| `START_TAG` | 2 | 开始标签 |
| `END_TAG` | 3 | 结束标签 |
| `TEXT` | 4 | 文本内容 |
| `CDSECT` | 5 | CDATA |
| `COMMENT` | 6 | 注释 |
| `DOCDECL` | 7 | 文档声明 |
| `INSTRUCTION` | 8 | 处理指令 |
| `ENTITY_REFERENCE` | 9 | 实体引用 |
| `WHITESPACE` | 10 | 空白 |

### ParseInfo 解析信息

| 属性/方法 | 说明 |
|-----------|------|
| `getDepth()` | 当前深度 |
| `getColumnNumber()` | 列号 |
| `getLineNumber()` | 行号 |
| `getName()` | 元素名称 |
| `getNamespace()` | 命名空间 |
| `getPrefix()` | 前缀 |
| `getText()` | 文本内容 |
| `isEmptyElementTag()` | 是否空元素 |
| `getAttributeCount()` | 属性数量 |
| `getAttributeName(index)` | 属性名 |
| `getAttributeValue(index)` | 属性值 |

### 解析示例

```typescript
const xmlStr = `
<?xml version="1.0" encoding="utf-8"?>
<note importance="high">
  <to>Tove</to>
  <from>Jani</from>
  <body>Don't forget me!</body>
</note>`;

const parser = new xml.XmlPullParser(xmlStr);

parser.parseXml({
  supportDoctype: true,
  ignoreNameSpace: true,
  tokenValueCallbackFunction: (eventType: xml.EventType, info: xml.ParseInfo) => {
    switch (eventType) {
      case xml.EventType.START_TAG:
        console.info(`Start: ${info.getName()}`);
        for (let i = 0; i < info.getAttributeCount(); i++) {
          console.info(`  Attr: ${info.getAttributeName(i)}=${info.getAttributeValue(i)}`);
        }
        break;
      case xml.EventType.END_TAG:
        console.info(`End: ${info.getName()}`);
        break;
      case xml.EventType.TEXT:
        const text = info.getText().trim();
        if (text) console.info(`Text: ${text}`);
        break;
    }
    return true;  // 继续解析
  }
});
```

---

## XML 转换

### fastConvertToJSObject (API 18+)

将 XML 快速转换为 JavaScript 对象。

```typescript
xml.fastConvertToJSObject(xmlString: string, options?: ConvertOptions): object
```

### ConvertOptions 转换选项

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `trim` | boolean | false | 去除文本空白 |
| `ignoreDeclaration` | boolean | false | 忽略 XML 声明 |
| `ignoreInstruction` | boolean | false | 忽略处理指令 |
| `ignoreAttributes` | boolean | false | 忽略属性 |
| `ignoreComment` | boolean | false | 忽略注释 |
| `ignoreCDATA` | boolean | false | 忽略 CDATA |
| `ignoreDoctype` | boolean | false | 忽略 DOCTYPE |
| `ignoreText` | boolean | false | 忽略文本 |
| `declarationKey` | string | "_declaration" | 声明键名 |
| `instructionKey` | string | "_instruction" | 指令键名 |
| `attributesKey` | string | "_attributes" | 属性键名 |
| `textKey` | string | "_text" | 文本键名 |
| `cdataKey` | string | "_cdata" | CDATA 键名 |
| `doctypeKey` | string | "_doctype" | DOCTYPE 键名 |
| `commentKey` | string | "_comment" | 注释键名 |
| `parentKey` | string | "_parent" | 父元素键名 |
| `elementsKey` | string | "_elements" | 子元素键名 |
| `nameKey` | string | "_name" | 名称键名 |
| `typeKey` | string | "_type" | 类型键名 |

### 转换示例

```typescript
const xmlStr = `
<?xml version="1.0" encoding="UTF-8"?>
<note importance="high">
  <to>Tove</to>
  <from>Jani</from>
</note>`;

const result = xml.fastConvertToJSObject(xmlStr, {
  trim: true,
  ignoreDeclaration: false,
  attributesKey: "_attrs"
});

// 结果:
// {
//   "_declaration": {"_attrs": {"version": "1.0", "encoding": "UTF-8"}},
//   "note": {
//     "_attrs": {"importance": "high"},
//     "to": "Tove",
//     "from": "Jani"
//   }
// }
```

---

## ConvertXML (旧版)

```typescript
import { convertxml } from '@kit.ArkTS';

const converter = new convertxml.ConvertXML();
const result = converter.convertToJSObject(xmlString, options);
```

**注意**: 推荐使用 `xml.fastConvertToJSObject`，性能更好

---

## 常用场景

### 生成配置文件

```typescript
const buffer = new ArrayBuffer(4096);
const serializer = new xml.XmlSerializer(buffer);

serializer.setDeclaration();
serializer.startElement("config");
  serializer.startElement("database");
    serializer.setAttributes("host", "localhost");
    serializer.setAttributes("port", "3306");
  serializer.endElement();
  serializer.startElement("cache");
    serializer.setAttributes("enabled", "true");
    serializer.setAttributes("ttl", "3600");
  serializer.endElement();
serializer.endElement();
```

### 解析 API 响应

```typescript
const xmlResponse = `<response><code>200</code><data>success</data></response>`;

const result = xml.fastConvertToJSObject(xmlResponse, { trim: true });
console.info(result.response.code);  // "200"
console.info(result.response.data);  // "success"
```

### 提取特定元素

```typescript
const parser = new xml.XmlPullParser(xmlStr);
const items: string[] = [];

parser.parseXml({
  tokenValueCallbackFunction: (eventType, info) => {
    if (eventType === xml.EventType.START_TAG && info.getName() === "item") {
      // 找到 item 元素
    }
    if (eventType === xml.EventType.TEXT) {
      items.push(info.getText().trim());
    }
    return true;
  }
});
```

---

## 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 10200062 | XML 累积长度超限 | 减小 XML 内容 |
| 10200063 | XML 位置设置错误 | 检查元素顺序 |
| 10200064 | 字符串为空 | 提供有效字符串 |
| 10200065 | 元素不匹配 | 检查 start/end 配对 |
| 10200066 | 编码格式错误 | 使用 utf-8 编码 |
