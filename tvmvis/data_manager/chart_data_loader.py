from tvmvis.models import Benchmark
import json


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

    return load_chart_datas(x_axes=x_axs, y_axes=y_axs)


def get_chart_title_list():
    x_axis = Benchmark._meta.pk.name

    y_axs = [field.name for field in Benchmark._meta.get_fields()]
    y_axs = [e for e in y_axs if e != x_axis]
    return y_axs


def load_chart_datas(x_axes, y_axes):
    """

    :param x_axes: x axis title list
    :param y_axes: y axis title list
    :return: packed jsoned char datas
    """
    data_pack = {}
    for i in range(0, len(x_axes)):
        data = load_paired_chart_data(
            x_axis=x_axes[i], y_axis=y_axes[i], serialize=False)
        data_pack[y_axes[i]] = data

    serialized_data_pack = json.dumps(data_pack)
    return serialized_data_pack


def load_paired_chart_data(x_axis, y_axis, serialize=True,
                           max_data_size=100, runId_filter='2024'):
    """
    get required chart data from db, turn to json format
    :param runId_filter: runId filter for requesting data
    :param max_data_size: maximum size for requesting data
    :param serialize: Decide whether to return a jsoned format
    :param x_axis: x title
    :param y_axis: y title
    :return: jsoned chart data
    """
    data = Benchmark.objects.filter(RunId__contains=runId_filter)[:max_data_size]\
        .values(x_axis, y_axis)
    chart_data = [[x_axis, y_axis]]

    for entry in data:
        chart_data.append([entry[x_axis], entry[y_axis]])

    if serialize:
        serialized_chart_data = json.dumps(chart_data)
        return serialized_chart_data
    else:
        return chart_data
