# 接口

## interface ValueListener\<T>

```cangjie
public interface ValueListener<T> {
    func lastValue(): Option<T>
    func allValues(): Array<T>
    func addCallback(callback: (T) -> Unit): Unit
    static func new(): ValueListener<T>
    static func onEach(callback: (T) -> Unit): ValueListener<T>
}
```

功能：此接口提供了多个成员函数以支持“监听”传入给桩签名的参数。即对每次调用中传入桩签名的参数进行指定的操作（ `addCallback()` 或 `onEach` 中的闭包函数即为对参数进行的操作内容）。

一般与参数匹配器生成函数 `argThat` 或者 `capture` 配合使用。

值侦听器与参数捕获器一同作为参数匹配器的一种被传入到桩签名中，作为入参。在定义桩签名的参数值范围的同时检查参数值。

举例来说：

```cangjie
struct Animal {
    Animal(
        let name: String,
        let info: String
    ) {}
}

abstract class AnimalUi {
    func showAnimal(animal: Animal): Unit
}

let animals = [Animal("Smokey", "Cat, age: 5"), Animal("Daisy", "Dog, age: 9")]

@Test func testAnimal(): Unit {
    let ui = mock<AnimalUi>()
    // 定义了一个值监听器：检查每个值，当值不满足条件时抛出异常。
    let listener = ValueListener<Animal>.onEach { animal =>
        if (animal.name == "Smokey") {
            @Assert(animal.info.contains("Cat"))
        }
    }
    // 定义一个桩签名的“桩行为”，参数匹配器为可执行上述值监听器的参数捕获器。
    @On(ui.showAnimal(capture(listener))).returns(())

    for (animal in animals) {
        // 此处将捕获传入的 animal 对象，并对其执行值监听器中的检查行为。
        ui.showAnimal(animal)
    }
}
```

### func addCallback((T) -> Unit)

```cangjie
func addCallback(callback: (T) -> Unit): Unit
```

功能：为当前“值监听器”对象增加闭包函数，该函数将处理传入的参数值。

参数：

- callback: (T) ->[Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 处理参数值的闭包函数。

### func allValues()

```cangjie
func allValues(): Array<T>
```

功能：返回当前“值监听器”对象已所处理的所有值。

返回值：

- [Array](../../core/core_package_api/core_package_structs.md#struct-arrayt)\<T> - 返回“值监听器”对象所处理的所有值列表。

### func lastValue()

```cangjie
func lastValue(): Option<T>
```

功能：返回当前“值监听器”对象所处理的最后一个值。

返回值：

- [Option](../../core/core_package_api/core_package_enums.md#enum-optiont)\<T> - 返回“值监听器”对象所处理的最后一个值，不存在时，返回 None 。

### func new()

```cangjie
static func new(): ValueListener<T>
```

功能：创建一个新的“值监听器”对象，不包含任何处理参数的闭包方法。

返回值：

- [ValueListener](unittest_mock_package_interfaces.md#interface-valuelistenert)\<T> - “值监听器”对象。

### func onEach((T) -> Unit)

```cangjie
static func onEach(callback: (T) -> Unit): ValueListener<T>
```

功能：创建一个新的“值监听器”对象，带有一个处理参数的闭包方法。

参数：

- callback: (T) ->[Unit](../../core/core_package_api/core_package_intrinsics.md#unit) - 处理参数值的闭包函数。

返回值：

- [ValueListener](unittest_mock_package_interfaces.md#interface-valuelistenert)\<T> - “值监听器”对象。
