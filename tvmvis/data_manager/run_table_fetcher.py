from command_line_io import run_command
from django.utils import timezone
from datetime import datetime

def build_run_table(description="Automated Jenkins pipeline"):
    run = {"Description": description}

    input_command = 'date +%Y-%m-%dT%H:%M:%S'
    line_datetime = run_command(input_command)

    date_time = timezone.now()
    if any(char.isdigit() for char in line_datetime):
        print("date from cmd:", line_datetime, ";")
        date_time_str = line_datetime.decode('utf-8').strip()
        date_time = datetime.fromisoformat(date_time_str)


    run["DateTime"] = date_time

    input_command = "tornado --version"
    lines_tver = run_command(input_command).splitlines()
    for line in lines_tver:
        if "version" in line:
            line_arr = line.split('=')
            if len(line_arr) > 1:
                run["Version"] = line_arr[1]
        if "commit" in line:
            line_arr = line.split('=')
            if len(line_arr) > 1:
                run["CommitPoint"] = line_arr[1]

    return run


