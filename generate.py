import os
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
                print "Artisan not found"
                sublime.status_message("Artisan not found")
        except IndexError:
            print "Please open a Laravel Project"
            sublime.status_message("Please open a Laravel Project")

    def call_artisan(self, value=''):
        if self.accept_fields:
            self.command_str += '%s --fields=' % value
            self.accept_fields = False
            self.window.show_input_panel(self.fields_label, '', self.call_artisan, None, None)
        else:
            self.command_str += '"%s"' % value
            print self.command_str
            args = shlex.split(str(self.command_str))
            proc = subprocess.Popen(args, shell=False)
            self.proc_status(proc)

    def proc_status(self, proc):
        if proc.poll() is None:
            sublime.set_timeout(lambda: self.proc_status(proc), 200)
        else:
            if proc.returncode == 0:
                sublime.status_message("%s generated successfully!" % self.command)
            else:
                sublime.status_message("Oh snap! %s failed" % command_str)
