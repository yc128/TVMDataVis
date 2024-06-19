from profiler_reader import parse_bm_line, parse_benchmark_file


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
    dispatch_DataTransfers_time = int(last_json_block['benchmark'].get('TOTAL_DISPATCH_DATA_TRANSFERS_TIME', 0))
    dispatch_kernel_time = int(last_json_block['benchmark'].get('TOTAL_DISPATCH_KERNEL_TIME', 0))
    kernel_time = int(last_json_block['benchmark'].get('TOTAL_KERNEL_TIME', 0))

    # 构建TaskGraphResults字典
    task_graph_results = {
        'Result': bm_info,  # 假设这是TotalResults的外键，需要实际对象
        'LastKernelTime': kernel_time,
        'KernelAverage': kernel_time,  # 假设使用最后一个迭代的内核时间作为平均值
        'Copy_IN': copy_in,
        'Copy_OUT': copy_out,
        'Compilation_Graal': compilation_graal,
        'Compilation_Driver': compilation_driver,
        'Dispatch_DataTransfers_Time': dispatch_DataTransfers_time,
        'Dispatch_Kernel_Time': dispatch_kernel_time

    }

    return task_graph_results


def build_total_results(bm_line, json_blocks):
    bm_data = parse_bm_line(bm_line)

    # 提取 bm_line 中的相关信息
    total_average_time = int(float(bm_data['average']))
    total_median_time = int(float(bm_data['median']))
    total_first_iteration = int(float(bm_data['firstIteration']))
    total_best = int(float(bm_data['best']))

    # 从 json_blocks 中提取最小时间（假设从两个迭代中获取最小值）
    iteration_times = []
    for block in json_blocks:
        benchmark_info = block['benchmark']['benchmark.montecarlo']
        if 'TASK_KERNEL_TIME' in benchmark_info:
            iteration_times.append(int(benchmark_info['TASK_KERNEL_TIME']))

    total_minimum = min(iteration_times)

    # 从 bm_line 中提取 speedup 信息（假设平均加速比）
    # Java_reference have no speedup info
    if 'speedupAvg' in bm_data:
        total_speedup = float(bm_data['speedupAvg'])
    else:
        total_speedup = 0

    # 构建 TotalResults 字典
    total_results = {
        'Benchmark': bm_data['bm'],  # 假设 Benchmark 对象可以从 bm_data['bm'] 中获取或查找
        'TotalAverageTime': total_average_time,
        'TotalMedianTime': total_median_time,
        'TotalFirstIteration': total_first_iteration,
        'TotalBest': total_best,
        'TotalMinimum': total_minimum,
        'TotalSpeedup': total_speedup,
    }

    return total_results


def build_task_results(bm_line, json_blocks):
    bm_data = parse_bm_line(bm_line)

    # 从 bm_line 中提取相关信息
    benchmark_name = bm_data['bm']
    hardware_info = None
    software_info = None

    task_results = []

    for i, json_block in enumerate(json_blocks):
        task_result = {}

        # 解析 JSON block
        benchmark_details = json_block.get("benchmark", {})
        benchmark_specifics = benchmark_details.get(f"benchmark.{benchmark_name.split('-')[0]}", {})

        # 填充 TaskResult 字典
        task_result['TaskID'] = f"{benchmark_name}_{i+1}"  # 生成唯一标识符
        task_result['TaskGraphResults'] = benchmark_name
        task_result['HardwareInfo'] = benchmark_specifics.get("DEVICE", hardware_info)
        task_result['SoftwareInfo'] = benchmark_specifics.get("BACKEND", software_info)

        # 根据 JSON block 填充不同的时间信息
        if i == 0:
            # 第一个 JSON block，包含编译信息
            task_result['Kernel Time (ns)'] = None
            task_result['Code generation Time (ns)'] = int(benchmark_details.get("TOTAL_CODE_GENERATION_TIME", 0))
            task_result['Driver compilation Time (ns)'] = int(benchmark_details.get("TOTAL_DRIVER_COMPILE_TIME", 0))
        else:
            # 第二和第三个 JSON block，包含执行迭代信息
            task_result['Kernel Time (ns)'] = int(benchmark_details.get("TOTAL_KERNEL_TIME", 0))
            task_result['Code generation Time (ns)'] = None
            task_result['Driver compilation Time (ns)'] = None

        task_results.append(task_result)

    return task_results


# 使用示例
file_path = 'sample_output/tornado_benchmarks_medium_profiler_2_iterations.txt'
bm_list = parse_benchmark_file(file_path)

benchmark_line = bm_list[10]['line']
json_blocks = bm_list[10]['json_blocks']
task_graph_results = build_task_graph_results(benchmark_line, json_blocks)
total_results = build_total_results(benchmark_line, json_blocks)
task_results = build_task_results(benchmark_line, json_blocks)

# 输出结果
import pprint

print("Raw:")
print(benchmark_line)
print(json_blocks)

print("Task_Graph_Results:")
pprint.pprint(task_graph_results)
print("\n", "Total_Results:")
pprint.pprint(total_results)
print("\n", "Task_Results:")
pprint.pprint(task_results)