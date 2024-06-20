import argparse
import os
import sys

import django
from benchmark_table_builder import build_benchmark_table_from_profiler

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 将项目根目录添加到 Python 的模块搜索路径中
sys.path.append(project_root)

# 设置 DJANGO_SETTINGS_MODULE 环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TVMDataVis.settings')

# 初始化 Django
django.setup()


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
        default=None,
        help='Pass options to the JVM e.g. -J="-Ds0.t0.device=0:1"',
    )

    args = parser.parse_args()

    benchmark_list = build_benchmark_table_from_profiler(number_of_iterations=args.iterations,
                                                          benchmark_flags=args.jvmFlags)
    print("Final benchmark tables: \n", benchmark_list)


if __name__ == "__main__":
    main()
