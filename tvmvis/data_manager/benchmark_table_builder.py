from profiler_reader import parse_benchmark_file, parse_bm_line
from django.conf import settings
from command_line_io import run_command

# ========================================================================================
# Dimensions
# ========================================================================================
__DIMENSIONS__ = {
    "saxpy": "1",
    "addImage": "2",
    "stencil": "1",
    "convolvearray": "2",
    "convolveimage": "2",
    "blackscholes": "1",
    "montecarlo": "1",
    "blurFilter": "2",
    "renderTrack": "2",
    "euler": "2",
    "nbody": "1",
    "sgemm": "2",
    "dgemm": "2",
    "mandelbrot": "2",
    "dft": "1",
    "juliaset": "2"
}


# ========================================================================================


def build_benchmark_table_from_profiler(number_of_iterations=-1,
                                        benchmark_flags="None", mtmd=-1):
    """
    Using result in profiler file to build benchmark tables
    Suitable for bm name in format like: "montecarlo-2-512"
    :param number_of_iterations:
    :param benchmark_flags:
    :param mtmd:
    :return: benchmark list, each element is a benchmark table in dict format
    """
    benchmark_list = []
    dim_dict = get_benchmarks_dimensions()
    bm_set = build_benchmark_name_set_from_profiler()

    for bm in bm_set:
        print(bm)
        size_type = 0
        bm_arr = bm.split('-')
        size = -1
        bm_name_short = "None"
        dims = -1
        if len(bm_arr) > 2:
            size = bm_arr[2]
            bm_name_short = bm_arr[0]
            if bm_name_short in dim_dict:
                dims = dim_dict[bm_name_short]
            else:
                print("cannot find dims for :", bm_name_short, " , set it to -1.")
        benchmark = build_single_benchmark_table(number_of_iterations=number_of_iterations,
                                                 benchmark_name=bm, benchmark_flags=benchmark_flags,
                                                 size_type=size_type, size_number=size,
                                                 dimension=dims)
        benchmark_list.append(benchmark)

    return benchmark_list


def get_benchmarks_dimensions():
    file_path = settings.BENCHMARK_PATH
    input_command = f"python {file_path} --properties"
    lines = run_command(input_command).splitlines()
    benchmark_dim_dict = {}
    for line in lines:
        arr = line.split(',')
        if len(arr) < 3:
            print("Error when handling part of --properties output")
            continue
        bm_name = arr[0]
        dim = -1
        if 'dims' in arr[1]:
            dim = arr[1].split('=')[1]
        benchmark_dim_dict[bm_name] = dim

    if len(benchmark_dim_dict) == 0:
        print("Cannot read dim from --properties output, using internal dim info")
        benchmark_dim_dict = __DIMENSIONS__

    return benchmark_dim_dict


def build_single_benchmark_table(number_of_iterations=-1, benchmark_name="None",
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


def build_benchmark_name_set_from_profiler():
    bm_list = parse_benchmark_file()
    bm_set = set()
    for bm in bm_list:
        benchmark_name = parse_single_benchmark_name(bm)
        if benchmark_name is not None:
            bm_set.add(benchmark_name)

    return bm_set


def parse_single_benchmark_name(bm):
    """
    :param bm: Single element in bm_list parsed from profiler,
    which should include line and json blocks
    :return: benchmark name if exists, else None
    """
    parsed_bm_line = parse_bm_line(bm['line'])
    if 'bm' in parsed_bm_line:
        return parsed_bm_line['bm']
    else:
        return None
