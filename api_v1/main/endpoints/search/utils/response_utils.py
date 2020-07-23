import re
import operator

from api_v1.main.endpoints.menu.db import Menu
from api_v1.main.endpoints.search.utils.request_utils import lemmatization


def smart_search(request_arr):
    """
    Получает обработаный запрос пользователя в виде массива, сопостовляет с тегами статей и подбирате наиболее
    подходящую статью.
    :param request_arr:
    :return: <Menu>
    """
    all_menu = Menu.query.all()
    index_lib = {menu.id: [lemmatization(word) for word in menu.tags.split(' ')] for menu in all_menu}
    menu_rating = {menu.id: 0 for menu in all_menu}

    for menu in index_lib:
        for word in request_arr:
            if word in index_lib[menu]:
                menu_rating[menu] += 1 / len(index_lib[menu])
            else:
                menu_rating[menu] -= 1 / len(index_lib[menu])

    res = [k for k, v in menu_rating.items() if v == max(menu_rating.values())]
    response = Menu.query.filter(Menu.id.in_(res)).all()
    return response

