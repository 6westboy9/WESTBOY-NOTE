# CLAUDE.md

此文件为 Claude Code (claude.ai/code) 在此代码库中工作时提供指导。

## 项目概述

这不是一个传统的软件项目 - 这是一个名为 **"WESTBOY-NOTE"** 的个人知识库，基于 **Obsidian** 构建。它主要服务于从事 Java/Spring 生态系统开发的程序员/工程师的综合技术知识库。

## 知识库结构

知识库按17个主要类别组织，包含691+个markdown文件：

- **00.OB** - Obsidian配置和字体
- **01.基础框架&方案** - 基础框架和解决方案（Spring、Java等）
- **02.DB&Cache** - 数据库（MySQL、Redis、MongoDB）和缓存
- **03.MQ** - 消息队列
- **04.分布式框架&组件** - 分布式框架和组件
- **05.搜索** - 搜索技术（Elasticsearch、Lucene）
- **06.大数据** - 大数据技术
- **07.系统架构设计** - 系统架构设计
- **08.开发规范** - 开发标准和最佳实践
- **09.开发&工具** - 开发工具和技术
- **10.运维** - 运维/DevOps
- **11.计算机** - 计算机科学基础
- **12.前端** - 前端开发（JavaScript、Vue等）
- **13.编程语言** - 编程语言
- **14.AI** - AI/ML内容
- **15.INTERVIEW** - 面试资料
- **16.WORK** - 工作相关的笔记和项目
- **17.OTHER** - 其他内容

## 主要技术领域

### 后端开发

- **Spring框架**（Spring Boot 3.x、Spring Core）- 深度覆盖
- **Java 17** 和 **JVM** 内部原理
- **MyBatis** 数据库操作框架
- **并发编程** 和 **字节码** 操作
- **网络编程** 和 **HTTP客户端**

### 数据库技术

- **MySQL** 优化和高级特性
- **Redis** 缓存策略
- **MongoDB** NoSQL操作
- **PostgreSQL** 和 **Oracle**

### 前端开发

- **JavaScript/ES6+**、**TypeScript**
- **Vue 3** 框架
- **Electron** 桌面应用

### 基础设施和运维

- **Docker** 容器化
- **消息队列**
- **Elasticsearch** 搜索引擎
- **分布式系统** 设计

## 在此知识库中工作

### 当前工作背景

工作空间显示正在积极开发 **移动护理** 医疗系统项目：
- 主要文件：`16.WORK/2.联新项目/01_日报/2025/` 和 `16.WORK/2.联新项目/02_任务/`
- 架构图：`16.WORK/1.联新知识库/02.移动护理/附件_EXCALIDRAW/`
- 按年月组织的日报和任务跟踪

### 常用操作

- **文件导航**：使用Obsidian的文件浏览器和搜索功能
- **链接管理**：所有markdown文件通过维基风格链接相互连接
- **图表**：使用Excalidraw文件（`.excalidraw.md`）绘制系统架构和流程图
- **Git集成**：通过obsidian-git插件自动每日备份

### Obsidian配置

- **已启用插件**：14个社区插件，包括obsidian-git、obsidian-excalidraw-plugin、obsidian-plantuml、webpage-html-export
- **主题**：已安装多个主题（Blue Topaz、AnuPpuccin、Minimal、Things）
- **工作空间**：当前显示与工作相关文件的分窗布局
- **Git设置**：每10分钟自动提交，每15分钟自动推送，提交格式为"vault backup: YYYY-MM-DD HH:mm:ss"

## 重要说明

1. **无构建系统**：这不是可部署的软件项目 - 没有package.json、pom.xml或构建脚本
2. **知识库性质**：包含实用代码示例、配置片段和技术文档
3. **版本控制**：使用Git进行备份和版本控制，每日自动提交
4. **交叉引用**：大量使用相关技术主题之间的内部链接
5. **持续更新**：不断更新新的学习内容、解决方案和项目文档

## 开发环境背景

- **平台**：macOS (Darwin 24.6.0)
- **IDE**：IntelliJ IDEA（配置为JDK 17）
- **主要语言**：Java和Spring Boot生态系统
- **当前重点**：医疗系统开发（移动护理系统），重点关注移动护理工作流程、文档管理和系统集成