from tvmvis.models import *


def insert_json_data(profiler_json_results, json_time, versions_json_result):
    """
    Store parsed json into db

    :param versions_json_result: versions json data
    :param json_time: json file last mod time, used for runID generation
    :param profiler_json_results: json data
    """
    if Run.objects.filter(DateTime=json_time).exists():
        print("This output profiler has already been read")
        return
    for idx, data in enumerate(profiler_json_results):

        # Create Tables
        run_instance = Run(
            DateTime=json_time,
        )

        benchmark_instance = Benchmark(
            Run=run_instance,
        )

        total_results_instance = TotalResults(
            Benchmark=benchmark_instance,

        )

        task_graph_result_instance = TaskGraphResults(
            Result=total_results_instance,
            Copy_IN=data.get('COPY_IN_TIME'),
            Copy_OUT=data.get('COPY_OUT_TIME')
        )

        software_config_instance = SoftwareConfiguration(
            OSVersion=versions_json_result.get('OS'),
            DriverVersion=versions_json_result.get('Driver'),
            JVMVersion=versions_json_result.get('JVM'),
            GCCVersion=versions_json_result.get('gcc'),
            MavenVersion=versions_json_result.get('Maven'),
            CmakeVersion=versions_json_result.get('CMake'),
            PythonVersion=versions_json_result.get('Python')
        )




        # benchmark_instance = Benchmark(
        #     RunId=json_time.strftime("%Y%m%d_%H:%M:%S") + '-' + str(idx),
        #     TOTAL_TASK_GRAPH_TIME=data.get('TOTAL_TASK_GRAPH_TIME'),
        #     COPY_IN_TIME=data.get('COPY_IN_TIME'),
        #     COPY_OUT_TIME=data.get('COPY_OUT_TIME'),
        #     TOTAL_KERNEL_TIME=data.get('TOTAL_KERNEL_TIME'),
        #     TOTAL_COPY_IN_SIZE_BYTES=data.get('TOTAL_COPY_IN_SIZE_BYTES'),
        #     TOTAL_COPY_OUT_SIZE_BYTES=data.get('TOTAL_COPY_OUT_SIZE_BYTES'),
        #     DRIVER=data.get('s0.t0', {}).get('DRIVER'),
        #     METHOD=data.get('s0.t0', {}).get('METHOD'),
        #     DEVICE_ID=data.get('s0.t0', {}).get('DEVICE_ID'),
        #     DEVICE=data.get('s0.t0', {}).get('DEVICE'),
        #     TOTAL_COPY_IN_SIZE_BYTES_R=data.get('s0.t0', {}).get('TOTAL_COPY_IN_SIZE_BYTES'),  # 注意字段名，如果有重复，需要调整
        #     TASK_KERNEL_TIME=data.get('s0.t0', {}).get('TASK_KERNEL_TIME')
        # )

        # save to db
        # try:
        #     benchmark_instance.save()
        # except Exception as e:
        #     print(f"Data insertion error: {e}")
