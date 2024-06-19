import json
from django.conf import settings


def parse_benchmark_file(file_path=None):
    """
    This function is used to read output_profiler file with format:
    one param line with 3 json_blocks
    It will store
    :param file_path:
    :return: bm_list: []['"bm=" line', json_blocks]
    """

    if file_path is None:
        file_path = settings.PROFILER_JSON_FILE_PATH

    with open(file_path, 'r') as file:
        lines = file.readlines()

    bm_list = []
    current_bm = None
    brace_count = 0
    in_json_block = False
    current_json = []

    for line in lines:
        line = line.strip()
        if line.startswith('bm='):
            if current_bm:
                # Add the previous bm element to bm_list
                if current_json:
                    current_bm['json_blocks'].append(''.join(current_json))
                bm_list.append(current_bm)
                current_json = []
            # Create a new bm element
            current_bm = {
                'line': line,
                'json_blocks': []
            }
        elif line.startswith('{') and not in_json_block:
            in_json_block = True
            brace_count = 1
            current_json.append(line)
        elif in_json_block:
            current_json.append(line)
            brace_count += line.count('{')
            brace_count -= line.count('}')
            if brace_count == 0:
                in_json_block = False
                current_bm['json_blocks'].append(''.join(current_json))
                current_json = []

    # Ensure the last bm element is processed
    if current_bm:
        if current_json:
            current_bm['json_blocks'].append(''.join(current_json))
        bm_list.append(current_bm)

    # Convert json strings to dictionaries
    for bm in bm_list:
        bm['json_blocks'] = [json.loads(block) for block in bm['json_blocks']]

    return bm_list


def parse_bm_line(bm_line):
    """
    Parse the line of "bm=...." read from profiler
    :param bm_line:
    :return:
    """
    parts = bm_line.split(',')
    result = {}
    for part in parts:
        key, value = part.split('=')
        result[key.strip()] = value.strip()
    return result

