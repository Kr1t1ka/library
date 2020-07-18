import re
import operator

from api_v1.main.endpoints.menu.db import Menu


def smart_search(request_arr):
    all_menu = Menu.query.all()

    index_lib = {menu.id: create_index_word(menu.text) for menu in all_menu}
    menu_rating = {menu.id: 0 for menu in all_menu}

    for word_request in request_arr:
        words_rating = {menu.id: index_lib[menu.id][word_request] for menu in all_menu if
                        word_request in index_lib[menu.id]}
        for i in range(len(menu_rating)):
            if i in words_rating:
                menu_rating[i] += words_rating[i]

    id_response = max(menu_rating.items(), key=operator.itemgetter(1))[0]
    menu_response = Menu.query.filter(Menu.id.in_(str(id_response))).all()

    return menu_response


def create_index_word(text):
    stopwords = {'в', 'и', 'с', 'на', 'при', 'об', 'не', 'по', 'со'}
    text = text.lower()
    text = re.sub("^\s+|[.,«»()–:]|\s+$", ' ', text)
    text = re.sub("^\s+|\n|\r|\s+$", '', text)
    text = [word for word in re.split("\W+", text) if word not in stopwords]
    text = {word: text.count(word) for word in set(text)}
    return text
