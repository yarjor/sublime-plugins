import sys
sys.path.insert(0, r'C:\Python27\Lib\site-packages')

import sublime
import sublime_plugin
from jedi import Script

def clean_list(lst: list) -> list:
    new_list = []
    for i in lst:
        if i not in new_list:
            new_list.append(i)
    return new_list

class ComfyLayoutCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        self.window.set_layout({
            'cols'  : [0.0, 0.5, 1.0],
            'rows'  : [0.0, 0.5, 1.0],
            'cells' : [
                        [0, 0, 1, 2],
                        [1, 0, 2, 1],
                        [1, 1, 2, 2]
                      ]
            })
        

class CloneToOtherViewCommand(sublime_plugin.WindowCommand):
    def run(self) -> None:
        self.window.set_layout({
            'cols'  : [0.0, 0.5, 1.0],
            'rows'  : [0.0, 1.0],
            'cells' : [
                        [0, 0, 1, 1],
                        [1, 0, 2, 1]
                      ]
            })
        self.window.run_command('clone_file')
        self.window.run_command('move_to_group', {'group' : 1})


class ShowDocCommand(sublime_plugin.TextCommand):
    def run(self, edit) -> None:
        try:
            loc = self.view.sel()[0].end()
            row, col = self.view.rowcol(loc)
            script = Script(source=(self.view.substr(sublime.Region(0, self.view.size()))), line=(row + 1), column=col, path=self.view.file_name())
            definitions = script.goto_definitions()
            if definitions:
                doc = definitions[-1].doc or 'No docstring found'
                self.view.show_popup(doc.replace('\n', '<br>'))
            else:
                self.view.show_popup('No docstring found')
        except Exception:
            self.view.show_popup('No docstring found')
            raise

class ShowDirCommand(sublime_plugin.TextCommand):
    def run(self, edit) -> None:
        try:
            loc = self.view.sel()[0].end()
            row, col = self.view.rowcol(loc)
            script = Script(source=(self.view.substr(sublime.Region(0, self.view.size()))), line=(row + 1), column=col, path=self.view.file_name())
            definitions = script.goto_definitions()
            if definitions:
                def_dir = definitions[0].defined_names()
                pop_contents = '<br>'.join(clean_list([i.description for i in def_dir])) or 'No dir found'
                self.view.show_popup(pop_contents)
            else:
                self.view.show_popup('No dir found')
        except Exception:
            self.view.show_popup('No dir found')
            raise

class ShowParamsCommand(sublime_plugin.TextCommand):
    def run(self, edit) -> None:
        try: 
            loc = self.view.sel()[0].end()
            row, col = self.view.rowcol(loc)
            script = Script(source=(self.view.substr(sublime.Region(0, self.view.size()))), line=(row + 1), column=col, path=self.view.file_name())
            definitions = script.goto_definitions()
            if definitions:
                try:
                    params = definitions[0].params
                    status_line = ', '.join([i.description for i in params]) or 'No params available'
                    self.view.window().status_message(status_line)
                except Exception:
                    self.view.window().status_message('No params available')
                    raise
            else:
                self.view.window().status_message('No params available')
        except Exception:
            self.view.window().status_message('No params available')
            raise
