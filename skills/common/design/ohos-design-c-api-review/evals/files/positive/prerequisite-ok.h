// Eval file for rule: 说明前置依赖关系和环境要求
// 正例1：说明前置调用要求
/**
 * Before using APIs in this header file, you need to call the HMS_XEG_GetString to query
 * whether the feature is supported.
 */

// 正例2：说明前置检查要求
/**
 * need to call HMS_XEG_EnumerateDeviceExtensionProperties to check whether the HPS feature
 * extension to be used is supported.
 */

// 正例3：说明前置条件
/**
 * Before calling this API, you need to apply for the workspace memory required by the executor.
 */
int32_t ExecuteOperation(Executor* executor);

// 正例4：说明前置设置要求
/**
 * Before calling this API, call HMS_HiAISingleOpTensor_CreateFromTensorDesc or
 * HMS_HiAISingleOpTensor_Create to create an input tensor.
 */
int32_t ProcessTensor(Tensor* tensor);
