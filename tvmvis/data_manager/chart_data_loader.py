from tvmvis.models import Benchmark
import json


def load_paired_chart_data(xAxis, yAxis):
    """
    get required chart data from db, turn to json format
    :param xAxis: x title
    :param yAxis: y title
    :return: jsoned chart data
    """
    data = Benchmark.objects.all().values(xAxis, yAxis)
    chart_data = [[xAxis, yAxis]]

    for entry in data:
        chart_data.append([entry[xAxis], entry[yAxis]])

    serialized_chart_data = json.dumps(chart_data)
    return serialized_chart_data
