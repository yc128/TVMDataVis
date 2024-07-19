from django.db.models import ForeignKey, Q, IntegerField, FloatField

from tvmvis.models import Benchmark, Run, TaskResults, TotalResults, TaskGraphResults
import json
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist


def load_all_datas():
    """
    Load all data pairs from table.
    X: pk
    Y: fields without pk
    :return: data pack
    """
    x_axis = Benchmark._meta.pk.name

    y_axs = get_chart_title_list()

    x_axs = [x_axis for _ in range(len(y_axs))]

    print("y_axs: ", y_axs)

    return load_chart_datas(x_axes=x_axs, y_axes=y_axs)


def get_chart_title_list():
    x_axis = Benchmark._meta.pk.name

    # code behind if not can exclude other fields using FK linking
    y_axs = [field.name for field in Benchmark._meta.get_fields() if not field.auto_created or field.concrete]
    y_axs = [e for e in y_axs if e != x_axis]
    return y_axs


def get_all_param_types():
    def extract_numeric_fields(model):
        fields = model._meta.get_fields()
        # 提取数字类型字段（整数和浮点数）
        field_names = [
            field.name for field in fields
            if (isinstance(field, IntegerField) or isinstance(field, FloatField))  # 只获取数字类型字段
               and not field.primary_key  # 排除主键
               and not isinstance(field, ForeignKey)  # 排除外键
               and field.name != 'HardwareInfo'  # 排除特定字段
        ]
        return field_names

    # 获取每个模型的数字类型字段
    task_results_fields = extract_numeric_fields(TaskResults)
    total_results_fields = extract_numeric_fields(TotalResults)
    task_graph_results_fields = extract_numeric_fields(TaskGraphResults)

    # 合并所有字段名到一个列表中
    all_fields = task_results_fields + total_results_fields + task_graph_results_fields

    return json.dumps(all_fields)



def get_all_run_ids():
    # query Run object's runId and remove duplicate
    run_ids = Run.objects.values_list('RunID', flat=True).distinct()

    # Convert QuerySet into list
    return json.dumps(list(run_ids))


def get_all_device_names():
    # query TaskResults object's HardwareInfo and remove duplicate
    device_names = TaskResults.objects.values_list('HardwareInfo', flat=True).distinct()

    # Convert QuerySet into list
    return json.dumps(list(device_names))


# To avoid non-exist bm
def get_common_benchmark_names_by_run_ids(run_ids):
    # 如果run_ids为空，返回空列表
    if not run_ids:
        return []

    # 查询每个runId对应的所有benchmarkName
    all_benchmark_names = []
    for run_id in run_ids:
        bm_names = set(Benchmark.objects.filter(Run_id=run_id).values_list('BenchmarkName', flat=True))
        all_benchmark_names.append(bm_names)

    # 找出交集
    common_benchmark_names = set.intersection(*all_benchmark_names)

    return json.dumps(list(common_benchmark_names))


def get_common_benchmark_names_by_device_names(device_names):
    if not device_names:
        return []

    all_benchmark_names = []
    for device_name in device_names:
        # Step 1: 获取与 device_name 相关的 TaskResults
        task_results = TaskResults.objects.filter(HardwareInfo=device_name)

        # Step 2: 获取与这些 TaskResults 相关的 TaskGraphResults
        task_graph_results_ids = task_results.values_list('TaskGraphResult', flat=True)

        # Step 3: 获取与这些 TaskGraphResults 相关的 TotalResults
        total_results_ids = TaskGraphResults.objects.filter(TaskGraphID__in=task_graph_results_ids).values_list('Result', flat=True)

        # Step 4: 获取与这些 TotalResults 相关的 Benchmarks
        benchmark_ids = TotalResults.objects.filter(ResultID__in=total_results_ids).values_list('Benchmark', flat=True)

        # Step 5: 获取 Benchmarks 的名字
        bm_names = set(Benchmark.objects.filter(BenchmarkID__in=benchmark_ids).values_list('BenchmarkName', flat=True))

        all_benchmark_names.append(bm_names)

    # 找出交集
    common_benchmark_names = set.intersection(*all_benchmark_names)

    return json.dumps(list(common_benchmark_names))




def load_chart_datas(x_axes, y_axes):
    """

    :param x_axes: x axis title list
    :param y_axes: y axis title list
    :return: packed jsoned char datas
    """
    # Dict with multi groups of data
    data_pack = {}
    for i in range(0, len(x_axes)):
        data = load_paired_chart_data(
            x_axis=x_axes[i], y_axis=y_axes[i], serialize=False)
        data_pack[y_axes[i]] = data

    serialized_data_pack = json.dumps(data_pack)
    return serialized_data_pack


