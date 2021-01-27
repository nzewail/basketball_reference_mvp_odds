#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import json
from datetime import date

URL = 'https://www.basketball-reference.com/friv/mvp.html'


def get_mvp_odds_page():
    r = requests.get(URL)
    if r.status_code == 200:
        return r


def parse_page(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    players = soup.find('tbody').findAll('tr')
    output = {'date': str(date.today()), 'players': {}}
    for player in players:
        parsed_row = parse_table_row(player)
        output['players'][parsed_row['player_id']] = parsed_row
    return output


def parse_table_row(row):
    name = row.find('td', class_='left').text
    probability = row.find('td', {'data-stat': 'value'}).text
    prob = probability_pct_to_float(probability)
    player_id = row.find('td')['data-append-csv']
    rank = int(row.find('th').text)
    return {
        'name': name,
        'player_id': player_id,
        'probability': prob,
        'rank': rank
    }


def probability_pct_to_float(probability):
    return float(probability[:-1])


def main(request):
    r = get_mvp_odds_page()
    output = parse_page(r)
    return f"{json.dumps(output)}\n"


if __name__ == '__main__':
    main()
