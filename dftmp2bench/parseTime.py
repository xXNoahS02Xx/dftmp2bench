import re

def parse_time_string(time_string):
    """
    Parse different time-string formats into a total number of seconds (float).
    
    Supports examples like:
      1) "TOTAL RUN TIME: 0 days 0 hours 0 minutes 0 seconds 684 msec"
      2) "Elapsed time: 0 days  0 hours  0 minutes  0.8 seconds."
      3) "Wall Time: 1.10 seconds"
      4) "cpu-time:     0 d,  0 h,  0 min,  0.987 sec"
    Returns None if it doesn't match any of the known patterns.
    """
    
    # --- Pattern 1) TOTAL RUN TIME ---
    # Example: "TOTAL RUN TIME: 0 days 0 hours 0 minutes 0 seconds 684 msec"
    match_run_time = re.search(
        r'TOTAL RUN TIME:\s*'
        r'(?P<days>\d+)\s*days\s+'
        r'(?P<hours>\d+)\s*hours\s+'
        r'(?P<minutes>\d+)\s*minutes\s+'
        r'(?P<seconds>\d+)\s*seconds\s+'
        r'(?P<msec>\d+)\s*msec',
        time_string
    )
    if match_run_time:
        days = int(match_run_time.group('days'))
        hours = int(match_run_time.group('hours'))
        minutes = int(match_run_time.group('minutes'))
        seconds = int(match_run_time.group('seconds'))
        msec = int(match_run_time.group('msec'))
        
        total_seconds = (days * 86400
                         + hours * 3600
                         + minutes * 60
                         + seconds
                         + msec / 1000.0)
        return total_seconds

    # --- Pattern 2) Elapsed time ---
    # Example: "Elapsed time: 0 days  0 hours  0 minutes  0.8 seconds."
    match_elapsed_time = re.search(
        r'Elapsed time:\s*'
        r'(?P<days>\d+)\s*days\s+'
        r'(?P<hours>\d+)\s*hours\s+'
        r'(?P<minutes>\d+)\s*minutes\s+'
        r'(?P<seconds>\d+(?:\.\d+)?)\s*seconds\.',
        time_string
    )
    if match_elapsed_time:
        days = int(match_elapsed_time.group('days'))
        hours = int(match_elapsed_time.group('hours'))
        minutes = int(match_elapsed_time.group('minutes'))
        seconds = float(match_elapsed_time.group('seconds'))
        
        total_seconds = (days * 86400
                         + hours * 3600
                         + minutes * 60
                         + seconds)
        return total_seconds

    # --- Pattern 3) Wall Time ---
    # Example: "Wall Time: 1.10 seconds"
    match_wall_time = re.search(
        r'Wall Time:\s*'
        r'(?P<seconds>\d+(?:\.\d+)?)\s*seconds',
        time_string
    )
    if match_wall_time:
        seconds = float(match_wall_time.group('seconds'))
        return seconds
    
    # --- Pattern 4) CPU-time ---
    # Example: "cpu-time:     0 d,  0 h,  0 min,  0.987 sec"
    match_cpu_time = re.search(
        r'cpu-time:\s*'
        r'(?P<days>\d+)\s*d,\s*'
        r'(?P<hours>\d+)\s*h,\s*'
        r'(?P<minutes>\d+)\s*min,\s*'
        r'(?P<seconds>\d+(?:\.\d+)?)\s*sec',
        time_string
    )
    if match_cpu_time:
        days = int(match_cpu_time.group('days'))
        hours = int(match_cpu_time.group('hours'))
        minutes = int(match_cpu_time.group('minutes'))
        seconds = float(match_cpu_time.group('seconds'))
        
        total_seconds = (days * 86400
                         + hours * 3600
                         + minutes * 60
                         + seconds)
        return total_seconds

    # If none of the patterns matched, return None
    return None


# ------------------ Testing the Function ------------------
examples = [
    "TOTAL RUN TIME: 0 days 0 hours 0 minutes 0 seconds 684 msec",
    "Elapsed time: 0 days  0 hours  0 minutes  0.8 seconds.",
    "Wall Time: 1.10 seconds",
    "cpu-time:     0 d,  0 h,  0 min,  0.987 sec"
]

for ex in examples:
    parsed_seconds = parse_time_string(ex)
    print(f"Input: {ex!r}\nParsed: {parsed_seconds} seconds\n")

