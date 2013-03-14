import os
import re
import time
import shlex
import subprocess
import sublime
import sublime_plugin

class GenerateCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        self.command = kwargs.get('generate', None)
        self.fill_in = kwargs.get('fill_in', 'Enter the resource name')
        self.accept_fields = kwargs.get('fields', False)
        self.fields_label = kwargs.get('fields_label', 'Enter the fields')

        try:
            # The first folder needs to be the Laravel Project
            self.PROJECT_PATH = self.window.folders()[0]
            self.command_str = 'php %s/artisan generate:%s ' % (self.PROJECT_PATH, self.command)

            if os.path.isfile("%s/artisan" % self.PROJECT_PATH):
                if self.command in ['model', 'seed', 'test', 'view', 'migration', 'resource']:
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
            self.command_str += '%s --fields=' % value
            self.accept_fields = False
            self.window.show_input_panel(self.fields_label, '', self.call_artisan, None, None)
        else:
            self.command_str += '"%s"' % value
            args = shlex.split(str(self.command_str))
            try:
                proc = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
                self.proc_status(proc)
            except IOError:
                sublime.status_message('IOError - command aborted')

    def proc_status(self, proc):
        if proc.poll() is None:
            sublime.set_timeout(lambda: self.proc_status(proc), 200)
        else:
            output = proc.communicate()[0]
            match = re.search(r'/app/\w+/.*[.]php', output)
            if match:
                if not self.command == 'resource':
                    self.window.open_file('%s%s' % (self.PROJECT_PATH, match.group(0)))
                sublime.status_message("%s generated successfully!" % self.command)
            else:
                sublime.status_message("Oh snap! %s failed" % self.command_str)

class ArtisanCommand(sublime_plugin.WindowCommand):
    def run(self, *args, **kwargs):
        self.window.show_input_panel('Enter an artisan command', '', self.call_artisan, None, None)

    def call_artisan(self, command):
        try:
            self.PROJECT_PATH = self.window.folders()[0]
            self.command_str = 'php %s/artisan %s' % (self.PROJECT_PATH, command)

            if command:
                try:
                    args = shlex.split(str(self.command_str))
                    proc = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
            err = proc.communicate()[1].decode('utf-8')
            if not err:
                sublime.status_message('artisan %s executed successfully' % command)
            else:
                new_file = sublime.active_window().new_file()
                new_file.run_command('artisan_error', {'insert': err })
                sublime.status_message('artisan %s failed' % command)

class ArtisanErrorCommand(sublime_plugin.TextCommand):
    def run(self, edit, insert):
        self.view.insert(edit, 0, insert)
