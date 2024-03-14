from tvmvis.models import Benchmark


def insert_json_data(json_results):
    """
    Store parsed json into db

    :param json_results: json data
    """
    for idx, data in enumerate(json_results):
        # Create Benchmark
        benchmark_instance = Benchmark(
            RunId=idx,  # Assuming 0, 1, 2, 3, ...
            TOTAL_TASK_GRAPH_TIME=data.get('TOTAL_TASK_GRAPH_TIME'),
            COPY_IN_TIME=data.get('COPY_IN_TIME'),
            COPY_OUT_TIME=data.get('COPY_OUT_TIME'),
            TOTAL_KERNEL_TIME=data.get('TOTAL_KERNEL_TIME'),
            TOTAL_COPY_IN_SIZE_BYTES=data.get('TOTAL_COPY_IN_SIZE_BYTES'),
            TOTAL_COPY_OUT_SIZE_BYTES=data.get('TOTAL_COPY_OUT_SIZE_BYTES'),
            DRIVER=data.get('s0.t0', {}).get('DRIVER'),
            METHOD=data.get('s0.t0', {}).get('METHOD'),
            DEVICE_ID=data.get('s0.t0', {}).get('DEVICE_ID'),
            DEVICE=data.get('s0.t0', {}).get('DEVICE'),
            TOTAL_COPY_IN_SIZE_BYTES_R=data.get('s0.t0', {}).get('TOTAL_COPY_IN_SIZE_BYTES'),  # 注意字段名，如果有重复，需要调整
            TASK_KERNEL_TIME=data.get('s0.t0', {}).get('TASK_KERNEL_TIME')
        )

        # save to db
        try:
            benchmark_instance.save()
        except Exception as e:
            print(f"Data insertion error: {e}")
