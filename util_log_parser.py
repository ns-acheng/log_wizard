"""
Utility functions for parsing log files.

Provides common log parsing functionality for extracting timestamps, process names,
and other structured information from Netskope agent logs.
"""

import re
import logging
from datetime import datetime
from typing import List, Dict, Optional, Generator


# Log format: YYYY/MM/DD HH:MM:SS.mmm
TIMESTAMP_PATTERN = r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d{3})'
TIMESTAMP_FORMAT = '%Y/%m/%d %H:%M:%S.%f'

# Process name pattern
PROCESS_PATTERN = r'process:\s+([^\s,]+)'

# Tunnel pattern for curl.exe or other processes
TUNNEL_PATTERN = (r'Tunneling flow from addr: ([^,]+), process: ([^\s,]+) '
                  r'to host: ([^,]+), addr: ([^\s]+) to')

logger = logging.getLogger(__name__)


def parse_timestamp(timestamp_str: str) -> Optional[datetime]:
    """
    Parse a timestamp string into a datetime object.

    Args:
        timestamp_str: Timestamp string in format 'YYYY/MM/DD HH:MM:SS.mmm'

    Returns:
        datetime object or None if parsing fails
    """
    try:
        return datetime.strptime(timestamp_str, TIMESTAMP_FORMAT)
    except ValueError as e:
        logger.warning(f"Failed to parse timestamp '{timestamp_str}': {e}")
        return None


def extract_timestamp(line: str) -> Optional[str]:
    """
    Extract timestamp from a log line.

    Args:
        line: Log line string

    Returns:
        Timestamp string or None if not found
    """
    match = re.search(TIMESTAMP_PATTERN, line)
    return match.group(1) if match else None


def extract_process_name(line: str) -> Optional[str]:
    """
    Extract process name from a log line.

    Args:
        line: Log line string

    Returns:
        Process name or None if not found
    """
    match = re.search(PROCESS_PATTERN, line)
    return match.group(1) if match else None


def extract_tunnel_info(line: str) -> Optional[Dict[str, str]]:
    """
    Extract tunneling information from a log line.

    Args:
        line: Log line string

    Returns:
        Dict with keys: src_addr, process, host, dst_addr, or None if not found
    """
    match = re.search(TUNNEL_PATTERN, line)
    if match:
        return {
            'src_addr': match.group(1),
            'process': match.group(2),
            'host': match.group(3),
            'dst_addr': match.group(4)
        }
    return None


def read_log_file(file_path: str, encoding: str = 'utf-8') -> Generator[str, None, None]:
    """
    Read log file line by line.

    Args:
        file_path: Path to log file
        encoding: File encoding (default: utf-8)

    Yields:
        Log lines as strings

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file can't be read
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        logger.error(f"Log file not found: {file_path}")
        raise
    except IOError as e:
        logger.error(f"Error reading log file {file_path}: {e}")
        raise


def filter_lines_by_pattern(file_path: str, pattern: str,
                            encoding: str = 'utf-8') -> List[str]:
    """
    Filter log lines matching a specific pattern.

    Args:
        file_path: Path to log file
        pattern: Regex pattern to match
        encoding: File encoding (default: utf-8)

    Returns:
        List of matching lines

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file can't be read
    """
    matching_lines = []
    compiled_pattern = re.compile(pattern)

    try:
        for line in read_log_file(file_path, encoding):
            if compiled_pattern.search(line):
                matching_lines.append(line)
    except (FileNotFoundError, IOError):
        raise

    logger.info(f"Found {len(matching_lines)} lines matching pattern '{pattern}'")
    return matching_lines
