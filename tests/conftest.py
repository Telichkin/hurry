import json

import os
import pytest


@pytest.fixture(autouse=True)
def change_dir():
    os.chdir(os.path.dirname(__file__))


@pytest.fixture()
def create_hurry_json():
    path_to_file = os.path.join(os.path.dirname(__file__), "hurry.json")

    def creator(dictionary):
        with open(path_to_file, "w+") as hurry_json:
            json.dump(dictionary, hurry_json)

    yield creator
    os.remove(path_to_file)
