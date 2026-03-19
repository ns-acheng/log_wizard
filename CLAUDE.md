# Project Coding Standards

This document defines the coding standards and conventions for the `log_wizard` project. All contributors must follow these guidelines when writing or modifying code.

## Project Overview

A Python-based log parsing and analysis tool for Netskope agent logs (`nsdebuglog.log`). The tool provides an extensible task-based architecture for analyzing log files and extracting specific information patterns.

**Key Features**:
- ✅ Task-based architecture for easy extension
- ✅ Interface-driven design
- ✅ UTF-8 log file parsing
- ✅ Modular and testable code structure

## Python Requirements

- **Minimum Version**: Python 3.10+
- **CI Testing**: Python 3.11, 3.12, 3.13
- **Platform Support**: Windows, macOS, and Linux

## Architecture Principles

### Interface-Based Design

- Use Abstract Base Classes (ABC) for all task and parser interfaces
- Place interfaces in `interfaces/` directory
- Prefix interface names with `I` (e.g., `ITask`, `ILogParser`)
- All interfaces must use `@abstractmethod` decorators

### Task Pattern

- Each analysis task is a separate class implementing `ITask` interface
- Tasks are self-contained and can be executed independently
- Task classes: `Task01CurlTraffic`, `Task02ServiceRestart`, etc.
- All tasks must implement the `ITask` interface
- Tasks should return structured results (dict or dataclass)

### Code Organization

- Task implementations go in `tasks/` directory
- Utilities for parsing go in root directory with `util_` prefix
- Shared utilities stay in root directory with `util_` prefix

## File and Directory Organization

```
interfaces/          # Abstract interfaces (ABC)
  i_task.py          # Task interface
  i_log_parser.py    # Log parser interface
tasks/               # Task implementations
  task_01_curl_traffic.py
  task_02_*.py
data/                # Log files
  nsdebuglog.log     # Input log file
test/                # Unit tests
  test_tasks/        # Task tests
  test_util/         # Utility tests
output/              # Task output (timestamped folders)
```

## Naming Conventions

### Files and Modules
- **Utility files**: `util_<name>.py` (e.g., `util_log.py`, `util_parser.py`)
- **Test files**: `test_<name>.py` (e.g., `test_util_parser.py`)
- **Interface files**: `i_<name>.py` (e.g., `i_task.py`, `i_log_parser.py`)
- **Task files**: `task_<number>_<name>.py` (e.g., `task_01_curl_traffic.py`)
- Use snake_case for all file names

### Classes
- **PascalCase**: All class names (e.g., `LogParser`, `TaskRunner`)
- **Interfaces**: Prefix with `I` (e.g., `ITask`, `ILogParser`)
- **Task classes**: Format as `Task<NN><Name>` (e.g., `Task01CurlTraffic`, `Task02ServiceRestart`)
- **Manager pattern**: Suffix with `Manager` (e.g., `TaskManager`, `OutputManager`)

### Functions and Variables
- **snake_case**: All functions and variables
- **Private methods**: Prefix with single underscore `_` (e.g., `_parse_line`, `_extract_timestamp`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `LOG_DATE_FORMAT`, `DEFAULT_ENCODING`)

## Code Style

### Import Organization

Organize imports in three groups with blank lines between:

```python
# 1. Standard library
import sys
import os
import re
import logging
from datetime import datetime
from typing import List, Dict, Optional

# 2. Third-party packages
import pytest
from unittest.mock import MagicMock

# 3. Local modules
from interfaces.i_task import ITask
from util_log import setup_logging
```

### Type Hints

- Use type hints for all interface methods
- Use type hints for function parameters and return types
- Import types from appropriate modules

```python
def execute(self) -> Dict[str, any]:
    pass

def parse_log_file(self, file_path: str) -> List[Dict[str, str]]:
    pass
```

### Line Length and Code Organization

- **Line Length**: Limit each line to 110 characters. Use shorter variable names or wrap lines when necessary
- **Simplicity**: Keep `main.py` simple. Move complex logic into utilities or task modules

### Documentation

- Add docstrings for public classes and non-trivial methods
- Use comments for complex logic that isn't self-evident
- Document log format patterns and regex expressions
- Keep comments concise and relevant

## Logging

### Logging Setup

- Use Python's `logging` module exclusively
- Configure logging via `util_log.py` module
- Log to both file and console
- Timestamped output folders: `output/YYYYMMDD-HHMMSS/`

### Logging Best Practices

- **Levels**:
  - INFO: Normal operations and significant events
  - WARNING: Issues that don't prevent operation
  - ERROR: Failures and exceptions
