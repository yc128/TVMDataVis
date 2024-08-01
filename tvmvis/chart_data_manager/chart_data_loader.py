from django.db.models import ForeignKey, IntegerField, FloatField
from django.core.exceptions import FieldDoesNotExist
from django.apps import apps
from tvmvis.models import Benchmark, Run, TaskResults, TotalResults, TaskGraphResults
import json
from django.core.serializers.json import DjangoJSONEncoder


def get_chart_title_list():
    """
    Get all field names from the Benchmark table, excluding auto-created fields and the primary key.
    :return: List of field names
    """
    x_axis = Benchmark._meta.pk.name
    y_axes = [field.name for field in Benchmark._meta.get_fields() if not field.auto_created and field.concrete]
    return [e for e in y_axes if e != x_axis]


def get_all_param_types():
    """
    Get all numeric fields from TaskResults, TotalResults, and TaskGraphResults models.
    :return: JSON serialized list of numeric field names
    """

    def extract_numeric_fields(model):
        fields = model._meta.get_fields()
        return [field.name for field in fields if isinstance(field, (IntegerField, FloatField))
                and not field.primary_key and not isinstance(field, ForeignKey) and field.name != 'HardwareInfo']

    task_results_fields = extract_numeric_fields(TaskResults)
    total_results_fields = extract_numeric_fields(TotalResults)
    task_graph_results_fields = extract_numeric_fields(TaskGraphResults)
    # all_fields = task_results_fields + total_results_fields + task_graph_results_fields
    all_fields = total_results_fields
    return json.dumps(all_fields)


def get_all_run_details():
    """
    Get all unique RunIDs, DateTime, and CommitPoint from the Run table.
    :return: JSON serialized list of lists, each containing [RunID, DateTime, CommitPoint]
    """
    run_details = Run.objects.values_list('RunID', 'DateTime', 'CommitPoint').distinct()

    # Convert DateTime to string format
    run_details_list = [
        [run_id, date_time.strftime('%Y-%m-%d %H:%M:%S'), commit_point]
        for run_id, date_time, commit_point in run_details
    ]

    return json.dumps(run_details_list, cls=DjangoJSONEncoder)


def get_all_device_names():
    """
    Get all unique device names (HardwareInfo) from the TaskResults table.
    :return: JSON serialized list of device names
    """
    device_names = TaskResults.objects.values_list('HardwareInfo', flat=True).distinct()
    return json.dumps(list(device_names))


# To avoid non-exist bm
def get_common_benchmark_names_by_run_ids(run_ids):
    """
    Get common Benchmark names for the given list of RunIDs.
    Only includes Benchmark names that are referenced in the TotalResults table.
    :param run_ids: List of RunIDs
    :return: JSON serialized list of common Benchmark names
    """
    if not run_ids:
        return []

    all_benchmark_names = []
    for run_id in run_ids:
        # Get Benchmark names for the given run_id
        benchmark_names = Benchmark.objects.filter(Run_id=run_id).values_list('BenchmarkName', flat=True)

        # Filter Benchmark names that are referenced in TotalResults
        valid_benchmark_names = []
        for benchmark_name in set(benchmark_names):
            benchmarks = Benchmark.objects.filter(Run=run_id, BenchmarkName=benchmark_name)
            # Get TotalResults
            total_results = TotalResults.objects.filter(Benchmark__in=benchmarks)
            if total_results.count() > 0:
                valid_benchmark_names.append(benchmark_name)

        print("benchmark_names: {}".format(len(set(benchmark_names))))
        print("valid_benchmark_names: {}".format(len(valid_benchmark_names)))

        all_benchmark_names.append(set(valid_benchmark_names))

    # Find common Benchmark names across all run_ids
    common_benchmark_names = set.intersection(*all_benchmark_names) if all_benchmark_names else set()

    return json.dumps(list(common_benchmark_names))


