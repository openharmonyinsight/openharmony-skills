# 用法：./check_test_suite_structure.sh [测试套路径]
# 功能：验证 CAPI 测试套工程结构的完整性

set -e

TEST_SUITE_PATH="${1:-.}"
CHECK_PASSED=true
ERROR_COUNT=0

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "CAPI 测试套工程结构检查"
echo "========================================="
echo "测试套路径: ${TEST_SUITE_PATH}"
echo ""

# 检查函数
check_item() {
    local item="$1"
    local description="$2"
    
    if [ -e "$TEST_SUITE_PATH/$item" ]; then
        echo -e "${GREEN}✅${NC} $description"
    else
        echo -e "${RED}❌${NC} $description"
        CHECK_PASSED=false
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
}

check_dir() {
    local item="$1"
    local description="$2"
    
    if [ -d "$TEST_SUITE_PATH/$item" ]; then
        echo -e "${GREEN}✅${NC} $description"
    else
        echo -e "${RED}❌${NC} $description"
        CHECK_PASSED=false
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
}

check_file() {
    local item="$1"
    local description="$2"
    
    if [ -f "$TEST_SUITE_PATH/$item" ]; then
        echo -e "${GREEN}✅${NC} $description"
    else
        echo -e "${RED}❌${NC} $description"
        CHECK_PASSED=false
        ERROR_COUNT=$((ERROR_COUNT + 1))
    fi
}

echo "【顶层目录检查】"
check_dir "AppScope/" "AppScope/ 目录存在"
check_file "AppScope/app.json5" "AppScope/app.json5 存在"
check_file "BUILD.gn" "BUILD.gn 文件存在"
check_file "Test.json" "Test.json 文件存在"
check_dir "signature/" "signature/ 目录存在"
check_file "build-profile.json5" "build-profile.json5 存在"
check_file "hvigorfile.ts" "hvigorfile.ts 存在"
check_dir "hvigor/" "hvigor/ 目录存在"
check_file "oh-package.json5" "oh-package.json5 存在"
check_file ".gitignore" ".gitignore 存在（可选）"

echo ""
echo "【AppScope/ 目录检查】"
check_dir "AppScope/resources/" "AppScope/resources/ 目录存在"
check_dir "AppScope/resources/base/" "AppScope/resources/base/ 目录存在"
check_dir "AppScope/resources/base/element/" "AppScope/resources/base/element/ 目录存在"
check_dir "AppScope/resources/base/media/" "AppScope/resources/base/media/ 目录存在"
check_file "AppScope/resources/base/element/string.json" "AppScope/resources/base/element/string.json 存在"
if [ -f "$TEST_SUITE_PATH/AppScope/resources/base/media/app_icon.png" ]; then
    echo -e "${GREEN}✅${NC} AppScope/resources/base/media/app_icon.png 存在"
elif [ -f "$TEST_SUITE_PATH/AppScope/resources/base/media/layered_image.json" ]; then
    echo -e "${GREEN}✅${NC} AppScope/resources/base/media/ 使用分层图标方案 (layered_image.json)"
else
    echo -e "${RED}❌${NC} AppScope/resources/base/media/ 缺少图标 (需要 app_icon.png 或 layered_image.json)"
    CHECK_PASSED=false
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

echo ""
echo "【entry/ 目录检查】"
check_file "entry/build-profile.json5" "entry/build-profile.json5 存在"
check_file "entry/hvigorfile.ts" "entry/hvigorfile.ts 存在"
check_file "entry/oh-package.json5" "entry/oh-package.json5 存在"
check_file "entry/.gitignore" "entry/.gitignore 存在（可选）"

echo ""
echo "【entry/src/main/ 目录检查】"
check_dir "entry/src/main/cpp/" "entry/src/main/cpp/ 目录存在"
check_file "entry/src/main/cpp/NapiTest.cpp" "entry/src/main/cpp/NapiTest.cpp 存在"
check_file "entry/src/main/cpp/CMakeLists.txt" "entry/src/main/cpp/CMakeLists.txt 存在"
check_dir "entry/src/main/cpp/types/" "entry/src/main/cpp/types/ 目录存在"
check_dir "entry/src/main/cpp/types/libentry/" "entry/src/main/cpp/types/libentry/ 目录存在"
check_file "entry/src/main/cpp/types/libentry/index.d.ts" "entry/src/main/cpp/types/libentry/index.d.ts 存在"
check_file "entry/src/main/cpp/types/libentry/oh-package.json5" "entry/src/main/cpp/types/libentry/oh-package.json5 存在"

