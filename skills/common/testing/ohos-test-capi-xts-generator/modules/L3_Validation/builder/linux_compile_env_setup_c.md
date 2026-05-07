# Linux CAPI 编译环境准备

> **模块信息**
> - 层级：L3_Validation
> - 优先级：按需加载（用户要求准备 Linux CAPI 编译环境时加载）
> - 适用范围：Linux 环境下的 OpenHarmony CAPI XTS 测试工程编译
> - 平台：Linux
> - 依赖：无
> - 相关：`build_workflow_c.md`（完整的 CAPI 编译工作流）

> **使用说明**
>
> 当用户要求准备 Linux CAPI 编译环境时，加载此模块。
> 此模块包含 CAPI 环境准备的全部内容，从 `build_workflow_c.md` 中抽取。

---

## 一、CAPI 环境准备概述

在 Linux 环境下编译 OpenHarmony CAPI XTS 测试工程之前，需要准备相应的编译环境、工具链和 CAPI 相关依赖。

### 1.1 准备内容

- **系统要求** - 操作系统版本要求和硬件配置
- **基础工具链** - Node.js、npm、Python、Git、C/C++ 编译器
- **CAPI 依赖** - OpenHarmony CAPI 头文件、原生库
- **SDK 下载** - OpenHarmony 预编译工具链和原生 SDK
- **环境验证** - 检查所有工具和 CAPI 依赖是否正确安装

---

## 二、CAPI 环境要求

### 2.1 操作系统

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Operating System | Ubuntu 18.04+ / OpenEuler 20.03+ | Linux CAPI 编译环境 |
| CPU | x86_64 架构 | 支持 C/C++ 原生编译 |
| 内存 | 8GB+ | 推荐 16GB+（CAPI 编译需要更多内存） |
| 磁盘空间 | 50GB+ | CAPI 编译需要更多磁盘空间 |

**推荐配置**：
- Ubuntu 20.04 LTS
- OpenEuler 22.03 LTS
- 16GB+ 内存
- 50GB+ 可用磁盘空间
- SSD 存储（提升编译速度）

### 2.2 基础开发工具

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Node.js | 14.x+ | 推荐 16.x 或更新版本 |
| npm | 6.x+ | 随 Node.js 安装 |
| Python | 3.x | 构建脚本依赖 |
| Git | 2.x | 代码管理 |
| GCC | 7.x+ | C/C++ 编译器 |
| Clang | 10.x+ | 可选，推荐使用 GCC |
| Make | 3.x+ | 构建工具 |

### 2.3 CAPI 特殊要求

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| CAPI 头文件 | OpenHarmony API 10+ | 原生 API 头文件 |
| 原生库 | OpenHarmony API 10+ | CAPI 实现库 |
| 工具链 | OpenHarmony 预编译 | 原生编译工具链 |

---

## 三、基础工具链安装

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

# 检查 GCC
gcc --version
g++ --version

# 检查 Make
make --version
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

### 3.5 安装 C/C++ 编译工具链

#### 3.5.1 安装 GCC

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install build-essential

# OpenEuler
sudo dnf install gcc gcc-c++ make

# 验证安装
gcc --version
g++ --version
make --version
```

#### 3.5.2 安装 Clang（可选）

```bash
# Ubuntu/Debian
sudo apt install clang

# OpenEuler
sudo dnf install clang

# 验证安装
clang --version
```

### 3.6 配置 Git（可选）

```bash
# 配置用户名
git config --global user.name "Your Name"

# 配置邮箱
git config --global user.email "your.email@example.com"

# 验证配置
git config --list
```

---

## 四、CAPI 依赖安装

### 4.1 下载 OpenHarmony 源码

```bash
# 创建工作目录
mkdir -p ~/openharmony
cd ~/openharmony

# 克隆 OpenHarmony 仓库
git clone https://gitee.com/openharmony/manifest.git
cd manifest

# 初始化仓库
repo init -u https://gitee.com/openharmony/manifest.git -b master

# 同步代码
repo sync -j$(nproc)
```

### 4.2 下载预编译工具链

OpenHarmony 提供了 `prebuilts_download.sh` 脚本来下载必要的 SDK 和工具链：

```bash
# 在 OpenHarmony 代码根目录执行
cd ~/openharmony
./build/prebuilts_download.sh
```

### 4.3 下载 CAPI 依赖

#### 4.3.1 下载 CAPI 头文件

```bash
# 确保在 OpenHarmony 根目录
cd ~/openharmony

