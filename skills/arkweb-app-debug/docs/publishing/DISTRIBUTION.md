# ArkWeb Debug Tool v1.0 - 分发指南

**版本**: 1.0 | **状态**: Production Ready | **依赖**: 零依赖 ✅

---

## 📦 分发方式速览

### 推荐方式：tar.gz 压缩包

**创建发布包**：

```bash
# 使用提供的脚本
cd arkweb-app-debug-skill/docs/publishing
./create-dist.sh

# 或手动创建
tar -czf arkweb-app-debug-skill-1.0.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='dist' \
    arkweb-app-debug-skill/
```

**用户使用**：

```bash
# 解压
tar -xzf arkweb-app-debug-skill-1.0.tar.gz
cd arkweb-app-debug-skill

# 直接运行（无需安装！）
./arkweb-app-debug start
```

---

## 🚀 快速分发步骤

### 1. 准备发布包

```bash
# 运行发布脚本
cd arkweb-app-debug-skill/docs/publishing
./create-dist.sh

# 生成的文件：
# dist/arkweb-app-debug-skill-1.0.tar.gz   (推荐)
# dist/arkweb-app-debug-skill-1.0.zip
```

### 2. 分发文件

选择一种方式：

- **GitHub Releases** - 上传到 Release 页面
- **文件共享** - 通过云盘、邮件等分享
- **内部分发** - 通过内部工具分发
- **Git 仓库** - 直接分享仓库地址

### 3. 用户接收后

```bash
# 解压
tar -xzf arkweb-app-debug-skill-1.0.tar.gz
cd arkweb-app-debug-skill

# 直接运行（无需任何安装！）
./arkweb-app-debug start

# 配置 MCP（一次性）
claude mcp add --transport stdio arkweb-devtools --scope user -- \
  npx chrome-devtools-mcp@latest -y \
  --browser-url=http://127.0.0.1:9222
```

---

## 📋 分发检查清单

### 发布前检查

- [ ] 版本号已更新 (VERSION, skill.json)
- [ ] 文档已更新 (README.md, CHANGELOG.md, RELEASE_NOTES.md)
- [ ] 发布注释已准备 (RELEASE_NOTES.md)
- [ ] 运行 `./create-dist.sh` 生成发布包
- [ ] 测试运行：`./arkweb-app-debug device list`
- [ ] 验证功能：`./arkweb-app-debug config show`
- [ ] 验证自动检测功能

### 发布包内容

```
arkweb-app-debug-skill/
├── README.md                   # 主文档
├── CHANGELOG.md                # 更新日志
├── RELEASE_NOTES.md            # 发布说明
├── LICENSE                     # MIT 许可证
├── skill.md                    # Skill 说明
├── skill.json                  # Skill 元数据
├── VERSION                     # 版本号 (1.0)
├── setup.py                    # 安装脚本（可选）
├── arkweb-app-debug                # Wrapper脚本（推荐使用）✨
├── arkweb_debug/               # 核心代码包
│   ├── __init__.py
│   ├── cli.py
│   ├── app/
│   │   └── manager.py
│   ├── config/
│   │   ├── detector.py         # 自动检测模块
│   │   └── manager.py
│   ├── device/
│   │   └── manager.py
│   ├── port/
│   │   └── manager.py
│   ├── session/
│   │   └── manager.py
│   └── utils/
│       ├── chrome.py
│       ├── hdc.py
│       └── logger.py
└── docs/                       # 参考文档
    ├── MCP_GUIDE.md            # MCP 使用指南
    ├── TROUBLESHOOTING.md      # 故障排除
    └── publishing/             # 发布相关
        ├── DISTRIBUTION.md
        └── create-dist.sh
```

**总计**: 约 20 个文件

---

## 🎯 用户安装提示

### 方式1：直接使用（推荐）✨

```bash
# 1. 解压
tar -xzf arkweb-app-debug-skill-1.0.tar.gz

# 2. 直接运行
cd arkweb-app-debug-skill
./arkweb-app-debug start

# 3. 配置 MCP（一次性）
claude mcp add --transport stdio arkweb-devtools --scope user -- \
  npx chrome-devtools-mcp@latest -y \
  --browser-url=http://127.0.0.1:9222
```

**优势**：
- ✅ 无需 pip install
- ✅ 无需任何依赖
- ✅ 下载即用
- ✅ 自动检测项目配置

### 方式2：安装到系统（可选）

如果希望在任意目录使用命令：

```bash
# 1. 解压并安装
tar -xzf arkweb-app-debug-skill-1.0.tar.gz
cd arkweb-app-debug-skill
pip3 install --user -e .

# 2. 全局使用
arkweb-app-debug start  # 任意目录可用
```

**注意**：pip install 仅为添加到 PATH，无需第三方依赖

---

## ⚡ 自动检测功能

工具会自动：
- ✓ 向上搜索 HarmonyOS 项目根目录（最多5层）
- ✓ 从 `AppScope/app.json5` 提取包名
- ✓ 查找 HAP 文件路径（`entry/build/.../*.hap`）
- ✓ 使用默认端口 9222（Chrome DevTools 标准）

**无需任何配置文件！**

---

## 📦 发布包验证

### 验证清单

解压后测试：

```bash
# 1. 进入目录
cd arkweb-app-debug-skill

# 2. 测试自动检测
./arkweb-app-debug config show

# 3. 测试设备列表
./arkweb-app-debug device list

# 4. 测试启动调试
./arkweb-app-debug start
```

### 预期输出

```bash
$ ./arkweb-app-debug config show
{
  "defaults": {
    "debug_port": 8888,
    "local_port_base": 9222,
    ...
  },
  "app": {
    "package": "com.example.arkwebtesting",
    "hap": "entry/build/default/outputs/default/entry-default-signed.hap"
  }
}

$ ./arkweb-app-debug device list
✓ Auto-detected bundle name: com.example.arkwebtesting
✓ Auto-detected HAP path: entry/build/default/outputs/default/entry-default-signed.hap
✓ Auto-detected modules: ['entry']
✓ Device listing works
```

---

## 📊 文件大小参考

| 项目 | 大小 |
|------|------|
| 源代码 | ~80 KB |
| 文档 | ~40 KB |
| 总计 | ~120 KB |
| tar.gz 压缩后 | ~30-40 KB |

---

## 📖 相关文档

- **README.md** - 主要文档
- **CHANGELOG.md** - 更新日志
- **RELEASE_NOTES.md** - 版本发布说明
- **docs/MCP_GUIDE.md** - MCP 使用指南
- **docs/TROUBLESHOOTING.md** - 故障排除

---

## 🔧 高级选项（可选）

### 环境变量配置

如果需要覆盖默认配置：

```bash
# 设置自定义端口
export ARKWEB_PORT=9223
./arkweb-app-debug start

# 设置 HDC 超时
export ARKWEB_HDC_TIMEOUT=15
./arkweb-app-debug start
```

### 命令行参数

```bash
# 指定项目路径
./arkweb-app-debug start --project /path/to/project

# 禁用自动检测
./arkweb-app-debug start --no-auto-detect

# 调试模式
./arkweb-app-debug start --debug
```

---

**版本**: 1.0 | **状态**: Production Ready | **依赖**: 零依赖 ✅
