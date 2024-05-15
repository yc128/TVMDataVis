import json


def parse_benchmark_file(file_path):
    """
    This function is used to read output_profiler file with format:
    one param line with 3 json_blocks
    It will store
    :param file_path:
    :return: bm_list: []['line', json_blocks]
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


def build_task_graph_results(benchmark_line, json_blocks):
    """
    Build task_graph_result field by parsed profiler
    :param benchmark_line: line starts with 'bm='
    :param json_blocks: json_block array
    :return: Dict of task_graph_results
    """
    # 从benchmark_line解析必要的信息
    bm_parts = benchmark_line.split(',')
    bm_info = {part.split('=')[0].strip(): part.split('=')[1].strip() for part in bm_parts}

    # 从第一个JSON块提取编译指标
    first_json_block = json_blocks[0]
    compilation_graal = int(first_json_block['benchmark']['TOTAL_GRAAL_COMPILE_TIME'])
    compilation_driver = int(first_json_block['benchmark']['TOTAL_DRIVER_COMPILE_TIME'])

    # 从最后一个JSON块提取数据传输和调度指标
    last_json_block = json_blocks[-1]
    copy_in = int(last_json_block['benchmark'].get('COPY_IN_TIME', 0))
    copy_out = int(last_json_block['benchmark'].get('COPY_OUT_TIME', 0))
    dispatch_time = int(last_json_block['benchmark'].get('TOTAL_DISPATCH_DATA_TRANSFERS_TIME', 0))
    kernel_time = int(last_json_block['benchmark'].get('TOTAL_KERNEL_TIME', 0))

    # 构建TaskGraphResults字典
    task_graph_results = {
        'Result': bm_info,  # 假设这是TotalResults的外键，需要实际对象
        'MinimumKernelsTime': kernel_time,
        'KernelAverage': kernel_time,  # 假设使用最后一个迭代的内核时间作为平均值
        'Copy_IN': copy_in,
        'Copy_OUT': copy_out,
        'Compilation_Graal': compilation_graal,
        'Compilation_Driver': compilation_driver,
        'Dispatch_Time': dispatch_time
    }

    return task_graph_results


# 使用示例
file_path = 'sample_output/tornado_benchmarks_medium_profiler_2_iterations.txt'
bm_list = parse_benchmark_file(file_path)

benchmark_line = bm_list[0]['line']
json_blocks = bm_list[0]['json_blocks']
task_graph_results = build_task_graph_results(benchmark_line, json_blocks)

# 输出结果
import pprint

pprint.pprint(task_graph_results)

#
# for i, bm in enumerate(bm_list):
#     print(f"Benchmark {i+1}:")
#     print("Line:")
#     print(bm['line'])
#     print("JSON Blocks:")
#     for j, json_block in enumerate(bm['json_blocks']):
#         print(f"JSON Block {j+1}:")
#         print(json.dumps(json_block, indent=4))
