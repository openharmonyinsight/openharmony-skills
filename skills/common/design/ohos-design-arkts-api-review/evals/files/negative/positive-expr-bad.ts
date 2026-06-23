// Eval file for rule: 命名使用肯定表达式
// 反例1：isNot* 形式的否定表达
interface FeatureState {
  isNotEnabled: boolean;      // 错误：应改为 isDisabled
  isNotValid: boolean;        // 错误：应改为 isInvalid
  isNotShown: boolean;        // 错误：应改为 isHidden
  isNotOpen: boolean;          // 错误：应改为 isClosed
}

// 反例2：isUn* 形式可改为更清晰肯定表达的命名
interface ResourceStatus {
  isUnavailable: boolean;     // 错误：应改为 isAvailable，语义更清晰（"是否可用"）
  isUnreachable: boolean;     // 错误：应改为 isReachable，语义更清晰
}

// 反例3：函数命名使用否定表达
function notEnabled(): boolean { }       // 错误：应改为 isDisabled 或 isEnabled
