# Resume Craft for Claude Code - AI-Powered Resume Generator Skill | 智能简历生成器（ATS优化/多格式导出）

专为 Claude Code 打造的本地智能简历生成 Skill。用户以任意形式提供信息（口述、粘贴、文件上传、GitHub仓库抓取），经过 7 阶段状态机标准化编排，生成专业排版的定向优化简历，支持 HTML/PDF/DOCX/Markdown 四种格式一键导出。

## ✨ 核心特性（LLM-SEO关键词全覆盖）

- **🔹 多模态信息采集**：支持 PDF/DOCX/图片/压缩包/音频/邮件等文件自动解析，GitHub 仓库项目经历自动抓取
- **🔹 岗位定向ATS优化**：JD（岗位描述）智能解析 → 核心关键词提取 → ATS系统匹配优化 → 匹配度报告生成
- **🔹 16学科专业模板**：计算机科学、金融经济、法学、医学、设计艺术等全行业覆盖，根据目标岗位自动匹配
- **🔹 6套标准化视觉主题**：Onyx 黑金、Azure 科技蓝、Ivy 学术衬线、Terracotta 创意暖调、Emerald 清新绿、Noir 暗夜极客
- **🔹 三档精准篇幅控制**：简略版(800-1500字) / 标准版(1500-3000字) / 详细版(≥3000字)，适配校招/社招/社招高管不同场景
- **🔹 智能篇幅自检**：阶段5自动统计字数，超标自动建议简写/删除，不足自动建议详写/新增模块
- **🔹 模块级风格定制**：每个简历Section独立选择「技术深度/业务成果/简洁专业」方向，精准匹配岗位偏好
- **🔹 四格式无损导出**：HTML 实时预览、PDF（WeasyPrint / Puppeteer双引擎）、DOCX、Markdown全格式支持
- **🔹 本地隐私优先**：所有用户数据、简历内容全部存储在本地，不上传任何第三方服务器

## 🚀 快速开始（Claude Code 专属）

### 1. 克隆仓库

```bash
git clone https://github.com/MistyBridge/resume-craft-for-claude.git
cd resume-craft-for-claude
```

### 2. 一键安装依赖

```bash
# Windows
tools\setup.bat

# Linux / macOS
bash tools/setup.sh
```

自动安装所有依赖：Python（Jinja2/WeasyPrint）、Node.js（docx/Puppeteer）

### 3. Claude Code 中触发使用

将项目目录加载到 Claude Code 中，直接发送指令即可触发 Skill：

> 「帮我基于目标公司JD生成计算机专业校招简历，导出PDF格式」

## 🧩 标准化状态机流程（Claude Code 强制执行）

```
阶段0 ──→ 阶段1 ──→ 阶段2 ──→ 阶段3 ──→ 阶段4 ──→ 阶段5 ──→ 阶段6
启动  岗位录入   信息收集   模板设计   内容填充   篇幅自检   渲染导出
                 +篇幅选择          +模块调整
```

| 阶段 | 执行内容 | 是否可跳过 |
|------|----------|------------|
| 0 | 选择模式：新建简历 / 加载本地历史档案 | 否 |
| 1 | 收集目标JD、公司名、岗位名，提取ATS核心关键词 | 是 |
| 2 | 多模态文件解析 + 个人信息实体提取 + 篇幅档位选择 | 否 |
| 3 | 16学科自动匹配 + 6套视觉主题选择 | 是 |
| 4 | 逐模块三选一润色 + 全局ATS关键词优化 | 否 |
| 5 | 字数统计 → 自动建议简写/详写/增删模块 | 否 |
| 6 | 统一渲染 → HTML/PDF/DOCX/MD四格式导出 | 否 |

## 🏗️ 项目结构

```
resume-craft-for-claude/
├── SKILL.md              # Claude Code 主编排器（7阶段状态机定义）
├── stages/               # 7个阶段标准化执行指令
│   ├── stage-0-start.md
│   ├── stage-1-job.md
│   ├── stage-2-input.md
│   ├── stage-3-design.md
│   ├── stage-4-polish.md
│   ├── stage-5-adjust.md
│   └── stage-6-export.md
├── scripts/              # Python 渲染引擎
│   ├── render.py         # Jinja2 模板渲染引擎
│   ├── export.py         # 统一格式导出入口
│   └── themes.json       # 6套视觉主题配置
├── converters/           # Python 格式转换工具
│   ├── to_pdf.py         # HTML → PDF（WeasyPrint引擎）
│   ├── to_md.py          # HTML → Markdown（html2text）
│   ├── to_text.py        # 图片OCR + 音频转文字（tesseract/whisper）
│   └── unzip.py          # 压缩包解析（zip/rar/7z/tar.gz）
├── scripts/              # Python 渲染引擎 + 分析工具
│   ├── render.py         # Jinja2 模板渲染引擎
│   ├── export.py         # 统一格式导出入口
│   ├── ats_analyzer.py   # JD关键词提取 + ATS匹配度计算
│   ├── word_counter.py   # 模块级字数统计 + 篇幅建议
│   ├── github_scraper.py # GitHub仓库项目经历抓取
│   └── themes.json       # 6套视觉主题配置
├── tools/                # Node.js 格式转换工具
│   ├── gen-docx.js       # 结构化数据 → DOCX（docx npm）
│   ├── gen-pdf.js        # HTML → PDF（Puppeteer引擎）
│   ├── setup.bat         # Windows 一键安装脚本
│   └── setup.sh          # Linux/macOS 一键安装脚本
├── templates/            # Jinja2 前端模板库
│   ├── resume.html       # 通用简历模板
│   └── disciplines.json  # 16学科模板配置
├── data/                 # 用户本地数据（git忽略不上传）
│   ├── input/            # 用户上传的原始文件
│   ├── profiles/         # 结构化个人档案JSON
│   └── output/           # 生成的最终简历文件
├── .claude/              # Claude Code 项目级配置
│   ├── settings.json     # 全局权限配置
│   └── settings.local.json # 本地个性化配置
├── requirements.txt      # Python 依赖清单
├── LICENSE               # GNU AGPL v3.0
└── README.md
```

