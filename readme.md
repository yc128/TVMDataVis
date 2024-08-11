## Documentation
- [User Guide](./README.md)
- [Developer Guide](./docs/DEVELOPER.md)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yc128/TVMDataVis.git
   cd TVMDataVis

2. **Set Environment**:
   1. Create virtual environment `python -m venv venv` in project root directory
   2. Activate environment:
      1. macOS and Linux: `source venv/bin/activate`
      2. Windows: `venv\Scripts\activate`
   3. Install Dependencies `pip install -r requirements.txt`
     
3. **Apply database migrations**:
   1. Run `python manage.py migrate` to configure the database 

## Data Manager

### Profiler Format Requirements
* Each dataset begins with a line starting with `bm=<benchmark_name>`, followed by benchmark-specific details like id, average, median, etc.
* The line is followed by one or more JSON blocks that contain detailed metrics. These JSON blocks provide information about the benchmark, such as compile times, kernel execution times, device information, and other relevant metrics.
* The profiler output typically follows this format when generated using the command:
`tornado-benchmarks.py --<benchmark_size> --profiler console --iterations 2`. This command will output the profiler data, the console_output is in the required format, which can be directed to a file.

**Example**
```
bm=montecarlo-2-512, id=java-reference, average=6.861045e+07, median=6.861045e+07, firstIteration=7.122675e+07, best=6.599415e+07
{
    "benchmark": {
        "TOTAL_GRAAL_COMPILE_TIME": "51106745",
        "TOTAL_BYTE_CODE_GENERATION": "3705366",
        "TOTAL_DRIVER_COMPILE_TIME": "12848027",
        ...
    }
}

```

### Read Profiler using Data_Reader

1. **Set Directories**:
   1. Open the file `/TVMDataVis/settings.py`
   2. Modify the paths:
      1. `PROFILER_JSON_FILE_PATH` for `output_profiler.json`. The profiler's default path is the project root. To change it, set the variable to an absolute path like `Path('/absolute/path/to/profiler_output.json')`
      2. `BENCHMARK_PATH` for `tornado-benchmarks.py`.

2. **Run Script**:
   1. Execute the command: `python tvmvis/data_manager/data_reader_main.py` with the parameters: 
      1. `--iterations`: Number of iterations
      2. `--jvm`: String for jvm flag: Pass options to the JVM e.g. -J="-Ds0.t0.device=0:1"
   2. Wait for the script to complete and look for the output message: `Data reading complete`.


## Clean Database


1. Activate venv in project root directory
2. Run command `python manage.py cleandatabase`


## Run WebUI Server
1. Activate venv in project root directory
2. Run command `python manage.py runserver`
3. Open http://localhost:8000/tvmvis/speedup-chart in browser