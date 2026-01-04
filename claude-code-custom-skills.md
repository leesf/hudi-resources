# How to Inject Custom Skills into Claude Code Locally

## Overview

This guide explains how to inject custom skills into Claude Code when running it locally. Custom skills extend Claude Code's capabilities by adding specialized tools, knowledge domains, or workflows tailored to your specific needs.

## What are Custom Skills?

Custom skills are modular extensions that enhance Claude Code's functionality. They can:

- Add domain-specific knowledge (e.g., Apache Hudi, data lake operations)
- Integrate with custom tools and APIs
- Implement specialized workflows
- Provide project-specific context and conventions

## Prerequisites

Before you begin, ensure you have:

- Claude Code installed locally
- Access to your Claude Code configuration directory
- Basic understanding of JSON/YAML configuration
- (Optional) Development environment for testing skills

## Configuration Location

Claude Code stores its configuration in the following locations:

### Linux/macOS
```
~/.config/claude-code/skills/
```

### Windows
```
%APPDATA%\claude-code\skills\
```

## Creating a Custom Skill

### 1. Skill Definition Structure

Create a new JSON or YAML file in the skills directory:

```json
{
  "name": "hudi-expert",
  "version": "1.0.0",
  "description": "Apache Hudi data lake expertise",
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
    "system": "You are an expert in Apache Hudi data lakes. Provide guidance on Hudi table operations, streaming data ingestion, and data lake architecture best practices.",
    "examples": [
      {
        "input": "How do I create a Hudi table?",
        "output": "To create a Hudi table, you can use Spark DataFrameWriter with the hudi format..."
      }
    ]
  },
  "tools": [
    {
      "name": "hudi-cli",
      "command": "hudi-cli",
      "description": "Execute Hudi CLI commands"
    }
  ]
}
```

### 2. Skill Types

#### Knowledge Skills
Inject specialized domain knowledge:

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

#### Tool Skills
Add custom tools and integrations:

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

#### Workflow Skills
Define multi-step workflows:

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

## Loading Custom Skills

### Method 1: Configuration File

Add to `~/.config/claude-code/config.json`:

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

### Method 2: Environment Variables

```bash
export CLAUDE_SKILLS_PATH=/path/to/custom/skills
export CLAUDE_ENABLE_CUSTOM_SKILLS=true
```

### Method 3: Command Line

```bash
claude-code --load-skill /path/to/skill.json
```

### Method 4: Programmatic API

```python
from claude_code import SkillManager

skill_manager = SkillManager()
skill_manager.load_skill("/path/to/skill.json")
skill_manager.activate("hudi-expert")
```

## Advanced Skill Configuration

### Context Injection

Provide project-specific context:

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

### Custom Functions

Define reusable functions:

