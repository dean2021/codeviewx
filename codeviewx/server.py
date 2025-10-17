"""
Web documentation server module
"""

import os
from flask import Flask, render_template, redirect
from .i18n import t


def get_markdown_title(file_path):
    """
    Extract the first title from a Markdown file
    
    Args:
        file_path (str): Markdown file path
    
    Returns:
        str: First title content, or None if not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                    if title:
                        return title
        return None
    except Exception:
        return None


def generate_file_tree(directory, current_file=None):
    """
    Generate file tree data structure for a directory
    
    Args:
        directory (str): Directory path to scan
        current_file (str, optional): Currently active file name
    
    Returns:
        list[dict]: File tree data, each element contains:
            - name: File name
            - path: Relative path
            - type: File type ('markdown' or 'file')
            - active: Whether it's the current file
            
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
        items = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                items.append(item)

        items.sort()

        for item in items:
            file_path = os.path.join(directory, item)
            rel_path = os.path.relpath(file_path, directory)

            file_type = 'file'
            display_name = item
            
            if item.lower().endswith('.md'):
                file_type = 'markdown'
                
                if item.upper() == 'README.MD':
                    display_name = 'README'
                else:
                    title = get_markdown_title(file_path)
                    if title:
                        display_name = title
                    else:
                        display_name = item[:-3] if item.endswith('.md') else item

            is_active = (item == current_file)

            file_tree.append({
                'name': item,
                'display_name': display_name,
                'path': rel_path,
                'type': file_type,
                'active': is_active
            })

    except Exception as e:
        print(t('server_error_generating_tree', error=str(e)))
        return []

    return file_tree


def start_document_web_server(output_directory):
    """
    Start documentation web server
    
    Args:
        output_directory: Documentation output directory path
    """
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
        
        print(t('server_debug_accessing', filename=filename))
        print(t('server_debug_output_dir', directory=output_directory))
        
        index_file_path = os.path.join(output_directory, filename)
        if os.path.exists(index_file_path):
            with open(index_file_path, "r") as f:
                content = f.read()
            if '[TOC]' not in content:
                lines = content.split('\n')
                insert_index = 0

                for i, line in enumerate(lines):
                    if line.strip().startswith('#'):
                        insert_index = i
                        break

                lines.insert(insert_index, '[TOC]')
                lines.insert(insert_index + 1, '')
                content = '\n'.join(lines)
                
            import markdown
            from markdown.extensions.toc import TocExtension

            toc_extension = TocExtension(
                permalink=True,
                permalink_class='headerlink',
                title=t('server_toc_title'),
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
                        'use_pygments': False
                    }
                }
            )

            file_tree_data = generate_file_tree(output_directory, filename)
            print(t('server_debug_file_tree', data=str(file_tree_data)))
            print(t('server_debug_file_count', count=len(file_tree_data) if file_tree_data else 0))

            return render_template('doc_detail.html', markdown_html_content=html, file_tree=file_tree_data)
        else:
            return t('server_file_not_found', path=index_file_path)

    app.run(debug=True)