def load_paired_chart_data(x_axis, y_axis, serialize=True,
                           max_data_size=100):
    """
    get required chart data from db, convert to json format
    :param max_data_size: maximum size for requesting data
    :param serialize: Decide whether to return a jsoned format
    :param x_axis: x title
    :param y_axis: y title
    :return: jsoned chart data
    """
    print(x_axis, y_axis)
    data = Benchmark.objects.all()[:max_data_size].values(x_axis, y_axis)
    # chart_data format:
    # [[xTitle, yTitle], [xPos_1, yPos_1], [xPos_2, yPos2]..]
    chart_data = [[x_axis, y_axis]]

    for entry in data:
        chart_data.append([entry[x_axis], entry[y_axis]])

    if serialize:
        serialized_chart_data = json.dumps(chart_data)
        return serialized_chart_data
    else:
        return chart_data


def load_customize_chart_datas(x_axes, y_axes):
    """

    :param x_axes: x axis title list
    :param y_axes: y axis title list
    :return: packed jsoned char datas
    """
    # Dict with multi groups of data
    data_pack = {}
    for i in range(0, len(x_axes)):
        data = load_paired_chart_data(
            x_axis=x_axes[i], y_axis=y_axes[i], serialize=False)
        data_pack[y_axes[i]] = data

    serialized_data_pack = json.dumps(data_pack)
    return serialized_data_pack


def load_compared_paired_chart_data(comparison_mode, parameter_type,
                                    run_ids, device_names, benchmark_name, max_data_size=100):
    """
    Get chart data from database
    :param comparison_mode: byRun or byDevice
    :param parameter_type: the data that wants to visualize
    :param run_ids:
    :param device_names:
    :param benchmark_name:
    :param max_data_size:
    :return:
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

            # Get TaskGraphResults
            task_graph_results = TaskGraphResults.objects.filter(Result__in=total_results)

            # Get TaskResults
            task_results = TaskResults.objects.filter(TaskGraphResult__in=task_graph_results)

            # Determine which table contains the parameter_type
            if parameter_type in [field.name for field in TaskResults._meta.fields]:
                datas = task_results.values('HardwareInfo', parameter_type)[:max_data_size]
                chart_data = [['HardwareInfo', parameter_type]]
            elif parameter_type in [field.name for field in TaskGraphResults._meta.fields]:
                # Map data to ('HardwareInfo', param_type) format
                mapped_datas = task_results.values('HardwareInfo', 'TaskGraphResult__' + parameter_type)[:max_data_size]
                chart_data = [['HardwareInfo', parameter_type]]
                datas = [
                    {'HardwareInfo': entry['HardwareInfo'], parameter_type: entry['TaskGraphResult__' + parameter_type]}
                    for entry in mapped_datas]
            elif parameter_type in [field.name for field in TotalResults._meta.fields]:
                # Map data to ('HardwareInfo', param_type) format
                mapped_datas = task_results.values('HardwareInfo', 'TaskGraphResult__Result__' + parameter_type)[
                               :max_data_size]
                chart_data = [['HardwareInfo', parameter_type]]
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
                TaskGraphID__in=task_results.values_list('TaskGraphResult_id', flat=True))

            # Get TotalResults from TaskGraphResults
            total_results = TotalResults.objects.filter(
                ResultID__in=task_graph_results.values_list('Result_id', flat=True))

            # Get Benchmarks from TotalResults with specific benchmark name
            benchmarks = Benchmark.objects.filter(BenchmarkID__in=total_results.values_list('Benchmark_id', flat=True),
                                                  BenchmarkName=benchmark_name)

            # Get Runs from Benchmarks
            runs = Run.objects.filter(RunID__in=benchmarks.values_list('Run_id', flat=True))

            # Determine which table contains the parameter_type
            if parameter_type in [field.name for field in TaskResults._meta.fields]:
                datas = task_results.values('TaskGraphResult__Result__Benchmark__Run__RunID', parameter_type)[
                        :max_data_size]
                chart_data = [['RunID', parameter_type]]
            elif parameter_type in [field.name for field in TaskGraphResults._meta.fields]:
                datas = task_graph_results.values('Result__Benchmark__Run__RunID', parameter_type)[:max_data_size]
                # Map data to ('RunID', param_type) format
                mapped_datas = task_results.values('TaskGraphResult__Result__Benchmark__Run__RunID',
                                                   'TaskGraphResult__' + parameter_type)[:max_data_size]
                chart_data = [['RunID', parameter_type]]
                datas = [{'TaskGraphResult__Result__Benchmark__Run__RunID': entry[
                    'TaskGraphResult__Result__Benchmark__Run__RunID'],
                          parameter_type: entry['TaskGraphResult__' + parameter_type]} for entry in mapped_datas]
            elif parameter_type in [field.name for field in TotalResults._meta.fields]:
                datas = total_results.values('Benchmark__Run__RunID', parameter_type)[:max_data_size]
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

    serialized_data_pack = json.dumps(data_pack)
    return serialized_data_pack




def get_model_by_field_name(field_name):
    # 遍历所有已注册的模型

    for model in apps.get_models():
        try:
            # 尝试获取字段
            model._meta.get_field(field_name)
            # 如果字段存在，返回模型名称
            return model
        except FieldDoesNotExist:
            # 如果字段不存在，继续检查下一个模型
            continue
            # 如果没有找到字段，返回 None
    return None