# CAPI 头文件通常在以下位置
# foundation/ace/interfaces.innerkits/capi/
# foundation/distributeddata/interfaces/capi/
# 等等

# 复制 CAPI 头文件到开发目录（如果需要）
cp -r foundation/ace/interfaces.innerkits/capi/ ~/capi/include/
```

#### 4.3.2 下载 CAPI 库文件

```bash
# CAPI 库文件通常在以下位置
# out/rk3568/lib/libcapi_*.so
# out/rk3568/lib/lib*_native*.so

# 创建 CAPI 库目录
mkdir -p ~/capi/lib

# 复制 CAPI 库文件（编译后）
cp out/rk3568/lib/libcapi_*.so ~/capi/lib/
```

### 4.4 配置 CAPI 环境变量

```bash
# 创建 CAPI 环境变量配置文件
cat > ~/.capi_env << 'EOF'
export CAPI_ROOT=~/capi
export CAPI_INCLUDE=$CAPI_ROOT/include
export CAPI_LIB=$CAPI_ROOT/lib
export LD_LIBRARY_PATH=$CAPI_LIB:$LD_LIBRARY_PATH

# OpenHarmony 路径
export OH_ROOT=~/openharmony
export PATH=$OH_ROOT/prebuilts/linux:$PATH
EOF

# 立即生效
source ~/.capi_env
```

### 4.5 验证 CAPI 依赖

```bash
# 验证 CAPI 头文件
ls $CAPI_INCLUDE/

# 验证 CAPI 库文件
ls $CAPI_LIB/

# 验证环境变量
echo $CAPI_ROOT
echo $CAPI_INCLUDE
echo $CAPI_LIB
echo $LD_LIBRARY_PATH
```

---

## 五、CAPI 环境验证

### 5.1 工具链验证

```bash
# 创建验证脚本
cat > verify_capi_env.sh << 'EOF'
#!/bin/bash

echo "=== CAPI 编译环境验证 ==="
echo ""

# 检查基础工具
echo -n "Node.js: "
if command -v node &> /dev/null; then
    node --version
else
    echo "❌ 未安装"
fi

echo -n "npm: "
if command -v npm &> /dev/null; then
    npm --version
else
    echo "❌ 未安装"
fi

echo -n "Python: "
if command -v python3 &> /dev/null; then
    python3 --version
else
    echo "❌ 未安装"
fi

echo -n "Git: "
if command -v git &> /dev/null; then
    git --version
else
    echo "❌ 未安装"
fi

# 检查 C/C++ 编译工具
echo -n "GCC: "
if command -v gcc &> /dev/null; then
    gcc --version | head -n1
else
    echo "❌ 未安装"
fi

echo -n "G++: "
if command -v g++ &> /dev/null; then
    g++ --version | head -n1
else
    echo "❌ 未安装"
fi

# 检查 CAPI 依赖
echo -n "CAPI 头文件: "
if [ -d "$CAPI_INCLUDE" ]; then
    echo "✅ 已安装 ($CAPI_INCLUDE)"
    echo "  内容: $(ls $CAPI_INCLUDE | wc -l) 个目录"
else
    echo "❌ 未安装"
fi

echo -n "CAPI 库文件: "
if [ -d "$CAPI_LIB" ]; then
    echo "✅ 已安装 ($CAPI_LIB)"
    echo "  内容: $(ls $CAPI_LIB | wc -l) 个文件"
else
    echo "❌ 未安装"
fi

# 检查 OpenHarmony 环境
echo -n "OpenHarmony ROOT: "
if [ -d "$OH_ROOT" ]; then
    echo "✅ 已设置 ($OH_ROOT)"
else
    echo "❌ 未设置"
fi

# 检查预编译工具链
echo -n "预编译工具链: "
if [ -d "$OH_ROOT/prebuilts/linux" ]; then
    echo "✅ 已下载"
else
    echo "❌ 未下载"
fi

echo ""
echo "=== 验证完成 ==="
EOF

