# Linux 编译环境准备

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载（用户要求准备 Linux 编译环境时加载）
> - 适用范围：Linux 环境下的 OpenHarmony XTS 测试工程编译
> - 平台：Linux
> - 依赖：无
> - 相关：`build_workflow_linux.md`（完整的编译工作流）

> **使用说明**
>
> 当用户要求准备 Linux 编译环境时，加载此模块。
> 此模块包含环境准备的全部内容，从 `build_workflow_linux.md` 中抽取。

---

## 一、环境准备概述

在 Linux 环境下编译 OpenHarmony XTS 测试工程之前，需要准备相应的编译环境和工具链。

### 1.1 准备内容

- **系统要求** - 操作系统版本要求
- **工具链安装** - Node.js、npm、Python、Git
- **SDK 下载** - OpenHarmony 预编译工具链
- **环境验证** - 检查所有工具是否正确安装

---

## 二、环境要求

### 2.1 操作系统

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Operating System | Ubuntu 18.04+ / OpenEuler 20.03+ | Linux 编译环境 |

**推荐配置**：
- Ubuntu 20.04 LTS
- OpenEuler 22.03 LTS
- 4GB+ 内存
- 20GB+ 可用磁盘空间

### 2.2 开发工具

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Node.js | 14.x+ | 推荐 16.x 或更新版本 |
| npm | 6.x+ | 随 Node.js 安装 |
| Python | 3.x | 构建脚本依赖 |
| Git | 2.x | 代码管理 |

---

## 三、工具链安装

### 3.1 检查当前环境

在开始安装之前，先检查当前系统已有的工具：

```bash
# 检查 Node.js
node --version

# 检查 npm
npm --version

# 检查 Python
python3 --version

# 检查 Git
git --version
```

### 3.2 安装 Node.js 和 npm

#### 方式 1：使用 NodeSource 仓库（推荐）

```bash
# 安装 Node.js 16.x
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

#### 方式 2：使用 nvm（Node Version Manager）

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 重新加载 shell 配置
source ~/.bashrc

# 安装最新 LTS 版本的 Node.js
nvm install --lts
nvm use --lts

# 验证安装
node --version
npm --version
```

#### 方式 3：使用系统包管理器

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nodejs npm

# OpenEuler
sudo dnf install nodejs npm
```

**更新到最新版**（如果版本过旧）：
参考 [更新 node 和 npm 到最新版](https://www.jianshu.com/p/3afb8f7dad3b)

### 3.3 安装 Python

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# OpenEuler
sudo dnf install python3 python3-pip

# 验证安装
python3 --version
pip3 --version
```

### 3.4 安装 Git

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install git

# OpenEuler
sudo dnf install git

# 验证安装
git --version
```

### 3.5 配置 Git（可选）

```bash
# 配置用户名
git config --global user.name "Your Name"

# 配置邮箱
git config --global user.email "your.email@example.com"

# 验证配置
git config --list
```

---

## 四、SDK 下载

### 4.1 使用预编译下载脚本

OpenHarmony 提供了 `prebuilts_download.sh` 脚本来下载必要的 SDK 和工具链：

```bash
# 在 OpenHarmony 代码根目录执行
cd /path/to/openharmony
./prebuilts_download.sh
```

### 4.2 脚本说明

`prebuilts_download.sh` 会下载以下内容：

- **编译工具链** - GCC、LLVM 等
- **预编译库** - 系统库和框架
- **测试工具** - XTS 测试框架依赖
- **签名工具** - HAP 签名相关工具

### 4.3 下载位置

下载的文件通常位于：

```
prebuilts/
├── build-tools/      # 编译工具
├── clang/            # Clang 工具链
├── gcc/              # GCC 工具链
└── ...               # 其他预编译工具
```

### 4.4 常见问题

**Q: 下载速度慢怎么办？**

A: 可以尝试以下方法：
1. 使用国内镜像源
2. 使用代理
3. 分批手动下载

**Q: 下载失败怎么办？**

A: 检查网络连接和磁盘空间，然后重新运行脚本。

---

## 五、环境验证

### 5.1 工具链验证

```bash
# 创建验证脚本
cat > verify_env.sh << 'EOF'
#!/bin/bash

echo "=== 编译环境验证 ==="
echo ""

# 检查 Node.js
echo -n "Node.js: "
if command -v node &> /dev/null; then
    node --version
else
    echo "❌ 未安装"
fi

# 检查 npm
echo -n "npm: "
if command -v npm &> /dev/null; then
    npm --version
else
    echo "❌ 未安装"
