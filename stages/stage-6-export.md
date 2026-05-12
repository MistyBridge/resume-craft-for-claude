# @MistyBridge — Resume Craft
# 阶段 6 — 渲染 + 导出

> 当前阶段：6 | 上一阶段：5 | 下一阶段：无（流程终点） | 可跳过：否

## 本阶段目标

将最终简历数据渲染为 HTML，并导出为 PDF/DOCX/MD。全部完成后流程结束。

## 前置条件

- 内容已填充完成（阶段4）
- 篇幅自检已通过（阶段5）
- 岗位匹配已应用（阶段4，如有）
- 输出目录已创建：`data/output/<公司名>/<公司名-岗位名>/`

## 执行步骤

### 5.1 保存档案到输出目录

```bash
cp data/profiles/<档案名>.json "data/output/<公司名>/<公司名-岗位名>/profile.json"
```

### 5.2 渲染 HTML

使用阶段3确定的学科模板和主题渲染：

```bash
python scripts/render.py \
  -p data/profiles/<档案名>.json \
  -o "data/output/<公司名>/<公司名-岗位名>/resume.html" \
  --discipline <学科名> \
  --theme <主题名>
```

告知用户 HTML 路径，用户可浏览器预览。

### 5.3 导出 PDF

**方案A — Python（weasyprint）**：

```bash
python converters/to_pdf.py \
  "data/output/<公司名>/<公司名-岗位名>/resume.html" \
  "data/output/<公司名>/<公司名-岗位名>/resume.pdf"
```

**方案B — Node.js（Puppeteer，推荐）**：

```bash
node tools/gen-pdf.js \
  "data/output/<公司名>/<公司名-岗位名>/resume.html" \
  "data/output/<公司名>/<公司名-岗位名>/resume.pdf"
```

如果两者都不可用，回退使用内置 `pdf` skill。

### 5.4 导出 MD（中间格式）

```bash
python converters/to_md.py \
  "data/output/<公司名>/<公司名-岗位名>/resume.html" \
  "data/output/<公司名>/<公司名-岗位名>/resume.md"
```

MD 文件同时作为 DOCX 生成的输入源。

### 5.5 导出 DOCX

**方案A — 内置 docx skill（推荐）**：

基于 MD 文件生成专业排版的 Word 文档：
1. 读取上一步生成的 MD 文件内容
2. 调用 `docx` skill，传入 MD 内容
3. docx skill 生成格式精美的 .docx 文件

**方案B — Node.js（docx npm 包）**：

```bash
node tools/gen-docx.js \
  data/profiles/<档案名>.json \
  "data/output/<公司名>/<公司名-岗位名>/resume.docx"
```

输出：`data/output/<公司名>/<公司名-岗位名>/resume.docx`

### 5.6 DOCX 格式检查与优化

生成 DOCX 后，**必须**进行格式检查，确保输出质量：

#### 5.6.1 加载并校验 DOCX

使用 Read 工具读取生成的 .docx 文件，检查以下项目：

```
🔍 DOCX 格式检查

□ 字体一致性
  · 标题/正文/联系方式所用字体是否统一
  · 中英文混排字体是否协调（中文用中文字体，英文保持原字体）

□ 排版对齐
  · 各 Section 标题对齐方式是否一致
  · 日期/地点等右对齐元素是否整齐
  · 页边距是否均匀

□ 间距检查
  · 段前段后间距是否均匀
  · 行距是否一致（建议 1.15-1.5）
  · Section 之间间距是否清晰

□ 表格/列表
  · 技能列表是否对齐
  · 项目符号缩进是否统一

□ 分页
  · 分页位置是否自然（不在段落中间断开）
  · 篇幅是否符合阶段2设定的目标

□ 特殊字符
  · 无乱码或缺失字符
  · 符号（· | /）显示正常
```

#### 5.6.2 问题修复

如发现格式问题：

```
🔧 发现以下格式问题：

  1. ⚠️ 工作经历模块日期未右对齐
  2. ⚠️ "项目作品"标题页尾孤行，建议在该 Section 前分页
  3. ⚠️ 英文技能名与中文描述字体不一致

修复策略：
  · 问题1 → 调整 docx skill 参数重新生成
  · 问题2 → 在 MD 源中插入分页标记后重新生成
  · 问题3 → 统一字体配置后重新生成

正在修复...
```

修复后重新生成 DOCX，再次检查直到通过。

#### 5.6.3 检查通过

```
✅ DOCX 格式检查通过
  · 字体统一：✓
  · 排版对齐：✓
  · 间距均匀：✓
  · 分页合理：✓
  · 特殊字符：✓
```

### 5.7 完成

```
✅ 简历已生成！

📁 输出目录：data/output/<公司名>/<公司名-岗位名>/
   ├── profile.json      — 档案数据
   ├── resume.html       — HTML 预览
   ├── resume.pdf        — PDF 版本
   ├── resume.docx       — Word 版本（已通过格式检查）
   ├── resume.md         — Markdown 版本
   └── match-report.md   — 匹配报告（如有岗位定向）

🎉 流程完成！
如需针对其他岗位定制，可以说「定向匹配 <岗位>」从头开始新流程。
如需修改当前简历，可以说「回退到阶段X」。
```

---

## 阶段控制

```
完成 → 流程结束
不可跳过
回退 → 可回退到任何前序阶段：
  · 回退到阶段1：修改岗位信息
  · 回退到阶段2：修改基础信息
  · 回退到阶段3：重新设计模板
  · 回退到阶段4：修改内容润色选择
  · 回退到阶段5：重新做篇幅自检与模块调整
```
