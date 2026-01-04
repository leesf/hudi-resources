# 如何在本地向 Claude Code 注入自定义技能

## 概述

本指南说明如何在本地运行 Claude Code 时注入自定义技能。自定义技能通过添加专门的工具、知识领域或工作流来扩展 Claude Code 的功能，以满足您的特定需求。

## 什么是自定义技能？

自定义技能是增强 Claude Code 功能的模块化扩展。它们可以：

- 添加特定领域的知识（例如：Apache Hudi、数据湖操作）
- 与自定义工具和 API 集成
- 实现专门的工作流
- 提供项目特定的上下文和约定

## 前置要求

开始之前，请确保您拥有：

- 本地安装的 Claude Code
- 访问 Claude Code 配置目录的权限
- 基本的 JSON/YAML 配置知识
- （可选）用于测试技能的开发环境

## 配置位置

Claude Code 将其配置存储在以下位置：

### Linux/macOS
```
~/.config/claude-code/skills/
```

### Windows
```
%APPDATA%\claude-code\skills\
```

## 创建自定义技能

### 1. 技能定义结构

在 skills 目录中创建新的 JSON 或 YAML 文件：

```json
{
  "name": "hudi-expert",
  "version": "1.0.0",
  "description": "Apache Hudi 数据湖专家知识",
  "type": "knowledge",
  "capabilities": [
    "hudi-operations",
    "data-lake-architecture",
    "streaming-ingestion"
  ],
  "context": {
    "domain": "big-data",
    "framework": "apache-hudi"
  },
  "prompts": {
    "system": "你是 Apache Hudi 数据湖专家。提供 Hudi 表操作、流式数据摄取和数据湖架构最佳实践的指导。",
    "examples": [
      {
        "input": "如何创建 Hudi 表？",
        "output": "要创建 Hudi 表，可以使用 Spark DataFrameWriter 配合 hudi 格式..."
      }
    ]
  },
  "tools": [
    {
      "name": "hudi-cli",
      "command": "hudi-cli",
      "description": "执行 Hudi CLI 命令"
    }
  ]
}
```

### 2. 技能类型

#### 知识技能
注入专门的领域知识：

```json
{
  "type": "knowledge",
  "knowledge_base": {
    "sources": [
      "/path/to/hudi-docs",
      "/path/to/custom-guides"
    ],
    "index": "enabled"
  }
}
```

#### 工具技能
添加自定义工具和集成：

```json
{
  "type": "tool",
  "tools": [
    {
      "name": "custom-analyzer",
      "endpoint": "http://localhost:8080/analyze",
      "method": "POST",
      "schema": {
        "input": "string",
        "output": "object"
      }
    }
  ]
}
```

#### 工作流技能
定义多步骤工作流：

```json
{
  "type": "workflow",
  "workflows": [
    {
      "name": "hudi-deployment",
      "steps": [
        "validate-config",
        "build-pipeline",
        "deploy-table",
        "verify-ingestion"
      ]
    }
  ]
}
```

## 加载自定义技能

### 方法 1: 配置文件

添加到 `~/.config/claude-code/config.json`：

```json
{
  "skills": {
    "enabled": true,
    "custom_skills_path": "~/.config/claude-code/skills",
    "auto_load": true,
    "skills": [
      "hudi-expert",
      "data-pipeline-builder"
    ]
  }
}
```

### 方法 2: 环境变量

```bash
export CLAUDE_SKILLS_PATH=/path/to/custom/skills
export CLAUDE_ENABLE_CUSTOM_SKILLS=true
```

### 方法 3: 命令行

```bash
claude-code --load-skill /path/to/skill.json
```

### 方法 4: 编程式 API

```python
from claude_code import SkillManager

skill_manager = SkillManager()
skill_manager.load_skill("/path/to/skill.json")
skill_manager.activate("hudi-expert")
```

## 高级技能配置

### 上下文注入

提供项目特定的上下文：

```json
{
  "name": "project-context",
  "context": {
    "project_type": "data-lake",
    "frameworks": ["hudi", "flink", "spark"],
    "conventions": {
      "naming": "snake_case",
      "table_format": "parquet",
      "partition_strategy": "date-based"
    },
    "paths": {
      "data": "/data/lakehouse",
      "configs": "/configs",
      "scripts": "/scripts"
    }
  }
}
```

