import json
import os
from django.conf import settings
from .JSON_reader import read_profiler_json_objects, get_file_mod_time, read_json_file
from .insert_data import insert_json_data


# def store_json_to_db():
#     profile_json_result = read_profiler_json_objects(settings.PROFILER_JSON_FILE_PATH)
#     versions_json_result = read_json_file(settings.VERSIONS_JSON_FILE_PATH)
#     last_mod_time = get_file_mod_time(file_path=settings.PROFILER_JSON_FILE_PATH)
#     insert_json_data(profiler_json_results=profile_json_result, json_time=last_mod_time,
#                      versions_json_result=versions_json_result)
