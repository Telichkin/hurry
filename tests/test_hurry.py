import os
import sys
import subprocess
from collections import OrderedDict

import pytest

import hurry

def test_run_hurry_e2e(create_hurry_json, tmpdir):
    create_hurry_json({
        "write <file_path>": "echo 'this is e2e test' > <file_path>",
        "read <file_path>": "cat <file_path>",
    })
    test_file = tmpdir.join("test.txt")

    stdout = execute("hurry write " + str(test_file))

    assert stdout.decode().strip() == "Execute: echo 'this is e2e test' > " + str(test_file)
    assert test_file.read().strip() == "this is e2e test"

    stdout = execute('hurry read some/path')

    assert stdout.decode().strip() == 'Execute: cat some/path'


def execute(command):
    return subprocess.check_output("PYTHONPATH=.. python ../bin/{cmd}".format(cmd=command), shell=True)


def test_run_hurry_without_hurry_json(capsys):
    hurry.main()

    stdout, _stderr = capsys.readouterr()
    assert stdout.strip() == "Can't find hurry.json in the current folder"


@pytest.mark.parametrize("content", ("\"-p wow! first with dash!\"", "\"first without dash\""))
def test_run_hurry_with_many_args(create_hurry_json, tmpdir, content):
    create_hurry_json({"write <file_path> <content>": "echo \"<content>\" > <file_path>"})
    test_file = tmpdir.join("test.txt")
    sys.argv[1:] = ["write", str(test_file), content]

    hurry.main()
    assert test_file.read().strip() == content.strip("\"")
