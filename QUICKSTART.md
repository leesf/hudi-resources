# Claude Code Custom Skills - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Skill File

```bash
# Linux/macOS
mkdir -p ~/.config/claude-code/skills
cp examples/hudi-expert-skill.json ~/.config/claude-code/skills/

# Windows
mkdir %APPDATA%\claude-code\skills
copy examples\hudi-expert-skill.json %APPDATA%\claude-code\skills\
```

### Step 2: Enable Skills

Create or edit `~/.config/claude-code/config.json`:

```json
{
  "skills": {
    "enabled": true,
    "auto_load": true,
    "skills": ["apache-hudi-expert"]
  }
}
```

### Step 3: Restart Claude Code

```bash
claude-code
```

That's it! Your custom skill is now active.

## Quick Commands

| Task | Command |
|------|---------|
| List skills | `claude-code --list-skills` |
| Load skill | `claude-code --load-skill path/to/skill.json` |
| Test skill | `claude-code --test-skill apache-hudi-expert` |
| Validate skill | `claude-code --validate-skill skill.json` |
| Enable skill | `claude-code --enable-skill apache-hudi-expert` |
| Disable skill | `claude-code --disable-skill apache-hudi-expert` |

## Common Skill Locations

### Linux
```
~/.config/claude-code/skills/
```

### macOS
```
~/.config/claude-code/skills/
```

### Windows
```
%APPDATA%\claude-code\skills\
```

## Minimal Skill Template

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "description": "My custom skill",
  "type": "knowledge",
  "prompts": {
    "system": "You are an expert in..."
  }
}
```

## Environment Variables

```bash
# Custom skills path
export CLAUDE_SKILLS_PATH=/path/to/skills

# Enable custom skills
export CLAUDE_ENABLE_CUSTOM_SKILLS=true

# Debug mode
export CLAUDE_CODE_DEBUG=true
```

## Skill Types

- **knowledge**: Domain expertise and information
- **tool**: External tools and API integrations
- **workflow**: Multi-step processes

## Testing Your Skill

```bash
# Validate JSON syntax
jq . my-skill.json

# Validate skill definition
claude-code --validate-skill my-skill.json

# Test with query
claude-code --test-skill my-skill --query "test question"

# Enable debug logging
export CLAUDE_CODE_DEBUG=true
claude-code --load-skill my-skill.json
```

## Troubleshooting

### Skill not loading?
1. Check file permissions: `chmod 644 skill.json`
2. Validate JSON: `jq . skill.json`
3. Check logs: `tail -f ~/.claude-code/logs/skills.log`

### Syntax error?
```bash
python -m json.tool skill.json
```

### Need help?
- See full guide: [claude-code-custom-skills.md](claude-code-custom-skills.md)
- See Chinese guide: [claude-code-custom-skills-zh.md](claude-code-custom-skills-zh.md)

## Example Use Cases

### 1. Project Conventions
```json
{
  "name": "project-style",
  "context": {
    "language": "Python",
    "style": "PEP 8",
    "naming": "snake_case"
  }
}
```

### 2. Custom Commands
```json
{
  "name": "deploy-tools",
  "tools": [{
    "name": "deploy",
    "command": "./deploy.sh"
  }]
}
```

### 3. Domain Knowledge
```json
{
  "name": "hudi-expert",
  "knowledge_sources": [{
    "type": "local",
    "path": "/docs/hudi"
  }]
}
```

## Pro Tips

1. **Version Control**: Store skills in Git
2. **Team Sharing**: Share skills via repository
3. **Modular Design**: One skill per domain
4. **Test First**: Validate before deploying
5. **Document Well**: Include examples and usage

## Resources

- [Full Documentation](claude-code-custom-skills.md)
- [中文文档](claude-code-custom-skills-zh.md)
- [Example Skills](examples/)
- [Hudi Resources](https://github.com/leesf/hudi-resources)

## Next Steps

1. ✅ Install the example skill
2. ✅ Test it with a query
3. ✅ Customize for your project
4. ✅ Share with your team
5. ✅ Contribute back to community

---

**Quick Help**: For detailed instructions, see the [full guide](claude-code-custom-skills.md).
