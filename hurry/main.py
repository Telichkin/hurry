import os
from subprocess import call

from docopt import docopt

from hurry.utils import (
    CommandList,
    ConfigReader,
    ExecChooser
)


def main():
    try:
        config = ConfigReader(os.getcwd()).get_dict()
    except FileNotFoundError:
        print("Can't find hurry.json in the current folder")
        return

    commands = CommandList(prefix="hurry")
    commands.add_config(config)
    arguments = docopt(commands.to_string())
    chooser = ExecChooser(config)
    call(chooser.get_exec(arguments), shell=True)
