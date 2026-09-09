# 工作流程详细说明

本文档包含 API 文档检查的详细工作流程和执行器实现。

## 步骤 1：加载规则（按7大维度分类）

```javascript
function loadRules() {
  const index = loadJson('references/index.json');
  const rules = {
    findability: [],      // 资源易找性
    completeness: [],     // 资源丰富性/完整性
    correctness: [],      // 资料正确性
    clarity: [],          // 资源清晰易懂
    capability: []        // 能力有效性/易用性/丰富性
  };
  
  // 按维度分组加载规则
  for (const [key, config] of Object.entries(index.rules)) {
    if (config.enabled) {
      const ruleFile = loadJson(`references/${config.file}`);
      ruleFile.priority = config.priority;
      ruleFile.category = config.category;
      
      // 映射到对应维度
      const dimension = mapToDimension(config.category);
      rules[dimension].push(ruleFile);
    }
  }
  
  return { index, rules, classification: index.classification };
}

function mapToDimension(category) {
  const mapping = {
    '资源易找性': 'findability',
    '资源丰富性/完整性': 'completeness',
    '资料正确性': 'correctness',
    '资源清晰易懂': 'clarity',
    '能力有效性/易用性/丰富性': 'capability'
  };
  return mapping[category] || 'correctness';
}
```

## 步骤 2：解析文档

```javascript
function parseDocument(doc) {
  return {
    content: doc,
    lines: doc.split('\n'),
    codeBlocks: extractCodeBlocks(doc),
    tables: extractTables(doc),
    links: extractLinks(doc),
    headings: extractHeadings(doc),
    sections: identifySections(doc),
    methodSignatures: extractMethodSignatures(doc),
    apiType: detectAPIType(doc)
  };
}
```

## 步骤 3：按7大维度执行检查

```javascript
function executeChecks(parsed, rules) {
  const issuesByDimension = {
    findability: [],
    completeness: [],
    correctness: [],
    clarity: [],
    capability: []
  };
  
  // 1. 资源易找性检查
  if (rules.findability.length > 0) {
    issuesByDimension.findability = executeFindabilityRules(parsed, rules.findability);
  }
  
  // 2. 资源丰富性/完整性检查
  if (rules.completeness.length > 0) {
    issuesByDimension.completeness = executeCompletenessRules(parsed, rules.completeness);
  }
  
  // 3. 资料正确性检查
  if (rules.correctness.length > 0) {
    issuesByDimension.correctness = executeCorrectnessRules(parsed, rules.correctness);
  }
  
  // 4. 资源清晰易懂检查
  if (rules.clarity.length > 0) {
    issuesByDimension.clarity = executeClarityRules(parsed, rules.clarity);
  }
  
  // 5. 能力有效性/易用性/丰富性检查
  if (rules.capability.length > 0) {
    issuesByDimension.capability = executeCapabilityRules(parsed, rules.capability);
  }
  
  return issuesByDimension;
}
```

## 步骤 4：规则执行器实现

### 4.1 资源易找性执行器

```javascript
function executeFindabilityRules(parsed, ruleFiles) {
  const issues = [];
  
  ruleFiles.forEach(ruleFile => {
    ruleFile.rules.forEach(rule => {
      if (!rule.enabled) return;
      
      switch (rule.id) {
        case 'findability-001': // keyword-accuracy
          issues.push(...checkKeywordAccuracy(parsed, rule));
          break;
        case 'findability-002': // external-reference-completeness
          issues.push(...checkExternalReference(parsed, rule));
          break;
        case 'findability-003': // document-discoverability
          issues.push(...checkDiscoverability(parsed, rule));
          break;
      }
    });
  });
  
  return issues;
}

function checkKeywordAccuracy(parsed, rule) {
  const issues = [];
  // 检查标题关键词与内容匹配度
  // 检查搜索关键词覆盖
  return issues;
}
```

### 4.2 资源丰富性/完整性执行器