def get_common_benchmark_names_by_device_names(device_names):
    """
    Get common Benchmark names for the given list of device names (HardwareInfo).
    :param device_names: List of device names
    :return: JSON serialized list of common Benchmark names
    """
    if not device_names:
        return []

    all_benchmark_names = []
    for device_name in device_names:
        task_results = TaskResults.objects.filter(HardwareInfo=device_name)
        task_graph_results_ids = task_results.values_list('TaskGraphResult', flat=True).distinct()
        total_results_ids = TaskGraphResults.objects.filter(TaskGraphID__in=task_graph_results_ids) \
            .values_list('Result', flat=True).distinct()
        benchmark_ids = TotalResults.objects.filter(ResultID__in=total_results_ids) \
            .values_list('Benchmark', flat=True).distinct()
        bm_names = set(Benchmark.objects.filter(BenchmarkID__in=benchmark_ids).values_list('BenchmarkName', flat=True))
        all_benchmark_names.append(bm_names)

    common_benchmark_names = set.intersection(*all_benchmark_names)
    return json.dumps(list(common_benchmark_names))


def load_compared_paired_chart_data_by_benchmarks(comparison_mode, parameter_type,
                                                  run_ids, device_names, benchmark_names,
                                                  max_data_size=100, is_json=True):
    data_pack = {}
    for benchmark_name in benchmark_names:
        data_pack[benchmark_name] = load_compared_paired_chart_data(comparison_mode, parameter_type,
                                                                    run_ids, device_names, benchmark_name,
                                                                    max_data_size, False)

    if is_json:
        serialized_data_pack = json.dumps(data_pack)
        return serialized_data_pack
    else:
        return data_pack


