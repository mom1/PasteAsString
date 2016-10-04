# -*- coding: utf-8 -*-
# @Author: mom1
# @Date:   2016-09-26 19:59:18
# @Last Modified by:   mom1
# @Last Modified time: 2016-10-04 11:51:13
import sublime
import sublime_plugin
from PasteAsString.tools import make_string

global global_settings


class PasteAsStringCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        global global_settings
        scopes = global_settings.get('scopes', [])
        view = self.view
        sel = view.sel()[0]
        for scope in scopes:
            if scope['scope'] not in view.scope_name(sel.begin()):
                continue
            stext = sublime.get_clipboard()
            if not stext:
                return

            for s in view.sel():
                line = view.line(s.begin())
                for_begin = len(view.substr(sublime.Region(line.begin(), s.begin())))
                len_bef_symbol = for_begin + \
                    len(scope['before_string'].split('\n')[-1]) - len(scope['line_start'])

                if len_bef_symbol < 0:
                    len_bef_symbol = 0

                text_for_paste = make_string(scope, stext, len_bef_symbol, for_begin)
                view.replace(edit, s, text_for_paste)

    def is_visible(self):
        global global_settings
        view = self.view
        sel = view.sel()[0]
        scopes = global_settings.get('scopes', [])
        isvis = False
        for scope in scopes:
            if scope['scope'] in view.scope_name(sel.begin()):
                isvis = True
                break
        return isvis

    def description(self):
        global global_settings
        view = self.view
        sel = view.sel()[0]
        s_descr = 'Paste as String'
        scopes = global_settings.get('scopes', [])
        for scope in scopes:
            if scope['scope'] in view.scope_name(sel.begin()):
                s_descr = scope.get('description', 'Paste as ' + scope['scope'].split('.')[-1])
        return s_descr


def plugin_loaded():
    global global_settings
    global_change = sublime.load_settings('PasteAsString.sublime-settings')
    global_settings = global_change
    global_change.clear_on_change('PasteAsString_settings')
    global_change.add_on_change("PasteAsString_settings", update_settings)


def update_settings():
    global global_settings
    global_settings = sublime.load_settings('PasteAsString.sublime-settings')
