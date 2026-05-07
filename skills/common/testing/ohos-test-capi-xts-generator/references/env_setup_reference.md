# 编译环境配置参考

> 从 `build_workflow_c.md` 提取的详细环境配置步骤

---

## 一、Linux 环境配置

### 1.1 环境验证

```bash
# 检查基础工具
for tool in gcc g++ node npm python3 git ninja gn; do
    if command -v "$tool" &> /dev/null; then
        echo "✅ $tool: $(which $tool)"
    else
        echo "❌ $tool: 未安装"
    fi
done

# 检查 CAPI 头文件和库
echo "CAPI 头文件数量: $(find $CAPI_INCLUDE -name '*.h' 2>/dev/null | wc -l)"
echo "CAPI 库文件数量: $(find $CAPI_LIB -name '*.so' 2>/dev/null | wc -l)"

# 检查编译脚本
[ -f "./test/xts/acts/build.sh" ] && echo "✅ 编译脚本存在" || echo "❌ 编译脚本不存在"
```

### 1.2 环境安装

```bash
# 安装基础工具
sudo apt update && sudo apt install -y build-essential git curl wget ninja-build gn

# 安装 Node.js
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs
```

### 1.3 环境变量

```bash
# 添加到 ~/.bashrc
export OH_ROOT=/path/to/openharmony
export CAPI_ROOT=~/capi
export CAPI_INCLUDE=$CAPI_ROOT/include
export CAPI_LIB=$CAPI_ROOT/lib
export LD_LIBRARY_PATH=$CAPI_LIB:$LD_LIBRARY_PATH
export PATH=$OH_ROOT/prebuilts/linux:$PATH
```

---

## 二、Windows WSL 配置

### 2.1 WSL 安装

```powershell
# PowerShell（管理员）
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
# 重启后：
wsl --set-default-version 2
wsl --install -d Ubuntu-20.04
```

### 2.2 WSL 内环境配置

```bash
# 在 Ubuntu WSL 中执行
sudo apt update && sudo apt install -y build-essential git curl wget

# 验证
node --version && npm --version && gcc --version && g++ --version

# 环境变量（WSL 路径）
export OH_ROOT=/mnt/c/openharmony
export CAPI_ROOT=~/capi
export CAPI_INCLUDE=$CAPI_ROOT/include
export CAPI_LIB=$CAPI_ROOT/lib
export LD_LIBRARY_PATH=$CAPI_LIB:$LD_LIBRARY_PATH
export PATH=$OH_ROOT/prebuilts/linux:$PATH

mkdir -p $CAPI_ROOT/{include,lib}
```

---

## 三、Windows DevEco Studio 配置

```powershell
# 下载 DevEco Studio: https://developer.harmonyos.com/cn/develop/deveco-studio
# 安装后配置：SDK 路径 → Node.js 路径 → Gradle
```

```javascript
// build.gradle 中添加 CAPI 支持
android {
    externalNativeBuild {
        cmake {
            cppFlags "-frtti -fexceptions"
            arguments "-DANDROID_STL=c++_shared"
        }
    }
}
// 注意：DevEco Studio 对 CAPI 支持有限，建议使用 WSL
```

---

## 四、Windows MinGW 配置（不推荐）

```powershell
# 下载 MinGW-w64: https://www.mingw-w64.org/
# 选择架构：x86_64，线程模型：posix，异常处理：seh
# 添加 bin 目录到 PATH
```

```bash
# 环境变量
export OH_ROOT=/c/openharmony
export CAPI_ROOT=~/capi
export CC=gcc && export CXX=g++ && export AR=ar && export RANLIB=ranlib
# 强烈建议使用 WSL 替代 MinGW
```
