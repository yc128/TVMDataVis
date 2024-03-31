import json
import os
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


def run_command(command):
    # check os
    os_type = platform.system()

    if os_type == "Windows":
        result = run_command_windows(command)
    else:
        result = run_command_linux(command)

    # print("res:\n", result.stdout)

    if result.returncode != 0:
        print("Error when running cmd:", result.stderr)

    return result.stdout


# tornado_path = "D:/Users/dell/Documents/Postgrad-D/TornadoVM-master/bin/bin/"
# tornado_executable = os.path.join(tornado_path, "tornado")

# # os.environ["PATH"] += os.pathsep + tornado_path

versions = {}



# GCC
input_command = "gcc --version"
lines_gcc = run_command(input_command).splitlines()
versions["gcc"] = lines_gcc[0] if len(lines_gcc) > 0 else "null"

# OS
versions["OS"] = platform.platform()

# Driver
input_command = ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"]
result = subprocess.run(input_command, capture_output=True, text=True)
versions["Driver"] = result.stdout.strip()

# JVM
input_command = "tornado -version"
lines_jvm = run_command(input_command).splitlines()
versions["JVM"] = lines_jvm[0] if len(lines_jvm) > 0 else "null"

# Maven
input_command = "mvn --version"
lines_nvm = run_command(input_command).splitlines()
versions["Maven"] = lines_nvm[0] if len(lines_nvm) > 0 else "null"

# CMake
input_command = "cmake --version"
lines_cmake = run_command(input_command).splitlines()
versions["CMake"] = lines_cmake[0] if len(lines_cmake) > 0 else "null"

# Python
major, minor, micro = sys.version_info[:3]
py_version = f"{major}.{minor}.{micro}"
versions["Python"] = py_version

# save to json
with open('versions.json', 'w') as f:
    json.dump(versions, f, indent=4)

print("Version information has been saved to versions.json.")
