"""Test tool functions"""

import os
import tempfile
import pytest
from codeviewx.tools import (
    execute_command,
    read_real_file,
    write_real_file,
    list_real_directory,
)


def invoke_tool(tool, **kwargs):
    """Invoke a LangChain tool with keyword arguments."""
    return tool.invoke(kwargs)


class TestExecuteCommand:
    """Test command execution"""
    
    def test_simple_command(self):
        """Test simple command"""
        result = invoke_tool(execute_command, command="echo 'test'")
        assert "test" in result
        assert "Error" not in result
    
    def test_command_with_working_dir(self):
        """Test command with working directory"""
        result = invoke_tool(execute_command, command="pwd", working_dir="/tmp")
        assert "/tmp" in result or "tmp" in result
    
    def test_failed_command(self):
        """Test failed command"""
        result = invoke_tool(execute_command, command="nonexistent_command_xyz")
        assert "Error" in result


class TestFileSystem:
    """Test filesystem operations"""
    
    def test_write_and_read_file(self):
        """Test file write and read"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.txt")
            content = "Hello, CodeViewX!"
            
            write_result = invoke_tool(write_real_file, file_path=test_file, content=content)
            assert "Success" in write_result or "wrote" in write_result
            
            read_result = invoke_tool(read_real_file, file_path=test_file)
            assert content in read_result
    
    def test_write_file_creates_directory(self):
        """Test automatic directory creation when writing files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_file = os.path.join(tmpdir, "subdir", "nested", "test.txt")
            content = "Nested content"
            
            write_result = invoke_tool(write_real_file, file_path=nested_file, content=content)
            assert "Success" in write_result or "wrote" in write_result
            
            assert os.path.exists(nested_file)
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        result = invoke_tool(read_real_file, file_path="/nonexistent/file.txt")
        assert "Error" in result or "not exist" in result
    
    def test_list_directory(self):
        """Test directory listing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "subdir"))
            open(os.path.join(tmpdir, "file1.txt"), 'w').close()
            open(os.path.join(tmpdir, "file2.txt"), 'w').close()
            
            result = invoke_tool(list_real_directory, directory=tmpdir)
            assert "file1.txt" in result
            assert "file2.txt" in result
            assert "subdir" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
