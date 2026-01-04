# Claude Code Custom Skills - Examples

This directory contains example skill definitions for use with Claude Code.

## Available Skills

### 1. Apache Hudi Expert Skill (`hudi-expert-skill.json`)

A comprehensive skill definition for Apache Hudi expertise, including:

- **Knowledge Areas:**
  - Hudi table types (COW and MOR)
  - Core operations (insert, upsert, delete, query)
  - Integrations (Spark, Flink, Hive, Presto, etc.)
  - Storage backends (S3, HDFS, Azure Blob, GCS)

- **Capabilities:**
  - Table creation and management
  - Data ingestion patterns
  - Query optimization
  - Compaction and clustering
  - Troubleshooting guidance

- **Code Examples:**
  - Creating COW tables with Spark
  - Upsert operations with Flink SQL
  - Incremental queries
  - Time travel queries
  - Async compaction
  - Clustering configuration

## How to Use

### Method 1: Direct Loading

Copy the skill file to your Claude Code skills directory:

```bash
# Linux/macOS
cp hudi-expert-skill.json ~/.config/claude-code/skills/

# Windows
copy hudi-expert-skill.json %APPDATA%\claude-code\skills\
```

### Method 2: Configuration

Add to your `~/.config/claude-code/config.json`:

```json
{
  "skills": {
    "enabled": true,
    "custom_skills_path": "~/.config/claude-code/skills",
    "auto_load": true,
    "skills": [
      "apache-hudi-expert"
    ]
  }
}
```

### Method 3: Command Line

Load the skill when starting Claude Code:

```bash
claude-code --load-skill ./examples/hudi-expert-skill.json
```

## Customization

You can customize the skill by modifying:

1. **Knowledge Sources**: Add your own documentation paths
2. **Examples**: Add project-specific code examples
3. **Best Practices**: Include team conventions
4. **Tools**: Add custom scripts and commands
5. **Configuration Templates**: Provide environment-specific configs

## Testing

Validate the skill definition:

```bash
claude-code --validate-skill ./examples/hudi-expert-skill.json
```

Test the skill:

```bash
claude-code --test-skill apache-hudi-expert --query "How do I create a MOR table?"
```

## Contributing

To contribute additional skills:

1. Create a new JSON file following the skill schema
2. Test thoroughly
3. Add documentation
4. Submit a pull request

## Resources

- [Custom Skills Guide (English)](../claude-code-custom-skills.md)
- [Custom Skills Guide (中文)](../claude-code-custom-skills-zh.md)
- [Apache Hudi Documentation](https://hudi.apache.org/docs/overview)
- [Hudi Resources Repository](https://github.com/leesf/hudi-resources)
