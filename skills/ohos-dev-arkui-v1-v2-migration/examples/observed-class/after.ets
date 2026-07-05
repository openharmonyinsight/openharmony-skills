// V2 示例：嵌套数据对象 — @ObservedV2 / @Trace
// 迁移要点：
//   1. @Observed → @ObservedV2（本身无观察能力，需配合 @Trace）
//   2. @Track → @Trace（直接替换）
//   3. @ObjectLink 子组件分解不再需要，@Trace 支持任意深度观测
//   4. $$ → !! 语法替换
//   5. 组件大幅简化：三层嵌套无需拆分子组件

@ObservedV2
class City {
  @Trace public name: string = ''
  @Trace public zipCode: string = ''

  constructor(name: string, zipCode: string) {
    this.name = name
    this.zipCode = zipCode
  }
}

@ObservedV2
class Address {
  @Trace public street: string = ''
  @Trace public city: City = new City('', '')

  constructor(street: string, city: City) {
    this.street = street
    this.city = city
  }
}

@ObservedV2
class UserProfile {
  @Trace public name: string = ''
  @Trace public age: number = 0
  @Trace public address: Address = new Address('', new City('', ''))

  constructor(name: string, age: number, address: Address) {
    this.name = name
    this.age = age
    this.address = address
  }
}

// ============ V2 无需逐层拆分，单组件直接观测任意深度属性 ============

@Entry
@ComponentV2
struct ProfilePage {
  @Local user: UserProfile = new UserProfile(
    'Alice', 28,
    new Address('123 Main St', new City('Shanghai', '200000'))
  )

  build() {
    Scroll() {
      Column({ space: 15 }) {
        Text('User Profile')
          .fontSize(24)
          .fontWeight(FontWeight.Bold)

        // 直接观察 user.name
        TextInput({ text: this.user.name!!, placeholder: 'Name' })
          .width('100%')
        // 直接观察 user.age
        TextInput({ text: this.user.age.toString()!!, placeholder: 'Age' })
          .width('100%')
          .type(InputType.Number)

        // 地址区域：直接观察 user.address.street
        Column({ space: 8 }) {
          Text('Address')
            .fontSize(16)
            .fontWeight(FontWeight.Medium)
          TextInput({ text: this.user.address.street!!, placeholder: 'Street' })
            .width('100%')
          // 直接观察 user.address.city.name 和 user.address.city.zipCode
          // V1 中这需要 CityView 子组件 + @ObjectLink，V2 不再需要
          TextInput({ text: this.user.address.city.name!!, placeholder: 'City name' })
            .width('100%')
          TextInput({ text: this.user.address.city.zipCode!!, placeholder: 'Zip code' })
            .width('100%')
        }

        // 调试：显示完整信息（所有属性变化都会被 @Trace 自动感知）
        Divider()
        Text(`Name: ${this.user.name}, Age: ${this.user.age}`)
          .fontSize(14)
          .fontColor('#666')
        Text(`Street: ${this.user.address.street}`)
          .fontSize(14)
          .fontColor('#666')
        Text(`City: ${this.user.address.city.name}, Zip: ${this.user.address.city.zipCode}`)
          .fontSize(14)
          .fontColor('#666')
      }
      .padding(20)
    }
    .width('100%')
    .height('100%')
  }
}
