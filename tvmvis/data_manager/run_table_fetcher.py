from command_line_io import run_command


def build_run_table(description="Automated Jenkins pipeline"):
    run = {"Description": description}

    input_command = "date"
    lines_datetime = run_command(input_command).splitlines()
    run["DateTime"] = lines_datetime[0] if len(lines_datetime) > 0 else "null"

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
