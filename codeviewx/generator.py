"""
Document generation module
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
    
    Args:
        working_directory: Project working directory (default: current directory)
        output_directory: Documentation output directory (default: docs)
        doc_language: Documentation language (default: auto-detect system language)
                     Supports: 'Chinese', 'English', 'Japanese', etc.
        ui_language: User interface language (default: auto-detect, options: 'en', 'zh')
        recursion_limit: Agent recursion limit (default: 1000)
        verbose: Show detailed logs (default: False)
    
    Examples:
        generate_docs()
        
        generate_docs(
            working_directory="/path/to/project",
            output_directory="docs",
            doc_language="English",
            ui_language="en"
        )
        
        generate_docs(doc_language="Chinese", ui_language="zh", verbose=True)
    """
    if ui_language is None:
        ui_language = detect_ui_language()
        ui_language_source = t('auto_detected')
    else:
        ui_language_source = t('user_specified')
    
    get_i18n().set_locale(ui_language)
    
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    if verbose:
        logging.getLogger("langchain").setLevel(logging.DEBUG)
        logging.getLogger("langgraph").setLevel(logging.DEBUG)
    
    if working_directory is None:
        working_directory = os.getcwd()
    
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
    
    prompt = load_prompt(
        "document_engineer",
        working_directory=working_directory,
        output_directory=output_directory,
        doc_language=doc_language
    )
    print(t('loading_prompt'))
    
    tools = [
        execute_command,
        ripgrep_search,
        write_real_file,
        read_real_file,
        list_real_directory,
    ]
    
    agent = create_deep_agent(tools, prompt)
    print(t('created_agent'))
    print(t('registered_tools', count=len(tools), tools=', '.join([tool.name for tool in tools])))
    print("=" * 80)
    
    print(f"\n{t('analyzing')}\n")
    
    step_count = 0
    docs_generated = 0
    analysis_phase = True
    last_todos_count = 0
    todos_shown = False
    
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": t('agent_task_instruction')}]},
        stream_mode="values",
        config={"recursion_limit": recursion_limit}
    ):
        if "messages" in chunk:
            step_count += 1
            last_message = chunk["messages"][-1]
            
            if not verbose:
                message_type = last_message.__class__.__name__
                
                if message_type == 'AIMessage' and hasattr(last_message, 'content'):
                    content = str(last_message.content).strip()
                    has_tool_calls = hasattr(last_message, 'tool_calls') and last_message.tool_calls
                    if content and len(content) > 20 and not has_tool_calls:
                        summary = content[:200].replace('\n', ' ').strip()
                        if len(content) > 200:
                            summary += "..."
                        print(f"\n💭 AI: {summary}")
                
                if message_type == 'ToolMessage' and step_count <= 25:
                    tool_name = getattr(last_message, 'name', 'unknown')
                    content = str(getattr(last_message, 'content', '')).strip()
                    
                    if tool_name == 'write_todos':
                        pass
                    elif tool_name == 'write_real_file':
                        pass
                    else:
                        result_info = ""
                        
                        if tool_name == 'read_real_file':
                            lines_count = content.count('\n') + 1 if content else 0
                            preview_lines = content.split('\n')[:2] if content else []
                            preview = ' '.join(preview_lines)[:60].replace('\n', ' ').strip()
                            if len(preview) > 60 or lines_count > 2:
                                preview += "..."
                            result_info = f"✓ {lines_count} lines | {preview}" if preview else f"✓ {lines_count} lines"
                        
                        elif tool_name == 'list_real_directory':
                            items = [x.strip() for x in content.split('\n') if x.strip()] if content else []
                            items_count = len(items)
                            preview = ', '.join(items[:3])
                            if len(items) > 3:
                                preview += f" ... (+{len(items)-3})"
                            result_info = f"✓ {items_count} items | {preview}" if preview else f"✓ {items_count} items"
                        
                        elif tool_name == 'ripgrep_search':
                            if content:
                                lines = [x.strip() for x in content.split('\n') if x.strip()]
                                matches_count = len(lines)
                                first_match = lines[0][:50] if lines else ""
                                if len(lines[0]) > 50 if lines else False:
                                    first_match += "..."
                                result_info = f"✓ {matches_count} matches | {first_match}" if first_match else f"✓ {matches_count} matches"
                            else:
                                result_info = "✓ No matches"
                        
                        elif tool_name == 'execute_command':
                            if content:
                                preview = content[:60].replace('\n', ' ').strip()
                                if len(content) > 60:
                                    preview += "..."
                                result_info = f"✓ {preview}"
                            else:
                                result_info = "✓ Done"
                        
                        else:
                            if content:
                                preview = content[:60].replace('\n', ' ').strip()
                                if len(content) > 60:
                                    preview += "..."
                                result_info = f"✓ {preview}"
                            else:
                                result_info = "✓ Done"
                        
                        tool_display = {
                            'read_real_file': t('reading'),
                            'list_real_directory': t('listing'),
                            'ripgrep_search': t('searching'),
                            'execute_command': t('executing'),
                        }
                        display_name = tool_display.get(tool_name, f'🔧 {tool_name}')
                        print(f"   {display_name}: {result_info}")
            
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls and not verbose:
                tool_names = []
                doc_file = None
                todos_info = None
                
                for tool_call in last_message.tool_calls:
                    if isinstance(tool_call, dict):
                        tool_name = tool_call.get('name', 'unknown')
                        args = tool_call.get('args', {})
                    else:
                        tool_name = getattr(tool_call, 'name', tool_call.get('name', 'unknown'))
                        args = getattr(tool_call, 'args', tool_call.get('args', {}))
                    
                    tool_names.append(tool_name)
                    
                    if tool_name == 'write_todos':
                        try:
                            if isinstance(args, dict):
                                todos = args.get('todos', [])
                            else:
                                todos = getattr(args, 'todos', [])
                            
                            if todos:
                                completed_count = sum(1 for t in todos if isinstance(t, dict) and t.get('status') == 'completed')
                                total_count = len(todos)
                                
                                should_show = False
                                
                                if not todos_shown and total_count > 0:
                                    should_show = True
                                elif completed_count >= last_todos_count + 2:
                                    should_show = True
                                elif completed_count == total_count and total_count > 0 and completed_count > last_todos_count:
                                    should_show = True
                                
                                if should_show:
                                    todos_shown = True
                                    
                                if completed_count > last_todos_count:
                                    last_todos_count = completed_count
                                
                                if should_show:
                                    todo_summaries = []
                                    for todo in todos:
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
                                                todo_summaries.append(f"{status_icon} {content}")
                                    
                                    if todo_summaries:
                                        todos_info = todo_summaries
                        except Exception as e:
                            pass
                    
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
                
                if tool_names:
                    if todos_info:
                        print(f"\n{t('task_planning')}:")
                        for todo_summary in todos_info:
                            print(f"   {todo_summary}")
                        print()
                    elif doc_file:
                        docs_generated += 1
                        print(t('generating_doc', current=docs_generated, filename=doc_file))
                        analysis_phase = False
                    elif analysis_phase and any(t in ['list_real_directory', 'ripgrep_search'] for t in tool_names):
                        print(t('analyzing_structure'))
                        analysis_phase = False
            
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

