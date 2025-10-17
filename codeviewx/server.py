"""
Web 文档服务器模块
"""

import os
from flask import Flask, render_template, redirect


def get_markdown_title(file_path):
    """
    从 Markdown 文件中提取第一个标题
    
    Args:
        file_path (str): Markdown 文件路径
    
    Returns:
        str: 第一个标题内容，如果没有则返回 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    # 移除 # 符号和空格
                    title = line.lstrip('#').strip()
                    if title:
                        return title
        return None
    except Exception:
        return None


def generate_file_tree(directory, current_file=None):
    """
    生成目录的文件树数据结构
    
    Args:
        directory (str): 要扫描的目录路径
        current_file (str, optional): 当前激活的文件名
    
    Returns:
        list[dict]: 文件树数据，每个元素包含:
            - name: 文件名
            - path: 相对路径
            - type: 文件类型 ('markdown' 或 'file')
            - active: 是否是当前文件
            
    Examples:
        >>> generate_file_tree("/path/to/wiki", "README.md")
        [
            {'name': 'README.md', 'path': 'README.md', 'type': 'markdown', 'active': True},
            {'name': 'guide.md', 'path': 'guide.md', 'type': 'markdown', 'active': False}
        ]
    """
    if not os.path.exists(directory):
        return []

    file_tree = []

    try:
        # 获取所有文件并排序
        items = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                items.append(item)

        items.sort()  # 按文件名排序

        for item in items:
            file_path = os.path.join(directory, item)
            rel_path = os.path.relpath(file_path, directory)

            # 确定文件类型
            file_type = 'file'
            display_name = item  # 默认显示文件名
            
            if item.lower().endswith('.md'):
                file_type = 'markdown'
                
                # README.md 特殊处理：直接显示文件名，不读取标题
                if item.upper() == 'README.MD':
                    display_name = 'README'
                else:
                    # 其他 Markdown 文件：尝试读取第一个标题
                    title = get_markdown_title(file_path)
                    if title:
                        display_name = title
                    else:
                        # 如果没有标题，使用文件名（去掉.md后缀）
                        display_name = item[:-3] if item.endswith('.md') else item

            # 检查是否是当前文件
            is_active = (item == current_file)

            file_tree.append({
                'name': item,  # 保留原始文件名用于链接
                'display_name': display_name,  # 用于显示的名称（标题或文件名）
                'path': rel_path,
                'type': file_type,
                'active': is_active
            })

    except Exception as e:
        print(f"Error generating file tree: {e}")
        return []

    return file_tree


def start_document_web_server(output_directory):
    """
    启动文档浏览 Web 服务器
    
    Args:
        output_directory: 文档输出目录路径
    """
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, 'tpl')
    static_dir = os.path.join(current_dir, 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    @app.route("/")
    def home():
        return index("README.md")
    
    @app.route("/<path:filename>")
    def index(filename):
        if not filename or filename == "":
            filename = "README.md"
        
        # 打印调试信息
        print(f"[DEBUG] 访问文件: {filename}")
        print(f"[DEBUG] 输出目录: {output_directory}")
        
        index_file_path = os.path.join(output_directory, filename)
        if os.path.exists(index_file_path):
            with open(index_file_path, "r") as f:
                content = f.read()    
                    # 在文档开头自动插入 TOC 标记（如果还没有的话）
            if '[TOC]' not in content:
                # 在第一个标题前插入 TOC
                lines = content.split('\n')
                insert_index = 0

                # 找到第一个标题的位置
                for i, line in enumerate(lines):
                    if line.strip().startswith('#'):
                        insert_index = i
                        break

                # 插入 TOC 标记
                lines.insert(insert_index, '[TOC]')
                lines.insert(insert_index + 1, '')  # 空行
                content = '\n'.join(lines)
                
            import markdown
            from markdown.extensions.toc import TocExtension

            # 配置 markdown 扩展
            toc_extension = TocExtension(
                permalink=True,
                permalink_class='headerlink',
                title='目录',
                baselevel=1,
                toc_depth=6,
                marker='[TOC]'
            )

            html = markdown.markdown(
                content,
                extensions=[
                    'tables',
                    'fenced_code',
                    'codehilite',
                    toc_extension
                ],
                extension_configs={
                    'codehilite': {
                        'css_class': 'language-',
                        'use_pygments': False  # 禁用 Pygments，使用 Prism.js
                    }
                }
            )

            # 生成文件树数据
            file_tree_data = generate_file_tree(output_directory, filename)
            print(f"[DEBUG] 文件树数据: {file_tree_data}")
            print(f"[DEBUG] 文件树条目数: {len(file_tree_data) if file_tree_data else 0}")

            return render_template('doc_detail.html', markdown_html_content=html, file_tree=file_tree_data)
        else:
            return f"File not found: {index_file_path}"

    app.run(debug=True)

