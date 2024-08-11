from command_line_io import run_command
from django.utils import timezone
from datetime import datetime

def build_run_table(description="Automated Jenkins pipeline"):
    """
    Builds a dictionary representing a run table with information such as the description,
    date and time, version, and commit point.

    The function executes system commands to gather the current date and time, and attempts to
    fetch the version and commit point from a specified command. If the command to fetch the
    date fails, it falls back to using the current system time.

    :param description: Description of the run, defaults to "Automated Jenkins pipeline".
    :return: A dictionary containing run information including DateTime, Version, CommitPoint,
             and Description.
    """

    # Initialize the run dictionary with a description
    run = {"Description": description}

    # Attempt to get the current date and time using the 'date' command
    input_command = 'date +%Y-%m-%dT%H:%M:%S'
    line_datetime = run_command(input_command)

    # If the 'date' command fails, use the current system time
    input_date_time = timezone.now()
    line_datetime = line_datetime.strip()
    if any(char.isdigit() for char in line_datetime):
        print("date from cmd:", line_datetime, ";")
        input_date_time = datetime.fromisoformat(line_datetime)

    # Set the DateTime field in the run dictionary
    run["DateTime"] = input_date_time

    # TODO Update the version reading function, make sure it can fetch correct version info
    #  (By checking whether the console can print proper 'Version cmd Results' when running data_reader)

    #  Attempt to get the version information using the 'tornado
    #  --version' command
    input_command = "tornado --version"
    lines_tver = run_command(input_command).splitlines()

    # Default CommitPoint for testing purposes
    run["CommitPoint"] = "No CommitPoint info"
    run["Version"] = "No Version info"

    # Parse the command output to find version and commit point information
    for line in lines_tver:
        if "version" in line:
            line_arr = line.split('=')
            if len(line_arr) > 1:
                run["Version"] = line_arr[1].strip()
        if "commit" in line:
            line_arr = line.split('=')
            if len(line_arr) > 1:
                run["CommitPoint"] = line_arr[1].strip()

    print("Version cmd Results: Ver:", run["Version"], "; CommitPoint:", run["CommitPoint"])

    return run