```javascript
function executeCompletenessRules(parsed, ruleFiles) {
  const issues = [];
  
  ruleFiles.forEach(ruleFile => {
    ruleFile.rules.forEach(rule => {
      if (!rule.enabled) return;
      
      switch (rule.id) {
        case 'completeness-001': // example-code-missing
          issues.push(...checkExampleCompleteness(parsed, rule));
          break;
        case 'completeness-002': // critical-description-missing
          issues.push(...checkCriticalDescription(parsed, rule));
          break;
        case 'completeness-003': // constraint-missing
          issues.push(...checkConstraintCompleteness(parsed, rule));
          break;
        case 'completeness-004': // default-behavior-missing
          issues.push(...checkDefaultBehavior(parsed, rule));
          break;
        case 'completeness-005': // related-info-missing
          issues.push(...checkRelatedInfo(parsed, rule));
          break;
      }
    });
  });
  
  return issues;
}

function checkExampleCompleteness(parsed, rule) {
  const issues = [];
  const codeBlocks = parsed.codeBlocks;
  
  // 检查是否有足够的示例代码
  if (codeBlocks.length < rule.validation?.codeBlockMinCount || 1) {
    issues.push({
      type: '资源丰富性/完整性',
      subType: '示例代码缺失',
      priority: rule.priority,
      confidence: rule.confidence,
      description: rule.message,
      explanation: '文档缺少必要的示例代码',
      suggestedFix: '为每个API或场景添加完整的、可运行的示例代码'
    });
  }
  
  return issues;
}
```

### 4.3 资料正确性执行器

```javascript
function executeCorrectnessRules(parsed, ruleFiles, options = {}) {
  const issues = [];
  
  ruleFiles.forEach(ruleFile => {
    // SDK源码一致性检查
    if (ruleFile.sdkSourceCheck?.enabled && options.sdkSourcePath) {
      const sdkIssues = checkSdkSourceConsistency(parsed, ruleFile.sdkSourceCheck, options);
      issues.push(...sdkIssues);
    }
    
    ruleFile.rules.forEach(rule => {
      if (!rule.enabled) return;
      
      switch (rule.id) {
        case 'correctness-001': // version-update-lag
          issues.push(...checkVersionSync(parsed, rule));
          break;
        case 'correctness-002': // example-code-broken
          issues.push(...checkExampleValidity(parsed, rule));
          break;
        case 'correctness-003': // jsdoc-description-error
          issues.push(...checkJSDocAccuracy(parsed, rule));
          break;
        case 'correctness-004': // path-consistency-across-doc
          issues.push(...checkPathConsistency(parsed, rule));
          break;
        case 'correctness-005': // link-validity
          issues.push(...checkLinkValidity(parsed, rule));
          break;
        case 'correctness-006': // sdk-source-consistency
          // 已在上面的sdkSourceCheck中处理
          break;
      }
    });
  });
  
  return issues;
}
```

### 4.4 资源清晰易懂执行器

```javascript
function executeClarityRules(parsed, ruleFiles) {
  const issues = [];
  
  ruleFiles.forEach(ruleFile => {
    ruleFile.rules.forEach(rule => {
      if (!rule.enabled) return;
      
      switch (rule.id) {
        case 'clarity-001': // title-content-mismatch
          issues.push(...checkTitleContentMatch(parsed, rule));
          break;
        case 'clarity-002': // description-accuracy
          issues.push(...checkDescriptionAccuracy(parsed, rule));
          break;
        case 'clarity-003': // missing-related-links
          issues.push(...checkRelatedLinks(parsed, rule));
          break;
        case 'clarity-004': // mechanism-explanation-missing
          issues.push(...checkMechanismExplanation(parsed, rule));
          break;
        case 'clarity-005': // terminology-consistency
          issues.push(...checkTerminologyConsistency(parsed, rule));
          break;
      }
    });
  });
  
  return issues;
}
```

### 4.5 能力有效性/易用性/丰富性执行器

