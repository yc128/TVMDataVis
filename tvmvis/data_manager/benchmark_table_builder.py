from profiler_reader import parse_benchmark_file, parse_bm_line
from django.conf import settings
from command_line_io import run_command


def build_benchmark_table(number_of_iterations=-1,
                          benchmark_flags="None", mtmd=-1):


def get_benchmarks_dimensions():
    file_path = settings.BENCHMARK_PATH
    input_command = f"python {file_path} --properties"
    lines = run_command(input_command)


def build_single_benchmark_table(number_of_iterations=-1,
                          benchmark_flags="None", size_type=-1,
                          size_number=-1, dimension=-1, mtmd=-1):
    benchmark = {"BenchmarkName": benchmark_name,
                 "NumberOfIterations": number_of_iterations,
                 "BenchmarkFlags": benchmark_flags,
                 "MTMD": mtmd,
                 "SizeType": size_type,
                 "SizeNumber": size_number,
                 "Dimension": dimension}

    return benchmark


def build_benchmark_name_dict_from_profiler():
    bm_list = parse_benchmark_file()
    bm_dict = {}
    for bm in bm_list:
        benchmark_name = parse_single_benchmark_name(bm)
        if benchmark_name is not None:
            bm_dict.add(benchmark_name)


def parse_single_benchmark_name(bm):
    """
    :param bm: Single element in bm_list parsed from profiler
    :return: benchmark name if exists, else None
    """
    parsed_bm_line = parse_bm_line(bm['line'])
    if 'bm' in parsed_bm_line:
        return parsed_bm_line['bm']
    else:
        return None
