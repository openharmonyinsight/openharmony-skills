# ohos-test-arkts-xts-generation 快速配置

## 前置条件

| 依赖 | 必需 | 说明 |
|------|:----:|------|
| XTS 测试仓库 | 是 | 如 `D:\xts_acts_0414` |
| SDK 接口定义 | 是 | 如 `D:\interface_sdk-js\ets` |
| DevEco Studio | 推荐 | 提供 Node.js、Java、hvigor |
| APICoverageDetector | 可选 | 覆盖率扫描工具，仅 Windows |

## 配置方法

### 1. 安装技能

将技能目录放到工具的 skills 路径下：

- opencode: `{用户主目录}\.opencode\skills\ohos-test-arkts-xts-generation\`
- Claude Code: `{用户主目录}\.claude\skills\ohos-test-arkts-xts-generation\`

### 2. 首次使用时提供路径

首次使用时技能会自动创建配置文件并询问路径：

**Windows 示例**：
```
用户：帮我为 media.createAVRecorder() 生成XTS测试用例，
     目标测试套是 D:\xts_acts_0414\multimedia\media\，语法类型是ets1.1动态语法

技能：我需要一些环境信息来配置工具：

      必填：
      1. XTS 测试仓库路径（如 D:\xts_acts_0414）          ← 从你的消息中自动提取
      2. SDK 接口定义路径（如 D:\interface_sdk-js\ets）

      可选（推荐填写，可解锁编译验证和覆盖率扫描功能）：
      3. DevEco Studio 安装路径（填后自动配置编译环境）
      4. APICoverageDetector 安装路径（用于覆盖率扫描）
      5. 静态编译 Hvigor 路径（仅 ArkTS-Sta 需要）
      6. 文档路径

用户：SDK 在 D:\interface_sdk-js\ets，DevEco Studio 在 D:\DevEco Studio

技能：✅ 配置完成，已自动推导 hvigor/Java/Node.js 路径。
```

**Linux 示例**：
```
用户：帮我为 ability 模块生成XTS测试，OH 根目录是 /home/user/openharmony

技能：已从 OH_ROOT 自动推导 XTS/SDK/文档路径，配置完成。
```

也可以手动创建：将 `.oh-xts-config.example.json` 复制为 `.oh-xts-config.json` 并填写路径。

## 快速测试

```
帮我为 multimedia 模块的 media.createAVRecorder() 方法生成XTS测试用例，
目标测试套是 D:\xts_acts_0414\multimedia\media\，语法类型是ets1.1动态语法
```

## 常见问题

**没有 APICoverageDetector？** 不影响使用，技能会提示选择跳过扫描或提供扫描结果。

**如何使用覆盖率扫描功能？** 需要准备两样东西：
1. **APICoverageDetector 工具**：仅支持 Windows，配置 `scan_tool_root` 路径即可
2. **ohos-sdk-full SDK 包**：从日构建下载 `ohos-sdk-full_Dyn_Sta`，解压后将其 `ets` 目录配置为 `sdk_path`。下载地址：https://dcp.openharmony.cn/workbench/cicd/dailybuild/detail/component

> **注意**：日构建 SDK 解压后 `ets` 目录下为 `dynamic/` 和 `static/`，扫描环境搭建时 `manage_scan_env.py` 会自动将其重命名为 `ets1.1/` 和 `ets1.2/`（APICoverageDetector 尚未适配 dynamic/static 路径命名）。

**ets_version 怎么选？** 默认 `["ets1.1"]`（动态语法）。需要静态语法时改为 `["ets1.2"]`。
