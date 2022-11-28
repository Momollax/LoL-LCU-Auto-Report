from lcu_driver import Connector
from time import sleep

connector = Connector()
@connector.ready

async def connect(connection):
    print("Welcome to the League of Legends most racist tool 🙂 !")
    while True:
        users = {}
        friends = []
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
            #print(got)
            try:
                gameID = got['gameId']
                teams = got['teams']
                print(gameID)
                for team in teams:
                    for player in team['players']:
                        if player['summonerId'] not in friends:
                            _report = {
                                "comment": "trash talk, toxic, racist",
                                "gameId": gameID,
                                "offenses": "Negative Attitude, Verbal Abuse",
                                "reportedSummonerId": player['summonerId']
                            }
                            response = await connection.request('post', "/lol-end-of-game/v2/player-complaints", data=_report)
                            print(player['summonerId'], player['summonerName'], "is reported.")
                            response = await response.json()
                            print(response)
                print("all the people get report 🙂 !")
                pass
            except KeyError:
                pass
        except KeyError:
            print("error in get conversation")
        sleep(3)

connector.start()