```json
{
  "functions": [
    {
      "name": "validate_hudi_config",
      "description": "Validate Hudi table configuration",
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

### Memory and State

Enable stateful skills:

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

## Example: Apache Hudi Expert Skill

Complete example for Hudi expertise:

```json
{
  "name": "apache-hudi-expert",
  "version": "1.0.0",
  "description": "Comprehensive Apache Hudi data lake expertise",
  "type": "knowledge",
  "author": "Hudi Community",
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
    "system": "You are an expert in Apache Hudi data lakes with deep knowledge of:\n- Hudi table types (COW and MOR)\n- Streaming data ingestion patterns\n- Query optimization techniques\n- Integration with compute engines\n- Production deployment best practices\n\nAlways provide practical, production-ready solutions with code examples.",
    
    "templates": {
      "create_table": "Show how to create a Hudi table with these requirements: ${requirements}",
      "troubleshoot": "Help diagnose this Hudi issue: ${error_message}",
      "optimize": "Suggest optimizations for this Hudi configuration: ${config}"
    }
  },
  
  "tools": [
    {
      "name": "hudi_cli",
      "description": "Execute Hudi CLI commands",
      "command": "hudi-cli",
      "args": ["--command", "${command}"]
    },
    {
      "name": "spark_shell_hudi",
      "description": "Launch Spark shell with Hudi dependencies",
      "command": "spark-shell",
      "args": ["--packages", "org.apache.hudi:hudi-spark-bundle:0.14.0"]
    }
  ],
  
  "examples": [
    {
      "title": "Create COW Table",
      "code": "df.write.format('hudi')\n  .option('hoodie.table.name', 'my_table')\n  .option('hoodie.datasource.write.recordkey.field', 'id')\n  .option('hoodie.datasource.write.partitionpath.field', 'date')\n  .option('hoodie.datasource.write.table.type', 'COPY_ON_WRITE')\n  .mode('append')\n  .save('/path/to/table')"
    },
    {
      "title": "Upsert with Flink",
      "code": "CREATE TABLE hudi_table (\n  id BIGINT,\n  name STRING,\n  ts TIMESTAMP(3)\n) WITH (\n  'connector' = 'hudi',\n  'path' = 's3://bucket/table',\n  'table.type' = 'MERGE_ON_READ'\n);"
    }
  ],
  
  "best_practices": [
    "Use appropriate table type based on read/write patterns",
    "Configure proper clustering for large tables",
    "Enable metadata table for better performance",
    "Set up incremental queries for downstream processing",
    "Monitor and tune compaction settings"
  ]
}
```

## Testing Custom Skills

### 1. Validate Skill Definition

```bash
claude-code --validate-skill /path/to/skill.json
```

### 2. Test Skill Activation

```bash
claude-code --test-skill hudi-expert --query "How do I create a MOR table?"
```

### 3. Debug Mode

Enable verbose logging:

```bash
export CLAUDE_CODE_DEBUG=true
claude-code --load-skill hudi-expert
```

## Common Use Cases

### 1. Project-Specific Conventions

```json
{
  "name": "project-conventions",
  "type": "knowledge",
  "context": {
    "coding_style": "Follow PEP 8 for Python",
    "naming": {
      "tables": "snake_case",
      "columns": "lowercase",
      "partitions": "dt=YYYY-MM-DD"
    },
    "required_headers": [
      "Author",
      "Date",
      "Description"
    ]
  }
}
```

### 2. Custom Tool Integration

```json
{
  "name": "ci-cd-tools",
  "type": "tool",
  "tools": [
    {
      "name": "deploy",
      "command": "./scripts/deploy.sh",
      "description": "Deploy Hudi pipeline"
    },
    {
      "name": "validate",
      "command": "./scripts/validate.sh",
      "description": "Validate data quality"
    }
  ]
}
```

### 3. Team Knowledge Base

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

## Skill Management

### List Available Skills

```bash
claude-code --list-skills
```

### Enable/Disable Skills

```bash
claude-code --enable-skill hudi-expert
claude-code --disable-skill old-skill
```

### Update Skills

```bash
claude-code --update-skill hudi-expert --version 2.0.0
```

## Troubleshooting

### Skill Not Loading

1. Check file permissions: `chmod 644 skill.json`
2. Validate JSON syntax: `jq . skill.json`
3. Check logs: `~/.claude-code/logs/skills.log`

### Skill Conflicts

If multiple skills provide similar capabilities:

```json
{
  "skill_priority": {
    "hudi-expert": 10,
    "generic-data-lake": 5
  }
}
```

### Performance Issues

Optimize skill loading:

```json
{
  "optimization": {
    "lazy_load": true,
    "cache_enabled": true,
    "max_context_size": "100KB"
  }
}
```

## Security Considerations

### 1. Skill Sandboxing

```json
{
  "security": {
    "sandbox": true,
    "allowed_commands": ["read", "analyze"],
    "forbidden_paths": ["/etc", "/sys"]
  }
}
```

### 2. Credential Management

Never store credentials in skills:

```json
{
  "credentials": {
    "method": "environment",
    "variables": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
  }
}
```

## Best Practices

1. **Modular Design**: Create focused skills for specific domains
2. **Documentation**: Include clear descriptions and examples
3. **Version Control**: Track skill versions in Git
4. **Testing**: Test skills before deployment
5. **Maintenance**: Regularly update skill knowledge
6. **Security**: Follow principle of least privilege
7. **Performance**: Optimize for fast loading
8. **Compatibility**: Ensure compatibility with Claude Code versions

## Sharing Skills

### Publishing to Community

1. Package skill:
```bash
tar -czf hudi-expert-skill.tar.gz skill.json README.md
```

2. Share via:
- GitHub repository
- Internal skill registry
- Community forums

### Skill Repository Structure

```
my-skill/
├── skill.json          # Main skill definition
├── README.md           # Documentation
├── examples/           # Usage examples
│   ├── basic.md
│   └── advanced.md
├── tests/              # Test cases
│   └── test_skill.py
└── resources/          # Additional resources
    └── knowledge/
        └── docs.md
```

## Resources

### Documentation
- Claude Code Official Documentation
- Skill Development Guide
- API Reference

### Community
- Claude Code Skills Repository
- Discussion Forums
- Stack Overflow Tag: `claude-code-skills`

### Examples
- [Hudi Resources](https://github.com/leesf/hudi-resources) - Apache Hudi learning materials
- Sample Skills Gallery
- Community Skill Contributions

## Changelog

### Version 1.0.0 (2026-01-04)
- Initial guide for custom skill injection
- Core concepts and examples
- Apache Hudi expert skill example
- Best practices and troubleshooting

## Contributing

To contribute to this guide:
1. Fork the repository
2. Make improvements
3. Submit pull request
4. Share your custom skills

## License

This guide is provided as-is for educational and reference purposes.

---

**Note**: This guide assumes Claude Code supports custom skill injection. Implementation details may vary based on the actual Claude Code version and capabilities. Always refer to official Claude Code documentation for the most accurate information.
