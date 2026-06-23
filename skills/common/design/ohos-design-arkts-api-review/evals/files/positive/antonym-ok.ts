// Eval file for rule: 准确使用对仗词
// 正例1：get/set对仗
interface Window {
  getPreferredOrientation(): Orientation;
  setPreferredOrientation(orientation: Orientation): void;
}

// 正例2：add/remove对仗
interface Container {
  addChild(child: Component): void;
  removeChild(child: Component): void;
}

// 正例3：start/stop对仗
interface Service {
  start(): void;
  stop(): void;
}

// 正例4：show/hide对仗
interface View {
  show(): void;
  hide(): void;
}

// 正例5：enable/disable对仗
interface Feature {
  enableFeature(): void;
  disableFeature(): void;
}