echo ""
echo "【entry/src/main/ets/ 目录检查】"
check_dir "entry/src/main/ets/entryability/" "entry/src/main/ets/entryability/ 目录存在"
check_file "entry/src/main/ets/entryability/EntryAbility.ts" "entry/src/main/ets/entryability/EntryAbility.ts 存在"
check_dir "entry/src/main/ets/pages/" "entry/src/main/ets/pages/ 目录存在"
check_file "entry/src/main/ets/pages/Index.ets" "entry/src/main/ets/pages/Index.ets 存在"
check_file "entry/src/main/module.json5" "entry/src/main/module.json5 存在"

echo ""
echo "【entry/src/main/resources/ 目录检查】"
check_dir "entry/src/main/resources/" "entry/src/main/resources/ 目录存在"
check_dir "entry/src/main/resources/base/" "entry/src/main/resources/base/ 目录存在"
check_file "entry/src/main/resources/base/element/color.json" "entry/src/main/resources/base/element/color.json 存在"
check_file "entry/src/main/resources/base/element/string.json" "entry/src/main/resources/base/element/string.json 存在"
check_dir "entry/src/main/resources/base/profile/" "entry/src/main/resources/base/profile/ 目录存在"
check_file "entry/src/main/resources/base/profile/main_pages.json" "entry/src/main/resources/base/profile/main_pages.json 存在"
check_dir "entry/src/main/resources/base/media/" "entry/src/main/resources/base/media/ 目录存在"
check_file "entry/src/main/resources/base/media/icon.png" "entry/src/main/resources/base/media/icon.png 存在"
check_dir "entry/src/main/resources/en_US/" "entry/src/main/resources/en_US/ 目录存在（可选）"
check_dir "entry/src/main/resources/zh_CN/" "entry/src/main/resources/zh_CN/ 目录存在（可选）"
check_file "entry/src/main/resources/en_US/element/string.json" "entry/src/main/resources/en_US/element/string.json 存在（可选）"
check_file "entry/src/main/resources/zh_CN/element/string.json" "entry/src/main/resources/zh_CN/element/string.json 存在（可选）"
check_file "entry/src/main/syscap.json" "entry/src/main/syscap.json 存在"

echo ""
echo "【entry/src/ohosTest/ 目录检查】"
check_dir "entry/src/ohosTest/" "entry/src/ohosTest/ 目录存在"
check_dir "entry/src/ohosTest/ets/" "entry/src/ohosTest/ets/ 目录存在"
check_dir "entry/src/ohosTest/ets/test/" "entry/src/ohosTest/ets/test/ 目录存在"
check_file "entry/src/ohosTest/ets/test/Ability.test.ets" "entry/src/ohosTest/ets/test/Ability.test.ets 存在（可选）"
check_file "entry/src/ohosTest/ets/test/List.test.ets" "entry/src/ohosTest/ets/test/List.test.ets 存在"
check_dir "entry/src/ohosTest/ets/testability/" "entry/src/ohosTest/ets/testability/ 目录存在"
check_dir "entry/src/ohosTest/ets/testability/pages/" "entry/src/ohosTest/ets/testability/pages/ 目录存在"
check_file "entry/src/ohosTest/ets/testability/TestAbility.ets" "entry/src/ohosTest/ets/testability/TestAbility.ets 存在"
check_file "entry/src/ohosTest/ets/testability/pages/Index.ets" "entry/src/ohosTest/ets/testability/pages/Index.ets 存在"
check_file "entry/src/ohosTest/module.json5" "entry/src/ohosTest/module.json5 存在"
check_file "entry/src/ohosTest/syscap.json" "entry/src/ohosTest/syscap.json 存在"

