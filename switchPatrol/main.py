import requests
import json
from .Game import Game


GAMES = [
    "Disco Elysium",
    "Diablo 2"
]

def get_proper_game_name(game_name):
    parsed = game_name.split()
    proper_name = ""
    if len(parsed) > 1:
        for i in parsed:
            proper_name = proper_name + "%20" + i
        proper_name = proper_name[3:]
    else:
        proper_name = parsed[0]
    return proper_name

def search_a_game(game_name):
    nintendo_search_link = "https://searching.nintendo-europe.com/ru/select?q="
    type_link_part = "&fq=type%3AGAME"
    return requests.get(nintendo_search_link + get_proper_game_name(game_name) + type_link_part)

def parse_json(json_text):
    result = []
    response = json_text.get('response')
    if response.get('numFound') > 0:
        for element in json_text['response']['docs']:
            game = Game()
            game.name = element['system_names_txt'][0]
            game.price = element['price_regular_f']
            game.new_price = element['price_lowest_f']
            result.append(game)
    else:
        print("No games found!")
    return result

if __name__ == "__main__":
    pass