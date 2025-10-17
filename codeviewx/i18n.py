"""
Internationalization (i18n) support module
"""

import os
import locale
from typing import Dict, Optional


MESSAGES: Dict[str, Dict[str, str]] = {
    'en': {
        # Generator messages
        'starting': '🚀 Starting CodeViewX Documentation Generator',
        'working_dir': '📂 Working Directory',
        'output_dir': '📝 Output Directory',
        'doc_language': '🌍 Document Language',
        'ui_language': '💬 UI Language',
        'auto_detected': 'Auto-detected',
        'user_specified': 'User-specified',
        'loading_prompt': '✓ Loaded system prompt (injected working directory, output directory, and document language)',
        'created_agent': '✓ Created AI Agent',
        'registered_tools': '✓ Registered {count} custom tools: {tools}',
        'analyzing': '📝 Analyzing project and generating documentation...',
        'analyzing_structure': '🔍 Analyzing project structure...',
        'generating_doc': '📄 Generating document ({current}): {filename}',
        'task_planning': '📋 Task Planning',
        'ai_thinking': '💭 AI',
        'reading': '📖 Reading',
        'listing': '📁 Listing',
        'searching': '🔎 Searching',
        'executing': '⚙️ Executing',
        'completed': '✅ Documentation generation completed!',
        'summary': '📊 Summary',
        'generated_files': '✓ Generated {count} document files',
        'doc_location': '✓ Document location',
        'execution_steps': '✓ Execution steps: {steps} steps',
        'generated_file_list': '📄 Generated files',
        
        # Verbose mode messages
        'verbose_progress_error': '⚠️  Progress detection error: {error}',
        'verbose_step': '📍 Step {step} - {message_type}',
        'verbose_tools_called': '🔧 Called {count} tools:',
        
        # Agent prompt message
        'agent_task_instruction': 'Please analyze the project in the working directory specified in the system prompt and generate comprehensive technical documentation',
        
        # CLI messages
        'cli_description': 'CodeViewX - AI-Driven Code Documentation Generator',
        'cli_examples': '''Examples:
  codeviewx                           # Analyze current directory (auto-detect language)
  codeviewx -w /path/to/project       # Analyze specific project
  codeviewx -o docs                   # Output to docs directory
  codeviewx -l English                # Generate English documentation
  codeviewx -l Chinese -o docs        # Use Chinese, output to docs
  codeviewx -w . -o docs --verbose    # Full config + detailed logs
  codeviewx --serve                   # Start documentation web server (default docs directory)
  codeviewx --serve -o docs           # Start server with specified directory
  
Supported languages:
  Chinese, English, Japanese, Korean, French, German, Spanish, Russian
  
Environment variables:
  OPENAI_API_KEY     OpenAI API key (if using OpenAI models)
  ANTHROPIC_API_KEY  Anthropic API key (if using Claude)
        ''',
        'cli_working_dir_help': 'Project working directory (default: current directory)',
        'cli_output_dir_help': 'Documentation output directory (default: docs)',
        'cli_language_help': 'Documentation language (default: auto-detect). Supports: Chinese, English, Japanese, Korean, French, German, Spanish, Russian',
        'cli_ui_language_help': 'User interface language (default: auto-detect). Options: en, zh',
        'cli_verbose_help': 'Show detailed debug logs',
        'cli_serve_help': 'Start web server to browse documentation',
        'cli_missing_docs': 'Error: Documentation directory "{path}" does not exist',
        'cli_serve_hint': 'Please generate documentation first using: codeviewx -w /path/to/project',
        'cli_starting_server': '🌐 Starting documentation web server...',
        'cli_server_address': '🔗 Server address: http://127.0.0.1:5000',
        'cli_server_stop': '⏹️  Press Ctrl+C to stop the server',
        
        # Error messages
        'error_file_not_found': 'Error: Prompt file not found: {filename}',
        'error_template_variable': 'Error: Template requires variable {variable} but not provided in parameters',
        'error_directory_not_exist': 'Error: Directory does not exist: {path}',
        
        # Server messages
        'server_debug_accessing': '[DEBUG] Accessing file: {filename}',
        'server_debug_output_dir': '[DEBUG] Output directory: {directory}',
        'server_debug_file_tree': '[DEBUG] File tree data: {data}',
        'server_debug_file_count': '[DEBUG] File tree entries: {count}',
        'server_file_not_found': 'File not found: {path}',
        'server_error_generating_tree': 'Error generating file tree: {error}',
        'server_toc_title': 'Table of Contents',
        
        # Web UI messages
        'web_title': 'CodeViewX - Documentation',
        'web_logo': 'CodeViewX',
        'web_subtitle': 'See the Wisdom Behind the Code',
        'web_file_tree_title': 'File Tree',
        'web_toc_toggle': 'Toggle TOC',
        'web_file_tree_toggle': 'Toggle File Tree',
        'web_mermaid_view_fullscreen': 'Click to view full size',
        'web_footer_text': '© 2025 CodeViewX - Documentation powered by AI',
        'web_footer_about': 'About',
        'web_footer_docs': 'Documentation',
    },
    'zh': {
        # Generator messages
        'starting': '🚀 启动 CodeViewX 文档生成器',
        'working_dir': '📂 工作目录',
        'output_dir': '📝 输出目录',
        'doc_language': '🌍 文档语言',
        'ui_language': '💬 界面语言',
        'auto_detected': '自动检测',
        'user_specified': '用户指定',
        'loading_prompt': '✓ 已加载系统提示词（已注入工作目录、输出目录和文档语言）',
        'created_agent': '✓ 已创建 AI Agent',
        'registered_tools': '✓ 已注册 {count} 个自定义工具: {tools}',
        'analyzing': '📝 开始分析项目并生成文档...',
        'analyzing_structure': '🔍 分析项目结构...',
        'generating_doc': '📄 正在生成文档 ({current}): {filename}',
        'task_planning': '📋 任务规划',
        'ai_thinking': '💭 AI',
        'reading': '📖 读取',
        'listing': '📁 列表',
        'searching': '🔎 搜索',
        'executing': '⚙️ 命令',
        'completed': '✅ 文档生成完成！',
        'summary': '📊 总结',
        'generated_files': '✓ 共生成 {count} 个文档文件',
        'doc_location': '✓ 文档位置',
        'execution_steps': '✓ 执行步骤: {steps} 步',
        'generated_file_list': '📄 生成的文件',
        
        # Verbose mode messages
        'verbose_progress_error': '⚠️  进度检测异常: {error}',
        'verbose_step': '📍 步骤 {step} - {message_type}',
        'verbose_tools_called': '🔧 调用了 {count} 个工具:',
        
        # Agent prompt message
        'agent_task_instruction': '请根据系统提示词中的工作目录，分析该项目并生成深度技术文档',
        
        # CLI messages
        'cli_description': 'CodeViewX - AI 驱动的代码文档生成器',
        'cli_examples': '''示例:
  codeviewx                           # 分析当前目录（自动检测语言）
  codeviewx -w /path/to/project       # 分析指定项目
  codeviewx -o docs                   # 输出到 docs 目录
  codeviewx -l English                # 使用英文生成文档
  codeviewx -l Chinese -o docs        # 使用中文，输出到 docs
  codeviewx -w . -o docs --verbose    # 完整配置 + 详细日志
  codeviewx --serve                   # 启动文档 Web 服务器（默认 docs 目录）
  codeviewx --serve -o docs           # 启动服务器并指定文档目录
  
支持的语言:
  Chinese, English, Japanese, Korean, French, German, Spanish, Russian
  
环境变量:
  OPENAI_API_KEY     OpenAI API 密钥（如使用 OpenAI 模型）
  ANTHROPIC_API_KEY  Anthropic API 密钥（如使用 Claude）
        ''',
        'cli_working_dir_help': '项目工作目录（默认：当前目录）',
        'cli_output_dir_help': '文档输出目录（默认：docs）',
        'cli_language_help': '文档语言（默认：自动检测）。支持：Chinese, English, Japanese, Korean, French, German, Spanish, Russian',
        'cli_ui_language_help': '用户界面语言（默认：自动检测）。选项：en, zh',
        'cli_verbose_help': '显示详细的调试日志',
        'cli_serve_help': '启动 Web 服务器浏览文档',
        'cli_missing_docs': '错误: 文档目录 "{path}" 不存在',
        'cli_serve_hint': '请先使用以下命令生成文档: codeviewx -w /path/to/project',
        'cli_starting_server': '🌐 启动文档 Web 服务器...',
        'cli_server_address': '🔗 服务器地址: http://127.0.0.1:5000',
        'cli_server_stop': '⏹️  按 Ctrl+C 停止服务器',
        
        # Error messages
        'error_file_not_found': '错误: 找不到提示词文件: {filename}',
        'error_template_variable': '错误: 模板需要变量 {variable}，但未在参数中提供',
        'error_directory_not_exist': '错误: 目录不存在: {path}',
        
        # Server messages
        'server_debug_accessing': '[调试] 访问文件: {filename}',
        'server_debug_output_dir': '[调试] 输出目录: {directory}',
        'server_debug_file_tree': '[调试] 文件树数据: {data}',
        'server_debug_file_count': '[调试] 文件树条目数: {count}',
        'server_file_not_found': '文件未找到: {path}',
        'server_error_generating_tree': '生成文件树时出错: {error}',
        'server_toc_title': '目录',
        
        # Web UI messages
        'web_title': 'CodeViewX - 文档展示',
        'web_logo': 'CodeViewX',
        'web_subtitle': '看见代码背后的智慧',
        'web_file_tree_title': '文档目录',
        'web_toc_toggle': '切换目录',
        'web_file_tree_toggle': '切换文件目录',
        'web_mermaid_view_fullscreen': '点击查看大图',
        'web_footer_text': '© 2025 CodeViewX - 文档由AI强力驱动',
        'web_footer_about': '关于',
        'web_footer_docs': '文档',
    }
}


