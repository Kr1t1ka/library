import re
from itertools import chain

from api_v1.main.endpoints.replace.db import Replace


def text_replace(filling_obj):
    all_text = ''

    for obj in filling_obj:
        all_text += obj.text

    names_arr = changing_array(set(chain(re.findall('{\w+}', all_text))))
    replace_arr = Replace.query.filter(Replace.name.in_(names_arr)).all()
    replace_obj = {replace.name: replace.value for replace in replace_arr}

    for obj in filling_obj:
        obj.text = obj.text.format(**replace_obj)

    return filling_obj


def changing_array(array):
    res = []
    for key in array:
        res.append(key[1:-1])
    return res
