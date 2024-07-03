# Data Manager
## Instructions

### Set Environment
1. Create virtual environment `python -m venv venv`
2. Activate environment:
   1. macOS and Linux: `source venv/bin/activate`
   2. Windows: `venv\Scripts\activate`
3. Install Dependencies `pip install -r requirements.txt`

### Set Directories
1. Open the file `/TVMDataVis/settings.py`
2. Modify the paths for `output_profiler.json` and `tornado-benchmarks.py` as needed.


### Launch Virtual Environment
1. In the root directory, run the command: `source venv/bin/activate`.

### Run Script
1. Execute the command: `python tvmvis/data_manager/data_reader_main.py` with the parameters: --iterations, --jvm.
2. Wait for the script to complete and look for the output message: `Data reading complete`.

