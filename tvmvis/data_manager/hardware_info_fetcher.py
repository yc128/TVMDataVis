from command_line_io import run_command
import re

keys = ["Device ID", "Device Type", "Device Name",
        "Global memory size", "Local memory size",
        "Threads", "Max clock frequency", "compute units",
        "Device Extensions", "Compute Capability",
        "Device Partition", "Max work item dimension",
        "Unified Memory", "Atomics",
        "Half-precision", "Double-precision"]
def read_hd_config(use_command=False):
    hd_config = {}
    lines = ""

    if use_command:
        input_command = "clinfo"
        lines = run_command(input_command).splitlines()
    else:
        with open('sample_output/clinfo.txt', 'r') as file:
            lines = file.read().splitlines()

    counter = 0
    for line in lines:
        counter += 1
        key, value = key_value_extractor(line)
        if key in keys:
            hd_config[key] = value
            # print("line:", counter, "; Key:", key, "; Value:", value)

    return hd_config




# def fetch_single_device_info(lines, start_idx):


def key_value_extractor(text_line):
    match = re.search(r'([^\s].*?)\s{5,}(.*)', text_line)

    if match:
        key, value = match.groups()  # 获取匹配的第一部分（例如 "Max size"）
        # print("Key:", key)
        # print("Value:", value)
        return key, value
    return False, 0


read_hd_config()
