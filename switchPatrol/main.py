import requests
import json
import logging
from .Game import Game
from .data.config import GAME_LIST, TG_API_TOKEN, TG_CHAT_ID


def get_proper_game_name(game_name):
    parsed = game_name.split()
    proper_name = ""
    if len(parsed) > 1:
        for i in parsed:
            proper_name = proper_name + "%20" + i
        proper_name = proper_name[3:]
        logging.debug(f'get_proper_game_name\nProper name of {game_name}: {proper_name}')
    else:
        proper_name = parsed[0]
    return proper_name

def search_a_game(game_name):
    nintendo_search_link = "https://searching.nintendo-europe.com/ru/select?q="
    type_link_part = "&fq=type%3AGAME"
    result = requests.get(nintendo_search_link + get_proper_game_name(game_name) + type_link_part)
    #logging.debug(f'Request result is :\t{result.text}')
    return result

def parse_json(json_text):
    games = []
    response = json_text.get('response')
    if response.get('numFound') > 0:
        for element in json_text['response']['docs']:
            try:
                game = Game()
                game.name = element.get('title')
                game.price = element.get('price_regular_f')
                game.new_price = element.get('price_lowest_f')
                games.append(game)
                logging.info(f'parse_json\tGame parsed:\n{game}')
            except KeyError:
                logging.error("Something wrong with response json!")
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
        logging.debug(f'send_notification\tgame:\n{game}')
        if game.presence:
            msg += game
            logging.info(f'send_notification\t!!!  \n{game}')
    logging.info(f'send_notification\tMsg is:\n{msg}')
    req = f"https://api.telegram.org/bot{api_token}/sendMessage?chat_id={chat_id}&text={msg}"
    r = requests.get(req)
    logging.info(f'send_notification\tTg notificator:\n{r.status_code}\t{r.text}')
    return r.status_code


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', 
        filename='patrol.log', encoding='utf-8', level=logging.DEBUG)
    for game in GAME_LIST:
        proper_name = get_proper_game_name(game)
        games_from_json = parse_json(json.loads(search_a_game(proper_name).text))
        checked_games = check_game(games_from_json, game)
        send_notification(checked_games, TG_API_TOKEN, TG_CHAT_ID)