def load_compared_paired_chart_data(comparison_mode, parameter_type,
                                    run_ids, device_names, benchmark_name,
                                    max_data_size=100, is_json=True):
    """
    Get chart data from the database for comparison.
    :param comparison_mode: Comparison mode ('byRun' or 'byDevice')
    :param parameter_type: Parameter type to visualize
    :param run_ids: List of RunIDs
    :param device_names: List of device names
    :param benchmark_name: Name of the benchmark
    :param max_data_size: Maximum number of data points to request
    :return: JSON serialized data pack
    """
    data_pack = {}

    if comparison_mode == 'byRun':
        for run_id in run_ids:
            # Get specific run table
            run = Run.objects.get(RunID=run_id)

            # Get specific bm with same run and specific bm name
            benchmarks = Benchmark.objects.filter(Run=run, BenchmarkName=benchmark_name)

            # Get TotalResults
            total_results = TotalResults.objects.filter(Benchmark__in=benchmarks)

            print("run_id: {}".format(run_id), "; ", "benchmarks:{}".format(benchmarks),
                  "total_results: {}".format(total_results.count()))

            # Get TaskGraphResults
            task_graph_results = TaskGraphResults.objects.filter(Result__in=total_results)

            # Get TaskResults
            task_results = TaskResults.objects.filter(TaskGraphResult__in=task_graph_results)

            chart_data = [['HardwareInfo', parameter_type]]
            # Determine which table contains the parameter_type
            if parameter_type in [field.name for field in TaskResults._meta.fields]:
                datas = task_results.values('HardwareInfo', parameter_type)[:max_data_size]
            elif parameter_type in [field.name for field in TaskGraphResults._meta.fields]:
                # Map data to ('HardwareInfo', param_type) format
                mapped_datas = task_results.values('HardwareInfo', 'TaskGraphResult__' + parameter_type)[:max_data_size]
                datas = [
                    {'HardwareInfo': entry['HardwareInfo'], parameter_type: entry['TaskGraphResult__' + parameter_type]}
                    for entry in mapped_datas]
            elif parameter_type in [field.name for field in TotalResults._meta.fields]:
                # Map data to ('HardwareInfo', param_type) format
                mapped_datas = task_results.values('HardwareInfo',
                                                   'TaskGraphResult__Result__' + parameter_type).distinct()[
                               :max_data_size]
                print("mapped_datas", mapped_datas)
                datas = [{'HardwareInfo': entry['HardwareInfo'],
                          parameter_type: entry['TaskGraphResult__Result__' + parameter_type]} for entry in
                         mapped_datas]
            else:
                raise ValueError(f"Unknown parameter type: {parameter_type}")

            for entry in datas:
                chart_data.append([entry['HardwareInfo'], entry[parameter_type]])
            data_pack[run_id] = chart_data

    # By Device
    elif comparison_mode == 'byDevice':
        for device_name in device_names:
            # Get TaskResults with specific HardwareInfo (device name)
            task_results = TaskResults.objects.filter(HardwareInfo=device_name)

            # Get TaskGraphResults from TaskResults
            task_graph_results = TaskGraphResults.objects.filter(
                TaskGraphID__in=task_results.values_list('TaskGraphResult_id', flat=True)).distinct()

            # Get TotalResults from TaskGraphResults
            total_results = TotalResults.objects.filter(
                ResultID__in=task_graph_results.values_list('Result_id', flat=True)).distinct()

            # Get Benchmarks from TotalResults with specific benchmark name
            benchmarks = Benchmark.objects.filter(BenchmarkID__in=total_results.values_list('Benchmark_id', flat=True),
                                                  BenchmarkName=benchmark_name)

            # Determine which table contains the parameter_type
            if parameter_type in [field.name for field in TaskResults._meta.fields]:
                datas = task_results.values('TaskGraphResult__Result__Benchmark__Run__RunID', parameter_type)[
                        :max_data_size]
                chart_data = [['RunID', parameter_type]]
            elif parameter_type in [field.name for field in TaskGraphResults._meta.fields]:
                # Map data to ('RunID', param_type) format
                mapped_datas = task_results.values('TaskGraphResult__Result__Benchmark__Run__RunID',
                                                   'TaskGraphResult__' + parameter_type)[:max_data_size]
                chart_data = [['RunID', parameter_type]]
                datas = [{'TaskGraphResult__Result__Benchmark__Run__RunID': entry[
                    'TaskGraphResult__Result__Benchmark__Run__RunID'],
                          parameter_type: entry['TaskGraphResult__' + parameter_type]} for entry in mapped_datas]
            elif parameter_type in [field.name for field in TotalResults._meta.fields]:
                # Map data to ('RunID', param_type) format
                mapped_datas = task_results.values('TaskGraphResult__Result__Benchmark__Run__RunID',
                                                   'TaskGraphResult__Result__' + parameter_type)[:max_data_size]
                chart_data = [['RunID', parameter_type]]
                datas = [{'TaskGraphResult__Result__Benchmark__Run__RunID': entry[
                    'TaskGraphResult__Result__Benchmark__Run__RunID'],
                          parameter_type: entry['TaskGraphResult__Result__' + parameter_type]} for entry in
                         mapped_datas]
            else:
                raise ValueError(f"Unknown parameter type: {parameter_type}")

            for entry in datas:
                chart_data.append([entry['TaskGraphResult__Result__Benchmark__Run__RunID'], entry[parameter_type]])
            data_pack[device_name] = chart_data

    if not is_json:
        return data_pack
    serialized_data_pack = json.dumps(data_pack)
    return serialized_data_pack


def get_model_by_field_name(field_name):
    """
    Traverse all registered models and return the model containing the specified field name.
    :param field_name: Name of the field to search for
    :return: Model containing the field, or None if not found
    """
    for model in apps.get_models():
        try:
            # Try to get the field from the model
            model._meta.get_field(field_name)
            return model  # Return the model if the field is found
        except FieldDoesNotExist:
            continue  # Continue to the next model if the field is not found
    return None  # Return None if no model contains the field


def get_commit_point_by_run_ids(run_ids):
    """
    Get the CommitPoint for the given list of RunIDs.
    :param run_ids: List of RunIDs
    :return: JSON serialized list of dictionaries with RunID and CommitPoint
    """
    # Query the database to get the CommitPoint for the given RunIDs
    commit_points = Run.objects.filter(RunID__in=run_ids).values('RunID', 'CommitPoint')

    # Convert QuerySet to list and return as JSON
    return json.dumps(list(commit_points))
