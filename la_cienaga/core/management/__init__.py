import sys
import os
import pkgutil
import functools
from importlib import import_module
from la_cienaga.core.management.base import (
        CommandError, CommandParser
)

def find_commands(management_dir):
    """
    Given a path to a management directory, return a list of all the command
    names that are available
    """
    command_dir = os.path.join(management_dir, 'commands')

    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]

def load_command_class(name):
    """
    Given a command name and a application name, return the Command class
    instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = import_module('la_cienaga.core.management.commands.%s' % name)
    return module.Command()

@functools.lru_cache(maxsize=None)
def get_commands():
    """
    Return a dictionary mapping command names to their callback applications.
    """
    commands = find_commands(os.path.dirname(os.path.abspath(__file__)))

    return commands

class Management(object):
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def main_help_text(self, commands_only=False):
        """TODO: Docstring for main_help_text.
        :returns: TODO

        """
        if commands_only:
            usage = sorted(get_commands)
        else:
            usage = [
                "",
                "Type '%s help <subcommand>' for help in a specific subcommand" % self.prog_name,
                "",
                "Available subcommands:",
            ]

        for name in sorted(get_commands()):
            usage.append(name)

        return '\n'.join(usage)

    def fetch_command(self, subcommand):
        """
        Try to fetch the given subcommand, printing a message with the
        appropiate command called from the command line if it
        can't be done.
        """
        klass = None
        commands = get_commands()
        if subcommand in commands:
            klass = load_command_class(subcommand)

        return klass

    def run(self):
        """
        Given the command-line arguments, figure out which subcommand is being
        run, create a parser appropiate to that command, and run it.
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help' # Display help if no arguments are given.

        ###
        parser = CommandParser(
            prog = self.prog_name,
            usage='%(prog)s subcommand [options] [args]',
            add_help=False,
            allow_abbrev=False,
        )
        parser.add_argument('args', nargs='*')
        try:
            options, args = parser.parse_known_args(self.argv[2:])
        except CommandError:
            pass
        if subcommand == 'help':
            if not options.args:
                sys.stdout.write(self.main_help_text() + '\n')
            else:
                self.fetch_command(options.args[0]).print_help(self.prog_name, options.args[0])
        else:
            subcmd = self.fetch_command(subcommand)
            if subcmd is not None:
                subcmd.run_from_argv(self.argv)
            else:
                sys.stdout.write(self.main_help_text() + '\n')


def execute_from_commandline(argv=None):
    """
    Run Management
    """
    management = Management(argv)
    management.run()
