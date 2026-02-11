/**
 * Component.onClick 测试用例示例
 *
 * 测试文件: Component.onClick.test.ets
 * 测试对象: Component.onClick() 方法
 * 测试环境: OpenHarmony API 10+
 */

import { describe, it, expect } from '@ohos/hypium';
import { TestType, Level, Size } from '@ohos/hypium';
import { Component } from '@kit.ArkUI';

export default function testSuite() {
  describe('Component.onClick', () => {

    /**
     * @tc.name onClickNormal001
     * @tc.number SUB_ARKUI_COMPONENT_ONCLICK_PARAM_001
     * @tc.desc 测试 Component 的 onClick 方法 - 正常点击场景.
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL3
     */
    it('onClickNormal001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
      let component = new Component();
      let clickCount = 0;

      // 设置 onClick 回调
      component.onClick = () => {
        clickCount++;
        return true;
      };

      // 触发点击事件（模拟）
      const result = component.onClick();
      expect(result).assertEqual(true);
      expect(clickCount).assertEqual(1);
    });

    /**
     * @tc.name onClickNullCallback002
     * @tc.number SUB_ARKUI_COMPONENT_ONCLICK_PARAM_002
     * @tc.desc 测试 Component 的 onClick 方法 - 空回调场景.
     * @tc.type FUNCTION
     * @tc.size SMALLTEST
     * @tc.level LEVEL3
     */
    it('onClickNullCallback002', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL3, () => {
      let component = new Component();

      // 不设置 onClick 回调
      expect(component.onClick).toBeUndefined();
    });

    /**
     * @tc.name onClickMultiple003
     * @tc.number SUB_ARKUI_COMPONENT_ONCLICK_PARAM_003
     * @tc.desc 测试 Component 的 onClick 方法 - 多次点击场景.
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL3
     */
    it('onClickMultiple003', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
      let component = new Component();
      let clickCount = 0;

      // 设置 onClick 回调
      component.onClick = () => {
        clickCount++;
        return clickCount <= 10;
      };

      // 模拟多次点击
      for (let i = 0; i < 10; i++) {
        const result = component.onClick();
        expect(result).assertEqual(true);
      }

      expect(clickCount).assertEqual(10);
    });

    /**
     * @tc.name onClickWithEventObject004
     * @tc.number SUB_ARKUI_COMPONENT_ONCLICK_PARAM_004
     * @tc.desc 测试 Component 的 onClick 方法 - 带事件对象场景.
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL3
     */
    it('onClickWithEventObject004', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL3, () => {
      let component = new Component();
      let capturedEvent: any = null;

      // 设置 onClick 回调，捕获事件对象
      component.onClick = (event: any) => {
        capturedEvent = event;
        return true;
      };

      // 模拟点击事件
      const mockEvent = { x: 100, y: 200, timestamp: Date.now() };
      const result = component.onClick(mockEvent);

      expect(result).assertEqual(true);
      expect(capturedEvent).not.toBeNull();
      expect(capturedEvent.x).assertEqual(100);
      expect(capturedEvent.y).assertEqual(200);
    });

    /**
     * @tc.name onClickReturnFalse005
     * @tc.number SUB_ARKUI_COMPONENT_ONCLICK_PARAM_005
     * @tc.desc 测试 Component 的 onClick 方法 - 返回 false 场景.
     * @tc.type FUNCTION
     * @tc.size SMALLTEST
     * @tc.level LEVEL3
     */
    it('onClickReturnFalse005', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL3, () => {
      let component = new Component();

      // 设置 onClick 回调，返回 false
      component.onClick = () => {
        return false;
      };

      const result = component.onClick();
      expect(result).assertEqual(false);
    });

  });
}
