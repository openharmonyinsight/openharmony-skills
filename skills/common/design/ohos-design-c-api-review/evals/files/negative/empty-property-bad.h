// Eval file for rule: 禁止创建空属性接口
// 反例1：预留属性，云侧当前未返回，使用void*类型无类型约束
typedef struct {
    const char* userId;
    const char* userName;
    // 后续新功能会使用，当前云侧未返回
    void* futureFeature;  // 问题：使用void*类型，无实际用途
} CloudResponse;

// 反例2：透传数据使用void*类型，无类型约束，端侧不做任何处理
typedef struct {
    int code;
    const char* message;
    // 透传云侧返回结果，当前无实际处理
    void* rawData;  // 问题：void*类型，透传无意义
} ServerResponse;

// 反例3：版本隔离预留属性，使用void*类型，当前端侧版本无实际处理逻辑
typedef struct {
    const char* version;
    void* data;  // 问题：void*类型，后续云侧要根据端侧版本做隔离
    // 当前端侧版本无实际处理逻辑
} VersionData;

// 反例4：为未来功能预留的空属性，使用void*类型，当前所有场景都无实际用途
typedef struct {
    bool enabled;
    // 预留字段，未来版本会使用
    void* reserved;     // 问题：预留属性，当前所有场景都无意义
    void* futureOption; // 问题：未知类型，无实际用途
} FeatureConfig;

// 反例5：多个预留字段，云侧当前未返回
typedef struct {
    const char* id;
    const char* name;
    // 以下为预留字段，云侧未返回
    void* reserved1;  // 问题：预留字段1
    void* reserved2;  // 问题：预留字段2
    void* reserved3;  // 问题：预留字段3
} UserDataBad;
