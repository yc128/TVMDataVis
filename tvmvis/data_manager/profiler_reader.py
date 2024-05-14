import json



def parse_benchmark_file(file_path):
    """
    This function is used to read output_profiler file with format:
    one param line with 3 json_blocks
    It will store
    :param file_path:
    :return:
    """
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

# 使用示例
file_path = 'sample_output/tornado_benchmarks_medium_profiler_2_iterations.txt'
bm_list = parse_benchmark_file(file_path)

for i, bm in enumerate(bm_list):
    print(f"Benchmark {i+1}:")
    print("Line:")
    print(bm['line'])
    print("JSON Blocks:")
    for j, json_block in enumerate(bm['json_blocks']):
        print(f"JSON Block {j+1}:")
        print(json.dumps(json_block, indent=4))
