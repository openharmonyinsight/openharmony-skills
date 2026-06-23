// Eval file for rule: 准确使用对仗词
// 反例1：有set无get
interface Window {
  setPreferredOrientation(orientation: Orientation): void;
  // 缺少 getPreferredOrientation(): Orientation;
}

// 反例2：对仗词不准确
interface Container {
  addChild(child: Component): void;
  deleteChild(child: Component): void;  // 应使用removeChild，与add对仗
}

// 反例3：对仗词混乱
interface Service {
  start(): void;
  end(): void;  // 与start对仗应为stop
}

// 反例4：对仗词缺失
interface View {
  show(): void;
  // 缺少 hide(): void;
}

// 反例5：对仗词不标准
interface Feature {
  enableFeature(): void;
  closeFeature(): void;  // 与enable对仗应为disable
}
