import os
import json
import subprocess

from docopt import docopt


def main():
    # Read json config from the "hurry.json" file in the current dir
    conf_path = os.path.join(os.getcwd(), 'hurry.json')
    try:
        with open(conf_path) as c:
            conf = json.load(c)
    except FileNotFoundError:
        print("Can't find hurry.json in the current folder")
        return

    # Transform read json into valid docopt string
    docopt_str = 'Usage:'
    for cmd in conf:
        docopt_str += ('\n    hurry ' + cmd)
    
    # Transform current command-line arguments into docopt format
    args = docopt(docopt_str, options_first=True)

    exec_str = compose_exec_str(conf, args)
    print("Execute: " + exec_str)
    subprocess.call(exec_str, shell=True)


def compose_exec_str(conf, parsed_args):
    enabled_args = {k: v for k, v in parsed_args.items() if v}

    for k in conf:
        if set(k.split()) == set(enabled_args.keys()):
            exec_str = conf[k]
            for arg, v in enabled_args.items():
                if not isinstance(v, bool):
                    exec_str = exec_str.replace(arg, v)
            return exec_str
