from command_line_io import run_command
from django.utils import timezone
from datetime import datetime


def build_run_table(description="Automated Jenkins pipeline"):
    run = {"Description": description}

    input_command = 'date +%Y-%m-%dT%H:%M:%S'
    line_datetime = run_command(input_command)

    # If failed to run date cmd, use current time instead.
    input_date_time = timezone.now()
    # line_datetime = '2024-07-05T07:44:23\n'
    line_datetime = line_datetime.strip()
    if any(char.isdigit() for char in line_datetime):
        print("date from cmd:", line_datetime, ";")
        input_date_time = datetime.fromisoformat(line_datetime)

    run["DateTime"] = input_date_time

    input_command = "tornado --version"
    lines_tver = run_command(input_command).splitlines()

    # Default CommitPoint for testing
    # TODO Remove this after testing
    run["CommitPoint"] = "606fc08"
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
