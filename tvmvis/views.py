from django.http import HttpResponse
from django.shortcuts import render
import json
import json

from django.shortcuts import render

from tvmvis.chart_data_manager.chart_data_loader import load_all_datas, get_chart_title_list, \
    load_compared_paired_chart_data


# Create your views here.
def index(request):
    serialized_chart_datas = load_all_datas()
    chart_title_list = json.dumps(get_chart_title_list())

    return render(request, 'tvmvis/index.html', {
        'serialized_datas': serialized_chart_datas,
        'serialized_titles': chart_title_list})


def fetch_data(request):
    comparison_mode = request.GET.get('comparisonMode')
    parameter_type = request.GET.get('parameterType')
    benchmark_name = request.GET.get('benchmarkName')
    run_ids = request.GET.getlist('runId')
    device_names = request.GET.getlist('deviceName')


    # TODO logic handling

    data = load_compared_paired_chart_data(comparison_mode=comparison_mode,
                                           parameter_type=parameter_type,
                                           run_ids=run_ids,
                                           device_names=device_names,
                                           benchmark_name=benchmark_name)

    print("data:", data)

    return HttpResponse(data, content_type="application/json")

    # if y_axis_add == "-" or y_axis_add == "--":
    #     data = load_chart_datas(x_axes=[Benchmark._meta.pk.name],
    #                             y_axes=[y_axis])
    # else:
    #     data = load_chart_datas(x_axes=[Benchmark._meta.pk.name, Benchmark._meta.pk.name],
    #                             y_axes=[y_axis, y_axis_add])
    #
    # return HttpResponse(data, content_type="application/json")
