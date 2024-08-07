from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('speedup-chart', views.speedup_chart, name='speedup_chart'),
    path('fetch-data/', views.fetch_data, name='fetch_data'),
    path('fetch-data-by-benchmarks/', views.fetch_data_by_benchmarks, name='fetch_data_by_benchmarks'),
    path('fetch-relative-mode-data/', views.fetch_relative_mode_data, name='fetch_relative_mode_data'),
    path('fetch-param-types-data/', views.fetch_param_types_data, name='fetch_param_types_data'),
    path('fetch-benchmark-name-data/', views.fetch_benchmark_name_data, name='fetch-benchmark-name-data'),
    path('fetch-commit-point-by-runid/', views.fetch_commit_points, name='fetch-commit-point-by-runid'),
    path('fetch-speedup-chart-data/', views.fetch_speedup_chart_data, name='fetch_speedup_chart_data')
]