import os
import json
from subprocess import check_output
from collections import OrderedDict

import pytest

from hurry import main
from hurry.utils import (
    CommandList,
    ExecChooser,
    ConfigReader
)


def test_create_doc():
    commands = CommandList(prefix="hurry")
    commands.add_command("up")
    assert commands.to_string() == "Usage:\n" \
                                   "    hurry up"


def test_create_doc_with_variable():
    commands = CommandList(prefix="hurry")
    commands.add_command("test <path>")
    assert commands.to_string() == "Usage:\n" \
                                   "    hurry test <path>"


def test_create_doc_with_two_commands():
    commands = CommandList(prefix="faster")
    commands.add_command("up")
    commands.add_command("test <test-name>")
    assert commands.to_string() == "Usage:\n" \
                                   "    faster up\n" \
                                   "    faster test <test-name>"


def test_create_doc_from_dict():
    config = OrderedDict()
    config["up <param>"] = "any shell command"
    config["down"] = "other shell command"
    commands = CommandList(prefix="conf")
    commands.add_config(config)
    assert commands.to_string() == "Usage:\n" \
                                   "    conf up <param>\n" \
                                   "    conf down"


def test_choose_execution():
    config = {
        "up": "any shell command",
        "down": "other command"
    }
    parsed_arguments = {
        "up": True,
        "down": False
    }
    chooser = ExecChooser(config=config)
    assert chooser.get_exec(parsed_arguments) == "any shell command"


def test_choose_execution_with_variable():
    config = {
        "up <var>": "this is var: <var>"
    }
    parsed_arguments = {
        "up": True,
        "<var>": "foo bar"
    }
    chooser = ExecChooser(config=config)
    assert chooser.get_exec(parsed_arguments) == "this is var: foo bar"


@pytest.fixture()
def create_hurry_json():
    path_to_file = os.path.join(os.path.dirname(__file__), "hurry.json")

    def creator(dictionary):
        with open(path_to_file, "w+") as hurry_json:
            json.dump(dictionary, hurry_json)

    yield creator
    os.remove(path_to_file)


def test_config_reader(create_hurry_json):
    create_hurry_json({"cmd": "some exec"})
    reader = ConfigReader(os.path.dirname(__file__))
    assert reader.get_dict() == {"cmd": "some exec"}


def test_config_reader_non_existing_file():
    try:
        ConfigReader(os.path.dirname(__file__)).get_dict()
        assert False, "FileNotFoundError did not rise"
    except FileNotFoundError:
        assert True


def test_run_main(create_hurry_json, tmpdir):
    os.chdir(os.path.dirname(__file__))
    create_hurry_json({"write <file_path>": "echo \"this is e2e test\" > <file_path>"})

    test_file = tmpdir.join("test.txt")
    stdout = execute("hurry write {}".format(test_file))

    assert stdout.decode().strip() == "Execute: echo \"this is e2e test\" > {}".format(test_file)
    assert test_file.read().strip() == "this is e2e test"


def test_run_main_without_hurry_json():
    os.chdir(os.path.dirname(__file__))
    stdout = execute("hurry")
    assert stdout.decode().strip() == "Can't find hurry.json in the current folder"


def execute(command):
    return check_output("PYTHONPATH=.. python ../bin/{cmd}".format(cmd=command), shell=True)