- **Format**: `'%(asctime)s - %(levelname)s - %(message)s'`
- **Security**: Never log passwords, credentials, or sensitive data

## Configuration

### Configuration Files

- **Task config**: `data/config.json` (JSON format, optional)
- **Log files**: `data/*.log` (input files)
- **Output**: `output/YYYYMMDD-HHMMSS/` (timestamped results)

## Testing

### Test Framework

- **Framework**: pytest
- **Coverage**: Use pytest-cov
- **Mocking**: Use pytest-mock and unittest.mock

### Test Organization

- Place all tests in `test/` directory
- Name test files: `test_<module_name>.py`
- Use descriptive test names: `test_<functionality>_<scenario>`
- Group related tests in classes

### Test Requirements

- **Mock I/O Operations**: Mock all file system operations
- **Sample Data**: Create small sample log files for testing
- **Leverage Fixtures**: Use shared fixtures from `conftest.py` for consistency
- **Temporary Files**: Use pytest's `tmp_path` fixture for any file system operations

### Running Tests

```bash
# Run all tests
python -m pytest test/ -v

# Run specific test file
python -m pytest test/test_tasks/test_task_01.py -v

# Run with coverage
python -m pytest test/ --cov=. --cov-report=term-missing
```

## Error Handling

### Exception Handling

- Wrap I/O operations in try-except blocks
- Use `logger.exception()` to log exceptions with full stack traces
- Provide clear, actionable error messages
- Always clean up resources in `finally` blocks

### File Encoding

- Default to UTF-8 encoding for all log files
- Handle encoding errors gracefully with fallback options

## Log Format Patterns

### Standard Log Line Format

```
YYYY/MM/DD HH:MM:SS.mmm <process> <pid> <tid> <level> <file>:<line> <component> <message>
```

### Example Log Lines

```
2026/03/19 14:55:23.385 stAgentSvc p1e64 t3054 info tunnel.cpp:1150 nsTunnel TLS [sessId 1] Tunneling flow from addr: 192.168.13.134:63893, process: curl.exe to host: www.citystgeorges.ac.uk, addr: 2.58.104.10:443 to nsProxy
```

### Regular Expression Patterns

Document all regex patterns used for parsing:

```python
# Timestamp pattern: YYYY/MM/DD HH:MM:SS.mmm
TIMESTAMP_PATTERN = r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3})'

# Process name pattern
PROCESS_PATTERN = r'process: ([^\s,]+)'

# Tunneling flow pattern
TUNNEL_PATTERN = r'Tunneling flow from.*?process: ([^\s,]+)'
```

## Task Development Guidelines

### Creating a New Task

1. **Define the task** - Clearly describe what information to extract
2. **Create task class** in `tasks/task_<number>_<name>.py`
3. **Implement ITask interface** with `execute()` method
4. **Return structured results** as a dictionary or dataclass
5. **Write tests** in `test/test_tasks/test_task_<number>.py`
6. **Document the task** - Add docstring explaining inputs and outputs

### Task Template

```python
from typing import Dict
from datetime import datetime
from interfaces.i_task import ITask


class Task01Example(ITask):
    """
    Task 01: Description of what this task does.

    Extracts: What information is extracted
    Returns: Structure of return value
    """

    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path

    def execute(self) -> Dict[str, any]:
        """Execute the task and return results."""
        # Implementation here
        return {
            'task': 'Task 01 - Example',
            'status': 'success',
            'data': {}
        }
```

## Security Considerations

- **Credentials**: Never log passwords, tokens, or credentials
- **Input Validation**: Validate all file paths and user inputs
- **File Operations**: Use safe file operations; avoid path traversal
- **Logging Levels**: Set appropriate levels to avoid leaking sensitive data
- **Version Control**: Never commit secrets or sensitive log data to the repository

## Git Workflow

### Branch Strategy

- Main branch: `master`
- Create feature branches for new work
- Submit pull requests for review

### Commit Messages

- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Follow conventional commit format when possible

### CI/CD

- Tests run automatically on pull requests and pushes to `master`
- All tests must pass before merging
- CI matrix: Python 3.11, 3.12, 3.13 on supported platforms

## Code Review Checklist

When reviewing code, verify:

- ✓ Task implements ITask interface properly
- ✓ Code follows project naming conventions
- ✓ Type hints are present for all public APIs
- ✓ Logging doesn't expose sensitive data
- ✓ Error handling is appropriate and comprehensive
- ✓ Tests are included for all new functionality
- ✓ Regex patterns are documented and tested
- ✓ Line length stays within 110 characters
- ✓ File encoding is handled correctly (UTF-8)
