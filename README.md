# Log Wizard

A Python-based log parsing and analysis tool for Netskope agent logs. Provides an extensible task-based architecture for analyzing log files and extracting specific information patterns.

## Features

- ✅ Task-based architecture for easy extension
- ✅ Interface-driven design
- ✅ UTF-8 log file parsing
- ✅ Modular and testable code structure

## Requirements

- Python 3.10+
- No external dependencies (uses only standard library)

## Project Structure

```
log_wizard/
├── interfaces/          # Abstract interfaces (ABC)
│   └── i_task.py        # Task interface
├── tasks/               # Task implementations
│   └── task_01_curl_traffic.py
├── data/                # Log files
│   └── nsdebuglog.log   # Input log file
├── util_log.py          # Logging utilities
├── util_log_parser.py   # Log parsing utilities
├── main.py              # Entry point
├── CLAUDE.md            # Coding standards
└── README.md            # This file
```

## Usage

1. Place your log file in the `data/` directory as `nsdebuglog.log`

2. Run the analyzer:
```bash
python main.py
```

## Implemented Tasks

### Task 01: Curl Traffic Analysis

Finds the first and last `curl.exe` tunneled traffic entries in the log file, extracts their timestamps, and calculates the duration.

**Example Output:**
```json
{
  "first_entry": {
    "timestamp": "2026/03/19 14:54:10.482",
    "host": "www.timeanddate.com",
    "dst_addr": "104.18.21.57:443",
    "src_addr": "192.168.13.134:60192"
  },
  "last_entry": {
    "timestamp": "2026/03/19 14:55:27.355",
    "host": "robota.ua",
    "dst_addr": "104.18.28.114:443",
    "src_addr": "192.168.13.134:64002"
  },
  "duration_seconds": 76.873,
  "duration_formatted": "0:01:16.873000",
  "entry_count": 1524
}
```

## Adding New Tasks

1. Create a new task file in `tasks/` directory: `task_<number>_<name>.py`

2. Implement the `ITask` interface:

```python
from typing import Dict, Any
from interfaces.i_task import ITask

class Task02Example(ITask):
    """Task 02: Description of what this task does."""

    def __init__(self, log_file_path: str):
        self.log_file_path = log_file_path

    def get_description(self) -> str:
        return "Task 02: Your description here"

    def execute(self) -> Dict[str, Any]:
        # Your implementation here
        return {
            'task': 'Task 02 - Example',
            'status': 'success',
            'data': {}
        }
```

3. Add the task to `main.py`:

```python
from tasks.task_02_example import Task02Example

tasks: List[ITask] = [
    Task01CurlTraffic(str(log_file)),
    Task02Example(str(log_file)),  # Add your new task here
]
```

## Log Format

The tool parses Netskope agent logs in the following format:

```
YYYY/MM/DD HH:MM:SS.mmm <process> <pid> <tid> <level> <file>:<line> <component> <message>
```

Example:
```
2026/03/19 14:55:23.385 stAgentSvc p1e64 t3054 info tunnel.cpp:1150 nsTunnel TLS [sessId 1] Tunneling flow from addr: 192.168.13.134:63893, process: curl.exe to host: www.citystgeorges.ac.uk, addr: 2.58.104.10:443 to nsProxy
```

## Development

See [CLAUDE.md](CLAUDE.md) for detailed coding standards and development guidelines.

### Running Tests

```bash
# Run all tests
python -m pytest test/ -v

# Run with coverage
python -m pytest test/ --cov=. --cov-report=term-missing
```

## License

Internal tool for Netskope log analysis.
