// Eval file for rule: 错误码的码值符合设计规范
  // 正例1：当display manager service异常属于业务逻辑相关的异常。错误码1400003，SysCap编号14，自定义号段00003，符合业务自定义错误码格式。
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

  // 正例2：当设备系统能力Capability不满足时，服务端无法获取USB设备列表，属于多设备相关的通用错误。错误码801符合错误码使用规范。
  /**
   * Obtains the USB device list.
   *
   * @returns { Array<Readonly<USBDevice>> } USB device list.
   * @throws { BusinessError } 801 - Capability not supported.
   * @syscap SystemCapability.USB.USBManager
   * @since 18 dynamic
   * @since 23 static
   */
  function getDevices(): Array<Readonly<USBDevice>>;

  // 正例2：当设备系统能力Capability不满足时，服务端无法获取USB设备列表，属于多设备相关的通用错误。错误码801符合错误码使用规范。
  /**
   * Obtains the USB device list.
   *
   * @returns { Array<Readonly<USBDevice>> } USB device list.
   * @throws { BusinessError } 801 - Capability not supported.
   * @syscap SystemCapability.USB.USBManager
   * @since 18 dynamic
   * @since 23 static
   */
  function getDevices(): Array<Readonly<USBDevice>>;

  // 正例3：801多设备（系统能力）相关，1300002（服务状态）、1300016（取值范围、格式校验）和业务逻辑相关，符合设计规范。1300004是未授权的操作，虽然看起来好像和权限有关，但这个实际上是业务逻辑上的授权，不是通用的@permission或@systemApi的权限检查错误，所以使用自定义错误码也是合理的。
  /**
   * Show window.
   *
   * @param { ShowWindowOptions } options - options for window show.
   * @returns { Promise<void> } Promise that returns no value.
   * @throws { BusinessError } 801 - Capability not supported. Function showWindow can not work correctly due to limited device capabilities.
   * @throws { BusinessError } 1300002 - This window state is abnormal.
   *     Possible cause: The window is not created or destroyed.
   * @throws { BusinessError } 1300004 - Unauthorized operation.
   *     Possible cause: Invalid window type. Modal subwindow and dialog window can not set focusOnShow.
   * @throws { BusinessError } 1300016 - Parameter validation error. Possible cause: 1. The value of the parameter is out of the allowed range;
   *                                                                                 2. The length of the parameter exceeds the allowed length;
   *                                                                                 3. The parameter format is incorrect.
   * @syscap SystemCapability.Window.SessionManager
   * @atomicservice
   * @since 20 dynamic
   * @since 23 static
   */
  showWindow(options: ShowWindowOptions): Promise<void>;
