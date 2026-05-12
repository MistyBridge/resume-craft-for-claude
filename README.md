# Resume Craft — AI-Powered Resume Generator for Claude Code

基于 Claude Code 的智能简历生成 Skill。用户以任意形式提供信息（口述、粘贴、文件上传），经过 7 阶段状态机编排，生成专业排版的简历，支持 HTML/PDF/DOCX/MD 四种格式导出。

## 特性

- **多模态信息采集**：支持 PDF/DOCX/图片/压缩包/音频/邮件等文件自动解析，GitHub 仓库自动抓取
- **岗位定向匹配**：JD 解析 → 关键词提取 → ATS 优化 → 匹配报告
- **16 学科模板**：计算机科学、金融经济、法学、医学、设计艺术等，根据岗位自动匹配
- **6 套视觉主题**：Onyx 黑金、Azure 科技蓝、Ivy 学术衬线、Terracotta 创意暖调、Emerald 清新绿、Noir 暗夜极客
- **三档篇幅控制**：简略(800-1500字) / 正常(1500-3000字) / 详细(≥3000字)
- **篇幅自检**：阶段5自动统计字数，超标建议简写/删除，不足建议详写/新增
- **模块级风格选择**：每个 Section 整体选择技术深度/业务成果/简洁专业方向
- **四格式导出**：HTML 预览、PDF (weasyprint / puppeteer)、DOCX (docx skill / npm)、MD

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/MistyBridge/resume-craft.git
cd resume-craft
```

### 2. 安装依赖

```bash
# Windows
tools\setup.bat

# Linux / macOS
bash tools/setup.sh
```

这会自动安装：
- Python 依赖：`jinja2`、`html2text`、`weasyprint`
- Node.js 依赖：`docx`、`puppeteer`

### 3. 在 Claude Code 中使用

将项目目录加载到 Claude Code 中，说「帮我写简历」即可触发 Skill。

## 状态机流程

```
阶段0 ──→ 阶段1 ──→ 阶段2 ──→ 阶段3 ──→ 阶段4 ──→ 阶段5 ──→ 阶段6
启动      岗位录入   信息收集   模板设计   内容填充   篇幅自检   渲染导出
                      +篇幅选择                         +模块调整
```

| 阶段 | 说明 | 可跳过 |
|------|------|--------|
| 0 | 选择模式（新建 / 加载档案） | 否 |
| 1 | 收集 JD、公司名、岗位名 | 是 |
| 2 | 文件解析 + 实体提取 + 篇幅选择 | 否 |
| 3 | 16学科匹配 + 6主题选择 | 是 |
| 4 | 逐模块三选一润色 + ATS优化 | 否 |
| 5 | 字数统计 → 简写/详写/增删模块 | 否 |
| 6 | HTML → PDF → DOCX → MD | 否 |

## 项目结构

```
resume-craft/
├── SKILL.md                  # 主编排器（状态机定义）
├── stages/                   # 7 个阶段执行指令
│   ├── stage-0-start.md
│   ├── stage-1-job.md
│   ├── stage-2-input.md
│   ├── stage-3-design.md
│   ├── stage-4-polish.md
│   ├── stage-5-adjust.md
│   └── stage-6-export.md
├── scripts/                  # Python 渲染引擎
│   ├── render.py             # Jinja2 模板引擎
│   ├── export.py             # 统一导出入口
│   └── themes.json           # 6 套主题配置
├── converters/               # Python 格式转换
│   ├── to_pdf.py             # HTML → PDF (weasyprint)
│   └── to_md.py              # HTML → MD (html2text)
├── tools/                    # Node.js 格式转换
│   ├── gen-docx.js           # JSON → DOCX (docx npm)
│   ├── gen-pdf.js            # HTML → PDF (puppeteer)
│   ├── package.json
│   ├── setup.bat             # Windows 一键安装
│   └── setup.sh              # Linux/macOS 一键安装
├── templates/                # Jinja2 前端模板
│   ├── resume.html           # 简历模板
│   └── disciplines.json      # 16 学科配置
├── data/                     # 用户数据（gitignored）
│   ├── input/                # 用户上传文件
│   ├── profiles/             # 结构化档案 JSON
│   └── output/               # 生成的简历
├── .claude/                  # Claude Code 配置
│   ├── settings.json         # 项目级权限
│   └── settings.local.json   # 本地设置（gitignored）
├── requirements.txt          # Python 依赖
├── LICENSE                   # GNU AGPL v3.0
└── README.md
```

## 技术架构

### 渲染管线

```
profile.json                    # 结构化档案数据
    │
    ▼
render.py (Jinja2)              # 模板引擎渲染
    │
    ▼
resume.html                     # 自包含 HTML（CSS 内联）
    │
    ├──→ to_pdf.py (weasyprint)  → resume.pdf
    ├──→ gen-pdf.js (puppeteer)  → resume.pdf
    ├──→ to_md.py (html2text)    → resume.md
    └──→ gen-docx.js (docx npm)  → resume.docx
```

### 学科模板系统

`templates/disciplines.json` 定义 17 个学科模板（含通用），每个包含：
- `keywords`：用于自动匹配的关键词列表
- `sections`：Section 顺序（如 CS 专业将 Skills 前置）
- `emphasis`：各 Section 权重（dominant > high > normal）
- `theme`：默认主题
- `design_notes`：该学科最佳实践说明

### 主题系统

`scripts/themes.json` 定义 6 套 CSS 变量主题，通过 Jinja2 注入到 HTML 模板中。每套主题包含 colors / fonts / layout 三组变量。

## 格式转换工具

| 格式 | 工具 | 底层引擎 | Stars |
|------|------|---------|-------|
| HTML | `scripts/render.py` | Jinja2 | — |
| PDF | `converters/to_pdf.py` | WeasyPrint | — |
| PDF | `tools/gen-pdf.js` | Puppeteer | 88k+ |
| DOCX | `tools/gen-docx.js` | docx (npm) | 4k+ |
| MD | `converters/to_md.py` | html2text | — |

## 许可证

本项目采用 [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html)。

Copyright (C) 2026 MistyBridge

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

## 致谢

- 简历模板设计参考 [Reactive Resume](https://github.com/AmruthPillai/Reactive-Resume) (36k★)
- PDF 渲染引擎 [Puppeteer](https://github.com/puppeteer/puppeteer) (88k★)
- DOCX 生成引擎 [docx](https://github.com/dolanmedia/docx) (4k★)
