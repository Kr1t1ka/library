import re

from api_v1.main.endpoints.replace.db import Replace


def text_replace(replace_object):

    names_arr = changing_array(re.findall('{\w+}', replace_object[0].text))

    replace = Replace.query.all()
    tmp = Replace.query.filter(Replace.name in names_arr).all()

    print(replace[0].name in names_arr)

    variables = {}
    for k in replace:
        variables[k.name] = k.value

    for i in replace_object:
        i.text = i.text.format(**variables)

    return replace_object


def changing_array(array):
    res = []
    for i in range(len(array)):
        res.append(array[i][1:-1])
    return res
