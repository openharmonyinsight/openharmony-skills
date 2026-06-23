// Eval file for rule: 错误码的码值符合设计规范
  // 反例1：401异常原则上只用来做参数个数、参数类型校验，并且无需声明。不应该在声明中出现401异常。
  /**
   * Set the zlevel of current sub window.
   *
   * @param { int } zLevel - the zlevel of current sub window.
   * @returns { Promise<void> } - The promise returned by the function.
   * @throws { BusinessError } 401 - Parameter error. Possible cause: 1. Mandatory parameters are left unspecified;
   *                                                                  2. Incorrect parameter types;
   *                                                                  3. Parameter verification failed.
   * @throws { BusinessError } 801 - Capability not supported. Function setSubWindowZLevel can not work correctly due to limited device capabilities.
   * @throws { BusinessError } 1300002 - This window state is abnormal. Possible cause:
   *     The window is not created or destroyed.
   * @throws { BusinessError } 1300003 - This window manager service works abnormally.
   * @throws { BusinessError } 1300004 - Unauthorized operation. Possible cause:
   *     Invalid window type. Only non-modal subwindows are supported.
   * @throws { BusinessError } 1300009 - The parent window is invalid.
   * @syscap SystemCapability.Window.SessionManager
   * @atomicservice
   * @since 18 dynamic
   * @since 23 static
   */
  setSubWindowZLevel(zLevel: int): Promise<void>;

  // 反例2：异常没有声明错误码。
  /**
   * Sets name of the window.
   *
   * @permission ohos.permission.PRIVACY_WINDOW
   * @param { string } name - name of the window, only underscore and l‌alphanumeric characters ([A-Z][a-z][0-9]_) are
   *     accepted and must be less than 32 characters.
   * @throws { BusinessError } - The window state is abnormal.
   * @syscap SystemCapability.WindowManager.WindowManager.Core
   * @stagemodelonly
   * @since 10
   */
  setName(name: string): void;

  // 反例3：异常错误码不符合格式。
  /**
   * Sets name of the window.
   *
   * @permission ohos.permission.PRIVACY_WINDOW
   * @param { string } name - name of the window, only underscore and l‌alphanumeric characters ([A-Z][a-z][0-9]_) are
   *     accepted and must be less than 32 characters.
   * @throws { BusinessError } 1 - The window state is abnormal.
   * @syscap SystemCapability.WindowManager.WindowManager.Core
   * @stagemodelonly
   * @since 10
   */
  setName(name: string): void;

  // 反例4：业务相关异常使用了通用错误码。
  /**
   * Sets name of the window.
   *
   * @permission ohos.permission.PRIVACY_WINDOW
   * @param { string } name - name of the window, only underscore and l‌alphanumeric characters ([A-Z][a-z][0-9]_) are
   *     accepted and must be less than 32 characters.
   * @throws { BusinessError } 801 - The window state is abnormal.
   * @syscap SystemCapability.WindowManager.WindowManager.Core
   * @stagemodelonly
   * @since 10
   */
  setName(name: string): void;


  // 反例5：业务无关通用错误使用了业务自定义错误码。
  /**
   * Add device access permission.
   * The system application has access to the device by default, and calling this interface will not have any impact.
   *
   * @param { string } bundleName - refers to application that require access permissions. It cannot be empty.
   * @param { string } deviceName - device name defined by USBDevice.name. It cannot be empty.
   * @returns { boolean } value to indicate whether the permission is granted.
   * @throws { BusinessError } 22400099 - The caller is not a system application.
   * @syscap SystemCapability.USB.USBManager
   * @systemapi
   * @since 9 dynamiconly
   * @deprecated since 12
   * @useinstead ohos.usbManager/usbManager#addDeviceAccessRight
   */
  function addRight(bundleName: string, deviceName: string): boolean;