### 自定义函数

定义可重用的函数：

```json
{
  "functions": [
    {
      "name": "validate_hudi_config",
      "description": "验证 Hudi 表配置",
      "parameters": {
        "config": "object"
      },
      "implementation": {
        "type": "script",
        "path": "./validators/hudi_config.py"
      }
    }
  ]
}
```

### 记忆和状态

启用有状态的技能：

```json
{
  "memory": {
    "enabled": true,
    "type": "persistent",
    "storage": "~/.claude-code/skill-memory",
    "retention": "30d"
  }
}
```

## 示例: Apache Hudi 专家技能

完整的 Hudi 专家知识示例：

```json
{
  "name": "apache-hudi-expert",
  "version": "1.0.0",
  "description": "全面的 Apache Hudi 数据湖专家知识",
  "type": "knowledge",
  "author": "Hudi 社区",
  "tags": ["data-lake", "streaming", "big-data"],
  
  "capabilities": {
    "hudi_operations": {
      "create_table": true,
      "upsert": true,
      "delete": true,
      "query": true,
      "compaction": true,
      "clustering": true
    },
    "integrations": [
      "spark",
      "flink",
      "hive",
      "presto",
      "trino"
    ],
    "storage": [
      "s3",
      "hdfs",
      "azure-blob",
      "gcs"
    ]
  },
  
  "knowledge_sources": [
    {
      "type": "documentation",
      "url": "https://hudi.apache.org/docs/overview",
      "cache": true
    },
    {
      "type": "local",
      "path": "/path/to/hudi-resources"
    }
  ],
  
  "prompts": {
    "system": "你是 Apache Hudi 数据湖专家，深入了解：\n- Hudi 表类型（COW 和 MOR）\n- 流式数据摄取模式\n- 查询优化技术\n- 与计算引擎的集成\n- 生产部署最佳实践\n\n始终提供实用的、生产就绪的解决方案和代码示例。",
    
    "templates": {
      "create_table": "展示如何根据以下要求创建 Hudi 表：${requirements}",
      "troubleshoot": "帮助诊断此 Hudi 问题：${error_message}",
      "optimize": "为此 Hudi 配置提供优化建议：${config}"
    }
  },
  
  "tools": [
    {
      "name": "hudi_cli",
      "description": "执行 Hudi CLI 命令",
      "command": "hudi-cli",
      "args": ["--command", "${command}"]
    },
    {
      "name": "spark_shell_hudi",
      "description": "启动带有 Hudi 依赖的 Spark shell",
      "command": "spark-shell",
      "args": ["--packages", "org.apache.hudi:hudi-spark-bundle:0.14.0"]
    }
  ],
  
  "examples": [
    {
      "title": "创建 COW 表",
      "code": "df.write.format('hudi')\n  .option('hoodie.table.name', 'my_table')\n  .option('hoodie.datasource.write.recordkey.field', 'id')\n  .option('hoodie.datasource.write.partitionpath.field', 'date')\n  .option('hoodie.datasource.write.table.type', 'COPY_ON_WRITE')\n  .mode('append')\n  .save('/path/to/table')"
    },
    {
      "title": "使用 Flink 执行 Upsert",
      "code": "CREATE TABLE hudi_table (\n  id BIGINT,\n  name STRING,\n  ts TIMESTAMP(3)\n) WITH (\n  'connector' = 'hudi',\n  'path' = 's3://bucket/table',\n  'table.type' = 'MERGE_ON_READ'\n);"
    }
  ],
  
  "best_practices": [
    "根据读/写模式使用适当的表类型",
    "为大表配置适当的聚类",
    "启用元数据表以获得更好的性能",
    "为下游处理设置增量查询",
    "监控和调整压缩设置"
  ]
}
```

## 测试自定义技能

### 1. 验证技能定义

```bash
claude-code --validate-skill /path/to/skill.json
```

### 2. 测试技能激活

```bash
claude-code --test-skill hudi-expert --query "如何创建 MOR 表？"
```

### 3. 调试模式

启用详细日志：

```bash
export CLAUDE_CODE_DEBUG=true
claude-code --load-skill hudi-expert
```

## 常见用例

### 1. 项目特定约定

