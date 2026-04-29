import { KeyCode } from '@kit.InputKit';

@Entry
@Component
struct FocusNavigationExample {
  @State focusedIndex: number = 0;

  build() {
    Column() {
      ForEach([0, 1, 2, 3], (index: number) => {
        Button(`按钮 ${index}`)
          .focusable(true)
          .defaultFocus(index === 0)
          .tabIndex(index)
          .stateStyles({
            focused: {
              .backgroundColor('#007DFF')
              .border({ width: 2, color: '#FF0000' })
            }
          })
          .onFocus(() => {
            this.focusedIndex = index;
          })
          .onBlur(() => {
          })
          .onKeyEvent((event?: KeyEvent) => {
            if (event && event.type === KeyType.Down) {
              if (event.keyCode === KeyCode.KEYCODE_ENTER || 
                  event.keyCode === KeyCode.KEYCODE_SPACE) {
                console.log(`按钮 ${index} 被激活`);
                return true;
              }
            }
            return false;
          })
      })
    }
    .width('100%')
    .height('100%')
    .padding(16)
  }
}
