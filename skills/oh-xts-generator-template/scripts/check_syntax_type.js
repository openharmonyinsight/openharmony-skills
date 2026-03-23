#!/usr/bin/env node

/**
 * API 语法类型检查脚本
 * 
 * 用途：在编译前验证测试用例使用的 API 是否支持目标语法类型
 * 
 * 使用方法：
 *   node check_syntax_type.js --syntax-type static --test-cases *.test.ets
 *   node check_syntax_type.js --syntax-type dynamic --test-dir ./test/
 *   node check_syntax_type.js --help
 */

const fs = require('fs');
const path = require('path');

// 命令行参数
const args = process.argv.slice(2);
const options = {
  syntaxType: null,      // 'static' 或 'dynamic'
  testCases: [],        // 测试用例文件列表
  testDir: null,         // 测试用例目录
  apiInfoPath: null,     // API 信息文件路径
  reportPath: null,       // 报告输出路径
  verbose: false          // 详细输出模式
};

// 解析命令行参数
function parseArgs() {
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else if (arg === '--syntax-type' || arg === '-s') {
      if (i + 1 < args.length) {
        options.syntaxType = args[++i];
      }
    } else if (arg === '--test-cases' || arg === '-t') {
      while (i + 1 < args.length && !args[i + 1].startsWith('--')) {
        options.testCases.push(args[++i]);
      }
    } else if (arg === '--test-dir' || arg === '-d') {
      if (i + 1 < args.length) {
        options.testDir = args[++i];
      }
    } else if (arg === '--api-info' || arg === '-a') {
      if (i + 1 < args.length) {
        options.apiInfoPath = args[++i];
      }
    } else if (arg === '--report' || arg === '-r') {
      if (i + 1 < args.length) {
        options.reportPath = args[++i];
      }
    } else if (arg === '--verbose' || arg === '-v') {
      options.verbose = true;
    }
  }
  
  // 验证必需参数
  if (!options.syntaxType) {
    console.error('错误: 必需指定 --syntax-type 参数');
    console.error('使用: node check_syntax_type.js --syntax-type <static|dynamic>');
    process.exit(1);
  }
  
  // 设置默认值
  if (!options.apiInfoPath) {
    // 尝试从常见的路径查找 API 信息文件
    const defaultPaths = [
      '/tmp/api_info_with_syntax.json',
      '/tmp/api_info_and_style_with_syntax.json',
      './api_info_with_syntax.json',
    ];
    
    for (const defaultPath of defaultPaths) {
      if (fs.existsSync(defaultPath)) {
        options.apiInfoPath = defaultPath;
        break;
      }
    }
    
    if (!options.apiInfoPath) {
      console.warn('警告: 未找到 API 信息文件，跳过验证');
    }
  }
  
  if (!options.reportPath) {
    options.reportPath = '/tmp/syntax_type_check_report.json';
  }
}

// 打印帮助信息
function printHelp() {
  console.log(`
API 语法类型检查脚本

用法: node check_syntax_type.js [选项]

选项:
  --syntax-type, -s <static|dynamic>  (必需) 任务语法类型
  --test-cases, -t <文件>...             测试用例文件列表
  --test-dir, -d <目录>                 测试用例目录
  --api-info, -a <文件>                  API 信息文件路径
  --report, -r <文件>                    报告输出路径 (默认: /tmp/syntax_type_check_report.json)
  --verbose, -v                            详细输出模式
  --help, -h                                显示帮助信息

示例:
  1. 检查单个文件:
     node check_syntax_type.js --syntax-type static --test-cases UitestOnTextErrorStatic.test.ets

  2. 检查目录:
     node check_syntax_type.js --syntax-type static --test-dir ./test/

  3. 指定 API 信息文件:
     node check_syntax_type.js --syntax-type static --test-cases *.test.ets --api-info ./api_info.json

  4. 生成详细报告:
     node check_syntax_type.js --syntax-type static --test-dir ./test/ --verbose

说明:
  - 本脚本用于在编译前验证测试用例使用的 API 是否支持目标语法类型
  - 如果使用了不支持目标语法的 API，会生成警告和错误报告
  - 支持 ArkTS-static 和 ArkTS-dynamic 两种语法类型
  - 自动识别测试用例中使用的 API
  - 支持批量检查多个测试文件
`);
}

// 读取测试用例文件
function readTestCase(filePath) {
  if (!fs.existsSync(filePath)) {
    console.warn(`警告: 文件不存在: ${filePath}`);
    return null;
  }
  
  const content = fs.readFileSync(filePath, 'utf-8');
  return {
    path: filePath,
    content: content,
    name: path.basename(filePath)
  };
}

// 提取测试用例中使用的 API
function extractAPIsFromTestCase(testCase) {
  const apis = new Map();
  const apiPattern = /(?:Driver|On|Component|UiWindow)\.(\w+)/g;
  let match;
  
  while ((match = apiPattern.exec(testCase.content)) !== null) {
    const className = match[1];
    const methodName = match[0].replace(className + '.', '');
    
    if (methodName && className) {
      const key = `${className}.${methodName}`;
      if (!apis.has(key)) {
        apis.set(key, {
          className,
          methodName,
          count: 0,
          lines: []
        });
      }
      const api = apis.get(key);
      api.count++;
      apis.set(key, api);
    }
  }
  
  return apis;
}