```javascript
function executeCapabilityRules(parsed, ruleFiles) {
  const issues = [];
  
  ruleFiles.forEach(ruleFile => {
    ruleFile.rules.forEach(rule => {
      if (!rule.enabled) return;
      
      switch (rule.id) {
        // 能力有效性
        case 'capability-001': // constraint-missing
          issues.push(...checkConstraint(parsed, rule));
          break;
        case 'capability-002': // known-issues-missing
          issues.push(...checkKnownIssues(parsed, rule));
          break;
        case 'capability-003': // outdated-documentation
          issues.push(...checkOutdatedDoc(parsed, rule));
          break;
        // 能力易用性
        case 'capability-004': // naming-ambiguity
          issues.push(...checkNamingAmbiguity(parsed, rule));
          break;
        case 'capability-005': // example-not-practical
          issues.push(...checkExamplePracticality(parsed, rule));
          break;
        // 能力丰富性
        case 'capability-006': // alternative-missing
          issues.push(...checkAlternative(parsed, rule));
          break;
        case 'capability-007': // system-capability-missing
          issues.push(...checkSystemCapability(parsed, rule));
          break;
        case 'capability-008': // debugging-support-missing
          issues.push(...checkDebuggingSupport(parsed, rule));
          break;
      }
    });
  });
  
  return issues;
}
```

## 步骤 5：生成报告数据

