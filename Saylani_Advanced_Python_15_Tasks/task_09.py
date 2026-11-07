### Task 09 | Streaming Log Inspector
### Concepts: Generators, iterators, file handling
### Problem: Write a generator read_errors(path) that streams a log file line by line, yielding (line_number, timestamp, message) only for ERROR records. Build summarize_errors() to count errors by date.
### Requirements: Do not load the whole file into memory. Skip malformed lines while tracking their count. Expected format: YYYY-MM-DD HH:MM:SS | LEVEL | message.
### Sample / expected behavior: Input line: 2026-11-07 10:30:00 | ERROR | Connection lost -> (1,"2026-11-07 10:30:00","Connection lost").


import os
from collections import defaultdict

def read_errors(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            parts = [p.strip() for p in line_stripped.split('|')]
            if len(parts) < 3:
                continue
            
            timestamp = parts[0]
            level = parts[1].upper()
            message = " | ".join(parts[2:])
            
            if level == "ERROR":
                yield (line_number, timestamp, message)


def summarize_errors(path):
    error_counts = defaultdict(int)
    malformed_count = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, start=1):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            
            parts = [p.strip() for p in line_stripped.split('|')]
            if len(parts) < 3:
                malformed_count += 1
                continue
            
            timestamp = parts[0]
            level = parts[1].upper()
            
            if level == "ERROR":
                
                date_part = timestamp.split()[0]
                error_counts[date_part] += 1
                
    return dict(error_counts), malformed_count



if __name__ == "__main__":
    sample_log_path = "sample_server.log"
    sample_data = """2026-11-07 10:30:00 | INFO | Server started successfully
2026-11-07 10:31:15 | ERROR | Database connection lost
2026-11-07 10:32:00 | WARNING | High memory usage detected
Invalid log line without proper format
2026-11-08 09:15:22 | ERROR | Timeout while fetching API response
2026-11-08 09:20:00 | ERROR | Null pointer exception in worker thread
"""
    
    
    with open(sample_log_path, 'w', encoding='utf-8') as f:
        f.write(sample_data)
        
    print("--- Streaming Error Records ---")
    for line_no, ts, msg in read_errors(sample_log_path):
        print(f"Line {line_no} [{ts}]: {msg}")
        
    print("\n--- Error Summary by Date ---")
    summary, malformed = summarize_errors(sample_log_path)
    print("Error Counts by Date:", summary)
    print("Malformed Lines Skipped:", malformed)
    
    
    if os.path.exists(sample_log_path):
        os.remove(sample_log_path)