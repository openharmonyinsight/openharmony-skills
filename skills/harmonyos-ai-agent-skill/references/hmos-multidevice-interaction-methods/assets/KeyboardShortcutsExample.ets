/**
 * KeyboardShortcutsExample.ets
 * 键盘快捷键示例
 */

import { KeyCode } from '@kit.InputKit';

/**
 * 快捷键定义
 */
export interface ShortcutKey {
  key: KeyCode;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
  action: () => void;
  description?: string;
}

/**
 * 键盘快捷键管理器
 */
export class KeyboardShortcutManager {
  private shortcuts: ShortcutKey[] = [];
  private enabled: boolean = true;

  /**
   * 注册快捷键
   */
  register(shortcut: ShortcutKey): void {
    this.shortcuts.push(shortcut);
  }

  /**
   * 批量注册快捷键
   */
  registerAll(shortcuts: ShortcutKey[]): void {
    shortcuts.forEach(s => this.register(s));
  }

  /**
   * 注销快捷键
   */
  unregister(shortcut: ShortcutKey): void {
    const index = this.shortcuts.indexOf(shortcut);
    if (index > -1) {
      this.shortcuts.splice(index, 1);
    }
  }

  /**
   * 清空所有快捷键
   */
  clear(): void {
    this.shortcuts = [];
  }

  /**
   * 启用/禁用快捷键
   */
  setEnabled(enabled: boolean): void {
    this.enabled = enabled;
  }

  /**
   * 处理键盘事件
   * @returns 是否消费了事件
   */
  handleKeyEvent(event: KeyEvent): boolean {
    if (!this.enabled || event.type !== KeyType.Down) {
      return false;
    }

    for (const shortcut of this.shortcuts) {
      if (this.matchShortcut(event, shortcut)) {
        shortcut.action();
        return true;
      }
    }

    return false;
  }

  /**
   * 检查事件是否匹配快捷键
   */
  private matchShortcut(event: KeyEvent, shortcut: ShortcutKey): boolean {
    // 检查主键
    if (event.keyCode !== shortcut.key) {
      return false;
    }

    // 检查修饰键
    try {
      const altPressed = event?.getModifierKeyState?.(['Alt']);
      const ctrlPressed = event?.getModifierKeyState?.(['Ctrl']);
      const shiftPressed = event?.getModifierKeyState?.(['Shift']);

      return (shortcut.ctrl ?? false) === ctrlPressed &&
        (shortcut.shift ?? false) === shiftPressed &&
        (shortcut.alt ?? false) === altPressed;
    } catch (error) {
      // TODO: Implement error handling.
      return false
    }
  }

  /**
   * 获取所有已注册的快捷键
   */
  getShortcuts(): ShortcutKey[] {
    return [...this.shortcuts];
  }
}

export interface keyCallbacks {
  onEscape?: () => void;
  onEnter?: () => void;
  onBack?: () => void;
  onSearch?: () => void;
}

export interface ShortcutsCallbacks {
  onSave?: () => void;
  onCopy?: () => void;
  onPaste?: () => void;
  onCut?: () => void;
  onUndo?: () => void;
  onRedo?: () => void;
  onSelectAll?: () => void;
}

/**
 * 常用快捷键定义
 */
export class CommonShortcuts {
  /**
   * 获取编辑类快捷键
   */
  static getEditShortcuts(callbacks: ShortcutsCallbacks): ShortcutKey[] {
    const shortcuts: ShortcutKey[] = [];

    if (callbacks.onSave) {
      shortcuts.push({
        key: KeyCode.KEYCODE_S,
        ctrl: true,
        action: callbacks.onSave,
        description: '保存'
      });
    }

    if (callbacks.onCopy) {
      shortcuts.push({
        key: KeyCode.KEYCODE_C,
        ctrl: true,
        action: callbacks.onCopy,
        description: '复制'
      });
    }

    if (callbacks.onPaste) {
      shortcuts.push({
        key: KeyCode.KEYCODE_V,
        ctrl: true,
        action: callbacks.onPaste,
        description: '粘贴'
      });
    }

    if (callbacks.onCut) {
      shortcuts.push({
        key: KeyCode.KEYCODE_X,
        ctrl: true,
        action: callbacks.onCut,
        description: '剪切'
      });
    }

    if (callbacks.onUndo) {
      shortcuts.push({
        key: KeyCode.KEYCODE_Z,
        ctrl: true,
        action: callbacks.onUndo,
        description: '撤销'
      });
    }

    if (callbacks.onRedo) {
      shortcuts.push({
        key: KeyCode.KEYCODE_Z,
        ctrl: true,
        shift: true,
        action: callbacks.onRedo,
        description: '重做'
      });
    }

    if (callbacks.onSelectAll) {
      shortcuts.push({
        key: KeyCode.KEYCODE_A,
        ctrl: true,
        action: callbacks.onSelectAll,
        description: '全选'
      });
    }

    return shortcuts;
  }

  /**
   * 获取导航类快捷键
   */
  static getNavigationShortcuts(callbacks: keyCallbacks): ShortcutKey[] {
    const shortcuts: ShortcutKey[] = [];

    if (callbacks.onEscape) {
      shortcuts.push({
        key: KeyCode.KEYCODE_ESCAPE,
        action: callbacks.onEscape,
        description: '取消/关闭'
      });
    }

    if (callbacks.onEnter) {
      shortcuts.push({
        key: KeyCode.KEYCODE_ENTER,
        action: callbacks.onEnter,
        description: '确认'
      });
    }

    if (callbacks.onBack) {
      shortcuts.push({
        key: KeyCode.KEYCODE_BACK,
        action: callbacks.onBack,
        description: '返回'
      });
    }

    if (callbacks.onSearch) {
      shortcuts.push({
        key: KeyCode.KEYCODE_F,
        ctrl: true,
        action: callbacks.onSearch,
        description: '搜索'
      });
    }

    return shortcuts;
  }
}

/**
 * 使用示例:
 *
 * @Entry
 * @Component
* struct KeyboardExample {
 *   private shortcutManager: KeyboardShortcutManager = new KeyboardShortcutManager();
 *   private shortcutsCallbacks: ShortcutsCallbacks =  {};
 *
 *   aboutToAppear() {
 *     // 注册快捷键
 *     this.shortcutManager.registerAll(CommonShortcuts.getEditShortcuts(this.shortcutsCallbacks));
 *   }
 *
 *   build() {
 *     Column() {
 *       // 内容
 *     }
 *     .onKeyEvent((event: KeyEvent) => {
 *       this.shortcutManager.handleKeyEvent(event);
 *     })
 *   }
 * }
 */
