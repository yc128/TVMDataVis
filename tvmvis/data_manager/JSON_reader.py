import datetime
import json
import os.path


def read_json_objects(file_path):
    """
    JSON reader for profiler_output
    :param file_path:
    :return:
    """
    results = []
    with open(file_path, 'r') as file:
        file_content = file.read()

        obj_depth = 0
        obj_start = 0
        for i, char in enumerate(file_content):
            if char == '{':
                if obj_depth == 0:
                    obj_start = i
                obj_depth += 1
            elif char == '}':
                obj_depth -= 1
                if obj_depth == 0:
                    obj_end = i + 1
                    try:
                        obj_str = file_content[obj_start:obj_end]
                        obj = json.loads(obj_str)
                        results.append(obj['s0'])  # 假设我们只对 's0' 键感兴趣
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
    return results


def get_file_mod_time(file_path):
    last_mod_time = os.path.getmtime(file_path)
    readable_time = datetime.datetime.fromtimestamp(last_mod_time)
    return readable_time