echo ""
echo "【entry/src/ohosTest/resources/ 目录检查】"
check_dir "entry/src/ohosTest/resources/" "entry/src/ohosTest/resources/ 目录存在"
check_dir "entry/src/ohosTest/resources/base/" "entry/src/ohosTest/resources/base/ 目录存在"
check_file "entry/src/ohosTest/resources/base/element/color.json" "entry/src/ohosTest/resources/base/element/color.json 存在"
check_file "entry/src/ohosTest/resources/base/element/string.json" "entry/src/ohosTest/resources/base/element/string.json 存在"
check_dir "entry/src/ohosTest/resources/base/profile/" "entry/src/ohosTest/resources/base/profile/ 目录存在"
check_file "entry/src/ohosTest/resources/base/profile/test_pages.json" "entry/src/ohosTest/resources/base/profile/test_pages.json 存在"
check_dir "entry/src/ohosTest/resources/base/media/" "entry/src/ohosTest/resources/base/media/ 目录存在"
check_file "entry/src/ohosTest/resources/base/media/icon.png" "entry/src/ohosTest/resources/base/media/icon.png 存在"
check_file "entry/src/ohosTest/ets/testrunner/OpenHarmonyTestRunner.ts" "entry/src/ohosTest/ets/testrunner/OpenHarmonyTestRunner.ts 存在"

echo ""
echo "【signature/ 目录检查】"
check_dir "signature/" "signature/ 目录存在"
check_file "signature/openharmony.p7b" "signature/openharmony.p7b 存在"

echo ""
echo "【hvigor/ 目录检查】"
check_file "hvigor/hvigor-config.json5" "hvigor/hvigor-config.json5 存在"

echo ""
echo "========================================="
echo "【配置验证检查】"
echo "========================================="

# 验证1：BUILD.gn 模板检查
echo ""
echo "[1/3] BUILD.gn 模板检查..."
if grep -q "ohos_app_assist_suite" "$TEST_SUITE_PATH/BUILD.gn" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} ohos_app_assist_suite 模板存在"
else
    echo -e "${RED}❌${NC} 缺少 ohos_app_assist_suite 模板"
    CHECK_PASSED=false
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

if grep -q "ohos_js_app_suite" "$TEST_SUITE_PATH/BUILD.gn" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} ohos_js_app_suite 模板存在"
else
    echo -e "${RED}❌${NC} 缺少 ohos_js_app_suite 模板"
    CHECK_PASSED=false
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

if grep -q "deps = \[ \":" "$TEST_SUITE_PATH/BUILD.gn" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} deps 配置存在"
else
    echo -e "${RED}❌${NC} 缺少 deps 配置"
    CHECK_PASSED=false
    ERROR_COUNT=$((ERROR_COUNT + 1))
fi

# 验证2：上层 BUILD.gn 注册检查
echo ""
echo "[2/3] 上层 BUILD.gn 注册检查..."
PARENT_DIR=$(dirname "$TEST_SUITE_PATH")
if [ -f "$PARENT_DIR/BUILD.gn" ]; then
    SUITE_DIR_NAME=$(basename "$TEST_SUITE_PATH")
    # 提取测试套名称（从 ohos_js_app_suite 中）
    SUITE_NAME=$(grep 'ohos_js_app_suite("' "$TEST_SUITE_PATH/BUILD.gn" 2>/dev/null | sed 's/.*ohos_js_app_suite("\([^"]*\)".*/\1/' | head -1)
    
    if [ -n "$SUITE_NAME" ]; then
        if grep -q "\"${SUITE_DIR_NAME}:${SUITE_NAME}\"" "$PARENT_DIR/BUILD.gn" 2>/dev/null; then
            echo -e "${GREEN}✅${NC} 上层 BUILD.gn 已注册测试套: ${SUITE_DIR_NAME}:${SUITE_NAME}"
        else
            echo -e "${RED}❌${NC} 上层 BUILD.gn 未引用测试套: ${SUITE_DIR_NAME}:${SUITE_NAME}"
            echo -e "${YELLOW}   请在 $PARENT_DIR/BUILD.gn 的 group() deps 中添加:${NC}"
            echo -e "${YELLOW}   \"${SUITE_DIR_NAME}:${SUITE_NAME}\"${NC}"
            CHECK_PASSED=false
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    else
        echo -e "${YELLOW}⚠️${NC} 无法从 BUILD.gn 中提取测试套名称"
    fi
else
    echo -e "${YELLOW}⚠️${NC} 未找到上层 BUILD.gn: $PARENT_DIR/BUILD.gn"
fi

# 验证3：TypeScript 声明一致性检查
echo ""
echo "[3/3] TypeScript 声明一致性检查..."
NAPI_TEST_CPP="$TEST_SUITE_PATH/entry/src/main/cpp/NapiTest.cpp"
INDEX_D_TS="$TEST_SUITE_PATH/entry/src/main/cpp/types/libentry/index.d.ts"

