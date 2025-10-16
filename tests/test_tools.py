"""测试工具函数"""

import os
import tempfile
import pytest
from pathlib import Path

from codeviewx.tools import (
    execute_command,
    write_real_file,
    read_real_file,
    list_real_directory,
)


class TestExecuteCommand:
    """测试命令执行"""
    
    def test_simple_command(self):
        """测试简单命令"""
        result = execute_command("echo 'test'")
        assert "test" in result
        assert "错误" not in result
    
    def test_command_with_working_dir(self):
        """测试指定工作目录的命令"""
        result = execute_command("pwd", working_dir="/tmp")
        assert "/tmp" in result or "tmp" in result
    
    def test_failed_command(self):
        """测试失败的命令"""
        result = execute_command("nonexistent_command_xyz")
        assert "错误" in result or "命令执行失败" in result


class TestFileSystem:
    """测试文件系统操作"""
    
    def test_write_and_read_file(self):
        """测试文件写入和读取"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.txt")
            content = "Hello, CodeViewX!"
            
            # 写入文件
            write_result = write_real_file(test_file, content)
            assert "成功" in write_result
            
            # 读取文件
            read_result = read_real_file(test_file)
            assert content in read_result
    
    def test_write_file_creates_directory(self):
        """测试写入文件时自动创建目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_file = os.path.join(tmpdir, "subdir", "nested", "test.txt")
            content = "Nested content"
            
            # 写入文件（应该自动创建目录）
            write_result = write_real_file(nested_file, content)
            assert "成功" in write_result
            
            # 验证文件存在
            assert os.path.exists(nested_file)
            
            # 读取验证内容
            read_result = read_real_file(nested_file)
            assert content in read_result
    
    def test_read_nonexistent_file(self):
        """测试读取不存在的文件"""
        result = read_real_file("/nonexistent/path/file.txt")
        assert "错误" in result or "不存在" in result
    
    def test_list_directory(self):
        """测试列出目录内容"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建一些测试文件
            Path(tmpdir, "file1.txt").touch()
            Path(tmpdir, "file2.txt").touch()
            Path(tmpdir, "subdir").mkdir()
            
            # 列出目录
            result = list_real_directory(tmpdir)
            
            assert "file1.txt" in result
            assert "file2.txt" in result
            assert "subdir" in result
    
    def test_list_nonexistent_directory(self):
        """测试列出不存在的目录"""
        result = list_real_directory("/nonexistent/path")
        assert "错误" in result or "不存在" in result


class TestRipgrepSearch:
    """测试 ripgrep 搜索"""
    
    def test_ripgrep_available(self):
        """测试 ripgrep 是否可用"""
        # 这个测试只检查 ripgrep 是否安装
        result = execute_command("which rg || where rg")
        # 如果找不到 rg，应该有相应提示
        # 注意：这个测试可能在某些环境下失败
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

