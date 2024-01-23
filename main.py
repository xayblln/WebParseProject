import pandas as pd
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    # url = "https://www.championat.com/hockey/_nhl/tournament/5075/statistic/player/goalpass/"
    # headers = {
    #     'Accept':'*/*',
    #     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
    # }
    # req = requests.get(url, headers=headers)
    # src = req.text
    # with open("index.html", "w", encoding="utf-8") as f:
    #     f.write(src)
    teams = []
    points = []
    ampluas = []
    players = []

    with open("index.html", encoding="utf-8") as f:
        src = f.read()

    soup = BeautifulSoup(src, "lxml")
    all_teams = soup.find_all(class_="table-responsive__row")
    players_points = soup.find_all(attrs={"data-label": "Гол+пас"})
    players_names = soup.find_all(class_="table-item__name")

    for item in all_teams:
        teams.append(item.get("data-team"))
        ampluas.append(item.get("data-amplua"))
    for item in players_points:
        points.append(item.text)
    for item in players_names:
        players.append(item.text)

    points_only_digits = [int(''.join(filter(str.isdigit, item))) for item in points]
    teams.pop(0)
    ampluas.pop(0)

    stats_df = pd.DataFrame({'Team': teams, 'Player': players, 'Amplua': ampluas, "Pts": points_only_digits})

    sorted_stats_df = stats_df.sort_values(['Team', 'Pts'], ascending=[True, False])
    print(sorted_stats_df[['Team', 'Player', 'Pts']])