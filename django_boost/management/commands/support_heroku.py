import sys
from os import path
from platform import python_version
try:
    from pip._internal.commands import freeze
except ImportError:
    try:
        from pip._internal.operations import freeze
    except ImportError:  # pip < 10.0
        from pip.operations import freeze

from django.conf import settings
from django.core.management.base import BaseCommand


def _make_all(runtime, prockfile, requirments, **_):
    return not any([runtime, prockfile, requirments])


class Command(BaseCommand):
    help = "Create a configuration file for heroku"
    PROCFILE = "Procfile"
    PROCFILE_FORMAT = "web: gunicorn %s\n"
    RUNTIME = "runtime.txt"
    RUNTIME_FORMAT = "python-%s\n"
    REQUIREMENTS = "requirements.txt"

    GUNICORN = 'gunicorn'

    def add_arguments(self, parser):
        parser.add_argument('--overwrite', action='store_true')
        parser.add_argument('--no-gunicorn', action='store_true')
        parser.add_argument('--runtime', action='store_true')
        parser.add_argument('--prockfile', action='store_true')
        parser.add_argument('--requirments', action='store_true')
        parser.add_argument('-q', '--quit', action='store_true')

    def handle(self, *args, **options):
        EXEC_PATH = sys.argv[0]
        ROOT_DIR = path.dirname(path.abspath(EXEC_PATH))
        make_all = _make_all(**options)
        if make_all or options['prockfile']:
            PROCFILE_PATH = path.join(ROOT_DIR, self.PROCFILE)
            self.make_prockfile(PROCFILE_PATH, **options)
        if make_all or options['runtime']:
            RUNTIME_PATH = path.join(ROOT_DIR, self.RUNTIME)
            self.make_runtime(RUNTIME_PATH, **options)
        if make_all or options['requirments']:
            REQUIREMENTS_PATH = path.join(ROOT_DIR, self.REQUIREMENTS)
            self.make_requirments(REQUIREMENTS_PATH, **options)

    def _print_generated_path(self, path, quit, **options):
        if not quit:
            self.stdout.write("Generated : " + path)

    def make_runtime(self, fpath, **options):
        if not path.exists(fpath) or options['overwrite']:
            with open(fpath, "w") as f:
                f.write(self.RUNTIME_FORMAT % python_version())
            self._print_generated_path(fpath, **options)

    def make_prockfile(self, fpath, **options):
        wsgi = ".".join(settings.WSGI_APPLICATION.split(".")[:-1])
        if not path.exists(fpath) or options['overwrite']:
            with open(fpath, "w") as f:
                f.write(self.PROCFILE_FORMAT % wsgi)
            self._print_generated_path(fpath, **options)

    def make_requirments(self, fpath, no_gunicorn, **options):
        gunicorn_exist = False
        if not path.exists(fpath) or options['overwrite']:
            with open(fpath, "w") as f:
                for i in freeze.freeze():
                    if i.startswith(self.GUNICORN):
                        gunicorn_exist = True
                    f.write(i)
                    f.write('\n')
                if not gunicorn_exist and not no_gunicorn:
                    f.write(self.GUNICORN)
            self._print_generated_path(fpath, **options)
