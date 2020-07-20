import re
import operator
from pyaspeller import Word
import pymorphy2

correct_word = {'иксс', 'исит', 'гф', 'вуц', 'ртс', 'цэуби', 'ффп', 'ино'}
layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                           'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                  "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                  'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))


def processing_user_request(word):
    """
    Для передаваймого слова исправляет опечатки и меняет раскладку, если она неправельная
    """
    word = word.translate(layout)
    res = Word(word)
    if not res.correct and word not in correct_word and res.spellsafe is not None:
        return lemmatization(res.spellsafe)
    else:
        return word


def lemmatization(word):
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(word)[0]
    return p.normal_form


def dict_args(args: dict):
    return {key: [value] for key, value in args.items()}
