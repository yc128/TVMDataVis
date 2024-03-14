import json


def read_json_objects(file_path):
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



