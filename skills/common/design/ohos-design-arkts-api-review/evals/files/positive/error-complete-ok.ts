// Eval file for rule: 异常或者返回的错误定义完整
  // 正例1：当display manager service异常时，无法判断屏幕是否可折叠。异常设计合理。
  /**
   * Check whether the device is foldable.
   *
   * @returns { boolean } true means the device is foldable.
   * @throws { BusinessError } 1400003 - This display manager service works abnormally.
   * @syscap SystemCapability.Window.SessionManager
   * @crossplatform
   * @atomicservice
   * @since 20 dynamic
   * @since 23 static
   */
  function isFoldable(): boolean;
