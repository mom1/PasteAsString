import re
import sublime
import sublime_plugin

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

            stext = re.sub(r"\n", scope['line_terminator'] + scope['line_start'], stext, flags=re.IGNORECASE)
            stext = re.sub(r"$", scope['after_string'], stext, flags=re.IGNORECASE)
            for s in view.sel():
                line = view.line(s.begin())
                for_begin = len(view.substr(sublime.Region(line.begin(), s.begin())))
                len_bef_symbol = for_begin + \
                    len(scope['before_string'].split('\n')[-1]) - len(scope['line_start'])

                if len_bef_symbol < 0:
                    len_bef_symbol = 0

                stext_ident = re.sub(r"\n", r'\n' + ' ' * len_bef_symbol, stext, flags=re.IGNORECASE)
                stext_ident_begin = re.sub(r"\n", r'\n' + ' ' * for_begin, scope['before_string'], flags=re.IGNORECASE)
                stext_ident = re.sub(r"^", stext_ident_begin, stext_ident, flags=re.IGNORECASE)
                view.replace(edit, s, stext_ident)

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
        # 'Вставить как строку'
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
