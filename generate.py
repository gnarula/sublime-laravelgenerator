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

        try:
            # The first folder needs to be the Laravel Project
            self.PROJECT_PATH = self.window.folders()[0]

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

    def call_artisan(self, resource_name):
        command_str = "php %s/artisan generate:%s %s" % (self.PROJECT_PATH, self.command, resource_name)
        args = shlex.split(str(command_str))
        self.proc = subprocess.Popen(args, shell=False)
        self.proc_status(resource_name)

    def proc_status(self, resource_name):
        if self.proc.poll() is None:
            sublime.set_timeout(lambda: self.proc_status(resource_name), 200)
        else:
            if self.proc.returncode == 0:
                sublime.status_message("%s %s generated!" % (self.command, resource_name))
            else:
                sublime.status_message("%s failed" % command_str)