# 运行验证脚本
chmod +x verify_capi_env.sh
./verify_capi_env.sh
```

### 5.2 CAPI 编译测试

```bash
# 创建简单的 CAPI 测试程序
cat > test_capi_compile.c << 'EOF'
#include <stdio.h>

// 假设的 CAPI 函数声明
extern int CAPI_TestFunction();

int main() {
    printf("CAPI 编译环境测试\n");
    
    // 调用 CAPI 函数（如果有）
    int result = CAPI_TestFunction();
    printf("CAPI 函数调用结果: %d\n", result);
    
    return 0;
}
EOF

# 测试编译
gcc -I$CAPI_INCLUDE -L$CAPI_LIB -o test_capi_compile test_capi_compile.c -lcapi_test 2>&1

# 检查编译结果
if [ -f test_capi_compile ]; then
    echo "✅ CAPI 编译测试成功"
    ./test_capi_compile
else
    echo "❌ CAPI 编译测试失败"
fi

# 清理
rm -f test_capi_compile test_capi_compile.c
```

### 5.3 PATH 验证

```bash
# 检查工具是否在 PATH 中
which node
which npm
which python3
which git
which gcc
which g++

# 检查 OpenHarmony 工具链
which $OH_ROOT/prebuilts/linux/clang/bin/clang
```

### 5.4 权限验证

```bash
# 检查是否有写权限（编译时需要）
test -w $OH_ROOT && echo "✅ OH_ROOT 有写权限" || echo "❌ OH_ROOT 无写权限"

# 检查 CAPI 目录权限
test -w $CAPI_ROOT && echo "✅ CAPI_ROOT 有写权限" || echo "❌ CAPI_ROOT 无写权限"
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

### 6.3 配置 C 开发环境

```bash
# 安装 C 开发工具（Ubuntu/Debian）
sudo apt install gdb valgrind

# 创建 .gdbinit 配置
cat > ~/.gdbinit << 'EOF'
set confirm off
set verbose off
set pagination on
EOF
```

### 6.4 配置 Shell 别名

```bash
# 添加到 ~/.bashrc
cat >> ~/.bashrc << 'EOF'

# CAPI 开发环境别名
alias capi-test='cd $OH_ROOT && ./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsCapiTest'
alias capi-clean='rm -rf out/rk3568/suites/acts/acts/testcases/ActsCapiTest'
alias capi-check='verify_capi_env.sh'

# 快速导航
alias oh='cd $OH_ROOT'
alias capi='cd $CAPI_ROOT'
alias capi-include='cd $CAPI_INCLUDE'
alias capi-lib='cd $CAPI_LIB'
EOF

# 立即生效
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

### 7.2 GCC 版本不兼容

**现象**：
```
error: GCC version too old/new
```

**解决方案**：
```bash
# 安装指定版本的 GCC
sudo apt install gcc-8 gcc-8 g++-8 g++-8

# 创建符号链接
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 80
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 80

# 选择 GCC 版本
sudo update-alternatives --config gcc
sudo update-alternatives --config g++
```

### 7.3 CAPI 头文件缺失

**现象**：
```
error: bundle/ability_resource_info.h: No such file or directory
```

**解决方案**：
```bash
# 检查 CAPI 头文件路径
echo $CAPI_INCLUDE
ls -la $CAPI_INCLUDE/

# 重新下载 CAPI 头文件
cd $OH_ROOT
find . -name "*.h" -path "*/capi/*" | head -10

# 复制缺失的头文件
cp -r foundation/ace/interfaces.innerkits/capi/ $CAPI_INCLUDE/
```

### 7.4 CAPI 库文件缺失

**现象**：
```
error: undefined reference to 'CAPI_XXX'
```

**解决方案**：
```bash
# 检查 CAPI 库文件
echo $CAPI_LIB
ls -la $CAPI_LIB/

# 重新编译 CAPI 库
cd $OH_ROOT
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsCapiTest

# 复制编译后的库文件
cp out/rk3568/lib/libcapi_*.so $CAPI_LIB/
```

### 7.5 预编译工具链下载失败

**现象**：
```
error: failed to download prebuilts
```

**解决方案**：
```bash
# 检查网络连接
ping -c 4 gitee.com

# 检查磁盘空间
df -h

# 使用代理（如果需要）
export https_proxy=http://proxy:port
export http_proxy=http://proxy:port

