// Eval file for rule: 声明式风格的函数名称可以使用名词
// 正例1：声明式UI组件
@Component
struct MyComponent {
  build() {
    Column() {
      Text('Hello')
      Button('Click')
    }
  }
}

// 正例2：声明式属性设置（链式调用）
interface Text {
  id(value: string): Text;
  width(value: number): Text;
  height(value: number): Text;
  color(value: string): Text;
  fontSize(value: number): Text;
}

// 正例3：Builder模式
interface DialogBuilder {
  title(value: string): DialogBuilder;
  message(value: string): DialogBuilder;
  positiveButton(text: string): DialogBuilder;
  negativeButton(text: string): DialogBuilder;
  build(): Dialog;
}

// 正例4：声明式配置
interface Animation {
  duration(value: number): Animation;
  delay(value: number): Animation;
  easing(value: Easing): Animation;
  repeat(value: number): Animation;
}

// 正例5：链式声明
/**
 * Id. User can set an id to the component to identify it.
 *
 * @param { string } value
 * @returns { T }
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform
 * @form
 * @atomicservice
 * @since 11
 */
id(value: string): T;
