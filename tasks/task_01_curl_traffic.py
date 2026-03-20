"""
Task 01: Curl Traffic Analysis

Finds the first and last curl.exe tunneled traffic entries in the log file,
extracts their timestamps, and calculates the duration.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from interfaces.i_task import ITask
from util_log_parser import (
    filter_lines_by_pattern,
    extract_timestamp,
    parse_timestamp,
    extract_tunnel_info
)


logger = logging.getLogger(__name__)


class Task01CurlTraffic(ITask):
    """
    Task 01: Find first and last curl.exe tunneled traffic.

    Analyzes log file to find:
    - First curl.exe tunnel entry with timestamp
    - Last curl.exe tunnel entry with timestamp
    - Duration between first and last entries
    """

    def __init__(self, log_file_path: str):
        """
        Initialize Task 01.

        Args:
            log_file_path: Path to the log file to analyze
        """
        self.log_file_path = log_file_path

    def get_description(self) -> str:
        """Get task description."""
        return ("Task 01: Find first and last curl.exe tunneled traffic, "
                "record timestamps and calculate duration")

    def _parse_curl_entry(self, line: str) -> Optional[Dict[str, Any]]:
        """
        Parse a curl.exe log entry.

        Args:
            line: Log line containing curl.exe traffic

        Returns:
            Dict with timestamp, timestamp_str, and tunnel_info, or None if parsing fails
        """
        timestamp_str = extract_timestamp(line)
        if not timestamp_str:
            return None

        timestamp = parse_timestamp(timestamp_str)
        if not timestamp:
            return None

        tunnel_info = extract_tunnel_info(line)
        if not tunnel_info or tunnel_info.get('process') != 'curl.exe':
            return None

        return {
            'timestamp': timestamp,
            'timestamp_str': timestamp_str,
            'tunnel_info': tunnel_info,
            'line': line
        }

    def execute(self) -> Dict[str, Any]:
        """
        Execute Task 01.

        Returns:
            Dict containing:
                - task: Task name
                - status: 'success' or 'error'
                - data: Dict with first_entry, last_entry, duration_seconds, entry_count
                - error: Error message if status is 'error'
        """
        try:
            logger.info(f"Starting Task 01: Analyzing {self.log_file_path}")

            # Filter lines containing curl.exe
            curl_lines = filter_lines_by_pattern(
                self.log_file_path,
                r'nsTunnel.+Tunneling\sflow.+process:\scurl\.exe'
            )

            if not curl_lines:
                return {
                    'task': 'Task 01 - Curl Traffic Analysis',
                    'status': 'success',
                    'data': {
                        'entry_count': 0,
                        'message': 'No curl.exe entries found in log file'
                    }
                }

            # Parse first and last entries
            first_entry = None
            last_entry = None

            for line in curl_lines:
                entry = self._parse_curl_entry(line)
                if entry:
                    if first_entry is None:
                        first_entry = entry
                    last_entry = entry

            if not first_entry or not last_entry:
                return {
                    'task': 'Task 01 - Curl Traffic Analysis',
                    'status': 'error',
                    'error': 'Failed to parse curl.exe entries'
                }

            # Calculate duration
            duration = last_entry['timestamp'] - first_entry['timestamp']
            duration_seconds = duration.total_seconds()

            logger.info(f"Found {len(curl_lines)} curl.exe entries")
            logger.info(f"First entry: {first_entry['timestamp_str']}")
            logger.info(f"Last entry: {last_entry['timestamp_str']}")
            logger.info(f"Duration: {duration_seconds:.3f} seconds")

            return {
                'task': 'Task 01 - Curl Traffic Analysis',
                'status': 'success',
                'data': {
                    'first_entry': {
                        'timestamp': first_entry['timestamp_str'],
                        'host': first_entry['tunnel_info']['host'],
                        'dst_addr': first_entry['tunnel_info']['dst_addr'],
                        'src_addr': first_entry['tunnel_info']['src_addr']
                    },
                    'last_entry': {
                        'timestamp': last_entry['timestamp_str'],
                        'host': last_entry['tunnel_info']['host'],
                        'dst_addr': last_entry['tunnel_info']['dst_addr'],
                        'src_addr': last_entry['tunnel_info']['src_addr']
                    },
                    'duration_seconds': round(duration_seconds, 3),
                    'duration_formatted': str(duration),
                    'entry_count': len(curl_lines)
                }
            }

        except FileNotFoundError:
            error_msg = f"Log file not found: {self.log_file_path}"
            logger.error(error_msg)
            return {
                'task': 'Task 01 - Curl Traffic Analysis',
                'status': 'error',
                'error': error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error during task execution: {str(e)}"
            logger.exception(error_msg)
            return {
                'task': 'Task 01 - Curl Traffic Analysis',
                'status': 'error',
                'error': error_msg
            }
