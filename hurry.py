import os
import sys
import json
import subprocess

def generate_exec_str(conf):
    ''' Generate executable string based on config and sys.argv

    Arguments of `hurry` consist of static and dynamic parts which are separated by "--" symbol:
        
      $ hurry up service -- --timeout=10000
             └─[static]─┘  └───[dynamic]───┘

    When static part is the same as a command from the config, function returns appropriate 
    executable string. Dynamic part is appended to the end of the executable string as is:

      $ cat ./hurry.json   
      $ { "up service": "docker-compose -f ./composes/service up -d" }
          └─[command]─┘  └────────────[executable string]───────────┘
      
      $ hurry up service -- --timeout=10000
      $ Execute: docker-compose -f ./composes/service up -d --timeout=10000
                 └───────────[executable string]──────────┘ └──[dynamic]──┘
    
    Command can contain variables, which should be inserted into appropriate place
    inside executable string:

      $ cat ./hurry.json
      $ { "up <sname>": "docker-compose -f ./composes/<sname> up -d" }
             └─[var]─┘                               └─[var]─┘
      
      $ hurry up auth ─────────────────────────┐
                                               V
      $ Execute: docker-compose -f ./composes/auth up -d

    If function can't find suitable command for givent static part, it returns `None`
    '''
    # Divide arguments into static and dynamic parts
    static, dynamic = [], []
    for arg in sys.argv[1:]:
        if (len(dynamic) > 0):
            dynamic.append(arg)
        elif (arg == '--'):
            # Empty string as the first item of dynamic part helps us 
            # decide in what part of argv we are right now. When dynamic
            # part is empty we are still in the static part of sys.argv,
            # otherwise we are in the dynamic part
            dynamic.append('')
        else:
            static.append(arg)

    # Find suitable command for given static part
    for command, exec_str in conf.items():
        command = command.split()

        if len(command) != len(static):
            continue
                                                         # +---------+--------+------------------------+
        is_suitable, variables = True, {}                # | command | static |         action         |
        for cm, st in zip(command, static):              # +---------+--------+------------------------+
            if cm.startswith('<') and cm.endswith('>'):  # |   up    |   up   |     continue loop      |         
                variables[cm] = st                       # +---------+--------+------------------------+           
            elif cm != st:                               # | <name>  | logger |     save veriable      |
                is_suitable = False                      # |         |        | { "<name>": "logger" } |
                break                                    # +---------+--------+------------------------+
                                                         # |  quite  |  loud  |  not suitable, break   |
        # Replace variable in executable string          # +---------+--------+------------------------+
        # and add dynamic part if needed
        if is_suitable:
            for name, value in variables.items():
                exec_str = exec_str.replace(name, value)
            if len(dynamic) > 1:
                exec_str += ' '.join(dynamic)
            return exec_str

def main():
    # Read json config from the "hurry.json" file in the current dir
    conf_path = os.path.join(os.getcwd(), 'hurry.json')
    try:
        with open(conf_path) as c:
            conf = json.load(c)
    except FileNotFoundError:
        print("Can't find hurry.json in the current folder")
        return

    exec_str = generate_exec_str(conf)
    if exec_str:
        print("Execute: " + exec_str)
        subprocess.call(exec_str, shell=True)
    else:
        help_str = 'Usage:'
        for cmd_template in conf:
            help_str += ('\n    hurry ' + cmd_template)
        print(help_str)