class I18n:
    """
    Internationalization manager
    
    Supports multiple languages with automatic detection and manual override.
    
    Examples:
        >>> i18n = I18n('en')
        >>> i18n.t('starting')
        '🚀 Starting CodeViewX Documentation Generator'
        
        >>> i18n.set_locale('zh')
        >>> i18n.t('starting')
        '🚀 启动 CodeViewX 文档生成器'
        
        >>> i18n.t('generated_files', count=5)
        '✓ 共生成 5 个文档文件'
    """
    
    def __init__(self, locale: str = 'en'):
        """
        Initialize I18n manager
        
        Args:
            locale: Language code ('en' or 'zh'), defaults to 'en'
        """
        self.locale = locale if locale in MESSAGES else 'en'
    
    def t(self, key: str, **kwargs) -> str:
        """
        Translate message key to current locale
        
        Args:
            key: Message key
            **kwargs: Format variables for the message
        
        Returns:
            Translated and formatted message string
        
        Examples:
            >>> i18n.t('starting')
            '🚀 Starting CodeViewX Documentation Generator'
            
            >>> i18n.t('generated_files', count=5)
            '✓ Generated 5 document files'
        """
        msg = MESSAGES.get(self.locale, {}).get(key, key)
        try:
            return msg.format(**kwargs) if kwargs else msg
        except KeyError as e:
            return msg
    
    def set_locale(self, locale: str):
        """
        Set the current locale
        
        Args:
            locale: Language code ('en' or 'zh')
        """
        if locale in MESSAGES:
            self.locale = locale
    
    def get_locale(self) -> str:
        """
        Get current locale
        
        Returns:
            Current language code
        """
        return self.locale
    
    def available_locales(self) -> list:
        """
        Get list of available locales
        
        Returns:
            List of available language codes
        """
        return list(MESSAGES.keys())


_i18n = I18n()


def get_i18n() -> I18n:
    """
    Get the global I18n instance
    
    Returns:
        Global I18n instance
    """
    return _i18n


def t(key: str, **kwargs) -> str:
    """
    Shortcut function for translation
    
    Args:
        key: Message key
        **kwargs: Format variables for the message
    
    Returns:
        Translated and formatted message string
    
    Examples:
        >>> t('starting')
        '🚀 Starting CodeViewX Documentation Generator'
        
        >>> t('generated_files', count=5)
        '✓ Generated 5 document files'
    """
    return _i18n.t(key, **kwargs)


def set_locale(locale: str):
    """
    Set the global locale
    
    Args:
        locale: Language code ('en' or 'zh')
    """
    _i18n.set_locale(locale)


def detect_ui_language() -> str:
    """
    Auto-detect UI language based on system locale
    
    Returns:
        'en' for English or 'zh' for Chinese
    
    Examples:
        >>> detect_ui_language()
        'zh'
        >>> detect_ui_language()
        'en'
    """
    try:
        lang, _ = locale.getdefaultlocale()
        
        if lang:
            if lang.startswith('zh'):
                return 'zh'
            else:
                return 'en'
        
        return 'en'
        
    except Exception:
        return 'en'

