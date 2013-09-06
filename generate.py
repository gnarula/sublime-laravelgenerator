import os
import re
import time
import shlex
import subprocess
import sublime
import sublime_plugin

class GenerateCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(GenerateCommand, self).__init__(*args, **kwargs)

        settings = sublime.load_settings('laravelgenerator.sublime-settings')
        self.php_path = settings.get('php_path', 'php')

    def run(self, *args, **kwargs):
        self.command = kwargs.get('generate', None)
        self.fill_in = kwargs.get('fill_in', 'Enter the resource name')
        self.accept_fields = kwargs.get('fields', False)
        self.fields_label = kwargs.get('fields_label', 'Enter the fields')
        self.accept_path = kwargs.get('path', False)
        self.path_label = kwargs.get('path_label', 'Enter the path')

        try:
            # The first folder needs to be the Laravel Project
            self.PROJECT_PATH = self.window.folders()[0]
            self.args = [self.php_path, os.path.join(self.PROJECT_PATH, 'artisan'), 'generate:%s' % self.command]

            if os.path.isfile("%s" % os.path.join(self.PROJECT_PATH, 'artisan')):
                if self.command in ['model', 'seed', 'test', 'view', 'migration', 'resource', 'scaffold']:
                    # call function to do the work
                    self.window.show_input_panel(self.fill_in, '', self.call_artisan, None, None)
                else:
                    sublime.status_message("Generator command not supported")
            else:
                sublime.status_message("Artisan not found")
        except IndexError:
            sublime.status_message("Please open a Laravel Project")

    def call_artisan(self, value=''):
        if self.accept_fields:
            self.args.extend([value, '--fields='])
            self.accept_fields = False
            self.window.show_input_panel(self.fields_label, '', self.call_artisan, None, None)
        elif self.accept_path and self.command == 'view':
            self.args.extend([value, '--path=%s' % os.path.join(self.PROJECT_PATH, 'app/views/')])
            self.accept_path = False
            self.window.show_input_panel(self.path_label, '', self.call_artisan, None, None)
        else:
            if self.args[-1] == '--fields=':
                self.args[-1] += '%s' % value
            elif self.args[-1] == '--path=%s' % os.path.join(self.PROJECT_PATH, 'app/views/'):
                self.args[-1] += '%s' % value
            else:
                self.args.append(value)
            if os.name != 'posix':
                self.args = subprocess.list2cmdline(self.args)
            try:
                proc = subprocess.Popen(self.args, cwd=self.PROJECT_PATH, shell=False, stdout=subprocess.PIPE)
                self.proc_status(proc)
            except IOError:
                sublime.status_message('IOError - command aborted')

    def proc_status(self, proc):
        if proc.poll() is None:
            sublime.set_timeout(lambda: self.proc_status(proc), 200)
        else:
            output = proc.communicate()[0].decode('utf-8')
            match = re.search(r'/app/\w+/.*[.]php', output)
            if match:
                if not self.command == 'resource':
                    self.window.open_file('%s%s' % (self.PROJECT_PATH, match.group(0)))
                sublime.status_message("%s generated successfully!" % self.command)
            else:
                sublime.status_message("Oh snap! generate:%s failed - %s" % (self.command, output))

class ArtisanCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(ArtisanCommand, self).__init__(*args, **kwargs)

        settings = sublime.load_settings('laravelgenerator.sublime-settings')
        self.php_path = settings.get('php_path', 'php')

    def run(self, *args, **kwargs):
        self.window.show_input_panel('Enter an artisan command', '', self.call_artisan, None, None)

    def call_artisan(self, command):
        try:
            self.PROJECT_PATH = self.window.folders()[0]
            self.args = '%s %s %s' % (self.php_path, os.path.join(self.PROJECT_PATH, 'artisan'), command)
            if os.name == 'posix':
                self.args = shlex.split(str(self.args))

            if command:
                try:
                    proc = subprocess.Popen(self.args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.proc_status(proc, command)
                except IOError:
                    sublime.status_message('IOError - command aborted')
            else:
                sublime.status_message('Command not set')
        except IndexError:
            sublime.status_message('Please open a Laravel Project')

    def proc_status(self, proc, command):
        if proc.poll() is None:
            sublime.set_timeout(lambda: self.proc_status(proc, command), 200)
        else:
            result = [x.decode('utf-8') for x in proc.communicate()]
            panel_name = 'artisan_output'
            panel = self.window.get_output_panel(panel_name)
            if not result[1]:
                if command == 'routes':
                    panel.run_command('artisan_output', {'insert': result[0]})
                    self.window.run_command('show_panel', {'panel': 'output.' + panel_name})
                sublime.status_message('artisan %s executed successfully' % command)
            else:
                panel.run_command('artisan_output', {'insert': result[1]})
                self.window.run_command('show_panel', {'panel': 'output.' + panel_name})
                sublime.status_message('artisan %s failed' % command)

class ArtisanOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit, insert):
        self.view.insert(edit, 0, insert)