if [ -f "$NAPI_TEST_CPP" ] && [ -f "$INDEX_D_TS" ]; then
    # 提取 C++ 中注册的函数名（支持多种注册方式）
    grep -E 'DECLARE_NAPI_PROPERTY|"napi_property_descriptor.*"' "$NAPI_TEST_CPP" 2>/dev/null | \
        grep -o '"[^"]*"' | tr -d '"' | grep -v '^napi_property_descriptor$' | sort > /tmp/cpp_funcs_$$.txt
    
    if [ ! -s /tmp/cpp_funcs_$$.txt ]; then
        grep -oP '"\K[A-Za-z0-9_]+(?="\s*,\s*nullptr)' "$NAPI_TEST_CPP" 2>/dev/null | sort > /tmp/cpp_funcs_$$.txt
    fi
    
    # 提取 TypeScript 中的函数名
    grep 'export const' "$INDEX_D_TS" 2>/dev/null | \
        awk '{print $3}' | cut -d':' -f1 | sort > /tmp/ts_funcs_$$.txt
    
    if [ -s /tmp/cpp_funcs_$$.txt ]; then
        # 对比差异
        if diff -q /tmp/cpp_funcs_$$.txt /tmp/ts_funcs_$$.txt > /dev/null 2>&1; then
            FUNC_COUNT=$(wc -l < /tmp/cpp_funcs_$$.txt)
            echo -e "${GREEN}✅${NC} TypeScript 声明与 C++ 注册一致（共 $FUNC_COUNT 个函数）"
        else
            echo -e "${RED}❌${NC} TypeScript 声明与 C++ 注册不一致"
            echo -e "${YELLOW}   差异如下：${NC}"
            diff /tmp/cpp_funcs_$$.txt /tmp/ts_funcs_$$.txt | head -10
            echo -e "${YELLOW}   请补充 index.d.ts 中的函数声明${NC}"
            CHECK_PASSED=false
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    else
        echo -e "${YELLOW}⚠️${NC} 未在 NapiTest.cpp 中找到 N-API 函数注册"
    fi
    
    # 清理临时文件
    rm -f /tmp/cpp_funcs_$$.txt /tmp/ts_funcs_$$.txt
else
    echo -e "${YELLOW}⚠️${NC} 缺少 NapiTest.cpp 或 index.d.ts，跳过 TypeScript 声明检查"
fi

echo ""
echo "========================================="
total_files=$(find "$TEST_SUITE_PATH" -type f 2>/dev/null | wc -l)
total_dirs=$(find "$TEST_SUITE_PATH" -type d 2>/dev/null | wc -l)
echo "总文件数: $total_files"
echo "总目录数: $total_dirs"
echo ""

if [ "$CHECK_PASSED" = true ]; then
    echo -e "${GREEN}✅ 检查通过！工程结构完整且配置正确${NC}"
    echo "========================================="
    exit 0
else
    echo -e "${RED}❌ 检查失败！发现 ${ERROR_COUNT} 个错误${NC}"
    echo "========================================="
    echo ""
    echo -e "${YELLOW}建议修复步骤：${NC}"
    echo "1. 查看上方标记为 ❌ 的缺失项"
    echo "2. 参考完整目录结构："
    echo "   ${TEST_SUITE_PATH}/AppScope/"
    echo "   ${TEST_SUITE_PATH}/entry/src/main/cpp/"
    echo "   ${TEST_SUITE_PATH}/entry/src/main/ets/"
    echo "   ${TEST_SUITE_PATH}/entry/src/main/resources/"
    echo "   ${TEST_SUITE_PATH}/entry/src/ohosTest/ets/"
    echo "   ${TEST_SUITE_PATH}/entry/src/ohosTest/resources/"
    echo ""
    echo "3. 配置文件修复："
    echo "   - BUILD.gn: 确保 ohos_app_assist_suite 和 ohos_js_app_suite 都存在"
    echo "   - 上层 BUILD.gn: 在 group() deps 中添加测试套依赖"
    echo "   - index.d.ts: 补充缺失的 TypeScript 函数声明"
    echo ""
    echo "4. 或运行快速修复脚本（如果提供）："
    echo "   bash scripts/fix_missing_structure.sh ${TEST_SUITE_PATH}"
    exit 1
fi
