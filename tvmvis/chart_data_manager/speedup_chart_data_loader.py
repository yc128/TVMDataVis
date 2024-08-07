import json

from django.db.models import Q
from tvmvis.models import Run, Benchmark, TotalResults, TaskResults


def get_total_speedup_data(runids, bm_names, device_name):
    """
    从数据库中提取特定 RunIDs、BenchmarkNames 和 DeviceName 对应的 TotalSpeedup 数据。

    :param runids: 包含多个 RunID 的列表
    :param bm_names: 包含多个 BenchmarkName 的列表
    :param device_name: 要筛选的设备名称，对应 TaskResults 中的 HardwareInfo
    :return: 一个字典，其中键是 BenchmarkName，值是另一个字典，包含 RunID 和 TotalSpeedup 的对应关系
    """
    # 第一步：获取符合条件的 Benchmark 对象
    print("runids", runids)
    benchmarks = Benchmark.objects.filter(
        Run_id__in=runids,
        BenchmarkName__in=bm_names
    )

    print("bm:", benchmarks)

    # 第二步：获取符合条件的 TaskResults 对象
    task_results = TaskResults.objects.filter(
        TaskGraphResult__Result__Benchmark__in=benchmarks,
        HardwareInfo=device_name
    )

    print("task_results:", task_results)

    # 第三步：从 TaskResults 中提取唯一的 TotalResults，并获取 TotalSpeedup 数据
    total_results_ids = task_results.values_list('TaskGraphResult__Result_id', flat=True).distinct()
    total_results = TotalResults.objects.filter(
        ResultID__in=total_results_ids
    )

    print("total_results:", set(total_results))

    # 构建结果字典
    data = {}
    for bm_name in bm_names:
        data[bm_name] = {}
        for run_id in runids:
            speedup = total_results.filter(
                Benchmark__BenchmarkName=bm_name,
                Benchmark__Run_id=run_id
            ).values_list('TotalSpeedup', flat=True).first()
            data[bm_name][run_id] = speedup if speedup is not None else 0

    return json.dumps(data)


