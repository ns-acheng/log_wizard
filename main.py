"""
Main entry point for log_wizard.

Analyzes log file timestamps and displays duration table.
"""

import sys
from pathlib import Path
from datetime import datetime


def analyze_log_files(log_files):
    """Analyze timestamps from log files and return table data."""
    results = []

    for log_file in log_files:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()

            with open(log_file, 'rb') as f:
                f.seek(0, 2)
                file_size = f.tell()
                if file_size == 0:
                    continue
                f.seek(-min(1024, file_size), 2)
                last_chunk = f.read().decode('utf-8', errors='ignore')
                last_line = last_chunk.strip().split('\n')[-1]

            first_parts = first_line.split()
            last_parts = last_line.split()

            if len(first_parts) < 2 or len(last_parts) < 2:
                continue

            first_ts = first_parts[0] + ' ' + first_parts[1]
            last_ts = last_parts[0] + ' ' + last_parts[1]

            t1 = datetime.strptime(first_ts, '%Y/%m/%d %H:%M:%S.%f')
            t2 = datetime.strptime(last_ts, '%Y/%m/%d %H:%M:%S.%f')
            duration = (t2 - t1).total_seconds()

            results.append({
                'filename': log_file.name,
                'first_ts': first_ts,
                'last_ts': last_ts,
                'duration': duration
            })
        except Exception as e:
            print(f"Error processing {log_file.name}: {e}", file=sys.stderr)
            continue

    return results


def print_table(results):
    """Print results as a formatted table."""
    print("\n" + "=" * 80)
    print("Log Wizard - Timestamp Analysis")
    print("=" * 80 + "\n")

    print('| Log File       | First Timestamp         | Last Timestamp          | Duration (seconds) |')
    print('|----------------|-------------------------|-------------------------|-------------------|')

    for r in results:
        print(f"| {r['filename']:<14} | {r['first_ts']} | {r['last_ts']} | {r['duration']:>17.3f} |")

    if len(results) > 1:
        avg_duration = sum(r['duration'] for r in results) / len(results)
        print('|----------------|-------------------------|-------------------------|-------------------|')
        print(f"| **Average**    |                         |                         | **{avg_duration:>13.3f}** |")

    print()


def main():
    """Main entry point."""
    data_dir = Path("data")

    if len(sys.argv) > 1:
        log_files = [Path(sys.argv[1])]
        if not log_files[0].exists():
            print(f"Error: Log file not found: {log_files[0]}", file=sys.stderr)
            sys.exit(1)
    else:
        log_files = sorted(data_dir.glob("*.log"))

        if not log_files:
            print("Error: No log files found in data/ directory", file=sys.stderr)
            print("Usage: python main.py [path/to/logfile.log]", file=sys.stderr)
            sys.exit(1)

    results = analyze_log_files(log_files)

    if not results:
        print("Error: No valid log files with timestamps found", file=sys.stderr)
        sys.exit(1)

    print_table(results)


if __name__ == "__main__":
    main()
