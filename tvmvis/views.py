from django.http import HttpResponse
from django.shortcuts import render
import json
import json

from django.shortcuts import render

from tvmvis.chart_data_manager.chart_data_loader import *


# Create your views here.
def index(request):
    serialized_chart_datas = {}
    chart_title_list = {}

    return render(request, 'tvmvis/index.html', {
        'serialized_datas': serialized_chart_datas,
        'serialized_titles': chart_title_list})


def fetch_data(request):
    comparison_mode = request.GET.get('comparisonMode')
    parameter_type = request.GET.get('parameterType')
    benchmark_name = request.GET.get('benchmarkName')
    run_ids = request.GET.getlist('runId')
    device_names = request.GET.getlist('deviceName')

    data = load_compared_paired_chart_data(comparison_mode=comparison_mode,
                                           parameter_type=parameter_type,
                                           run_ids=run_ids,
                                           device_names=device_names,
                                           benchmark_name=benchmark_name)

    print("data:", data)

    return HttpResponse(data, content_type="application/json")


def fetch_data_by_benchmarks(request):
    comparison_mode = request.GET.get('comparisonMode')
    parameter_type = request.GET.get('parameterType')
    benchmark_names = request.GET.getlist('benchmarkName')
    run_ids = request.GET.getlist('runId')
    device_names = request.GET.getlist('deviceName')

    data = load_compared_paired_chart_data_by_benchmarks(comparison_mode=comparison_mode,
                                                         parameter_type=parameter_type,
                                                         run_ids=run_ids,
                                                         device_names=device_names,
                                                         benchmark_names=benchmark_names)

    print("data:", data)

    return HttpResponse(data, content_type="application/json")


def fetch_relative_mode_data(request):
    comparison_mode = request.GET.get('comparisonMode')
    if comparison_mode == 'byRun':
        data = get_all_run_details()
    else:
        data = get_all_device_names()

    print("mode data:", data)
    return HttpResponse(data, content_type="application/json")


def fetch_param_types_data(request):
    data = get_all_param_types()
    print("param data:", data)
    return HttpResponse(data, content_type="application/json")


def fetch_benchmark_name_data(request):
    comparison_mode = request.GET.get('comparisonMode')
    compare_targets = request.GET.getlist('compareTargets')
    print("mode:", comparison_mode)
    if comparison_mode == "byRun":
        data = get_common_benchmark_names_by_run_ids(compare_targets)
    else:
        data = get_common_benchmark_names_by_device_names(compare_targets)

    print("bmName data:", data)
    return HttpResponse(data, content_type="application/json")


def fetch_commit_points(request):
    run_ids = request.GET.getlist('runId')
    commit_points = get_commit_point_by_run_ids(run_ids)

    print("commit_points:", commit_points)
    return HttpResponse(commit_points, content_type="application/json")



def speedup_chart(request):
    return render(request, 'tvmvis/speedupChart.html')