# 重新下载
cd $OH_ROOT
./build/prebuilts_download.sh
```

### 7.6 权限问题

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

---

## 八、CAPI 最佳实践

### 8.1 版本管理

```bash
# 使用 nvm 管理 Node.js 版本
nvm install 14
nvm install 16
nvm use 16  # 默认使用 16

# 设置默认版本
nvm alias default 16

# 编译器版本管理
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 80
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-8 80
```

### 8.2 环境隔离

```bash
# 为不同项目使用不同的 Node.js 版本
cd project1
nvm use 14

cd project2
nvm use 16

# 使用虚拟环境（Python）
python3 -m venv capi_env
source capi_env/bin/activate
```

### 8.3 定期更新

```bash
# 更新 npm
npm install -g npm@latest

# 更新 Node.js
nvm install --lts
nvm use --lts

# 更新 OpenHarmony
cd $OH_ROOT
repo sync -j$(nproc)
```

### 8.4 CAPI 开发建议

```bash
# 创建 CAPI 开发模板
mkdir -p ~/capi_templates
cp -r $OH_ROOT/test/xts/acts/capi/* ~/capi_templates/

# 设置代码格式化工具
npm install -g clang-format
clang-format --style=Google -i *.c *.cpp *.h
```

---

## 九、CAPI 检查清单

在开始 CAPI 编译之前，确保完成以下检查：

- [ ] 操作系统版本符合要求（Ubuntu 18.04+ / OpenEuler 20.03+）
- [ ] Node.js 版本 >= 14.x
- [ ] npm 版本 >= 6.x
- [ ] Python 3.x 已安装
- [ ] Git 2.x 已安装
- [ ] GCC 7.x+ 已安装
- [ ] 已运行 `prebuilts_download.sh` 下载 SDK
- [ ] CAPI 头文件已安装到 $CAPI_INCLUDE
- [ ] CAPI 库文件已安装到 $CAPI_LIB
- [ ] 所有工具都在 PATH 中
- [ ] 有足够的磁盘空间（50GB+）
- [ ] 有 OpenHarmony 代码库的写权限
- [ ] 环境变量 $CAPI_ROOT, $CAPI_INCLUDE, $CAPI_LIB 已设置
- [ ] CAPI 编译测试通过

---

## 十、参考资源

### 10.1 官方文档

- [OpenHarmony CAPI 开发指南](https://docs.openharmony.cn/)
- [OpenHarmony 编译环境准备](https://docs.openharmony.cn/)
- [Node.js 官方网站](https://nodejs.org/)
- [nvm 文档](https://github.com/nvm-sh/nvm)
- [GCC 官方文档](https://gcc.gnu.org/)

### 10.2 相关工具

- [NodeSource](https://github.com/nodesource/distributions) - Node.js 安装脚本
- [npm 文档](https://docs.npmjs.com/)
- [Git 官方文档](https://git-scm.com/doc)
- [GDB 调试器](https://sourceware.org/gdb/)

### 10.3 社区资源

- [更新 node 和 npm 到最新版](https://www.jianshu.com/p/3afb8f7dad3b)
- [OpenHarmony 社区](https://www.openharmony.cn/)
- [CAPI 开发论坛](https://gitee.com/openharmony/)

---

## 十一、CAPI 故障排查速查表

| 错误现象 | 可能原因 | 解决方案 |
|---------|---------|---------|
| `CAPI_XXX: undefined reference` | 库文件缺失 | 检查 $CAPI_LIB，重新编译 |
| `bundle/xxx.h: No such file` | 头文件缺失 | 检查 $CAPI_INCLUDE，重新复制 |
| `Node version too old` | Node.js 版本过低 | 使用 nvm 升级 |
| `GCC version too old` | 编译器版本不兼容 | 安装兼容版本的 GCC |
| `permission denied` | 权限问题 | 修复 npm 权限或使用 sudo |
| `failed to download prebuilts` | 网络问题 | 检查网络，使用代理 |
| `memory exhausted` | 内存不足 | 增加交换空间或减少并行任务 |

---

**版本**: 1.0.0
**创建日期**: 2026-03-09
**更新日期**: 2026-03-09
**兼容性**: OpenHarmony API 10+，CAPI XTS 测试框架