import pytest
import json
import requests
import switchPatrol.main
from switchPatrol.Game import Game


def test_proper_name_single_word():
    name = "Test"
    assert switchPatrol.main.get_proper_game_name(name) == "Test"

def test_proper_name_multiple_words():
    name = "Test Test Test"
    assert switchPatrol.main.get_proper_game_name(name) == "Test%20Test%20Test"

@pytest.mark.skip
def test_search_send_request():
    name = "Mario"
    assert switchPatrol.main.search_a_game(name).status_code == requests.codes.ok

def test_json_parse_one_game():
    jsn = '{"response": {"numFound": 1, "docs":[{"title" : "Test", "price_regular_f" : 100500,"price_lowest_f" : 100500}]}}'
    x = json.loads(jsn)
    parsed = switchPatrol.main.parse_json(x)
    assert len(parsed) > 0
    assert parsed[0].name == "Test"
    assert parsed[0].price == 100500
    assert parsed[0].new_price == 100500

def test_json_parse_no_games():
    jsn = '{"response": {"numFound": 0}}'
    x = json.loads(jsn)
    parsed = switchPatrol.main.parse_json(x)
    assert len(parsed) == 0

def test_json_parse_two_games():
    jsn = '{"response": {"numFound": 2, "docs":[{"title" : "Test","price_regular_f" : 100500,"price_lowest_f" : 100500},{"title" : "Test2","price_regular_f" : 10500,"price_lowest_f" : 10500}]}}'
    x = json.loads(jsn)
    parsed = switchPatrol.main.parse_json(x)
    assert len(parsed) == 2

# TODO: Add test with response.json

def test_game_has_discount():
    game = Game()
    game.price = 500
    game.new_price = 400
    assert game.is_discount() == True

def test_parse_game_price():
    jsn = '{"docs":[{"title" : "Test", "price_regular_f" : null,"price_lowest_f" : 100500}]}'
    x = json.loads(jsn)
    game = Game()
    game.price = switchPatrol.main.parse_game_price(x)
    assert game.price == 0.0

def test_parse_game_new_price():
    jsn = '{"docs":[{"title" : "Test", "price_regular_f" : 100500,"price_lowest_f" : null}]}'
    x = json.loads(jsn)
    game = Game()
    game.new_price = switchPatrol.main.parse_game_new_price(x)
    assert game.new_price == 0.0

def test_check_game_not_present():
    game_name = "Test Test"
    game1 = Game()
    game1.name = "1 Test"
    games = [game1]
    switchPatrol.main.check_game(games, game_name)
    assert game1.presence == False

def test_check_game_is_present():
    game_name = "Test Test"
    game1 = Game()
    game1.name = "Test Test"
    games = [game1]
    switchPatrol.main.check_game(games, game_name)
    assert game1.presence == True