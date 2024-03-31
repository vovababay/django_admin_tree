# coding=utf-8
import importlib
import re

from django.core.management import BaseCommand


class Command(BaseCommand):

    help = 'Выполняет функцию run_script() в файле, указанном в аргументах. Предпологается, что этот файл будет ' \
           'лежать в папке scripts/'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)
        parser.add_argument('--script-args', nargs='*', type=str)

    def handle(self, *args, **options):
        if not options.get('file_name'):
            self.stderr.write('Не правильно указано название скрипта')
            return

        file_name = options.get('file_name')
        file_name = re.sub(r'\.py$', '', file_name)
        module_name = 'scripts.' + file_name
        self.stdout.write('Импортируем модуль: {}'.format(module_name))
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            self.stderr.write('Модуль {} не найден'.format(module_name))
            return

        if not hasattr(module, 'run_script'):
            self.stderr.write('В модуле {} не найдена функция run_script()'.format(module_name))
            return

        params = [self.stdout, self.stderr]
        if options.get('script_args'):
            params.append(options['script_args'])

        module.run_script(*params)
        self.stdout.write('Скрипт успешно отработал')