fi

# 检查 Python
echo -n "Python: "
if command -v python3 &> /dev/null; then
    python3 --version
else
    echo "❌ 未安装"
fi

# 检查 Git
echo -n "Git: "
if command -v git &> /dev/null; then
    git --version
else
    echo "❌ 未安装"
fi

echo ""
echo "=== 验证完成 ==="
EOF

# 运行验证脚本
chmod +x verify_env.sh
./verify_env.sh
```

### 5.2 PATH 验证

```bash
# 检查 Node.js 和 npm 是否在 PATH 中
which node
which npm
which python3
which git
```

### 5.3 权限验证

```bash
# 检查是否有写权限（编译时需要）
test -w /path/to/openharmony && echo "✅ 有写权限" || echo "❌ 无写权限"
```

---

## 六、环境配置（可选）

### 6.1 配置 npm 镜像（国内用户）

```bash
# 使用淘宝镜像
npm config set registry https://registry.npmmirror.com

# 验证配置
npm config get registry
```

### 6.2 配置缓存目录

```bash
# 设置 npm 缓存目录（避免权限问题）
npm config set cache ~/.npm-cache

# 验证配置
npm config get cache
```

### 6.3 配置环境变量

如果某些工具不在标准路径，可以添加到 PATH：

```bash
# 编辑 ~/.bashrc
echo 'export PATH=$PATH:/custom/path/to/tools' >> ~/.bashrc

# 重新加载配置
source ~/.bashrc
```

---

## 七、故障排查

### 7.1 Node.js 版本过低

**现象**：
```
error: Node version too old
```

**解决方案**：
```bash
# 使用 nvm 安装新版本
nvm install 16
nvm use 16

# 或使用 NodeSource 仓库安装
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### 7.2 权限问题

**现象**：
```
Error: EACCES: permission denied
```

**解决方案**：
```bash
# 方案 1：使用 sudo（不推荐）
sudo npm install -g package-name

# 方案 2：修复 npm 权限（推荐）
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

### 7.3 SDK 下载失败

**现象**：
```
error: failed to download prebuilts
```

**解决方案**：
```bash
# 检查网络连接
ping -c 4 google.com

# 检查磁盘空间
df -h

# 重新下载
./prebuilts_download.sh
```

### 7.4 工具链不兼容

**现象**：
```
error: incompatible toolchain version
```

**解决方案**：
```bash
# 检查 OpenHarmony 文档中的版本要求
# 安装指定版本的工具链

# 例如：安装 Node.js 14.x
nvm install 14
nvm use 14
```

---

## 八、最佳实践

### 8.1 版本管理

```bash
# 使用 nvm 管理 Node.js 版本
nvm install 14
nvm install 16
nvm use 16  # 默认使用 16

# 设置默认版本
nvm alias default 16
```

### 8.2 环境隔离

```bash
# 为不同项目使用不同的 Node.js 版本
cd project1
nvm use 14

cd project2
nvm use 16
```

### 8.3 定期更新

```bash
# 更新 npm
npm install -g npm@latest

# 更新 Node.js
nvm install --lts
nvm use --lts
```

---

## 九、检查清单

在开始编译之前，确保完成以下检查：

- [ ] 操作系统版本符合要求（Ubuntu 18.04+ / OpenEuler 20.03+）
- [ ] Node.js 版本 >= 14.x
- [ ] npm 版本 >= 6.x
- [ ] Python 3.x 已安装
- [ ] Git 2.x 已安装
- [ ] 已运行 `prebuilts_download.sh` 下载 SDK
- [ ] 所有工具都在 PATH 中
- [ ] 有足够的磁盘空间（20GB+）
- [ ] 有 OpenHarmony 代码库的写权限

---

## 十、参考资源

### 10.1 官方文档

- [OpenHarmony 编译环境准备](https://docs.openharmony.cn/)
- [Node.js 官方网站](https://nodejs.org/)
- [nvm 文档](https://github.com/nvm-sh/nvm)

### 10.2 相关工具

- [NodeSource](https://github.com/nodesource/distributions) - Node.js 安装脚本
- [npm 文档](https://docs.npmjs.com/)
- [Git 官方文档](https://git-scm.com/doc)

### 10.3 社区资源

- [更新 node 和 npm 到最新版](https://www.jianshu.com/p/3afb8f7dad3b)
- [OpenHarmony 社区](https://www.openharmony.cn/)

---

## 十一、版本历史

- **v1.0.0** (2026-02-06): 从 `build_workflow_linux.md` 中抽取环境准备相关内容，创建独立模块
