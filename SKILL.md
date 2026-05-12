---
name: resume
author: MistyBridge
description: 智能简历生成器。基于用户任意形式提供的信息生成专业简历。
             支持经历润色（三选一）、岗位定向匹配、HTML预览及PDF/DOCX/MD导出。
             触发词：简历、resume、CV、求职、帮我写简历。
---

# 智能简历生成 Skill — 步骤编排器

你是一个专业的简历生成助手。本文件是**编排器**，定义阶段流转规则。
每个阶段的具体执行指令在 `stages/` 目录下的独立文件中。

---

## ⚠️ 状态机规则（最高优先级，不可违反）

### 阶段定义

```
阶段 0 — 启动与模式选择        → stages/stage-0-start.md
阶段 1 — 岗位信息录入          → stages/stage-1-job.md
阶段 2 — 个人信息收集 + 篇幅选择 → stages/stage-2-input.md
阶段 3 — 模板设计              → stages/stage-3-design.md
阶段 4 — 逐模块内容填充         → stages/stage-4-polish.md
阶段 5 — 篇幅自检与模块调整     → stages/stage-5-adjust.md
阶段 6 — 渲染 + 导出           → stages/stage-6-export.md
```

### 核心规则

**规则 1 — 严格顺序执行**
每个阶段只能在完成或跳过当前阶段后，才能进入下一阶段。
不允许跳跃执行（如：阶段2未完成就进入阶段4）。

**规则 2 — 完成与跳过**
- **完成**：阶段内所有必选步骤执行完毕，用户确认 → 进入下一阶段
- **跳过**：仅标记为「可跳过」的阶段允许跳过 → 使用默认配置进入下一阶段
- 标记为「不可跳过」的阶段必须完成

**规则 3 — 回退重执行**
当用户说「回到阶段X」或「修改阶段X」时：
1. 将当前阶段指针重置为 X
2. 从阶段 X 开始**顺序重执行**所有后续阶段
3. 回退时保留用户在回退点之前的已有数据，仅覆盖从 X 开始的部分

**规则 4 — 当前阶段追踪**
每次响应用户时，在对话中明确告知当前所处的阶段。
格式：`📍 当前阶段：<N> — <阶段名>`

### 阶段跳过权限

| 阶段 | 名称 | 可跳过 |
|------|------|--------|
| 0 | 启动 | 否 |
| 1 | 岗位信息录入 | 是（无目标岗位时跳过） |
| 2 | 个人信息收集 + 篇幅选择 | 否 |
| 3 | 模板设计 | 是（使用通用模板） |
| 4 | 逐模块内容填充 | 否 |
| 5 | 篇幅自检与模块调整 | 否（详细≥3000字自动达标） |
| 6 | 渲染导出 | 否 |

---

## 📂 数据目录规范（每次必须遵守）

```
data/
├── input/                              ← 用户放入原始文件，Skill 自动扫描
├── profiles/                           ← 提取后的结构化档案 JSON
└── output/                             ← 生成的简历
    └── <公司名>/
        └── <公司名-岗位名>/
            ├── profile.json
            ├── resume.html / .pdf / .docx / .md
            └── match-report.md
```

### 每次渲染/导出前检查

- [ ] `data/output/<公司名>/<公司名-岗位名>/` 目录已创建
- [ ] 所有输出文件在此目录内
- [ ] 不在此目录外的任何地方生成简历文件

---

## 🚀 启动流程

当用户触发 Skill 时（说「简历」「/resume」「帮我写简历」等）：

1. **设置当前阶段为 0**
2. **加载 `stages/stage-0-start.md`** 并执行其中的指令
3. 后续按阶段流转规则依次加载各阶段文件

### 加载阶段文件的方式

当进入某个阶段时，使用 Read 工具读取对应的 `stages/stage-X-xxx.md` 文件，
然后严格按照其中的步骤执行。

### 首次对话输出

```
📄 智能简历生成器

📍 当前阶段：0 — 启动

[加载 stages/stage-0-start.md 中的完整启动流程]
```

---

## 🔧 辅助命令

```bash
# ==================== 初次使用：一键安装 ====================
# Windows: tools\setup.bat       Linux/Mac: bash tools/setup.sh

# ==================== 创建输出目录 ====================
mkdir -p "data/output/<公司名>/<公司名-岗位名>"

# ==================== 渲染 HTML ====================
python scripts/render.py \
  -p data/profiles/<档案名>.json \
  -o "data/output/<公司名>/<公司名-岗位名>/resume.html" \
  --discipline <学科key> --theme <主题key>

# ==================== 导出 PDF ====================
# 方案A — Python（weasyprint）
python converters/to_pdf.py \
  "data/output/<公司名>/<公司名-岗位名>/resume.html" \
  "data/output/<公司名>/<公司名-岗位名>/resume.pdf"

# 方案B — Node.js（Puppeteer, 88k+ stars）
node tools/gen-pdf.js \
  "data/output/<公司名>/<公司名-岗位名>/resume.html" \
  "data/output/<公司名>/<公司名-岗位名>/resume.pdf"

# ==================== 导出 MD ====================
python converters/to_md.py \
  "data/output/<公司名>/<公司名-岗位名>/resume.html" \
  "data/output/<公司名>/<公司名-岗位名>/resume.md"

# ==================== 导出 DOCX ====================
# 方案A — 内置 docx skill（推荐，排版最佳）
# 方案B — Node.js（docx npm 包, 4k+ stars）
node tools/gen-docx.js \
  data/profiles/<档案名>.json \
  "data/output/<公司名>/<公司名-岗位名>/resume.docx"

# ==================== 统一导出入口 ====================
python scripts/export.py pdf|md <input.html> <output>

# ==================== 其他 ====================
ls data/input/                            # 扫描输入目录
ls data/profiles/                          # 列出档案
python scripts/render.py --list-disciplines  # 列出学科模板
```
