import { KeyCode } from '@kit.InputKit';

@Entry
@Component
struct VideoPlayPauseAdapterSample {
  @State playing: boolean = false;

  private togglePlay(): void {
    this.playing = !this.playing;
  }

  build() {
    Column() {
      Text(this.playing ? 'Playing' : 'Paused')
        .fontSize(22)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .onClick(() => this.togglePlay())
    .onKeyEvent((event?: KeyEvent) => {
      if (!event || event.type !== KeyType.Down) {
        return false;
      }
      if (event.keyCode === KeyCode.KEYCODE_SPACE || event.keyCode === KeyCode.KEYCODE_ENTER) {
        this.togglePlay();
        return true;
      }
      return false;
    })
    .focusable(true)
    .defaultFocus(true)
  }
}