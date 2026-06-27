// Eval file for rule: 指针数组属性明确化
// 反例1：未说明是单元素还是数组
/**
 * @param data Data pointer.
 */
int32_t WriteData(char* data);

// 反例2：虽有count但未明确是否指向数组首地址
/**
 * @param p Info pointer.
 * @param count Count value.
 */
int32_t GetInfo(Info* p, int32_t count);

// 反例3：仅重复参数名未说明数组属性
/**
 * @param buffer Buffer.
 */
int32_t ProcessBuffer(void* buffer);

// 反例4：指针参数未说明指向对象类型
/**
 * @param handle Handle pointer.
 */
int32_t SetHandle(void* handle);

// 反例5：数组参数未说明边界
/**
 * @param items Items array.
 */
int32_t ProcessItems(Item* items);
