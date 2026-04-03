#!/usr/bin/env python3
"""
File Operations Tool for LangChain ReAct Agent
Provides safe file read, write, and list operations within workspace
"""

import os
from pathlib import Path
from typing import Optional
from langchain.tools import BaseTool
from pydantic import Field


class FileOperationsTool(BaseTool):
    """Tool for safe file operations within a workspace directory"""
    
    name: str = "file_operations"
    description: str = """Useful for file operations within the workspace directory.
    Supports the following operations:
    
    1. READ a file:
       Input: "read: filename.txt"
       Returns the contents of the file
    
    2. WRITE to a file:
       Input: "write: filename.txt | content to write"
       Creates or overwrites the file with the content
    
    3. LIST files:
       Input: "list" or "list: directory_name"
       Lists all files in the workspace or specified directory
    
    4. DELETE a file:
       Input: "delete: filename.txt"
       Deletes the specified file
    
    Examples:
    - "read: notes.txt"
    - "write: summary.txt | This is a summary of the research"
    - "list"
    - "list: subdirectory"
    - "delete: old_file.txt"
    
    All operations are restricted to the workspace directory for security.
    """
    
    workspace_dir: Path = Field(default_factory=lambda: Path("workspace"))
    
    def __init__(self, workspace_dir: Optional[str] = None, **kwargs):
        """Initialize the file operations tool"""
        if workspace_dir:
            kwargs['workspace_dir'] = Path(workspace_dir)
        super().__init__(**kwargs)
        # Ensure workspace directory exists
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_safe_path(self, filename: str) -> Optional[Path]:
        """
        Get a safe path within the workspace directory
        
        Args:
            filename: The filename or relative path
            
        Returns:
            Safe path or None if path is outside workspace
        """
        try:
            # Resolve the path relative to workspace
            file_path = (self.workspace_dir / filename).resolve()
            
            # Ensure the path is within workspace
            if not str(file_path).startswith(str(self.workspace_dir.resolve())):
                return None
            
            return file_path
        except Exception:
            return None
    
    def _read_file(self, filename: str) -> str:
        """Read a file from the workspace"""
        file_path = self._get_safe_path(filename)
        if not file_path:
            return f"Error: Invalid file path '{filename}'"
        
        if not file_path.exists():
            return f"Error: File '{filename}' does not exist"
        
        if not file_path.is_file():
            return f"Error: '{filename}' is not a file"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"Content of '{filename}':\n{content}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def _write_file(self, filename: str, content: str) -> str:
        """Write content to a file in the workspace"""
        file_path = self._get_safe_path(filename)
        if not file_path:
            return f"Error: Invalid file path '{filename}'"
        
        try:
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return f"Successfully wrote {len(content)} characters to '{filename}'"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def _list_files(self, directory: str = ".") -> str:
        """List files in the workspace or subdirectory"""
        dir_path = self._get_safe_path(directory)
        if not dir_path:
            return f"Error: Invalid directory path '{directory}'"
        
        if not dir_path.exists():
            return f"Error: Directory '{directory}' does not exist"
        
        if not dir_path.is_dir():
            return f"Error: '{directory}' is not a directory"
        
        try:
            items = []
            for item in sorted(dir_path.iterdir()):
                rel_path = item.relative_to(self.workspace_dir)
                if item.is_dir():
                    items.append(f"📁 {rel_path}/")
                else:
                    size = item.stat().st_size
                    items.append(f"📄 {rel_path} ({size} bytes)")
            
            if not items:
                return f"Directory '{directory}' is empty"
            
            return f"Files in '{directory}':\n" + "\n".join(items)
        except Exception as e:
            return f"Error listing files: {str(e)}"
    
    def _delete_file(self, filename: str) -> str:
        """Delete a file from the workspace"""
        file_path = self._get_safe_path(filename)
        if not file_path:
            return f"Error: Invalid file path '{filename}'"
        
        if not file_path.exists():
            return f"Error: File '{filename}' does not exist"
        
        if not file_path.is_file():
            return f"Error: '{filename}' is not a file (cannot delete directories)"
        
        try:
            file_path.unlink()
            return f"Successfully deleted '{filename}'"
        except Exception as e:
            return f"Error deleting file: {str(e)}"
    
    def _run(self, query: str) -> str:
        """
        Execute the file operations tool
        
        Args:
            query: Operation command (read/write/list/delete)
            
        Returns:
            Result of the operation or error message
        """
        try:
            query = query.strip()
            
            # Parse the operation
            if query.lower().startswith("read:"):
                filename = query[5:].strip()
                return self._read_file(filename)
            
            elif query.lower().startswith("write:"):
                # Split on first pipe character
                parts = query[6:].split("|", 1)
                if len(parts) != 2:
                    return "Error: Write operation requires format 'write: filename | content'"
                filename = parts[0].strip()
                content = parts[1].strip()
                return self._write_file(filename, content)
            
            elif query.lower().startswith("list"):
                if ":" in query:
                    directory = query.split(":", 1)[1].strip()
                else:
                    directory = "."
                return self._list_files(directory)
            
            elif query.lower().startswith("delete:"):
                filename = query[7:].strip()
                return self._delete_file(filename)
            
            else:
                return (
                    "Error: Unknown operation. Use one of:\n"
                    "- read: filename\n"
                    "- write: filename | content\n"
                    "- list or list: directory\n"
                    "- delete: filename"
                )
        
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of _run"""
        return self._run(query)


# Example usage and testing
if __name__ == "__main__":
    # Create tool with test workspace
    tool = FileOperationsTool(workspace_dir="test_workspace")
    
    print("File Operations Tool Test Cases:")
    print("=" * 50)
    
    # Test write
    print("\n1. Writing a file:")
    result = tool._run("write: test.txt | Hello, this is a test file!")
    print(result)
    
    # Test read
    print("\n2. Reading the file:")
    result = tool._run("read: test.txt")
    print(result)
    
    # Test list
    print("\n3. Listing files:")
    result = tool._run("list")
    print(result)
    
    # Test delete
    print("\n4. Deleting the file:")
    result = tool._run("delete: test.txt")
    print(result)
    
    # Test list again
    print("\n5. Listing files after delete:")
    result = tool._run("list")
    print(result)

# Made with Bob
