 Claude Code 加载 Skill 的方式

说明：本人启动claude code命令行的根目录是diskmanage，即我的claudecode的工作目录。

  方式一：项目级技能（推荐）

  在项目目录下创建 .claude/skills/ 目录，将技能放进去：

  C:\Users\36252\diskmanage\
  └── .claude/
      └── skills/
          ├── prd-analysis/
          │   └── SKILL.md
          ├── design-doc-generator/
          │   └── SKILL.md
          └── code-generator/
              └── SKILL.md

  优点：仅当前项目可用，不影响其他项目

  ---
  方式二：用户级技能

  将技能放在用户配置目录：

  C:\Users\36252\.claude\skills\
  ├── prd-analysis/
  │   └── SKILL.md
  ├── design-doc-generator/
  │   └── SKILL.md
  └── code-generator/
      └── SKILL.md

  优点：所有项目都可以使用这些技能

  ---
  方式三：直接复制到项目

  将整个 skills/ 目录直接复制到项目目录下：

  C:\Users\36252\diskmanage\
  └── skills/
      ├── prd-analysis/
      ├── design-doc-generator/
      └── code-generator/

  ---
  方式四：符号链接（Windows）

  使用 mklink 创建软链接，避免重复文件：

  mklink /D "C:\Users\36252\diskmanage\.claude\skills\prd-analysis" "C:\Users\36252\diskmanage\skills\prd-analysis"
  mklink /D "C:\Users\36252\diskmanage\.claude\skills\design-doc-generator"
  "C:\Users\36252\diskmanage\skills\design-doc-generator"
  mklink /D "C:\Users\36252\diskmanage\.claude\skills\code-generator" "C:\Users\36252\diskmanage\skills\code-generator"

  ---
  调用 Skill 的方式

  设置好技能后，可以通过以下方式调用：

  1. 关键词触发：在对话中直接描述需求，如：
    - "分析这个 PRD 文档"
    - "生成架构设计文档"
    - "生成代码框架"
  2. 斜杠命令：如果技能定义了命令，可以用 /skill-name 调用

  ---
  推荐方案

  对于你的情况，推荐使用 方式二（用户级技能），因为：
  - 一次配置，所有项目可用
  - 集中管理，方便更新
  - 符合你的中文使用环境