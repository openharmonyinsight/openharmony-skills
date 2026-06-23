// Eval file for rule: 禁止创建空属性接口
/**
 * 云响应接口 - 反例
 *
 * 反例说明：包含空属性问题
 * - futureFeature: 空属性类型 - any类型，云侧当前未返回，为未来功能预留但当前无实际用途
 *
 * 空属性问题：预留属性，云侧当前未返回，使用any类型无类型约束
 * 建议修改：待云侧实现该功能后，定义明确类型再添加此属性
 */
interface CloudResponse {
  userId: string;
  userName: string;
  // 后续新功能会使用，当前云侧未返回
  futureFeature?: any;  // 问题：使用any类型，无实际用途
}

/**
 * 服务器响应接口 - 反例
 *
 * 反例说明：包含空属性问题
 * - rawData: 空属性类型 - unknown类型，透传云侧返回结果但当前无实际处理
 *
 * 空属性问题：透传数据使用unknown类型，无类型约束，端侧不做任何处理
 * 建议修改：如需透传，应定义具体类型或使用泛型；如当前无用途，应删除此属性
 */
interface ServerResponse {
  code: number;
  message: string;
  // 透传云侧返回结果，当前无实际处理
  rawData?: unknown;  // 问题：unknown类型，透传无意义
}

/**
 * 版本数据接口 - 反例
 *
 * 反例说明：包含空属性问题
 * - data: 空属性类型 - any类型，后续云侧要根据端侧版本做隔离，当前端侧版本无实际处理
 *
 * 空属性问题：版本隔离预留属性，使用any类型，当前端侧版本无实际处理逻辑
 * 建议修改：定义具体的版本数据类型，或待功能实现后再添加此属性
 */
interface VersionData {
  version: string;
  data: any;  // 问题：any类型，后续云侧要根据端侧版本做隔离
  // 当前端侧版本无实际处理逻辑
}

/**
 * 功能配置接口 - 反例
 *
 * 反例说明：包含空属性问题
 * - reserved: 空属性类型 - any类型，预留字段，当前所有场景都无意义
 * - futureOption: 空属性类型 - unknown类型，未知类型，无实际用途
 *
 * 空属性问题：为未来功能预留的空属性，使用any/unknown类型，当前所有场景都无实际用途
 * 建议修改：待功能实现时再添加这些属性，并定义明确类型
 */
interface FeatureConfig {
  enabled: boolean;
  // 预留字段，未来版本会使用
  reserved?: any;  // 问题：预留属性，当前所有场景都无意义
  futureOption?: unknown;  // 问题：未知类型，无实际用途
}

/**
 * 用户数据接口 - 反例
 *
 * 反例说明：包含空属性问题
 * - reserved1: 空属性类型 - any类型，预留字段，云侧未返回
 * - reserved2: 空属性类型 - any类型，预留字段，云侧未返回
 * - reserved3: 空属性类型 - unknown类型，预留字段，云侧未返回
 *
 * 空属性问题：多个预留字段，使用any/unknown类型，云侧当前未返回
 * 建议修改：删除所有无用的预留字段，待功能实现后再添加
 */
interface UserData {
  id: string;
  name: string;
  // 以下为预留字段，云侧未返回
  reserved1?: any;  // 问题：预留字段1
  reserved2?: any;  // 问题：预留字段2
  reserved3?: unknown;  // 问题：预留字段3
}

/**
 * API响应接口 - 反例
 *
 * 反例说明：包含空属性问题
 * - data: 空对象类型 - 无任何属性的空对象，仅作为占位符
 *
 * 空属性问题：使用空对象类型作为属性，无实际属性，仅作为占位符
 * 建议修改：定义具体的data类型，或待功能实现后再定义此属性
 */
interface ApiResponse {
  code: number;
  data: {
    // 空对象，仅作为占位符
  };  // 问题：空对象类型，无实际属性
}
