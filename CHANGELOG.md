# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [未发布] (Unreleased)

### 新增 (Added)
- 🌐 **Web 服务器模式** ⭐
  - 新增 `--serve` 命令行参数启动文档浏览服务器
  - 内置 Flask Web 服务器，运行在 `http://127.0.0.1:5000`
  - 美观的 Markdown 渲染（代码高亮、表格、Mermaid 图表）
  - 自动生成目录（TOC）和文件树导航
  - 支持指定文档目录：`codeviewx --serve -o docs`
  - 使用流程：生成文档 → 启动服务器 → 浏览器访问
  - **依赖**：新增 `flask>=2.0.0` 和 `markdown>=3.4.0` 依赖
  
- 📊 **实时进度提示功能（增强版）** ⭐
  - **简洁一行式显示**（前25步）- 工具名 + 返回结果摘要：
    - 📖 读取：`✓ 行数 | 内容预览前60字符...`（如 `✓ 42 行 | [tool.poetry] name = "codeviewx"...`）
    - 📁 列表：`✓ 项数 | 前3项 ... (+N剩余)`（如 `✓ 8 项 | codeviewx, tests, examples ... (+5)`）
    - 🔎 搜索：`✓ 匹配数 | 首个匹配前50字符...`（如 `✓ 127 处匹配 | from deepagents import Agent...`）
    - ⚙️ 命令：`✓ 输出摘要前60字符...`（如 `✓ Package installed successfully...`）
    - 格式：`工具图标 工具名: 结果摘要`，清晰直观
    - TODO 工具例外：不显示返回结果，保持任务列表格式
  - **智能 TODO 显示**：仅在关键时刻显示任务规划（📋 任务规划）
    - 显示所有 TODO 任务（完整内容，不截断）
    - 首次创建任务时显示
    - 有实质性进展时更新（完成数 +2）
    - 全部完成时显示最终状态
    - 避免重复刷屏，保持输出简洁
  - **AI 消息显示**：展示 AI 的思考和规划内容（💭 AI: ...）
  - **分析阶段提示**：自动检测项目分析阶段（🔍 分析项目结构...）
  - **文档生成进度**：实时显示文档生成（📄 正在生成文档 (1): README.md）
  - **统计摘要**：完成时显示汇总信息（共生成文档数、执行步骤数）
  - **清爽输出**：自动隐藏 HTTP 请求日志（httpx/httpcore），输出更简洁
  - Verbose 模式保持原有详细日志
  - 进度演示脚本和测试 (`examples/progress_demo.py`, `tests/test_progress.py`)

- 🌍 **多语言文档生成支持**
  - 支持 8 种主要语言：Chinese, English, Japanese, Korean, French, German, Spanish, Russian
  - 自动检测系统语言功能 (`detect_system_language()`)
  - CLI 新增 `-l/--language` 参数
  - 系统提示词动态注入文档语言变量

### 修复 (Fixed)
- 🐛 **Web 服务器模板路径修复**
  - 修复模板文件 `doc_detail.html` 找不到的问题
  - 使用绝对路径配置 Flask 的 template_folder 和 static_folder
  - 在 `pyproject.toml` 中添加模板和静态文件到 package-data
  - 创建 `codeviewx/static/` 目录以存放静态资源

### 优化 (Optimized)
- ⚡ **系统提示词压缩** 🔥
  - 精简 `DocumentEngineer.md` 从 **33KB (868行) → 10KB (275行)**
  - **减少 70% 大小**，解决 API Prompt 超长错误（error type 1261）
  - 保留所有核心功能和质量标准
  - 移除冗余示例和重复说明
  - 备份原文件为 `DocumentEngineer_original.md`
  - 提升 API 调用成功率和响应速度

### 改进 (Improved)
- 📝 **DocumentEngineer 提示词增强**
  - 新增"技术栈验证与假设避免"原则
  - 强调不要假设任何库或框架存在
  - 要求先验证依赖文件和导入语句
  - 使用代码中实际的命名，不凭想象命名
  - 增加准确性检查清单

---

## [0.1.0] - 2024-10-15

### 新增 (Added)
- 🚀 初始版本发布
- ✨ AI 驱动的项目文档生成功能
- 🔧 基于 deepagents 框架的智能 Agent
- 📁 真实文件系统操作工具集成
- 🔎 Ripgrep 代码搜索集成
- 📖 多文件文档结构生成（README, 01-11 章节）
- 🎨 Mermaid 图表支持
- 🖥️ 命令行界面（Click）
- 📦 项目打包和分发配置

### 文档 (Documentation)
- 📚 完整的 README.md
- 📝 使用示例和快速开始指南
- 🏗️ 项目架构说明
- 🔄 开发流程文档

---

## 版本说明

### 版本号规范
本项目遵循 [语义化版本 2.0.0](https://semver.org/spec/v2.0.0.html)：
- **主版本号（Major）**: 不兼容的 API 修改
- **次版本号（Minor）**: 向下兼容的功能性新增
- **修订号（Patch）**: 向下兼容的问题修正

### 图例
- ✨ 新功能
- 🐛 Bug 修复
- 📝 文档更新
- 🎨 代码格式/结构优化
- ⚡ 性能优化
- 🔧 配置变更
- 🚀 部署相关
- ⭐ 重要更新
- 🔥 突破性变更

