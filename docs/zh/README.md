# CodeViewX 技术文档

> AI 驱动的代码文档生成器

## 项目简介

CodeViewX 是一个基于 AI 的代码文档自动生成工具，使用 Anthropic Claude + DeepAgents + LangChain 技术栈，能够深入分析代码库并生成专业的技术文档。

## 文档结构

本文档按照标准技术文档结构组织，便于开发者快速理解和上手项目：

| 文档 | 描述 | 必要性 |
|------|------|--------|
| **README.md** | 本文件，项目概览和导航 | ✅ 必需 |
| **01-overview.md** | 项目概览、技术栈和目录结构详解 | ✅ 必需 |
| **02-quickstart.md** | 快速开始指南和配置说明 | ✅ 必需 |
| **03-architecture.md** | 系统架构设计和组件说明 | ✅ 推荐 |
| **04-core-mechanisms.md** | 核心工作机制深度解析 | ✅ 推荐 |
| **05-data-models.md** | 数据模型和流程 | 📊 按需 |
| **06-api-reference.md** | API 接口参考文档 | 🔌 按需 |
| **07-development-guide.md** | 开发指南和贡献规范 | 👨‍💻 推荐 |
| **08-testing.md** | 测试策略和用例说明 | 🧪 按需 |

## 文档元信息

- **生成时间**: 2025-06-17
- **分析范围**: 50+ 个文件，15,000+ 行代码
- **项目类型**: Python CLI 工具 + Web 服务
- **主要技术栈**: Python 3.8+, Flask, LangChain, DeepAgents, Anthropic Claude

## 快速导航

### 📖 新手入门
- [项目概览](01-overview.md) - 了解项目整体情况
- [快速开始](02-quickstart.md) - 安装配置和基本使用

### 🏗️ 架构理解
- [系统架构](03-architecture.md) - 理解项目架构设计
- [核心机制](04-core-mechanisms.md) - 深入了解工作原理

### 🔧 开发使用
- [API 参考](06-api-reference.md) - 完整 API 文档
- [开发指南](07-development-guide.md) - 开发和贡献指南

### 🧪 质量保证
- [测试文档](08-testing.md) - 测试策略和用例
- [数据模型](05-data-models.md) - 数据结构和流程

## 核心特性

- 🤖 **AI 智能分析**: 基于 Anthropic Claude 的深度代码理解
- 📝 **完整文档体系**: 自动生成 8 个标准章节
- 🌐 **多语言支持**: 支持中文、英文等 8 种语言
- 🖥️ **文档浏览器**: 内置 Web 服务器优雅展示文档
- ⚡ **快速搜索**: 集成 ripgrep 实现高速代码搜索

## 使用场景

- **新项目接入**: 快速生成技术文档，加速团队上手
- **代码审查**: 深度理解代码结构和设计意图  
- **知识沉淀**: 将代码逻辑转化为易于理解的文档
- **开源项目**: 为开源项目生成专业文档

## 开始使用

```bash
# 安装 CodeViewX
pip install codeviewx

# 为当前目录生成文档
codeviewx

# 启动文档浏览器
codeviewx --serve
```

## 技术栈总览

| 组件 | 技术选型 | 版本 | 用途 |
|------|----------|------|------|
| **核心语言** | Python | 3.8+ | 主要开发语言 |
| **Web 框架** | Flask | 3.0.0 | 文档 Web 服务器 |
| **AI 框架** | LangChain | 0.3.27 | AI 应用开发框架 |
| **AI 模型** | Anthropic Claude | latest | 文档生成核心引擎 |
| **Agent 框架** | DeepAgents | 0.0.5 | AI Agent 代理 |
| **搜索工具** | ripgrep | 2.0.0 | 高性能代码搜索 |
| **文档处理** | Markdown | 3.5.1 | 文档格式化 |

## 许可证

本项目采用 [GNU General Public License v3.0](../LICENSE) 许可证。

---

💡 **提示**: 建议按照文档顺序阅读，从概览开始，逐步深入到架构和核心机制。如有疑问，可参考 [快速开始指南](02-quickstart.md) 或 [开发指南](07-development-guide.md)。