```json
{
  "name": "project-conventions",
  "type": "knowledge",
  "context": {
    "coding_style": "Python 遵循 PEP 8",
    "naming": {
      "tables": "snake_case",
      "columns": "lowercase",
      "partitions": "dt=YYYY-MM-DD"
    },
    "required_headers": [
      "作者",
      "日期",
      "描述"
    ]
  }
}
```

### 2. 自定义工具集成

```json
{
  "name": "ci-cd-tools",
  "type": "tool",
  "tools": [
    {
      "name": "deploy",
      "command": "./scripts/deploy.sh",
      "description": "部署 Hudi 管道"
    },
    {
      "name": "validate",
      "command": "./scripts/validate.sh",
      "description": "验证数据质量"
    }
  ]
}
```

### 3. 团队知识库

```json
{
  "name": "team-knowledge",
  "type": "knowledge",
  "knowledge_base": {
    "runbooks": "/docs/runbooks",
    "architecture": "/docs/architecture",
    "faqs": "/docs/faqs"
  }
}
```

## 技能管理

### 列出可用技能

```bash
claude-code --list-skills
```

### 启用/禁用技能

```bash
claude-code --enable-skill hudi-expert
claude-code --disable-skill old-skill
```

### 更新技能

```bash
claude-code --update-skill hudi-expert --version 2.0.0
```

## 故障排除

### 技能未加载

1. 检查文件权限：`chmod 644 skill.json`
2. 验证 JSON 语法：`jq . skill.json`
3. 检查日志：`~/.claude-code/logs/skills.log`

### 技能冲突

如果多个技能提供类似的功能：

```json
{
  "skill_priority": {
    "hudi-expert": 10,
    "generic-data-lake": 5
  }
}
```

### 性能问题

优化技能加载：

```json
{
  "optimization": {
    "lazy_load": true,
    "cache_enabled": true,
    "max_context_size": "100KB"
  }
}
```

## 安全考虑

### 1. 技能沙箱

```json
{
  "security": {
    "sandbox": true,
    "allowed_commands": ["read", "analyze"],
    "forbidden_paths": ["/etc", "/sys"]
  }
}
```

### 2. 凭据管理

切勿在技能中存储凭据：

```json
{
  "credentials": {
    "method": "environment",
    "variables": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
  }
}
```

## 最佳实践

1. **模块化设计**：为特定领域创建专注的技能
2. **文档化**：包含清晰的描述和示例
3. **版本控制**：在 Git 中跟踪技能版本
4. **测试**：部署前测试技能
5. **维护**：定期更新技能知识
6. **安全性**：遵循最小权限原则
7. **性能**：优化以实现快速加载
8. **兼容性**：确保与 Claude Code 版本兼容

## 共享技能

### 发布到社区

1. 打包技能：
```bash
tar -czf hudi-expert-skill.tar.gz skill.json README.md
```

2. 通过以下方式共享：
- GitHub 仓库
- 内部技能注册表
- 社区论坛

### 技能仓库结构

```
my-skill/
├── skill.json          # 主技能定义
├── README.md           # 文档
├── examples/           # 使用示例
│   ├── basic.md
│   └── advanced.md
├── tests/              # 测试用例
│   └── test_skill.py
└── resources/          # 附加资源
    └── knowledge/
        └── docs.md
```

## 资源

### 文档
- Claude Code 官方文档
- 技能开发指南
- API 参考

### 社区
- Claude Code 技能仓库
- 讨论论坛
- Stack Overflow 标签：`claude-code-skills`

### 示例
- [Hudi Resources](https://github.com/leesf/hudi-resources) - Apache Hudi 学习资料
- 示例技能画廊
- 社区技能贡献

## 更新日志

### 版本 1.0.0 (2026-01-04)
- 自定义技能注入的初始指南
- 核心概念和示例
- Apache Hudi 专家技能示例
- 最佳实践和故障排除

## 贡献

为本指南做贡献：
1. Fork 仓库
2. 进行改进
3. 提交 pull request
4. 分享您的自定义技能

## 许可证

本指南按原样提供，用于教育和参考目的。

---

**注意**：本指南假设 Claude Code 支持自定义技能注入。实现细节可能因实际的 Claude Code 版本和功能而异。请始终参考官方 Claude Code 文档以获取最准确的信息。
