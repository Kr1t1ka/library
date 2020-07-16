import re
from itertools import groupby

from api_v1.main.endpoints.replace.db import Replace


def text_replace(filling_obj):
    all_text = ''

    for obj in filling_obj:
        all_text += obj.text

    names_arr = [el for el, _ in groupby(changing_array(re.findall('{\w+}', all_text)))]
    replace_arr = Replace.query.filter(Replace.name.in_(names_arr)).all()
    replace_obj = {replace.name: replace.value for replace in replace_arr}

    for obj in filling_obj:
        obj.text = obj.text.format(**replace_obj)

    return filling_obj


def changing_array(array):
    res = []
    for i in range(len(array)):
        res.append(array[i][1:-1])
    return res


"""def text_replace(filling_obj):

    for obj in filling_obj:
        names_arr = changing_array(re.findall('{\w+}', obj.text))
        replace_arr = Replace.query.filter(Replace.name.in_(names_arr)).all()
        replace_obj = {replace.name: replace.value for replace in replace_arr}
        obj.text = obj.text.format(**replace_obj)

    return filling_obj"""
