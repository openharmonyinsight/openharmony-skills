// Eval file for rule: 存根/空方法实现检测
// 反例1：空方法体 - 不使用参数
int32_t OnAccountsChanged(int32_t id) {
    return ERR_OK;  // Parameter 'id' completely ignored
}

// 反例2：空回调 - 忽略所有参数
void OnAccountsChanged(const std::vector<AppAccountInfo>& accounts) {}

// 反例3：方法明确标记为未实现
void CreateAccountImplicitly(const Options& options, Callback callback) {
    ACCOUNT_LOGE("CreateAccountImplicitly is not implemented");
}

// 反例4：TODO 占位符，没有实际逻辑
int32_t ProcessRequest(const Request& req) {
    // TODO: implement later
    return ERR_OK;
}

// 反例5：总是返回默认值，没有任何处理
int CalculateValue(const InputData& data) {
    return 0;
}

// 反例6：只记录日志，没有实际实现
int32_t UpdateConfig(const Config& config) {
    ACCOUNT_LOGW("UpdateConfig called");
    return ERR_OK;
}

// 反例7：参数被接受但从未使用
int32_t OnRequestRedirected(const AAFwk::Want& request) {
    return ERR_OK;  // 'request' completely ignored
}

// 反例8：多个参数被忽略
void Configure(const ConfigOptions& options, bool enable) {
    SetDefaultConfig();  // Both 'options' and 'enable' ignored
}
