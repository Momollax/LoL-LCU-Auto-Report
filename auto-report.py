from lcu_driver import Connector
from time import sleep

connector = Connector()
@connector.ready

async def connect(connection):
    users = {}
    friends = []
    print("Welcome to the League of Legends must racist tool :) !")
    tmp = await connection.request('get', '/lol-chat/v1/friends')
    tmp = await tmp.json()
    for friend in tmp:
        friends.append(friend['summonerId'])
        users[friend['summonerId']] = friend['name']
    me = await connection.request('get', '/lol-chat/v1/me')
    me = await me.json()
    friends.append(me['summonerId'])
    try:
        got = await connection.request('get', "/lol-end-of-game/v1/eog-stats-block")
        got = await got.json()
        try:
            gameID = got['gameId']
            teams = got['teams']
            print(gameID)
            for team in teams:
                for player in team['players']:
                    if player['summonerId'] not in friends:     
                        _report = {
                            "comment": "Useless AF",
                            "gameId": gameID,
                            "offenses": "Negative Attitude",
                            "reportedSummonerId": player['summonerId']
                        }
                        response = await connection.request('post', "/lol-end-of-game/v2/player-complaints", data=_report)
                        print(player['summonerId'], player['summonerName'], "is reported.")
                        response = await response.json()
                        print(response)
                        sleep(1)
        except KeyError:
            print("error in get gameId")
    except KeyError:
        print("error in get conversation")

connector.start()