from django.http import HttpResponse
from django.shortcuts import render
from django.core.serializers import serialize
from tvmvis.models import Benchmark
import json
from tvmvis.data_manager.chart_data_loader import load_chart_datas, load_all_datas, get_chart_title_list


# Create your views here.
def index(request):
    serialized_chart_datas = load_all_datas()
    chart_title_list = json.dumps(get_chart_title_list())

    return render(request, 'tvmvis/index.html', {
        'serialized_datas': serialized_chart_datas,
        'serialized_titles': chart_title_list})


def fetch_data(request):
    y_axis = request.GET.get('yTitle', "default_value")

    data = load_chart_datas(x_axes=[Benchmark._meta.pk.name],
                            y_axes=[y_axis])

    return HttpResponse(data, content_type="application/json")
