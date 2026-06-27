// Eval file for rule: 说明和其他API配合制约关系
// 正例1：说明资源释放配合关系
/**
 * The caller is responsible for destroying the returned object by calling
 * OH_Ability_DestroyChildProcessConfigs to avoid memory leaks.
 */
ChildProcessConfig* OH_Ability_CreateChildProcessConfigs(void);

// 正例2：说明调用顺序要求
/**
 * @note This method must be called before the show method.
 */
int OH_Dialog_SetContent(ArkUI_NodeHandle dialog, ArkUI_NodeHandle content);

// 正例3：说明内存释放要求
/**
 * When you no longer use the HiAI_SingleOpTensor object, destroy it by calling
 * HMS_HiAISingleOpTensor_Destroy.
 */
HiAI_SingleOpTensor* CreateTensor(void);

// 正例4：说明释放方法
/**
 * instead call OH_AudioSessionManager_ReleaseDevices to release the DeviceDescriptor array
 */
int32_t OH_AudioSessionManager_GetDevices(AudioDeviceDescriptor** devices, int32_t* count);
