import json
import os
from django.conf import settings
from .JSON_reader import read_json_objects
from .insert_data import insert_json_data


def store_json_to_db():
    json_result = read_json_objects(settings.PROFILER_JSON_FILE_PATH)
    insert_json_data(json_result)
