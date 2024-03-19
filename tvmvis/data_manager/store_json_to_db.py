import json
import os
from django.conf import settings
from .JSON_reader import read_json_objects, get_file_mod_time
from .insert_data import insert_json_data


def store_json_to_db():
    json_result = read_json_objects(settings.PROFILER_JSON_FILE_PATH)
    last_mod_time = get_file_mod_time(file_path=settings.PROFILER_JSON_FILE_PATH)
    insert_json_data(json_results=json_result, json_time=last_mod_time)
