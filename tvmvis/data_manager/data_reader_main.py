import argparse
import os
import sys

import django

from profiler_reader import parse_benchmark_file
from result_builder import build_total_results, build_task_graph_results, build_task_results

from benchmark_table_builder import build_benchmark_table_from_profiler, parse_single_benchmark_name
from run_table_fetcher import build_run_table

# Get root dir
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add root to Python searching dir
sys.path.append(project_root)

# Set DJANGO_SETTINGS_MODULE environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TVMDataVis.settings')

# initialize Django
django.setup()

from tvmvis.models import *

benchmark_count = 0
run_count = 0
results_count = 0
tgr_count = 0
task_result_count = 0


def main():
    # Create parser
    parser = argparse.ArgumentParser(description="Script to read and store benchmark data into database")

    # Add params
    parser.add_argument(
        "--medium",
        action="store_true",
        dest="medium",
        default=False,
        help="Run benchmarks with medium sizes",
    )
    parser.add_argument(
        "--iterations",
        action="store",
        type=int,
        dest="iterations",
        default=-1,
        help="Set the number of iterations",
    )
    parser.add_argument(
        "--jvm",
        "-J",
        dest="jvmFlags",
        required=False,
        default="None",
        help='Pass options to the JVM e.g. -J="-Ds0.t0.device=0:1"',
    )

    args = parser.parse_args()

    build_tables(args=args)

    print("Data reading complete.")


def build_tables(args):
    # Run table build
    run_data = build_run_table()
    new_run = Run(**run_data)
    new_run.save()

    print("New Run table saved")

    # Benchmark table build
    benchmark_list = build_benchmark_table_from_profiler(number_of_iterations=args.iterations,
                                                         benchmark_flags=args.jvmFlags)
    benchmark_name_object_dict = {}
    for benchmark_data in benchmark_list:
        new_benchmark = Benchmark(Run=new_run, **benchmark_data)
        new_benchmark.save()

        # Save to dict
        bm_name = new_benchmark.BenchmarkName
        benchmark_name_object_dict[bm_name] = new_benchmark

    # Result tables build
    bm_list = parse_benchmark_file()
    for data in bm_list:
        bm_line = data['line']
        json_blocks = data['json_blocks']

        # if len(json_blocks) < 3:
        #     continue

        # TotalResult table build
        # Look up Benchmark from dict to be the FK
        bm_name = parse_single_benchmark_name(data)
        fk_bm = None
        if bm_name in benchmark_name_object_dict:
            fk_bm = benchmark_name_object_dict[bm_name]
        total_result_data = build_total_results(bm_line=bm_line,
                                                json_blocks=json_blocks)
        new_total_result = TotalResults(Benchmark=fk_bm, **total_result_data)
        new_total_result.save()

        # TaskGraphResults table build
        tg_result_data = build_task_graph_results(bm_line=bm_line,
                                                  json_blocks=json_blocks)
        new_task_graph_result = TaskGraphResults(Result=new_total_result, **tg_result_data)
        new_task_graph_result.save()

        task_result_datas = build_task_results(bm_line=bm_line,
                                               json_blocks=json_blocks)
        for task_result_data in task_result_datas:
            new_task_result = TaskResults(TaskGraphResult=new_task_graph_result, **task_result_data)
            new_task_result.save()


if __name__ == "__main__":
    main()
