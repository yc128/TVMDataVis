### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yc128/TVMDataVis.git
   cd TVMDataVis

2. **Set Environment**:
   1. Create virtual environment `python -m venv venv`
   2. Activate environment:
      1. macOS and Linux: `source venv/bin/activate`
      2. Windows: `venv\Scripts\activate`
   3. Install Dependencies `pip install -r requirements.txt`
     
3. **Apply database migrations**:
   1. Run `python manage.py migrate` to configure the database 

### Data Manager

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

