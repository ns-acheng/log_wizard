"""
Task interface for log analysis tasks.

All tasks must implement this interface to be executable by the task runner.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ITask(ABC):
    """Interface for all log analysis tasks."""

    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        Execute the task and return results.

        Returns:
            Dict containing:
                - task: str - Task name/description
                - status: str - 'success' or 'error'
                - data: Dict - Task-specific results
                - error: str (optional) - Error message if status is 'error'
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Get a human-readable description of what this task does.

        Returns:
            str: Task description
        """
        pass
