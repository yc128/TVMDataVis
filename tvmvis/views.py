from django.shortcuts import render
from django.core.serializers import serialize
from tvmvis.models import Benchmark
import json
from tvmvis.data_manager.chart_data_loader import load_paired_chart_data


# Create your views here.
def index(request):
    serialized_chart_data = load_paired_chart_data('RunId', 'TOTAL_TASK_GRAPH_TIME')

    return render(request, 'tvmvis/index.html', {'serialized_data': serialized_chart_data})
