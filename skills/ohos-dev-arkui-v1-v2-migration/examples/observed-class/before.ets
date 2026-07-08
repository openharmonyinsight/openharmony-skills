// V1 示例：嵌套数据对象 — @Observed / @ObjectLink / @Track
// 场景：用户信息编辑页，嵌套 Address → City，V1 需要逐层拆分子组件才能观测深层属性

@Observed
class City {
  @Track public name: string = ''
  @Track public zipCode: string = ''

  constructor(name: string, zipCode: string) {
    this.name = name
    this.zipCode = zipCode
  }
}

@Observed
class Address {
  @Track public street: string = ''
  @Track public city: City = new City('', '')

  constructor(street: string, city: City) {
    this.street = street
    this.city = city
  }
}

@Observed
class UserProfile {
  @Track public name: string = ''
  @Track public age: number = 0
  @Track public address: Address = new Address('', new City('', ''))

  constructor(name: string, age: number, address: Address) {
    this.name = name
    this.age = age
    this.address = address
  }
}

// ============ V1 需要逐层拆分子组件 ============

// 第三层：CityView 观察 city.name 和 city.zipCode
@Component
struct CityView {
  @ObjectLink city: City

  build() {
    Column({ space: 5 }) {
      Text(`City: ${this.city.name}`)
        .fontSize(14)
      TextInput({ text: $$this.city.name, placeholder: 'City name' })
        .width('100%')
      TextInput({ text: $$this.city.zipCode, placeholder: 'Zip code' })
        .width('100%')
    }
  }
}

// 第二层：AddressView 观察 address.street，传递 city 给 CityView
@Component
struct AddressView {
  @ObjectLink address: Address

  build() {
    Column({ space: 8 }) {
      Text('Address')
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
      TextInput({ text: $$this.address.street, placeholder: 'Street' })
        .width('100%')
      CityView({ city: this.address.city })
    }
  }
}

// 顶层：ProfileView 观察 user.name / user.age，传递 address 给 AddressView
@Entry
@Component
struct ProfilePage {
  @State user: UserProfile = new UserProfile(
    'Alice', 28,
    new Address('123 Main St', new City('Shanghai', '200000'))
  )

  build() {
    Scroll() {
      Column({ space: 15 }) {
        Text('User Profile')
          .fontSize(24)
          .fontWeight(FontWeight.Bold)

        TextInput({ text: $$this.user.name, placeholder: 'Name' })
          .width('100%')
        TextInput({ text: $$this.user.age.toString(), placeholder: 'Age' })
          .width('100%')
          .type(InputType.Number)

        AddressView({ address: this.user.address })

        // 调试：显示完整信息
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
