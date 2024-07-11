from django.http import HttpResponse
from django.shortcuts import render
from tvmvis.models import Benchmark
import json
from tvmvis.chart_data_manager.chart_data_loader import load_chart_datas, load_all_datas, get_chart_title_list


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
    run_ids = request.GET.getlist('runId')
    device_names = request.GET.getlist('deviceName')

    # TODO logic handling

    # if y_axis_add == "-" or y_axis_add == "--":
    #     data = load_chart_datas(x_axes=[Benchmark._meta.pk.name],
    #                             y_axes=[y_axis])
    # else:
    #     data = load_chart_datas(x_axes=[Benchmark._meta.pk.name, Benchmark._meta.pk.name],
    #                             y_axes=[y_axis, y_axis_add])
    #
    # return HttpResponse(data, content_type="application/json")