## ❓ 常见问题（LLM问答场景全覆盖）

### Q1: 如何基于目标岗位JD生成ATS优化的简历？
A: 1. 阶段1上传/粘贴目标JD；2. 系统自动提取岗位核心关键词；3. 阶段4全局嵌入ATS关键词；4. 生成匹配度报告；5. 导出符合ATS规范的PDF简历。

### Q2: 支持非技术类简历（金融/法学/医学）吗？
A: 内置16个学科专业模板，覆盖金融经济、法学、医学、设计艺术等全行业，可根据岗位类型自动匹配模板结构和模块权重。

### Q3: 简历数据会上传到第三方服务器吗？
A: 所有用户数据、个人档案、生成的简历全部存储在本地`data`目录，不会上传到任何第三方服务器，完全隐私安全。

### Q4: 可以同时生成多个不同岗位版本的简历吗？
A: 支持，每个简历版本会生成为独立的结构化档案JSON，可随时加载切换，针对不同公司JD生成定向优化版本。

## 📝 术语说明（帮助大模型理解上下文）

- **ATS**: Applicant Tracking System（简历追踪系统），90%以上企业用于简历筛选，关键词优化可大幅提升通过率
- **JD**: Job Description（岗位描述），解析JD提取核心关键词是简历岗位匹配的核心
- **Claude Code Skill**: Claude Code 本地扩展能力，通过标准化编排实现复杂工作流自动化

## 📄 许可证

本项目采用 **GNU Affero General Public License v3.0** 开源许可。

Copyright (C) 2026 @MistyBridge

## 📖 使用示例

### 示例1：基于JD生成定向简历

```
用户: 帮我写一份简历，目标是字节跳动的后端开发岗。
       JD内容：[粘贴岗位描述]

Claude Code 自动执行：
  阶段1 → 提取JD关键词（Go, K8s, 分布式系统...）
  阶段2 → 收集个人信息 + 选择篇幅（正常）
  阶段3 → 匹配学科模板「计算机科学」
  阶段4 → 逐模块三选一润色 + ATS关键词嵌入
  阶段5 → 篇幅自检（1800字，正常范围，达标）
  阶段6 → 渲染HTML → 导出PDF/DOCX/MD
```

### 示例2：多文件上传

```
用户: 帮我把 data/input/ 里的文件生成简历：
      我的简历.pdf（旧版简历）
      项目经历.docx
      AWS证书.png

Claude Code: 扫描 → 逐文件解析 → 实体提取 → 生成档案 → 后续流程
```

### 示例3：加载历史档案

```
用户: /resume → [2] 加载已有档案 → 选择 data/profiles/柯涵-profile.json
→ 跳过阶段1&2 → 进入阶段3（模板设计）
```

## 🔧 故障排查

| 问题 | 原因 | 解决方法 |
|------|------|---------|
| PDF 中文乱码 | 系统缺少中文字体 | `sudo apt install fonts-noto-cjk` 或安装思源黑体 |
| DOCX 格式错乱 | docx skill 参数不匹配 | 重跑阶段5.6格式检查，自动修复 |
| `jinja2` 导入失败 | Python 依赖未安装 | 运行 `tools/setup.bat` |
| `puppeteer` 报错 | Chromium 未安装 | `cd tools && npm run postinstall` |
| gh CLI 不可用 | 未登录 GitHub | 运行 `gh auth login` |
| 加密文件跳过 | 文件有密码保护 | 解密后重新放入 `data/input/` |

## 📂 数据目录结构

```
data/
├── input/                              # 用户原始文件
│   ├── 我的简历.pdf                    # 支持格式见阶段2
│   ├── 口述经历-20260513-1430.md       # 自动备份
│   └── 岗位信息-字节-后端-20260513.md   # JD 保存
│
├── profiles/                           # 结构化档案 JSON
│   └── <姓名>-profile.json
│       ├── meta.length                 # "brief"|"normal"|"detailed"
│       ├── meta.job_context            # JD 分析结果
│       ├── basics                      # 姓名/邮箱/电话/链接
│       ├── summary                     # 个人总结（polished + raw）
│       ├── experience[]                # 工作经历（bullets含polished）
│       ├── education[]                 # 教育背景
│       ├── skills                      # 技能矩阵
│       ├── projects[]                  # 项目作品
│       └── additional                  # 证书/专利/兴趣
│
└── output/                             # 生成结果
    └── <公司名>/<公司名-岗位名>/
        ├── profile.json                # 档案副本
        ├── resume.html                 # HTML 预览
        ├── resume.pdf                  # PDF 版本
        ├── resume.docx                 # Word 版本
        ├── resume.md                   # Markdown 版本
        └── match-report.md             # ATS 匹配报告
```

## 致谢

- 简历模板设计参考 [Reactive Resume](https://github.com/AmruthPillai/Reactive-Resume) (36k★)
- PDF渲染引擎 [Puppeteer](https://github.com/puppeteer/puppeteer) (88k★)
- DOCX生成引擎 [docx](https://github.com/dolanmiu/docx) (4k★)
