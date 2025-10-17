"""Test tool functions"""

import os
import tempfile
import pytest
from codeviewx.tools import (
    execute_command,
    read_real_file,
    write_real_file,
    list_real_directory,
    ripgrep_search
)


class TestExecuteCommand:
    """Test command execution"""
    
    def test_simple_command(self):
        """Test simple command"""
        result = execute_command("echo 'test'")
        assert "test" in result
        assert "Error" not in result
    
    def test_command_with_working_dir(self):
        """Test command with working directory"""
        result = execute_command("pwd", working_dir="/tmp")
        assert "/tmp" in result or "tmp" in result
    
    def test_failed_command(self):
        """Test failed command"""
        result = execute_command("nonexistent_command_xyz")
        assert "Error" in result


class TestFileSystem:
    """Test filesystem operations"""
    
    def test_write_and_read_file(self):
        """Test file write and read"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, "test.txt")
            content = "Hello, CodeViewX!"
            
            write_result = write_real_file(test_file, content)
            assert "Success" in write_result or "wrote" in write_result
            
            read_result = read_real_file(test_file)
            assert content in read_result
    
    def test_write_file_creates_directory(self):
        """Test automatic directory creation when writing files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_file = os.path.join(tmpdir, "subdir", "nested", "test.txt")
            content = "Nested content"
            
            write_result = write_real_file(nested_file, content)
            assert "Success" in write_result or "wrote" in write_result
            
            assert os.path.exists(nested_file)
    
    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        result = read_real_file("/nonexistent/file.txt")
        assert "Error" in result or "not exist" in result
    
    def test_list_directory(self):
        """Test directory listing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "subdir"))
            open(os.path.join(tmpdir, "file1.txt"), 'w').close()
            open(os.path.join(tmpdir, "file2.txt"), 'w').close()
            
            result = list_real_directory(tmpdir)
            assert "file1.txt" in result
            assert "file2.txt" in result
            assert "subdir" in result


class TestRipgrepSearch:
    """Test ripgrep search functionality"""
    
    def test_search_in_current_dir(self):
        """Test search in current directory"""
        result = ripgrep_search("def test_", "tests/", file_type="py")
        
        if "not installed" in result or "not found" in result:
            pytest.skip("ripgrep not installed")
        
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
