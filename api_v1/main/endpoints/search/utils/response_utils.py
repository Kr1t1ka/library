import re
import operator

from api_v1.main.endpoints.menu.db import Menu


def smart_search(request_arr):
    all_menu = Menu.query.all()
    index_lib = {menu.id: menu.tags.split(' ') for menu in all_menu}
    menu_rating = {menu.id: 0 for menu in all_menu}

    # print(request_arr)

    for menu in index_lib:
        for word in request_arr:
            if word in index_lib[menu]:
                # print(word)
                # print(index_lib[menu])
                menu_rating[menu] += 1

    # print(menu_rating)
    res = [k for k, v in menu_rating.items() if v == max(menu_rating.values())]
    response = Menu.query.filter(Menu.id.in_(res)).all()
    return response

