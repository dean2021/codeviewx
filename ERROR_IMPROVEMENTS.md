# CodeViewX 错误处理改进说明

## 问题背景

用户反馈 CodeViewX 运行时出现错误提示：
```
Error: "Could not resolve authentication method. Expected either api_key or auth_token to be set. Or for one of the `X-Api-Key` or `Authorization` headers to be explicitly omitted"
```

这种提示不够明确，用户不清楚具体原因和解决方法。

## 改进内容

### 1. API 密钥验证函数

在 `codeviewx/generator.py` 中新增了 `validate_api_key()` 函数，提供：
- **检测缺失的 API 密钥**
- **验证 API 密钥长度**
- **检查 API 密钥格式**（必须以 `sk-ant-api` 开头）
- **详细的错误提示和解决建议**

### 2. 改进的 CLI 错误处理

在 `codeviewx/cli.py` 中增强了对认证错误的处理：
- **识别常见认证错误模式**
- **提供更友好的错误信息**
- **包含具体的解决步骤**
- **在详细模式下显示技术细节**

### 3. 国际化支持

在 `codeviewx/i18n.py` 中添加了新的错误信息：
- **中英文双语支持**
- **统一的错误信息格式**
- **上下文相关的提示**

### 4. 辅助工具

创建了以下辅助文件：
- **`scripts/setup_api_key.sh`** - 自动化 API 密钥设置脚本
- **`test_error_improvements.py`** - 错误处理验证测试

## 改进效果

### 之前的错误提示
```
❌ Error: Could not resolve authentication method. Expected either api_key or auth_token to be set...
```

### 现在的错误提示
```
❌ ANTHROPIC_AUTH_TOKEN environment variable not found

To fix this issue:
1. Get your API key from https://console.anthropic.com
2. Set the environment variable:
   export ANTHROPIC_AUTH_TOKEN='your-api-key-here'
3. Or add it to your shell profile (~/.bashrc, ~/.zshrc, etc.)
4. Restart your terminal or run: source ~/.bashrc

================================================================================
🔗 Need help?
================================================================================
• Get your API key: https://console.anthropic.com
• View documentation: https://docs.anthropic.com
================================================================================
```

## 测试验证

运行测试脚本验证所有改进：
```bash
python test_error_improvements.py
```

测试包括：
- ✅ 缺失 API 密钥的错误处理
- ✅ 无效 API 密钥格式的检测
- ✅ 短 API 密钥的验证
- ✅ 帮助命令的正常运行

## 使用方法

### 自动设置（推荐）
```bash
bash scripts/setup_api_key.sh
```

### 手动设置
```bash
export ANTHROPIC_AUTH_TOKEN='your-api-key-here'
```

### 验证设置
```bash
python -c "from codeviewx.generator import validate_api_key; validate_api_key(); print('✅ API key is valid')"
```

## 总结

通过这些改进，CodeViewX 现在提供：
1. **🔍 自动检测** - 预先验证 API 密钥
2. **📝 清晰提示** - 具体的错误原因和解决方案
3. **🔗 直接帮助** - 提供获取 API 密钥的链接
4. **🌐 双语支持** - 中英文错误信息
5. **⚙️ 自动化工具** - 简化配置过程

这些改进大大提升了用户体验，让 API 密钥相关的错误变得容易理解和解决。