// 验证 API 是否支持目标语法类型
function validateAPIs(testCases, apiInfo, syntaxType) {
  const validationResults = [];
  const invalidAPIs = [];
  
  for (const testCase of testCases) {
    const apis = extractAPIsFromTestCase(testCase);
    
    for (const [key, api] of apis.entries()) {
      const apiInfoDetail = apiInfo.apiInfo?.[api.className]?.[api.methodName];
      
      if (!apiInfoDetail) {
        if (options.verbose) {
          console.warn(`警告: 未找到 API 信息: ${key}`);
        }
        continue;
      }
      
      if (!apiInfoDetail.syntaxSupport) {
        if (options.verbose) {
          console.warn(`警告: API ${key} 缺少语法支持信息`);
        }
        continue;
      }
      
      const apiSyntaxType = apiInfoDetail.syntaxType || 'unknown';
      
      // 检查是否支持目标语法类型
      if (apiSyntaxType !== 'both' && apiSyntaxType !== syntaxType) {
        invalidAPIs.push({
          testCase: testCase.name,
          api: key,
          className: api.className,
          methodName: api.methodName,
          syntaxType: apiSyntaxType,
          requiredSyntax: syntaxType,
          reason: `API 仅支持 ${apiSyntaxType} 语法，但任务要求 ${syntaxType} 语法`
        });
        
        validationResults.push({
          type: 'error',
          message: `测试文件 ${testCase.name} 使用了不支持 ${syntaxType} 语法的 API: ${key}`,
          api: key,
          testCase: testCase.name
        });
      } else {
        if (options.verbose) {
          console.log(`✓ ${testCase.name}: ${key} 支持 ${syntaxType} 语法`);
        }
        
        validationResults.push({
          type: 'success',
          message: `测试文件 ${testCase.name} 使用的 API: ${key} 支持 ${syntaxType} 语法`,
          api: key,
          testCase: testCase.name
        });
      }
    }
  }
  
  return {
    validationResults,
    invalidAPIs,
    validCount: validationResults.filter(r => r.type === 'success').length,
    errorCount: validationResults.filter(r => r.type === 'error').length
  };
}

// 生成报告
function generateReport(validation, apiInfo) {
  const report = {
    timestamp: new Date().toISOString(),
    syntaxType: options.syntaxType,
    summary: {
      totalAPIs: validation.validCount + validation.errorCount,
      validAPIs: validation.validCount,
      invalidAPIs: validation.errorCount,
      successRate: validation.totalAPIs > 0 ? ((validation.validCount / validation.totalAPIs) * 100).toFixed(2) + '%' : '0%'
    },
    invalidAPIs: validation.invalidAPIs,
    syntaxStatistics: apiInfo.statistics || null
  };
  
  fs.writeFileSync(options.reportPath, JSON.stringify(report, null, 2));
  console.log(`\n报告已保存到: ${options.reportPath}`);
  
  // 打印摘要
  console.log(`\n=== 检查摘要 ===`);
  console.log(`语法类型: ${options.syntaxType}`);
  console.log(`检查的测试文件: ${validation.validCount + validation.errorCount} 个`);
  console.log(`使用的 API 数量: ${report.summary.totalAPIs}`);
  console.log(`有效的 API 数量: ${report.summary.validAPIs}`);
  console.log(`无效的 API 数量: ${report.summary.invalidAPIs}`);
  console.log(`成功率: ${report.summary.successRate}`);
  
  if (validation.errorCount > 0) {
    console.log(`\n⚠️  发现 ${validation.errorCount} 个问题`);
    console.log(`详情请查看报告: ${options.reportPath}`);
  } else {
    console.log(`\n✅ 所有 API 都支持 ${options.syntaxType} 语法`);
  }
  
  return report;
}

// 主函数
async function main() {
  parseArgs();
  
  console.log(`API 语法类型检查脚本`);
  console.log(`语法类型: ${options.syntaxType}`);
  
  // 读取 API 信息
  let apiInfo = null;
  if (options.apiInfoPath && fs.existsSync(options.apiInfoPath)) {
    try {
      apiInfo = JSON.parse(fs.readFileSync(options.apiInfoPath, 'utf-8'));
      console.log(`API 信息文件: ${options.apiInfoPath}`);
    } catch (error) {
      console.error(`错误: 无法读取 API 信息文件: ${options.apiInfoPath}`);
      console.error(error.message);
      process.exit(1);
    }
  }
  
  // 读取测试用例文件
  let testFiles = [];
  
  if (options.testCases.length > 0) {
    console.log(`\n检查 ${options.testCases.length} 个测试文件...`);
    testFiles = options.testCases.map(readTestCase);
  } else if (options.testDir && fs.existsSync(options.testDir)) {
    console.log(`\n扫描测试目录: ${options.testDir}`);
    const entries = fs.readdirSync(options.testDir, { withFileTypes: true });
    testFiles = entries
      .filter(entry => entry.name.endsWith('.test.ets'))
      .map(entry => readTestCase(path.join(options.testDir, entry.name)));
    console.log(`找到 ${testFiles.length} 个测试文件`);
  } else {
    console.error(`\n错误: 必须指定 --test-cases 或 --test-dir 参数`);
    printHelp();
    process.exit(1);
  }
  
  // 过滤有效的测试文件
  testFiles = testFiles.filter(tf => tf !== null);
  
  if (testFiles.length === 0) {
    console.error(`\n错误: 没有找到有效的测试文件`);
    process.exit(1);
  }
  
  // 验证 API 语法类型
  console.log(`\n验证 API 语法类型...`);
  const validation = validateAPIs(testFiles, apiInfo, options.syntaxType);
  
  // 生成报告
  const report = generateReport(validation, apiInfo);
  
  // 返回退出码
  if (validation.errorCount > 0) {
    process.exit(1);
  } else {
    process.exit(0);
  }
}

// 执行主函数
main().catch(error => {
  console.error(`\n错误: ${error.message}`);
  console.error(error.stack);
  process.exit(1);
});
