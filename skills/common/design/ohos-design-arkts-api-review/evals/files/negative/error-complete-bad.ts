// Eval file for rule: 异常或者返回的错误定义完整
  // 反例1：查询接口，返回值并不包含null/undefined，并且也没有声明查询不到场景的异常，异常设计遗漏。
  /**
   * Obtains the query key of a contact based on a specified ID and holder.
   *
   * @permission ohos.permission.READ_CONTACTS
   * @param { number } id - Indicates the contact ID.
   * @param { Holder } holder - Indicates the contact holder.
   * If this parameter is null, the default holder is used for matching.
   * @returns { Promise<string> } Returns the query key of the contact.
   * @syscap SystemCapability.Applications.ContactsData
   * @since 7
   * @deprecated since 10
   * @useinstead contact.queryKey#queryKey
   */
  function queryKey(id: number, holder?: Holder): Promise<string>;

  // 反例2：系统接口，包含@systemApi标记，但没有声明系统权限校验相关异常（非系统应用调用的场景，应该抛出异常拒绝服务），异常设计遗漏。
  /**
   * Add device access permission.
   * The system application has access to the device by default, and calling this interface will not have any impact.
   *
   * @param { string } bundleName - refers to application that require access permissions. It cannot be empty.
   * @param { string } deviceName - device name defined by USBDevice.name. It cannot be empty.
   * @returns { boolean } value to indicate whether the permission is granted.
   * @throws { BusinessError } 401 - Parameter error. Possible causes:
   * <br>1.Mandatory parameters are left unspecified.
   * <br>2.Incorrect parameter types.
   * @syscap SystemCapability.USB.USBManager
   * @systemapi
   * @since 9 dynamiconly
   * @deprecated since 12
   * @useinstead ohos.usbManager/usbManager#addDeviceAccessRight
   */
  function addRight(bundleName: string, deviceName: string): boolean;

  // 反例3：需要权限的接口，具有@permission标记，但没有声明权限校验相关异常，异常设计遗漏。
  /**
   * Sets whether this window is in privacy mode.
   *
   * @permission ohos.permission.PRIVACY_WINDOW
   * @param { boolean } isPrivacyMode - Whether the window is in privacy mode. The value true means that
   *                                    the window is in privacy mode, and false means the opposite.
   * @param { AsyncCallback<void> } callback - Callback used to return the result.
   * @syscap SystemCapability.Ability.AbilityRuntime.Core
   * @stagemodelonly
   * @since 10 dynamic
   * @since 23 static
   */
  setWindowPrivacyMode(isPrivacyMode: boolean, callback: AsyncCallback<void>): void;

  // 反例4：参数存在取值范围、格式约束，但没有声明参数校验异常错误码或其他合适的异常能够匹配传错格式、超出取值范围的场景。
  /**
   * Sets name of the window.
   *
   * @permission ohos.permission.PRIVACY_WINDOW
   * @param { string } name - name of the window, only underscore and l‌alphanumeric characters ([A-Z][a-z][0-9]_) are
   *     accepted and must be less than 32 characters.
   * @syscap SystemCapability.WindowManager.WindowManager.Core
   * @stagemodelonly
   * @since 10
   */
  setName(name: string): void;


  // 反例5：非系统接口，不包含@systemApi标记，但声明了系统权限校验相关201异常。
  /**
   * Obtains the USB device list.
   *
   * @returns { Array<Readonly<USBDevice>> } USB device list.
   * @throws { BusinessError } 201 - Permission verification failed. The application does not have the permission required to call the API.
   * @throws { BusinessError } 801 - Capability not supported.
   * @syscap SystemCapability.USB.USBManager
   * @since 18 dynamic
   * @since 23 static
   */
  function getDevices(): Array<Readonly<USBDevice>>;

  // 反例6：无参数的接口，声明了参数校验异常。
  /**
   * Start the gallery sync task.
   *
   * @permission ohos.permission.CLOUDFILE_SYNC
   * @returns { Promise<void> } - Return Promise.
   * @throws { BusinessError } 201 - Permission verification failed.
   * @throws { BusinessError } 202 - The caller is not a system application.
   * @throws { BusinessError } 401 - The input parameter is invalid.Possible causes:Incorrect parameter types.
   * @throws { BusinessError } 22400001 - Cloud status not ready.
   * @throws { BusinessError } 22400002 - Network unavailable.
   * @throws { BusinessError } 22400003 - Low battery level.
   * @syscap SystemCapability.FileManagement.DistributedFileService.CloudSync.Core
   * @systemapi
   * @since 10 dynamic
   * @since 23 static
   */
  start(): Promise<void>;

  // 反例7：都是可选参数，但声明了参数校验异常并且异常描述中包含"Mandatory parameters are left unspecified"，和声明矛盾。
  /**
   * Resets a counter based on the specified label name.
   *
   * @param { string } [label] - Counter label name. The default value is default.
   * @throws { BusinessError } 401 - The parameter check failed. Possible causes:
   * <br> 1. Mandatory parameters are left unspecified.
   * <br> 2. Incorrect parameters types.
   * <br> 3. Parameter verification failed.
   * @static
   * @syscap SystemCapability.Utils.Lang
   * @crossplatform
   * @atomicservice
   * @since 12 dynamic
   */
  static countReset(label?: string): void;

  // 反例8：都是可选参数或不定参数，没有必选参数，但声明了参数校验异常并且异常描述中包含"Mandatory parameters are left unspecified"，和声明矛盾。
  /**
   * Prints assertion information.
   *
   * @param { Object } [value] - Result value. If value is false or left blank, the output starting with "Assertion failed" is printed. If value is true, no information is printed.
   * @param { Object[] } arguments - Other information to be printed when value is false. If this parameter is left blank, other information is not printed.
   * @throws { BusinessError } 401 - The parameter check failed. Possible causes:
   * <br> 1. Mandatory parameters are left unspecified.
   * <br> 2. Incorrect parameters types.
   * <br> 3. Parameter verification failed.
   * @static
   * @syscap SystemCapability.Utils.Lang
   * @crossplatform
   * @atomicservice
   * @since 12 dynamic
   */
  static assert(value?: Object, ...arguments: Object[]): void;

  // 反例9：唯一的boolean类型的参数不可能存在格式、取值范围等校验，但接口声明了参数校验的自定义异常。
  /**
   * Set whether restoration is enabled when the UIAbility is switched back from the background.
   *
   * @param { boolean } enabled - The flag that indicates whether restoration is enabled when the UIAbility is switched
   * back from the background.
   * @throws { BusinessError } 16000010 - The input parameter verification failed.
   * @throws { BusinessError } 16000011 - The context does not exist.
   * @syscap SystemCapability.Ability.AbilityRuntime.Core
   * @stagemodelonly
   * @atomicservice
   * @since 14 dynamic
   * @since 23 static
   */
  setRestoreEnabled(enabled: boolean): void;

  // 反例10：从声明上看，2501000完全覆盖了2501003的场景，并且没有讲明白两者区别。注意，单独列举一些明确的系统内部错误，同时又提供了一个更模糊的兜底的系统内部错误是允许的。
  /**
   * Enable Wi-Fi.
   *
   * @permission ohos.permission.SET_WIFI_INFO and (ohos.permission.MANAGE_WIFI_CONNECTION or
   *  ohos.permission.MANAGE_ENTERPRISE_WIFI_CONNECTION)
   * @throws {BusinessError} 201 - Permission denied.
   * @throws {BusinessError} 801 - Capability not supported.
   * @throws {BusinessError} 2501000 - Operation failed.
   * @throws {BusinessError} 2501003 - Operation failed because the service is being closed.
   * @syscap SystemCapability.Communication.WiFi.STA
   * @since 15 dynamic
   * @since 23 static
   */
  function enableWifi(): void;

  // 反例11：异常1400003设计杂糅，系统服务异常和找不到对应display应该是2种不相关、不同的异常。
  /**
   * Obtain the target display.
   *
   * @param { long } displayId Display id to query. This parameter should be greater than or equal to 0.
   * @returns { Display } the result of display
   * @throws { BusinessError } 1400003 - This display manager service works abnormally. Possible causes:
   *    Display is null, display id corresponding display does not exist.
   * @syscap SystemCapability.WindowManager.WindowManager.Core
   * @atomicservice
   * @since 12 dynamic
   * @since 23 static
   */
  function getDisplayByIdSync(displayId: long): Display;
