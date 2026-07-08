// 'theme' key 的生产者。迁移相关组件时需判断：是否还有 V1 组件通过 @StorageLink 引用此 key；
// 若有，则保留此 V1 调用；当所有 decoratorUsage 都迁到 V2 后方可移除。
AppStorage.setOrCreate('theme', 'dark');
