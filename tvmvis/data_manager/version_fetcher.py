import json
import os
import subprocess
import platform
import sys
import re

from command_line_io import run_command

nvidia_SMI_failed = "NVIDIA-SMI has failed"


def fetch_version_from_cmd():
    versions = {}

    # GCC
    input_command = "gcc --version"
    lines_gcc = run_command(input_command).splitlines()
    versions["gcc"] = lines_gcc[0] if len(lines_gcc) > 0 else "null"

    # OS
    versions["OS"] = platform.platform()

    # Driver
    # nvidia
    input_command = "nvidia-smi --query-gpu=driver_version --format=csv,noheader"
    lines_nv = run_command(input_command).splitlines()
    version_nv = lines_nv[0] if len(lines_nv) > 0 and (nvidia_SMI_failed not in lines_nv[0]) else "null"
    # opencl
    input_command = "clinfo"
    lines_cl = run_command(input_command).splitlines()
    driver_version = "null"
    for line in lines_cl:
        if "Version" in line:
            driver_version = line
            line_arr = line.split(':')
            if len(line_arr) > 1:
                driver_version = line_arr[1]
            break
    version_cl = driver_version

    versions["Driver"] = "Nvidia_smi: " + version_nv + "; OpenCL: " + version_cl

    # JVM
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
            version_jvm = version_jvm + line + ";"
    versions["JVM"] = version_jvm if len(version_jvm) > 0 else "null"

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
