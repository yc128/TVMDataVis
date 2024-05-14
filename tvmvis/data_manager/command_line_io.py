import subprocess
import platform
import sys

# Used to run command on Windows. Ignore when running on Linux
bash_path = "D:/Users/dell/Documents/Postgrad-D/msys64/usr/bin/bash.exe"

def run_command_linux(command):
    """on Linux"""
    return subprocess.run(command, shell=True, capture_output=True, text=True)


def run_command_windows(command):
    """on Windows by MinGW64"""
    return subprocess.run([bash_path, "-c", command], capture_output=True, text=True)


def run_command(command, full_result_return = False):
    try:
        # check os
        os_type = platform.system()

        if os_type == "Windows":
            result = run_command_windows(command)
        else:
            result = run_command_linux(command)

        # print("result:\n", result.stdout)

        if result.returncode != 0:
            print("Error when running cmd: ", command, "\nwith error: ", result.stderr)

        if full_result_return:
            return result
        return result.stdout
    except Exception as e:
        print("An error occurred:", e)
        return " "