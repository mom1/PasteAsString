# -*- coding: utf-8 -*-
# @Author: mom1
# @Date:   2016-10-04 10:39:21
# @Last Modified by:   mom1
# @Last Modified time: 2016-10-04 12:22:42
import re


def make_string(scope, text, len_bef_symbol=0, for_begin=0):
    ret_text = text
    if not ret_text or not scope:
        return ret_text
    m = re.search(r"(\"|“|”|')", scope.get('before_string', '').split('\n')[-1], flags=re.IGNORECASE)
    if m is not None:
        esc = m.group(1)
        reg = r'%s%s' % (scope.get('esc_chr', r''), esc)
        text = re.sub(r'(' + esc + r')', reg, text, flags=re.IGNORECASE)

    text = re.sub(r"\n", scope.get('line_terminator', '') + scope.get('line_start', ''), text, flags=re.IGNORECASE)
    text = re.sub(r"$", scope.get('after_string', ''), text, flags=re.IGNORECASE)

    stext_ident = re.sub(r"\n", r'\n' + ' ' * len_bef_symbol, text, flags=re.IGNORECASE)
    stext_ident_begin = re.sub(r"\n", r'\n' + ' ' * for_begin, scope.get('before_string', ''), flags=re.IGNORECASE)
    ret_text = re.sub(r"^", stext_ident_begin, stext_ident, flags=re.IGNORECASE)
    return ret_text
