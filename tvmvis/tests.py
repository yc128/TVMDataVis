import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'tvmvis/data_manager'))
print("Current working directory:", os.getcwd())

from django.test import TestCase
from django.test import TestCase
from tvmvis.data_manager.result_builder import build_total_results, build_task_graph_results, build_task_results




# Create your tests here.
class TotalResultsTests(TestCase):
    def test_build_total_results(self):
        bm_line = "bm=montecarlo-2-512, id=java-reference, average=6.904088e+07, median=6.904088e+07, firstIteration=7.224416e+07, best=6.583760e+07"
        json_blocks = [
            {
                "benchmark": {
                    "TOTAL_GRAAL_COMPILE_TIME": "50931038",
                    "benchmark.montecarlo": {
                        "TASK_KERNEL_TIME": "5087968"
                    }

                }
            },
            {
                "benchmark": {
                    "benchmark.montecarlo": {
                        "TASK_KERNEL_TIME": "5085248"
                    }

                }
            },
            {
                "benchmark": {

                    "benchmark.montecarlo": {
                        "TASK_KERNEL_TIME": "5085248"
                            }
                }
            }
        ]
        expected_result = {
            'TotalAverageTime': 69040880,
            'TotalMedianTime': 69040880,
            'TotalFirstIteration': 72244160,
            'TotalBest': 65837600,
            'TotalMinimum': 5085248,
            'TotalSpeedup': 0  # No speedupAvg in bm_line, so defaults to 0
        }

        total_results = build_total_results(bm_line, json_blocks)
        self.assertEqual(total_results, expected_result)


class TaskGraphResultsTests(TestCase):
    def test_build_task_graph_results(self):
        bm_line = "bm=montecarlo-2-512, id=java-reference"
        json_blocks = [
            {
                "benchmark": {
                    "TOTAL_GRAAL_COMPILE_TIME": "50931038",
                    "TOTAL_DRIVER_COMPILE_TIME": "55941114"
                }
            },
            {
                "benchmark": {
                    "COPY_IN_TIME": "1024",
                    "TOTAL_DISPATCH_DATA_TRANSFERS_TIME": "29728",
                    "TOTAL_DISPATCH_KERNEL_TIME": "3712",
                    "TOTAL_KERNEL_TIME": "5087968"
                }
            },
            {
                "benchmark": {
                    "COPY_IN_TIME": "768",
                    "TOTAL_DISPATCH_DATA_TRANSFERS_TIME": "13568",
                    "TOTAL_DISPATCH_KERNEL_TIME": "3808",
                    "TOTAL_KERNEL_TIME": "5085248"
                }
            }
        ]

        expected_result = {
            'LastKernelTime': 5085248,
            'KernelAverage': 5085248,
            'Copy_IN': 768,
            'Copy_OUT': 0,  # No COPY_OUT_TIME in provided json_blocks
            'Compilation_Graal': 50931038,
            'Compilation_Driver': 55941114,
            'Dispatch_DataTransfers_Time': 13568,
            'Dispatch_Kernel_Time': 3808
        }

        task_graph_results = build_task_graph_results(bm_line, json_blocks)
        self.assertEqual(task_graph_results, expected_result)


class TaskResultsTests(TestCase):
    def test_build_task_results(self):
        bm_line = "bm=montecarlo-2-512, device=0:0"
        json_blocks = [
            {
                "benchmark": {
                    "TOTAL_CODE_GENERATION_TIME": "5723718",
                    "TOTAL_DRIVER_COMPILE_TIME": "55941114",
                    "benchmark.montecarlo": {
                        "DEVICE": "NVIDIA GeForce RTX 4090",
                        "BACKEND": "OPENCL"
                    }
                }
            },
            {
                "benchmark": {
                    "TOTAL_KERNEL_TIME": "5087968",
                    "benchmark.montecarlo": {
                        "DEVICE": "NVIDIA GeForce RTX 4090",
                        "BACKEND": "OPENCL"
                    }
                }
            }
        ]

        expected_results = [
            {
                'HardwareInfo': None,
                'SoftwareInfo': "OPENCL",
                'KernelTime': 0,
                'CodeGenerationTime': 5723718,
                'DriverCompilationTime': 55941114
            },
            {
                'HardwareInfo': None,
                'SoftwareInfo': "OPENCL",
                'KernelTime': 5087968,
                'CodeGenerationTime': 0,
                'DriverCompilationTime': 0
            }
        ]


        task_results = build_task_results(bm_line, json_blocks)
        self.assertEqual(task_results, expected_results)


    def test_build_task_results_with_device(self):
        bm_line_with_device = "bm=montecarlo-2-512, device=0:1  , average=1.147013e+07, median=1.147013e+07, firstIteration=1.335639e+07, best=9.583857e+06, speedupAvg=6.0192, speedupMedian=6.0192, speedupFirstIteration=5.4090, CV=-0.0000%, deviceName= [Intel(R) OpenCL Graphics] -- Intel(R) UHD Graphics 770"
        json_blocks = [
            {
                "benchmark": {
                    "TOTAL_CODE_GENERATION_TIME": "5723718",
                    "TOTAL_DRIVER_COMPILE_TIME": "55941114",
                    "benchmark.montecarlo": {
                        "DEVICE": "NVIDIA GeForce RTX 4090",
                        "BACKEND": "OPENCL"
                    }
                }
            },
            {
                "benchmark": {
                    "TOTAL_KERNEL_TIME": "5087968",
                    "benchmark.montecarlo": {
                        "DEVICE": "NVIDIA GeForce RTX 4090",
                        "BACKEND": "OPENCL"
                    }
                }
            }
        ]

        expected_results_with_device = [
            {
                'HardwareInfo': "[Intel(R) OpenCL Graphics] -- Intel(R) UHD Graphics 770",
                'SoftwareInfo': "OPENCL",
                'KernelTime': 0,
                'CodeGenerationTime': 5723718,
                'DriverCompilationTime': 55941114
            },
            {
                'HardwareInfo': "[Intel(R) OpenCL Graphics] -- Intel(R) UHD Graphics 770",
                'SoftwareInfo': "OPENCL",
                'KernelTime': 5087968,
                'CodeGenerationTime': 0,
                'DriverCompilationTime': 0
            }
        ]

        task_results_with_device = build_task_results(bm_line_with_device, json_blocks)
        self.assertEqual(task_results_with_device, expected_results_with_device)
