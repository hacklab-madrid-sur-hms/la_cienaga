"""
Base classes for writing management commands (named commands which can
be executed through ``manage.py`` ).
"""
import os
import sys
from argparse import ArgumentParser

class CommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.

    If this Exception is raised during the execution of a management
    command, it will be caught and turned into a nicely-printed error
    message to the appropiate output stream; as a result, raising this
    exception (with a sensible description of the error) is the preferred
    way to indicate that something has gone wrong in the execution of a
    command.
    """
    def __init__(self, *args, returncode=1, **kwargs):
        self.returncode = returncode
        super().__init__(*args, **kwargs)

class CommandParser(ArgumentParser):
    """
    Customized ArgumentParser class to improve some error messages and prevent
    SystemExit in several occasions, as SystemExit is unacceptable when a
    command is called programmatically.
    """
    def __init__(self, *, missing_args_message=None, called_from_command_line=None, **kwargs):
        self.missing_args_message = missing_args_message
        self.called_from_command_line = called_from_command_line
        super().__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        # Catch missing argument for a better error message
        if (self.missing_args_message and not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.missing_args_message)
        return super().parse_args(args, namespace)

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error %s" % message)

class BaseCommand(object):
    def __init__(self):
        self.help = ''
        self._called_from_command_line = False

    def create_parser(self, prog_name, subcommand, **kwargs):
        """
        Create and return the ``ArgumentParser`` which will be used
        to parse the arguments to this Command
        """
        parser = CommandParser(
            prog=f'{os.path.basename(prog_name)} {subcommand}',
            description=self.help or None,
            missing_args_message=getattr(self, 'missing_args_message', None),
            called_from_command_line=getattr(self,'_called_from_command_line', None),
            **kwargs
        )

        # Añadimos los genéricos

        self.add_arguments(parser)

        return parser


    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments
        """
        pass

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for this Command,
        derived from usage()
        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])

        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        self.run(*args, **cmd_options)


    def run(self, *args, **options):
        """
        Try to execute this command, performing system checks if needed (as
        controlled by the ``requires_system_checks`` attribute, except if
        force-skipped)
        """
        output = self.handle(*args, **options)

        return output

    def handle(self):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method.')
