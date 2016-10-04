# -*- coding: utf-8 -*-
# @Author: mom1
# @Date:   2016-10-04 10:39:21
# @Last Modified by:   MOM
# @Last Modified time: 2016-10-04 22:04:39
import re


def make_string(scope, text, for_begin=0):
    """ Преобразовывает строку text в строку для вставки по правилам из scope

    scope - настройки
            scope['before_string'] - строка добавляемая в начало text.
                Последний не пробельный сивол используется для определения сивола который нужно экранировать
                Последняя строка используется для выстраивания отступов новых строк
            scope['after_string'] - строка добавляемая в конец text
            scope['line_start'] - строка добавляемая в начало каждой новой строки
            scope['line_terminator'] - строка добавляемая вместо конца каждой новой строки
            scope['esc_chr'] - символ экранирования
    text - текст из буфера, который будет преобразован
    for_begin - количество символов перед курсором вставки. Используется для выстраивания отступов новых строк
    """
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

    len_bef_symbol = for_begin + \
        len(scope.get('before_string', '').split('\n')[-1]) - len(scope.get('line_start', ''))
    if len_bef_symbol < 0:
        len_bef_symbol = 0

    stext_ident = re.sub(r"\n", r'\n' + ' ' * len_bef_symbol, text, flags=re.IGNORECASE)
    stext_ident_begin = re.sub(r"\n", r'\n' + ' ' * for_begin, scope.get('before_string', ''), flags=re.IGNORECASE)
    ret_text = re.sub(r"^", stext_ident_begin, stext_ident, flags=re.IGNORECASE)
    return ret_text
