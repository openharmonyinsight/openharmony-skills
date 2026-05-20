# 数学基础运算示例

<!-- verify -->

```cangjie
import std.math.clamp
import std.math.gcd
import std.math.lcm
import std.math.rotate

// 范围截断示例
func clampTest() {
    let min: Float16 = -0.123
    let max: Float16 = 0.123
    let v: Float16 = 0.121
    let c = clamp(v, min, max)
    println("${c == v}")
    let min2: Float16 = -0.999
    let max2: Float16 = 10.123
    let v2: Float16 = 11.121
    let c2 = clamp(v2, min2, max2)
    println("${c2 == max2}")
    let min3: Float16 = -0.999
    let max3: Float16 = 10.123
    let v3: Float16 = -1.121
    let c3 = clamp(v3, min3, max3)
    println("${c3 == min3}")
}

// 求两个数的最大公约数
func gcdTest() {
    let c2 = gcd(0, -60)
    println("c2=${c2}")
    let c4 = gcd(-33, 27)
    println("c4=${c4}")
}

// 求两个数的最小公倍数
func lcmTest() {
    let a: Int8 = lcm(Int8(-3), Int8(5))
    println("a=${a}")
}

// 整数按二进制某一位前后翻转
func rotateTest() {
    let a: Int8 = rotate(Int8(92), Int8(4))
    println("a=${a}")

    let b: Int32 = rotate(Int32(1), Int8(4))
    println("b=${b}")
}

main(): Unit {
    println("/***********************    clampTest    **********************/")
    clampTest()
    println("/***********************    gcdTest    ************************/")
    gcdTest()
    println("/***********************    lcmTest    ************************/")
    lcmTest()
    println("/***********************    rotateTest    *********************/")
    rotateTest()
}
```

运行结果：

```text
/***********************    clampTest    **********************/
true
true
true
/***********************    gcdTest    ************************/
c2=60
c4=3
/***********************    lcmTest    ************************/
a=15
/***********************    rotateTest    *********************/
a=-59
b=16
```
