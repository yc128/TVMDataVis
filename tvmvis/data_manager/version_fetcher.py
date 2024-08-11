import json
import os
import subprocess
import platform
import sys
import re

from command_line_io import run_command

nvidia_SMI_failed = "NVIDIA-SMI has failed"

def fetch_version_from_cmd():
    """
    Fetches various software and system version information using command-line tools
    and saves the results in a JSON file.

    The function retrieves the following version information:
    - GCC version
    - Operating System version
    - Nvidia driver version (via nvidia-smi) and OpenCL driver version (via clinfo)
    - JVM version (via Tornado JVM)
    - Maven version
    - CMake version
    - Python version

    The gathered version information is then saved to a JSON file named 'versions.json'.
    """

    versions = {}

    # Fetch GCC version
    input_command = "gcc --version"
    lines_gcc = run_command(input_command).splitlines()
    versions["gcc"] = lines_gcc[0] if len(lines_gcc) > 0 else "null"

    # Fetch Operating System version
    versions["OS"] = platform.platform()

    # Fetch Nvidia driver version using nvidia-smi
    input_command = "nvidia-smi --query-gpu=driver_version --format=csv,noheader"
    lines_nv = run_command(input_command).splitlines()
    version_nv = lines_nv[0] if len(lines_nv) > 0 and (nvidia_SMI_failed not in lines_nv[0]) else "null"

    # Fetch OpenCL driver version using clinfo
    input_command = "clinfo"
    lines_cl = run_command(input_command).splitlines()
    driver_version = "null"
    for line in lines_cl:
        if "Version" in line:
            driver_version = line
            line_arr = line.split(':')
            if len(line_arr) > 1:
                driver_version = line_arr[1].strip()  # Remove leading/trailing whitespace
            break
    version_cl = driver_version

    # Combine Nvidia and OpenCL driver versions
    versions["Driver"] = f"Nvidia_smi: {version_nv}; OpenCL: {version_cl}"

    # Fetch JVM version using Tornado JVM
    input_command = "tornado -version"
    jvm_output_full = run_command(input_command, full_result_return=True)
    lines_jvm = jvm_output_full.stdout.splitlines() if len(jvm_output_full.stdout) > 0 \
        else jvm_output_full.stderr.splitlines()
    version_jvm = ""
    for line in lines_jvm:
        if "command not found" in line:
            version_jvm = "null"
            break
        if "java" in line.lower():
            version_jvm += line + ";"
    versions["JVM"] = version_jvm if len(version_jvm) > 0 else "null"

    # Fetch Maven version
    input_command = "mvn --version"
    lines_nvm = run_command(input_command).splitlines()
    versions["Maven"] = lines_nvm[0] if len(lines_nvm) > 0 else "null"

    # Fetch CMake version
    input_command = "cmake --version"
    lines_cmake = run_command(input_command).splitlines()
    versions["CMake"] = lines_cmake[0] if len(lines_cmake) > 0 else "null"

    # Fetch Python version
    major, minor, micro = sys.version_info[:3]
    py_version = f"{major}.{minor}.{micro}"
    versions["Python"] = py_version

    # Save version information to a JSON file
    with open('versions.json', 'w') as f:
        json.dump(versions, f, indent=4)

    print("Version information has been saved to versions.json.")
