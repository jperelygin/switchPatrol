import requests
import json
from Game import Game
from data.config import GAME_LIST, TG_API_TOKEN, TG_CHAT_ID


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
    games = []
    response = json_text.get('response')
    if response.get('numFound') > 0:
        for element in json_text['response']['docs']:
            try:
                game = Game()
                game.name = element['system_names_txt'][0]
                game.price = element['price_regular_f']
                game.new_price = element['price_lowest_f']
                games.append(game)
            except KeyError:
                print("Something wrong with response json!")
    else:
        print("No games found!")
    return games

def check_game(games, game_name):
    if len(games) > 0:
        for i in games:
            if i.name == game_name:
                i.presence = True
    return games

def send_notification(games, api_token, chat_id):
    msg = ""
    for game in games:
        if game.presence:
            msg = msg + str(game)
    req = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={chat_id}&text={msg}"
    r = requests.get(req)
    return r.status_code


if __name__ == "__main__":
    for game in GAME_LIST:
        proper_name = get_proper_game_name(game)
        games_from_json = parse_json(json.loads(search_a_game(proper_name).text))
        checked_games = check_game(games_from_json, game)
        send_notification(checked_games, TG_API_TOKEN, TG_CHAT_ID)
