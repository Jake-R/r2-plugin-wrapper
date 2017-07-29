from __future__ import print_function
from builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)
from future.utils import iteritems
import r2lang
import IPython
import json
import traceback
import base64

commands = {}


class Command(object):
    """Defines a radare2 command"""

    def __init__(self, cmd, desc, func, print_func=None, quiet_func=None, json_func=None, help_func=None):
        self.cmd = cmd
        self.desc = desc
        if func:
            self.func = func
        if print_func:
            self.print_func = print_func
        if quiet_func:
            self.quiet_func = quiet_func
        if json_func:
            self.json_func = json_func
        if help_func:
            self.help_func = help_func

    def func(self, string):
        """
        defines the behaviour of the r2 command
        :param string: contains all arguments that were specified after the command
        :return: a list of dictionaries representing the results of the command
        """
        return [{}]

    def print_result(self, result, quiet=False, json=False):
        """
        determines which function to use when printing result of command
        :param result: result of command
        :param quiet: use quiet function
        :param json: use json function (preempts quiet function)
        """
        if json:
            return self.json_func(result)
        elif quiet:
            return self.quiet_func(result)
        else:
            return self.print_func(result)

    def print_func(self, result, quiet=False):
        """
        prints the standard output format
        :param result: result of the command
        :param quiet: print only values
        """
        fmt_string = '{1}' if quiet else '{0}={1}'
        line_list = []
        for line in result:
            line = {key: (hex(value) if isinstance(value, int) else value) for key, value in iteritems(line)}
            line_list.append(' '.join([fmt_string.format(key, value) for key, value in iteritems(line)]))
        return '\n'.join(line_list) + '\n'

    def quiet_func(self, result):
        """
        prints the quiet output format
        :param result: 
        """
        return self.print_func(result, quiet=True)

    def json_func(self, result):
        """
        prints the json output format
        :param result: 
        """
        return json.dumps(result) + '\n'

    def help_func(self):
        """
        prints the help string for the command
        """
        print("{0}: {1}".format(self.cmd, self.desc))


def print_help(cmd):
    matches = [value for key, value in iteritems(commands) if key.startswith(cmd)]
    if not matches:
        return 0
    for match in matches:
        match.help_func()
    return 1


def plugify(cmd, desc):
    """
    decorator to turn a function into a Command object
    """

    def wrap(f):
        commands[cmd] = Command(cmd, desc, f)
        return f

    return wrap


def add_cmd(command):
    """
    add a Command object to the plugin
    """
    commands[command.cmd] = command


def plug(a):
    def call(string):
        try:
            json_output = False
            quiet_output = False
            lst = string.split(' ', 1)
            cmd = lst[0] if lst[:1] else ''
            rest = lst[1] if lst[1:] else ''
            if cmd.endswith('?') and len(cmd) > 1:
                return print_help(cmd[:-1])
            elif cmd.endswith('j'):
                cmd = cmd[:-1]
                json_output = True
            elif cmd.endswith('q'):
                cmd = cmd[:-1]
                quiet_output = True
            command = commands.get(cmd, None)
            if not command:
                return print_help(cmd)
            result = command.func(rest)
            return command.print_result(result, quiet_output, json_output)

        except Exception as e:
            traceback.print_exc()
        return 0

    return {
        'name': 'plug',
        'desc': 'asdf',
        'license': 'asdf',
        'call': call
    }



print(r2lang.plugin("core", plug))