```javascript
function generateReport(issuesByDimension, index, fileName) {
  const excelData = [];
  
  const summary = {
    total: 0,
    byDimension: {},
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
    autoFixable: 0
  };
  
  const dimensionNameMap = {
    findability: '资源易找性',
    completeness: '资源丰富性/完整性',
    correctness: '资料正确性',
    clarity: '资源清晰易懂',
    capability: '能力有效性/易用性/丰富性'
  };
  
  for (const [dimensionKey, issues] of Object.entries(issuesByDimension)) {
    const dimensionName = dimensionNameMap[dimensionKey] || dimensionKey;
    summary.byDimension[dimensionName] = issues.length;
    summary.total += issues.length;
    
    issues.forEach(issue => {
      if (issue.priority === 'critical') summary.critical++;
      else if (issue.priority === 'high') summary.high++;
      else if (issue.priority === 'medium') summary.medium++;
      else if (issue.priority === 'low') summary.low++;
      if (issue.autoFixable) summary.autoFixable++;
      
      excelData.push({
        filename: fileName,
        issueType: issue.type || dimensionName,
        lineNumber: formatLineNumber(issue.line, issue.lineEnd),
        reason: issue.description || issue.message || '',
        suggestion: issue.suggestedFix || issue.explanation || '',
        severity: translatePriority(issue.priority),
        priority: issue.priority,
        dimension: dimensionName
      });
    });
  }
  
  const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
  excelData.sort((a, b) => {
    const priorityDiff = priorityOrder[a.priority] - priorityOrder[b.priority];
    if (priorityDiff !== 0) return priorityDiff;
    return a.filename.localeCompare(b.filename);
  });
  
  summary.score = calculateScore(summary);
  
  return {
    excelData,
    summary,
    fileName
  };
}

function formatLineNumber(start, end) {
  if (!start) return '-';
  if (!end || start === end) return String(start);
  return `${start}-${end}`;
}

function translatePriority(priority) {
  const map = {
    critical: '严重',
    high: '高',
    medium: '中',
    low: '低'
  };
  return map[priority] || priority;
}

function calculateScore(summary) {
  const weights = { critical: 10, high: 5, medium: 2, low: 1 };
  const totalWeight = summary.critical * weights.critical +
                      summary.high * weights.high +
                      summary.medium * weights.medium +
                      summary.low * weights.low;
  return Math.max(0, 100 - totalWeight);
}

// SDK源码一致性检查实现
function checkSdkSourceConsistency(parsed, sdkConfig, options) {
  const issues = [];
  
  // 1. 找到对应的SDK文件
  const sdkFilePath = resolveSdkFilePath(parsed.fileName, sdkConfig.mappingRules, options.sdkSourcePath);
  if (!sdkFilePath) {
    return [{
      type: '资料正确性',
      subType: 'SDK文件映射失败',
      priority: 'medium',
      confidence: 80,
      description: `无法找到文档对应的SDK源文件: ${parsed.fileName}`,
      suggestedFix: '检查文件命名是否符合映射规则，或确认SDK仓库是否完整'
    }];
  }
  
  // 2. 加载并解析SDK文件
  const sdkContent = loadSdkFile(sdkFilePath);
  const sdkParsed = parseSdkSource(sdkContent);
  
  // 3. 解析文档中的API信息
  const docApis = extractDocApis(parsed);
  
  // 4. 对比检查
  for (const docApi of docApis) {
    const sdkApi = findSdkApi(sdkParsed, docApi.name);
    if (!sdkApi) {
      issues.push({
        type: '资料正确性',
        subType: 'SDK中未找到对应API',
        priority: 'high',
        confidence: 90,
        line: docApi.line,
        description: `文档中的API "${docApi.name}" 在SDK源码中未找到`,
        suggestedFix: '确认API名称拼写正确，或检查SDK版本是否匹配'
      });
      continue;
    }
    
    // 4.1 检查起始版本
    const versionIssue = checkSinceVersion(docApi, sdkApi);
    if (versionIssue) issues.push(versionIssue);
    
    // 4.2 检查参数
    const paramIssues = checkParameters(docApi, sdkApi);
    issues.push(...paramIssues);
    
    // 4.3 检查返回值
    const returnIssue = checkReturnType(docApi, sdkApi);
    if (returnIssue) issues.push(returnIssue);
    
    // 4.4 检查错误码
    const errorCodeIssues = checkErrorCodes(docApi, sdkApi);
    issues.push(...errorCodeIssues);
    
    // 4.5 检查系统接口标记
    const systemApiIssue = checkSystemApiMark(docApi, sdkApi, parsed.fileName);
    if (systemApiIssue) issues.push(systemApiIssue);
    
    // 4.6 检查模型约束
    const stageModelIssue = checkStageModelMark(docApi, sdkApi);
    if (stageModelIssue) issues.push(stageModelIssue);
    
    // 4.7 检查枚举值完整性
    if (docApi.type === 'enum') {
      const enumIssues = checkEnumValues(docApi, sdkApi);
      issues.push(...enumIssues);
    }
    
    // 4.8 检查接口字段完整性
    if (docApi.type === 'interface') {
      const fieldIssues = checkInterfaceFields(docApi, sdkApi);
      issues.push(...fieldIssues);
    }
  }
  
  return issues;
}

/**
 * 根据文档文件名解析对应的SDK文件路径
 */
function resolveSdkFilePath(docFileName, mappingRules, sdkBasePath) {
  const fileName = docFileName.split('/').pop();
  
  // 应用映射规则
  for (const [pattern, sdkPath] of Object.entries(mappingRules.sdkFileMapping)) {
    const regex = patternToRegex(pattern);
    const match = fileName.match(regex);
    if (match) {
      // 替换模板变量
      let resolvedPath = sdkPath;
      for (let i = 1; i < match.length; i++) {
        const key = Object.keys(match.groups || {})[i - 1] || i;
        resolvedPath = resolvedPath.replace(`{${key}}`, match[i]);
      }
      return `${sdkBasePath}/${resolvedPath}`;
    }
  }
  
  return null;
}

/**
 * 解析SDK源码文件，提取JSDOC信息
 */
function parseSdkSource(content) {
  const apis = [];
  
  // 匹配JSDOC块和对应的声明
  const jsdocPattern = /\/\*\*\s*([\s\S]*?)\s*\*\/\s*(?:export\s+)?(?:declare\s+)?(?:namespace|interface|class|function|enum|type|const)?\s*([\w$]+)/g;
  
  let match;
  while ((match = jsdocPattern.exec(content)) !== null) {
    const jsdoc = match[1];
    const name = match[2];
    
    const api = {
      name,
      jsdoc,
      since: extractTag(jsdoc, '@since'),
      deprecated: extractTag(jsdoc, '@deprecated'),
      systemapi: jsdoc.includes('@systemapi'),
      stagemodelonly: jsdoc.includes('@stagemodelonly'),
      params: extractParams(jsdoc),
      returns: extractReturn(jsdoc),
      throws: extractThrows(jsdoc),
      line: calculateLineNumber(content, match.index)
    };
    
    apis.push(api);
  }
  
  return apis;
}

/**
 * 从文档中提取API信息
 */
function extractDocApis(parsed) {
  const apis = [];
  
  // 匹配方法/函数签名
  const methodPattern = /^###\s+(\w+)(?:<sup>(\d+)\+?<\/sup>)?\s*\n+\s*(\w+)\s*\(/gm;
  
  // 匹配接口定义
  const interfacePattern = /^##\s+(\w+)(?:<sup>(\d+)\+?<\/sup>)?\s*\n+[^#]*?\|[^|]+\|/gm;
  
  // 匹配枚举定义
  const enumPattern = /^##\s+(\w+)(?:<sup>(\d+)\+?<\/sup>)?\s*\n+[^#]*?(?:枚举|enum)/i;
  
  // 实现提取逻辑...
  
  return apis;
}

/**
 * 检查起始版本一致性
 */
function checkSinceVersion(docApi, sdkApi) {
  const docVersion = docApi.since;
  const sdkVersion = parseSdkVersion(sdkApi.since);
  
  if (docVersion && sdkVersion && docVersion !== sdkVersion) {
    return {
      type: '资料正确性',
      subType: 'API起始版本不一致',
      priority: 'critical',
      confidence: 95,
      line: docApi.line,
      description: `API "${docApi.name}" 起始版本不一致：文档标注为 ${docVersion}+，SDK中为 @since ${sdkVersion}`,
      suggestedFix: `统一修改为正确的起始版本 ${Math.max(docVersion, sdkVersion)}`
    };
  }
  
  return null;
}

/**
 * 检查参数一致性
 */
function checkParameters(docApi, sdkApi) {
  const issues = [];
  
  // 检查参数数量
  if (docApi.params?.length !== sdkApi.params?.length) {
    issues.push({
      type: '资料正确性',
      subType: '入参数量不一致',
      priority: 'high',
      confidence: 90,
      line: docApi.line,
      description: `API "${docApi.name}" 入参数量不一致：文档有 ${docApi.params?.length || 0} 个，SDK中有 ${sdkApi.params?.length || 0} 个`,
      suggestedFix: '核对并补充缺失的参数说明'
    });
  }
  
  // 检查参数名称和类型
  for (const docParam of docApi.params || []) {
    const sdkParam = sdkApi.params?.find(p => p.name === docParam.name);
    if (!sdkParam) {
      issues.push({
        type: '资料正确性',
        subType: '入参名称不匹配',
        priority: 'high',
        confidence: 90,
        line: docApi.line,
        description: `参数 "${docParam.name}" 在SDK中未找到，可能拼写错误`,
        suggestedFix: `检查参数名称拼写，SDK中的参数名为: ${sdkApi.params?.map(p => p.name).join(', ')}`
      });
    } else if (docParam.type !== sdkParam.type) {
      issues.push({
        type: '资料正确性',
        subType: '入参类型不一致',
        priority: 'high',
        confidence: 85,
        line: docApi.line,
        description: `参数 "${docParam.name}" 类型不一致：文档为 ${docParam.type}，SDK中为 ${sdkParam.type}`,
        suggestedFix: '统一参数类型描述'
      });
    }
  }
  
  return issues;
}

/**
 * 检查返回值类型一致性
 */
function checkReturnType(docApi, sdkApi) {
  if (docApi.returns && sdkApi.returns && docApi.returns !== sdkApi.returns) {
    return {
      type: '资料正确性',
      subType: '返回值类型不一致',
      priority: 'high',
      confidence: 85,
      line: docApi.line,
      description: `API "${docApi.name}" 返回值类型不一致：文档为 ${docApi.returns}，SDK中为 ${sdkApi.returns}`,
      suggestedFix: '统一返回值类型描述'
    };
  }
  
  return null;
}

/**
 * 检查错误码一致性
 */
function checkErrorCodes(docApi, sdkApi) {
  const issues = [];
  
  const docErrorCodes = docApi.errorCodes || [];
  const sdkErrorCodes = sdkApi.throws?.map(t => t.code).filter(Boolean) || [];
  
  // 检查文档中是否有SDK中没有的错误码
  for (const code of docErrorCodes) {
    if (!sdkErrorCodes.includes(code)) {
      issues.push({
        type: '资料正确性',
        subType: '错误码不一致',
        priority: 'medium',
        confidence: 80,
        line: docApi.line,
        description: `错误码 ${code} 在SDK的@throws中未定义`,
        suggestedFix: '确认错误码是否有效，或从文档中移除'
      });
    }
  }
  
  // 检查SDK中是否有文档未列出的错误码
  for (const code of sdkErrorCodes) {
    if (!docErrorCodes.includes(code)) {
      issues.push({
        type: '资料正确性',
        subType: '错误码缺失',
        priority: 'medium',
        confidence: 80,
        line: docApi.line,
        description: `SDK中定义的错误码 ${code} 在文档中未列出`,
        suggestedFix: '在文档中补充该错误码的说明'
      });
    }
  }
  
  return issues;
}

/**
 * 检查系统接口标记一致性
 */
function checkSystemApiMark(docApi, sdkApi, fileName) {
  const isSysDoc = fileName.includes('-sys');
  const isSysSdk = sdkApi.systemapi;
  
  if (isSysDoc && !isSysSdk) {
    return {
      type: '资料正确性',
      subType: '系统接口标记不一致',
      priority: 'high',
      confidence: 90,
      line: docApi.line,
      description: `文档标记为系统接口(-sys)，但SDK中未标记@systemapi`,
      suggestedFix: '确认API是否为系统接口，统一标记方式'
    };
  }
  
  if (!isSysDoc && isSysSdk) {
    return {
      type: '资料正确性',
      subType: '系统接口标记缺失',
      priority: 'high',
      confidence: 90,
      line: docApi.line,
      description: `SDK标记为@systemapi，但文档未标记为系统接口`,
      suggestedFix: '文档文件名应添加-sys后缀，或添加系统接口说明'
    };
  }
  
  return null;
}

/**
 * 检查Stage模型约束标记
 */
function checkStageModelMark(docApi, sdkApi) {
  const hasStageModelInDoc = docApi.constraints?.includes('Stage模型');
  const isStageModelOnly = sdkApi.stagemodelonly;
  
  if (hasStageModelInDoc && !isStageModelOnly) {
    return {
      type: '资料正确性',
      subType: '模型约束标记不一致',
      priority: 'medium',
      confidence: 85,
      line: docApi.line,
      description: `文档标注Stage模型约束，但SDK未标记@stagemodelonly`,
      suggestedFix: '确认模型约束是否正确'
    };
  }
  
  return null;
}

/**
 * 检查枚举值完整性
 */
function checkEnumValues(docApi, sdkApi) {
  const issues = [];
  
  const docValues = docApi.enumValues || [];
  const sdkValues = sdkApi.enumValues || [];
  
  // 检查缺失的枚举值
  for (const value of sdkValues) {
    if (!docValues.find(v => v.name === value.name)) {
      issues.push({
        type: '资料正确性',
        subType: '枚举值缺失',
        priority: 'medium',
        confidence: 85,
        line: docApi.line,
        description: `枚举值 "${value.name}" 在文档中未列出`,
        suggestedFix: '在文档中补充该枚举值的说明'
      });
    }
  }
  
  // 检查文档中多余的枚举值
  for (const value of docValues) {
    if (!sdkValues.find(v => v.name === value.name)) {
      issues.push({
        type: '资料正确性',
        subType: '枚举值不存在',
        priority: 'high',
        confidence: 90,
        line: docApi.line,
        description: `枚举值 "${value.name}" 在SDK中不存在，可能拼写错误`,
        suggestedFix: `检查枚举值名称拼写，SDK中的枚举值为: ${sdkValues.map(v => v.name).join(', ')}`
      });
    }
  }
  
  return issues;
}

/**
 * 检查接口字段完整性
 */
function checkInterfaceFields(docApi, sdkApi) {
  const issues = [];
  
  const docFields = docApi.fields || [];
  const sdkFields = sdkApi.fields || [];
  
  // 检查缺失的字段
  for (const field of sdkFields) {
    if (!docFields.find(f => f.name === field.name)) {
      issues.push({
        type: '资料正确性',
        subType: '接口字段缺失',
        priority: 'medium',
        confidence: 80,
        line: docApi.line,
        description: `接口字段 "${field.name}" 在文档中未列出`,
        suggestedFix: '在文档中补充该字段的说明'
      });
    }
  }
  
  // 检查文档中多余的字段
  for (const field of docFields) {
    if (!sdkFields.find(f => f.name === field.name)) {
      issues.push({
        type: '资料正确性',
        subType: '接口字段不存在',
        priority: 'high',
        confidence: 85,
        line: docApi.line,
        description: `接口字段 "${field.name}" 在SDK中不存在，可能拼写错误`,
        suggestedFix: `检查字段名称拼写，SDK中的字段为: ${sdkFields.map(f => f.name).join(', ')}`
      });
    }
  }
  
  return issues;
}

// 辅助函数
function extractTag(jsdoc, tagName) {
  const match = jsdoc.match(new RegExp(`${tagName}\\s+(.+)`));
  return match ? match[1].trim() : null;
}

function extractParams(jsdoc) {
  const params = [];
  const regex = /@param\s+\{([^}]+)\}\s+(\w+)/g;
  let match;
  while ((match = regex.exec(jsdoc)) !== null) {
    params.push({ type: match[1], name: match[2] });
  }
  return params;
}

function extractReturn(jsdoc) {
  const match = jsdoc.match(/@returns?\s+\{([^}]+)\}/);
  return match ? match[1] : null;
}

function extractThrows(jsdoc) {
  const throws = [];
  const regex = /@throws\s+\{([^}]+)\}\s+(\d{6,})/g;
  let match;
  while ((match = regex.exec(jsdoc)) !== null) {
    throws.push({ type: match[1], code: match[2] });
  }
  return throws;
}

function parseSdkVersion(sinceTag) {
  if (!sinceTag) return null;
  
  // 处理 @since arkts {'1.1':'12', '1.2':'20'} 格式
  const arktsMatch = sinceTag.match(/arkts\s*\{[^}]*\}/);
  if (arktsMatch) {
    // 提取版本号
    const versionMatch = sinceTag.match(/'\d+\.\d+'\s*:\s*'(\d+)'/);
    return versionMatch ? parseInt(versionMatch[1]) : null;
  }
  
  // 普通数字格式
  const numMatch = sinceTag.match(/(\d+)/);
  return numMatch ? parseInt(numMatch[1]) : null;
}

function patternToRegex(pattern) {
  // 将规则模板转换为正则表达式
  let regex = pattern
    .replace(/\./g, '\\.')
    .replace(/\{name\}/g, '(?<name>\\w+)')
    .replace(/\{module\}/g, '(?<module>[\\w-]+)');
  return new RegExp(regex);
}
```
