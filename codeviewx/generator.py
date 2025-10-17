"""
Document generation module
文档生成模块
"""

import os
import logging
from datetime import datetime
from typing import Optional

from deepagents import create_deep_agent

from .tools import (
    execute_command,
    ripgrep_search,
    write_real_file,
    read_real_file,
    list_real_directory,
)
from .language import detect_system_language
from .prompt import load_prompt
from .i18n import get_i18n, t, detect_ui_language


def generate_docs(
    working_directory: Optional[str] = None,
    output_directory: str = "docs",
    doc_language: Optional[str] = None,
    ui_language: Optional[str] = None,
    recursion_limit: int = 1000,
    verbose: bool = False
) -> None:
    """
    Generate project documentation using AI
    使用 AI 生成项目文档
    
    Args:
        working_directory: Project working directory (default: current directory)
                          项目工作目录（默认：当前目录）
        output_directory: Documentation output directory (default: docs)
                         文档输出目录（默认：docs）
        doc_language: Documentation language (default: auto-detect system language)
                     Supports: 'Chinese', 'English', 'Japanese', etc.
                     文档语言（默认：自动检测系统语言）
                     支持：'Chinese', 'English', 'Japanese', 等
        ui_language: User interface language (default: auto-detect, options: 'en', 'zh')
                    用户界面语言（默认：自动检测，选项：'en', 'zh'）
        recursion_limit: Agent recursion limit (default: 1000)
                        Agent 递归限制（默认：1000）
        verbose: Show detailed logs (default: False)
                是否显示详细日志（默认：False）
    
    Examples:
        # Analyze current directory with auto-detected language
        # 分析当前目录，自动检测语言
        generate_docs()
        
        # Analyze specific project with English documentation and UI
        # 分析指定项目，使用英文文档和界面
        generate_docs(
            working_directory="/path/to/project",
            output_directory="docs",
            doc_language="English",
            ui_language="en"
        )
        
        # Generate Chinese documentation with Chinese UI
        # 使用中文生成文档，中文界面
        generate_docs(doc_language="Chinese", ui_language="zh", verbose=True)
    """
    # Set UI language / 设置界面语言
    if ui_language is None:
        ui_language = detect_ui_language()
        ui_language_source = t('auto_detected')
    else:
        ui_language_source = t('user_specified')
    
    # Set global i18n locale / 设置全局语言
    get_i18n().set_locale(ui_language)
    
    # Configure logging / 配置日志
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Disable HTTP request logs (always hidden, even in verbose mode)
    # 禁用 HTTP 请求日志（总是隐藏，即使在 verbose 模式）
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    if verbose:
        logging.getLogger("langchain").setLevel(logging.DEBUG)
        logging.getLogger("langgraph").setLevel(logging.DEBUG)
    
    # Get working directory / 获取工作目录
    if working_directory is None:
        working_directory = os.getcwd()
    
    # Detect or use specified document language / 检测或使用指定的文档语言
    if doc_language is None:
        doc_language = detect_system_language()
        doc_language_source = t('auto_detected')
    else:
        doc_language_source = t('user_specified')
    
    print("=" * 80)
    print(f"{t('starting')} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print(f"{t('working_dir')}: {working_directory}")
    print(f"{t('output_dir')}: {output_directory}")
    print(f"{t('doc_language')}: {doc_language} ({doc_language_source})")
    print(f"{t('ui_language')}: {ui_language} ({ui_language_source})")
    
    # Load prompt / 加载提示词
    prompt = load_prompt(
        "DocumentEngineer_compact",
        working_directory=working_directory,
        output_directory=output_directory,
        doc_language=doc_language
    )
    print(t('loading_prompt'))
    
    # Create tools list / 创建工具列表
    tools = [
        execute_command,
        ripgrep_search,
        write_real_file,
        read_real_file,
        list_real_directory,
    ]
    
    # Create Agent / 创建 Agent
    agent = create_deep_agent(tools, prompt)
    print(t('created_agent'))
    print(t('registered_tools', count=len(tools), tools=', '.join([t.__name__ for t in tools])))
    print("=" * 80)
    
    # Generate documentation / 生成文档
    print(f"\n{t('analyzing')}\n")
    
    step_count = 0
    docs_generated = 0
    analysis_phase = True
    last_todos_count = 0  # 跟踪上次的 todo 数量
    todos_shown = False   # 是否已显示过 todo
    
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": t('agent_task_instruction')}]},
        stream_mode="values",
        config={"recursion_limit": recursion_limit}
    ):
        if "messages" in chunk:
            step_count += 1
            last_message = chunk["messages"][-1]
            
            # 标准模式：显示简洁的消息内容
            if not verbose:
                message_type = last_message.__class__.__name__
                
                # 显示 AI 的文本回复（非工具调用）
                if message_type == 'AIMessage' and hasattr(last_message, 'content'):
                    content = str(last_message.content).strip()
                    # 只显示有意义的文本内容（不包含 tool_calls）
                    has_tool_calls = hasattr(last_message, 'tool_calls') and last_message.tool_calls
                    if content and len(content) > 20 and not has_tool_calls:
                        # 提取前 200 个字符作为摘要
                        summary = content[:200].replace('\n', ' ').strip()
                        if len(content) > 200:
                            summary += "..."
                        print(f"\n💭 AI: {summary}")
                
                # 显示工具返回结果（ToolMessage）
                if message_type == 'ToolMessage' and step_count <= 25:
                    tool_name = getattr(last_message, 'name', 'unknown')
                    content = str(getattr(last_message, 'content', '')).strip()
                    
                    # 跳过 todos 工具的返回
                    if tool_name == 'write_todos':
                        pass
                    # 跳过文档写入的返回（单独显示）
                    elif tool_name == 'write_real_file':
                        pass
                    else:
                        # 格式化工具返回内容
                        result_info = ""
                        
                        if tool_name == 'read_real_file':
                            # 统计行数并显示前几行预览
                            lines_count = content.count('\n') + 1 if content else 0
                            # 提取前2行作为预览
                            preview_lines = content.split('\n')[:2] if content else []
                            preview = ' '.join(preview_lines)[:60].replace('\n', ' ').strip()
                            if len(preview) > 60 or lines_count > 2:
                                preview += "..."
                            result_info = f"✓ {lines_count} 行 | {preview}" if preview else f"✓ {lines_count} 行"
                        
                        elif tool_name == 'list_real_directory':
                            # 统计并列出前几项
                            items = [x.strip() for x in content.split('\n') if x.strip()] if content else []
                            items_count = len(items)
                            preview = ', '.join(items[:3])
                            if len(items) > 3:
                                preview += f" ... (+{len(items)-3})"
                            result_info = f"✓ {items_count} 项 | {preview}" if preview else f"✓ {items_count} 项"
                        
                        elif tool_name == 'ripgrep_search':
                            # 统计匹配数并显示示例
                            if content:
                                lines = [x.strip() for x in content.split('\n') if x.strip()]
                                matches_count = len(lines)
                                # 显示第一个匹配
                                first_match = lines[0][:50] if lines else ""
                                if len(lines[0]) > 50 if lines else False:
                                    first_match += "..."
                                result_info = f"✓ {matches_count} 处匹配 | {first_match}" if first_match else f"✓ {matches_count} 处匹配"
                            else:
                                result_info = "✓ 无匹配"
                        
                        elif tool_name == 'execute_command':
                            # 显示命令执行结果摘要
                            if content:
                                preview = content[:60].replace('\n', ' ').strip()
                                if len(content) > 60:
                                    preview += "..."
                                result_info = f"✓ {preview}"
                            else:
                                result_info = "✓ 执行成功"
                        
                        else:
                            # 其他工具：显示内容摘要
                            if content:
                                preview = content[:60].replace('\n', ' ').strip()
                                if len(content) > 60:
                                    preview += "..."
                                result_info = f"✓ {preview}"
                            else:
                                result_info = "✓ 完成"
                        
                        # Print tool call and result (concise one-liner)
                        # 打印工具调用和结果（简洁的一行式）
                        tool_display = {
                            'read_real_file': t('reading'),
                            'list_real_directory': t('listing'),
                            'ripgrep_search': t('searching'),
                            'execute_command': t('executing'),
                        }
                        display_name = tool_display.get(tool_name, f'🔧 {tool_name}')
                        print(f"   {display_name}: {result_info}")
            
            # 检测工具调用，提供简洁的进度提示
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls and not verbose:
                # 统计工具调用信息
                tool_names = []
                doc_file = None
                todos_info = None
                
                for tool_call in last_message.tool_calls:
                    # 兼容字典和对象两种格式
                    if isinstance(tool_call, dict):
                        tool_name = tool_call.get('name', 'unknown')
                        args = tool_call.get('args', {})
                    else:
                        tool_name = getattr(tool_call, 'name', tool_call.get('name', 'unknown'))
                        args = getattr(tool_call, 'args', tool_call.get('args', {}))
                    
                    tool_names.append(tool_name)
                    
                    # 检测 todos 创建/更新
                    if tool_name == 'write_todos':
                        try:
                            if isinstance(args, dict):
                                todos = args.get('todos', [])
                            else:
                                todos = getattr(args, 'todos', [])
                            
                            if todos:
                                # 统计已完成任务数
                                completed_count = sum(1 for t in todos if isinstance(t, dict) and t.get('status') == 'completed')
                                total_count = len(todos)
                                
                                # 只在特定情况下显示 todo
                                should_show = False
                                
                                # 情况1：第一次创建（从0到有todo）
                                if not todos_shown and total_count > 0:
                                    should_show = True
                                # 情况2：有实质性进展（完成数增加2+）
                                elif completed_count >= last_todos_count + 2:
                                    should_show = True
                                # 情况3：全部完成
                                elif completed_count == total_count and total_count > 0 and completed_count > last_todos_count:
                                    should_show = True
                                
                                # 更新外层变量（Python 在 if 块中可以直接修改外层变量）
                                if should_show:
                                    todos_shown = True
                                    
                                if completed_count > last_todos_count:
                                    last_todos_count = completed_count
                                
                                if should_show:
                                    # 显示所有 todos
                                    todo_summaries = []
                                    for todo in todos:  # 显示所有 todo
                                        if isinstance(todo, dict):
                                            content = todo.get('content', '')
                                            status = todo.get('status', 'pending')
                                            if content:
                                                status_icon = {
                                                    'pending': '⏳',
                                                    'in_progress': '🔄',
                                                    'completed': '✅',
                                                    'cancelled': '❌'
                                                }.get(status, '○')
                                                # 显示完整内容，不截断
                                                todo_summaries.append(f"{status_icon} {content}")
                                    
                                    if todo_summaries:
                                        todos_info = todo_summaries
                        except Exception as e:
                            pass
                    
                    # 检测文档写入操作
                    elif tool_name == 'write_real_file':
                        try:
                            if isinstance(args, dict):
                                file_path = args.get('file_path', '')
                            else:
                                file_path = getattr(args, 'file_path', '')
                            
                            if file_path and output_directory in file_path:
                                doc_file = file_path.split('/')[-1]
                        except Exception as e:
                            if verbose:
                                print(t('verbose_progress_error', error=str(e)))
                
                # Display tool call summary / 显示工具调用摘要
                if tool_names:
                    # Display todos (highest priority) / 显示 todos（最高优先级）
                    if todos_info:
                        print(f"\n{t('task_planning')}:")
                        for todo_summary in todos_info:
                            print(f"   {todo_summary}")
                        print()
                    # Display document generation (second priority) / 显示文档生成（第二优先级）
                    elif doc_file:
                        docs_generated += 1
                        print(t('generating_doc', current=docs_generated, filename=doc_file))
                        analysis_phase = False
                    # Display analysis phase hint (only once) / 显示分析阶段提示（只显示一次）
                    elif analysis_phase and any(t in ['list_real_directory', 'ripgrep_search'] for t in tool_names):
                        print(t('analyzing_structure'))
                        analysis_phase = False
            
            # Verbose mode: show detailed information / verbose 模式：显示详细信息
            if verbose:
                print(f"\n{'='*80}")
                print(t('verbose_step', step=step_count, message_type=last_message.__class__.__name__))
                print(f"{'='*80}")
                last_message.pretty_print()
                
                if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                    print(f"\n{t('verbose_tools_called', count=len(last_message.tool_calls))}")
                    for tool_call in last_message.tool_calls:
                        print(f"   - {tool_call.get('name', 'unknown')}")
    
    print("\n" + "=" * 80)
    print(t('completed'))
    print("=" * 80)
    
    if docs_generated > 0:
        print(f"\n{t('summary')}:")
        print(f"   {t('generated_files', count=docs_generated)}")
        print(f"   {t('doc_location')}: {output_directory}/")
        print(f"   {t('execution_steps', steps=step_count)}")
    
    if "files" in chunk:
        print(f"\n{t('generated_file_list')}:")
        for filename in chunk["files"].keys():
            print(f"   - {filename}")

