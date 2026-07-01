# Feat Decomposition Analysis Guide

When the user provides only a component or functional-domain name (e.g. "补齐Toggle组件的规格") **without** specifying a concrete FeatID or Feat scope, analyze the full API surface before committing to registration. This prevents monolithic 20KB+ specs and produces more maintainable, reviewable documents.

**Skip condition**: the user already named a specific Feat (e.g. "Toggle Feat-02 Switch样式") or the component has ≤ 5 public APIs.

## 0.5.1 Quick API surface scan

Use an Explore agent to gather:
1. **SDK API enumeration**: read the canonical `.d.ts` / `.d.ets` files to list all public APIs, properties, events, and their `@since` versions
2. **Source structure reconnaissance**: identify Pattern classes, Model dispatch, sub-component delegation, and major configuration layers
3. **Existing coverage**: check `features.yaml` for any Feats already registered under this FuncID — only propose Feats for **uncovered** capability clusters

**If the Explore agent cannot locate source files** (path renamed, new architecture layer):
- Try `grep -rn "<ComponentName>Pattern\|<ComponentName>Model" frameworks/` to find the actual path
- Ask the user to confirm the component's module location
- Do NOT proceed with guessed paths — wrong source → wrong decomposition

## 0.5.2 Apply decomposition heuristics

Select the most appropriate heuristic(s) based on what the scan reveals. Common strategies (may be combined):

| Heuristic | When to use | Existing example |
|-----------|-------------|------------------|
| **Sub-capability cluster** | Component has many independent property/API groups | Text → 字体属性, 行/段落布局, 溢出与截断, 装饰与样式, 选择与复制, 事件回调 |
| **Type/mode dispatch** | Component dispatches to different Pattern classes by type | Toggle → Switch形态, Checkbox形态, Button形态 |
| **API version boundary** | Significant API evolution across versions | API 8–10 基础能力 vs API 11–12 增强 vs API 13+ 新特性 |
| **Interaction model** | Interactive component with distinct interaction phases | 状态与数据, 视觉样式, 用户交互/事件, 无障碍/C API |
| **Implementation layer** | Deep architecture stack with separable concerns | Image → 核心显示, 颜色与效果, 高级功能, 事件回调, 内存优化 |

**Sizing guideline**: each Feat should produce a **5–15 KB** spec. Estimated > 20 KB → split further; estimated < 3 KB → merge with a neighbor.

## 0.5.3 Propose breakdown to user

Present the proposed Feat breakdown using `AskUserQuestion`:

- **Question header**: "Feat 拆分方案"
- **Question body**: include a preview table showing each proposed Feat with ID, title, scope summary, and estimated complexity
- Clearly state which heuristic(s) were applied and why

Preview table format:
```
| Feat-ID | 标题 | 覆盖范围 | 预估复杂度 |
|---------|------|----------|-----------|
| Feat-01 | ... | ... | 简单/标准/复杂 |
| Feat-02 | ... | ... | ... |
```

Options:
- Option A (Recommended): Accept the proposed breakdown
- Option B: Adjust breakdown (user describes modifications)
- Option C: Single monolithic Feat (appropriate for simple components with ≤ 5 APIs)

## 0.5.4 Register confirmed Feats and proceed

After user confirmation:
1. **Batch-register** all confirmed Feats in `features.yaml` with `status: Draft` and `spec: null`
2. Return to **Step 0.4–0.6** to complete registration and index regeneration
3. Proceed to **Step 1** with the **first Feat** — each subsequent Feat repeats Steps 1–6 (design.md uses the incremental-merge path for Feat-02+)
