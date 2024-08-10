import json
from django.db.models import Q
from tvmvis.models import Run, Benchmark, TotalResults, TaskResults


def get_total_speedup_data(runids, bm_names, device_name):
    """
    Retrieves TotalSpeedup data from the database for specified RunIDs, BenchmarkNames, and DeviceName.

    :param runids: List of RunIDs to filter the data.
    :param bm_names: List of BenchmarkNames to filter the data.
    :param device_name: The name of the device to filter by, corresponding to HardwareInfo in TaskResults.
    :return: A dictionary where the key is the BenchmarkName, and the value is another dictionary mapping RunID to TotalSpeedup.
    """
    # Step 1: Retrieve Benchmark objects that match the specified RunIDs and BenchmarkNames
    print("runids", runids)
    benchmarks = Benchmark.objects.filter(
        Run_id__in=runids,
        BenchmarkName__in=bm_names
    )

    print("bm:", benchmarks)

    # Step 2: Retrieve TaskResults objects that match the specified Benchmarks and DeviceName (HardwareInfo)
    task_results = TaskResults.objects.filter(
        TaskGraphResult__Result__Benchmark__in=benchmarks,
        HardwareInfo=device_name
    )

    print("task_results:", task_results)

    # Step 3: Extract unique TotalResults from TaskResults and retrieve the TotalSpeedup data
    total_results_ids = task_results.values_list('TaskGraphResult__Result_id', flat=True).distinct()
    total_results = TotalResults.objects.filter(
        ResultID__in=total_results_ids
    )

    print("total_results:", set(total_results))

    # Step 4: Construct the result dictionary
    data = {}
    for bm_name in bm_names:
        data[bm_name] = {}
        for run_id in runids:
            # Filter TotalResults to get the TotalSpeedup for the specific Benchmark and RunID
            speedup = total_results.filter(
                Benchmark__BenchmarkName=bm_name,
                Benchmark__Run_id=run_id
            ).values_list('TotalSpeedup', flat=True).first()
            # Store the speedup value or 0 if no speedup data is found
            data[bm_name][run_id] = speedup if speedup is not None else 0

    return json.dumps(data)
