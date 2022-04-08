import json
import requests
import consts as Consts
from api import RiotApi

riot_key = 'RGAPI-194f26d6-7df2-4674-95d1-83465a206e5e'

rest_key = 'Token a7cb48f9a0645e2eb18ea44795907fb7be41dc58'

rest_url = 'https://csc490-lsm-rest-api.azurewebsites.net/api/{api}'

na1_api = RiotApi(riot_key, Consts.REGIONS['north_america'])
americas_api = RiotApi(riot_key, Consts.REGIONS['americas'])

def start() :
    summonerName = input('Enter summoner name: ')

    response = requests.get(rest_url.format(api='summoners?name={name}'.format(name=summonerName)), headers={'Authorization': rest_key}).json()

    if len(response) == 0:
        print('Summoner not found')
        summoner = na1_api.get_summoner_by_name(summonerName)

        response = requests.post(rest_url.format(api='summoners/'), data={
            "id" : "{id}".format(id=summoner['id']),
            "accountid" : "{accountId}".format(accountId=summoner['accountId']),
            "puuid" : "{puuid}".format(puuid=summoner['puuid']),
            "name" : "{name}".format(name=summoner['name']),
            "profileiconid" : int(summoner['profileIconId']),
            "revisiondate" : int(summoner['revisionDate']),
            "summonerlevel" : int(summoner['summonerLevel'])
        }, headers={'Authorization': rest_key})

    else :
        summoner = response[0]
    
    return summoner

def get_summoner(puuid) :
    response = requests.get(rest_url.format(api='summoners?puuid={puuid}'.format(puuid=puuid)), headers={'Authorization': rest_key})

    if len(response.json()) == 0 or response.status_code == 404 :
        print('Summoner not found')
        
        summoner = na1_api.get_summoner_by_puuid(puuid)

        response = requests.post(rest_url.format(api='summoners/'), data={
            "id" : "{id}".format(id=summoner['id']),
            "accountid" : "{accountId}".format(accountId=summoner['accountId']),
            "puuid" : "{puuid}".format(puuid=summoner['puuid']),
            "name" : "{name}".format(name=summoner['name']),
            "profileiconid" : int(summoner['profileIconId']),
            "revisiondate" : int(summoner['revisionDate']),
            "summonerlevel" : int(summoner['summonerLevel'])
        }, headers={'Authorization': rest_key})
    else :
        summoner = response.json()[0]
    
    return summoner


puuid = start()['puuid']

count=input('Enter match count: ')

match_list = americas_api.get_match_list_by_summoner_id(puuid, 0, int(count))

for match in match_list :
    response = requests.get(rest_url.format(api='matches/{matchId}'.format(matchId=match)), headers={'Authorization': rest_key})
    
    if len(response.json()) == 0 or response.status_code== 404 or response.status_code == 400:
        print('Match not found')
        match_data = americas_api.get_match_by_match_id(match)

        response = requests.post(rest_url.format(api='matches/'), data={
                "matchid" : "{matchId}".format(matchId=match),
                "gamemode" : "{gameMode}".format(gameMode=match_data['info']['gameMode']),
                "gameduration" : int(match_data['info']['gameDuration']),
                "gamename" : "{gameName}".format(gameName=match_data['info']['gameName']),
                "gametype" : "{gameType}".format(gameType=match_data['info']['gameType']),
                "mapid" : int(match_data['info']['mapId']),
                "queueid" : int(match_data['info']['queueId']),
                "platformid" : "{platformId}".format(platformId=match_data['info']['platformId']),
                "gameversion" : "{gameVersion}".format(gameVersion=match_data['info']['gameVersion']),
                "gamecreation" : int(match_data['info']['gameCreation']),
                "gameendtimestamp" : int(match_data['info']['gameEndTimestamp']),
                "gamestarttimestamp" : int(match_data['info']['gameStartTimestamp'])
            }, headers={'Authorization': rest_key})
        participants = match_data['info']['participants']
        teams = match_data['info']['teams']

        for team in teams :
            bans = []
            for ban in team['bans'] :
                bans.append(ban['championId'])

            response = requests.post(rest_url.format(api='matchteams/'), data=json.dumps({
                "matchid" : "{matchId}".format(matchId=match),
                "teamid" : int(team['teamId']),
                "win" : "{win}".format(win=team['win']),
                "ban1" : int(bans[0]),
                "ban2" : int(bans[1]),
                "ban3" : int(bans[2]),
                "ban4" : int(bans[3]),
                "ban5" : int(bans[4]),
                "firstbaron" : team['objectives']['baron']['first'],
                "baronkills" : int(team['objectives']['baron']['kills']),
                "firstchampion" : team['objectives']['champion']['first'],
                "championkills" : int(team['objectives']['champion']['kills']),
                "firstdragon" : team['objectives']['dragon']['first'],
                "dragonkills" : int(team['objectives']['dragon']['kills']),
                "firstinhibitor" : team['objectives']['inhibitor']['first'],
                "inhibitorkills" : int(team['objectives']['inhibitor']['kills']),
                "firstriftherald" : team['objectives']['riftHerald']['first'],
                "riftheraldkills" : int(team['objectives']['riftHerald']['kills']),
                "firsttower" : team['objectives']['tower']['first'],
                "towerkills" : int(team['objectives']['tower']['kills'])
            }), headers={'Authorization': rest_key, "Content-Type": "application/json"})

        for participant in participants :
            summoner = get_summoner(participant['puuid'])

            response = requests.post(rest_url.format(api='matchparticipants?matchid={matchId}&matchpuuid={puuid}'.format(matchId=match,puuid=summoner['puuid'])), headers={'Authorization': rest_key})

            if len(response.json()) == 0 or response.status_code == 404  or response.status_code == 400 :
                print('Match participant not found')

                styles = []
                runes = []

                for style in participant['perks']['styles'] :
                    styles.append(style['style'])
                for style in participant['perks']['styles'] :
                    for selection in style['selections'] :
                        runes.append(selection['perk'])

                response = requests.post(rest_url.format(api='matchparticipants/'), data=json.dumps({
                    "customparticipantid" : "{matchid}{puuid}".format(matchid=match,puuid=summoner['puuid']),   #customparticipantid
                    "matchid" : "{matchId}".format(matchId=match),
                    "summonerid" : "{summonerId}".format(summonerId=summoner['id']),
                    "assists" : int(participant['assists']),
                    "baronkills" : int(participant['baronKills']),
                    "bountylevel" : int(participant['bountyLevel']),
                    "champexperience" : int(participant['champExperience']),
                    "champlevel" : int(participant['champLevel']),
                    "championid" : int(participant['championId']),
                    "championname" : "{championName}".format(championName=participant['championName']),
                    "damagedealttobuildings" : int(participant['damageDealtToBuildings']),
                    "damagedealttoobjectives" : int(participant['damageDealtToObjectives']),
                    "damagedealttoturrets" : int(participant['damageDealtToTurrets']),
                    "damageselfmitigated" : int(participant['damageSelfMitigated']),
                    "deaths" : int(participant['deaths']),
                    "detectorwardsplaced" : int(participant['detectorWardsPlaced']),
                    "doublekills" : int(participant['doubleKills']),
                    "dragonkills" : int(participant['dragonKills']),
                    "firstbloodassist" : int(participant['firstBloodAssist']),
                    "firstbloodkill" : int(participant['firstBloodKill']),
                    "firsttowerassisted" : int(participant['firstTowerAssist']),
                    "firsttowerkill" : int(participant['firstTowerKill']),
                    "gameendedinearlysurrender" : participant['gameEndedInEarlySurrender'],
                    "gameendedinsurrender" : participant['gameEndedInSurrender'],
                    "goldearned" : int(participant['goldEarned']),
                    "goldspent" : int(participant['goldSpent']),
                    "inhibitorkills" : int(participant['inhibitorKills']),
                    "inhibitortakedowns" : int(participant['inhibitorTakedowns']),
                    "inhibitorslost" : int(participant['inhibitorsLost']),
                    "item0" : int(participant['item0']),
                    "item1" : int(participant['item1']),
                    "item2" : int(participant['item2']),
                    "item3" : int(participant['item3']),
                    "item4" : int(participant['item4']),
                    "item5" : int(participant['item5']),
                    "item6" : int(participant['item6']),
                    "itemspurchased" : int(participant['itemsPurchased']),
                    "killingsprees" : int(participant['killingSprees']),
                    "kills" : int(participant['kills']),
                    "lane" : "{lane}".format(lane=participant['lane']),
                    "largestcriticalstrike" : int(participant['largestCriticalStrike']),
                    "largestkillingspree" : int(participant['largestKillingSpree']),
                    "largestmultikill" : int(participant['largestMultiKill']),
                    "longesttimespentliving" : int(participant['longestTimeSpentLiving']),
                    "magicdamagedealt" : int(participant['magicDamageDealt']),
                    "magicdamagedealttochampions" : int(participant['magicDamageDealtToChampions']),
                    "magicdamagetaken" : int(participant['magicDamageTaken']),
                    "neutralminionskilled" : int(participant['neutralMinionsKilled']),
                    "nexuskills" : int(participant['nexusKills']),
                    "nexuslost" : int(participant['nexusLost']),
                    "nexustakedowns" : int(participant['nexusTakedowns']),
                    "objectivesstolen" : int(participant['objectivesStolen']),
                    "objectivesstolenassists" : int(participant['objectivesStolenAssists']),
                    "participantid" : int(participant['participantId']),
                    "pentakills" : int(participant['pentaKills']),
                    "physicaldamagedealt" : int(participant['physicalDamageDealt']),
                    "physicaldamagedealttochampions" : int(participant['physicalDamageDealtToChampions']),
                    "physicaldamagetaken" : int(participant['physicalDamageTaken']),
                    "profileiconid" : int(participant['profileIcon']),
                    "puuid" : str(participant['puuid']),
                    "quadrakills" : int(participant['quadraKills']),
                    "riotidname" : "{riotIdName}".format(riotIdName=participant['riotIdName']),
                    "riotidtagline" : "{riotIdTagline}".format(riotIdTagline=participant['riotIdTagline']),
                    "role" : "{role}".format(role=participant['role']),
                    "rune1id" : int(runes[0]),
                    "rune2id" : int(runes[1]),
                    "rune3id" : int(runes[2]),
                    "rune4id" : int(runes[3]),
                    "rune5id" : int(runes[4]),
                    "rune6id" : int(runes[5]),
                    "runestyle1id" : int(styles[0]),
                    "runestyle2id" : int(styles[1]),
                    "sightwardsboughtingame" : int(participant['sightWardsBoughtInGame']),
                    "spell1casts" : int(participant['spell1Casts']),
                    "spell2casts" : int(participant['spell2Casts']),
                    "spell3casts" : int(participant['spell3Casts']),
                    "spell4casts" : int(participant['spell4Casts']),
                    "summoner1casts" : int(participant['summoner1Casts']),
                    "summoner1id" : int(participant['summoner1Id']),
                    "summoner2casts" : int(participant['summoner2Casts']),
                    "summoner2id" : int(participant['summoner2Id']),
                    "summonerlevel" : int(participant['summonerLevel']),
                    "summonername" : "{summonerName}".format(summonerName=participant['summonerName']),
                    "teamearlysurrendered" : participant['teamEarlySurrendered'],
                    "teamid" : int(participant['teamId']),
                    "teamposition" : "{teamPosition}".format(teamPosition=participant['teamPosition']),
                    "timeccingothers" : int(participant['timeCCingOthers']),
                    "timeplayed" : int(participant['timePlayed']),
                    "totaldamagedealt" : int(participant['totalDamageDealt']),
                    "totaldamagedealttochampions" : int(participant['totalDamageDealtToChampions']),
                    "totaldamageshieldedonteammates" : int(participant['totalDamageShieldedOnTeammates']),
                    "totaldamagetaken" : int(participant['totalDamageTaken']),
                    "totalheal" : int(participant['totalHeal']),
                    "totalhealsonteammates" : int(participant['totalHealsOnTeammates']),
                    "totalminionskilled" : int(participant['totalMinionsKilled']),
                    "totaltimeccdealt" : int(participant['totalTimeCCDealt']),
                    "totaltimespentdead" : int(participant['totalTimeSpentDead']),
                    "totalunitshealed" : int(participant['totalUnitsHealed']),
                    "triplekills" : int(participant['tripleKills']),
                    "truedamagedealt" : int(participant['trueDamageDealt']),
                    "truedamagedealttochampions" : int(participant['trueDamageDealtToChampions']),
                    "truedamagetaken" : int(participant['trueDamageTaken']),
                    "turretkills" : int(participant['turretKills']),
                    "turrettakedowns" : int(participant['turretTakedowns']),
                    "turretslost" : int(participant['turretsLost']),
                    "unrealkills" : int(participant['unrealKills']),
                    "visionscore" : int(participant['visionScore']),
                    "visionwardsboughtingame" : int(participant['visionWardsBoughtInGame']),
                    "wardskilled" : int(participant['wardsKilled']),
                    "wardsplaced" : int(participant['wardsPlaced']),
                    "win" : participant['win']
                }))

                print(json.dumps({
                    "matchid" : "{matchId}".format(matchId=match),
                    "summonerid" : "{summonerId}".format(summonerId=summoner['id']),
                    "assists" : int(participant['assists']),
                    "baronkills" : int(participant['baronKills']),
                    "bountylevel" : int(participant['bountyLevel']),
                    "champexperience" : int(participant['champExperience']),
                    "champlevel" : int(participant['champLevel']),
                    "championid" : int(participant['championId']),
                    "championname" : "{championName}".format(championName=participant['championName']),
                    "damagedealttobuildings" : int(participant['damageDealtToBuildings']),
                    "damagedealttoobjectives" : int(participant['damageDealtToObjectives']),
                    "damagedealttoturrets" : int(participant['damageDealtToTurrets']),
                    "damageselfmitigated" : int(participant['damageSelfMitigated']),
                    "deaths" : int(participant['deaths']),
                    "detectorwardsplaced" : int(participant['detectorWardsPlaced']),
                    "doublekills" : int(participant['doubleKills']),
                    "dragonkills" : int(participant['dragonKills']),
                    "firstbloodassist" : int(participant['firstBloodAssist']),
                    "firstbloodkill" : int(participant['firstBloodKill']),
                    "firsttowerassisted" : int(participant['firstTowerAssist']),
                    "firsttowerkill" : int(participant['firstTowerKill']),
                    "gameendedinearlysurrender" : participant['gameEndedInEarlySurrender'],
                    "gameendedinsurrender" : participant['gameEndedInSurrender'],
                    "goldearned" : int(participant['goldEarned']),
                    "goldspent" : int(participant['goldSpent']),
                    "individualposition" : "{individualPosition}".format(individualPosition=participant['individualPosition']),
                    "inhibitorkills" : int(participant['inhibitorKills']),
                    "inhibitortakedowns" : int(participant['inhibitorTakedowns']),
                    "inhibitorslost" : int(participant['inhibitorsLost']),
                    "item0" : int(participant['item0']),
                    "item1" : int(participant['item1']),
                    "item2" : int(participant['item2']),
                    "item3" : int(participant['item3']),
                    "item4" : int(participant['item4']),
                    "item5" : int(participant['item5']),
                    "item6" : int(participant['item6']),
                    "itemspurchased" : int(participant['itemsPurchased']),
                    "killingsprees" : int(participant['killingSprees']),
                    "kills" : int(participant['kills']),
                    "lane" : "{lane}".format(lane=participant['lane']),
                    "largestcriticalstrike" : int(participant['largestCriticalStrike']),
                    "largestkillingspree" : int(participant['largestKillingSpree']),
                    "largestmultikill" : int(participant['largestMultiKill']),
                    "longesttimespentliving" : int(participant['longestTimeSpentLiving']),
                    "magicdamagedealt" : int(participant['magicDamageDealt']),
                    "magicdamagedealttochampions" : int(participant['magicDamageDealtToChampions']),
                    "magicdamagetaken" : int(participant['magicDamageTaken']),
                    "neutralminionskilled" : int(participant['neutralMinionsKilled']),
                    "nexuskills" : int(participant['nexusKills']),
                    "nexuslost" : int(participant['nexusLost']),
                    "nexustakedowns" : int(participant['nexusTakedowns']),
                    "objectivesstolen" : int(participant['objectivesStolen']),
                    "objectivesstolenassists" : int(participant['objectivesStolenAssists']),
                    "participantid" : int(participant['participantId']),
                    "pentakills" : int(participant['pentaKills']),
                    "physicaldamagedealt" : int(participant['physicalDamageDealt']),
                    "physicaldamagedealttochampions" : int(participant['physicalDamageDealtToChampions']),
                    "physicaldamagetaken" : int(participant['physicalDamageTaken']),
                    "profileiconid" : int(participant['profileIcon']),
                    "puuid" : str(participant['puuid']),
                    "quadrakills" : int(participant['quadraKills']),
                    "riotidname" : "{riotIdName}".format(riotIdName=participant['riotIdName']),
                    "riotidtagline" : "{riotIdTagline}".format(riotIdTagline=participant['riotIdTagline']),
                    "role" : "{role}".format(role=participant['role']),
                    "rune1id" : int(runes[0]),
                    "rune2id" : int(runes[1]),
                    "rune3id" : int(runes[2]),
                    "rune4id" : int(runes[3]),
                    "rune5id" : int(runes[4]),
                    "rune6id" : int(runes[5]),
                    "runestyle1id" : int(styles[0]),
                    "runestyle2id" : int(styles[1]),
                    "sightwardsboughtingame" : int(participant['sightWardsBoughtInGame']),
                    "spell1casts" : int(participant['spell1Casts']),
                    "spell2casts" : int(participant['spell2Casts']),
                    "spell3casts" : int(participant['spell3Casts']),
                    "spell4casts" : int(participant['spell4Casts']),
                    "summoner1casts" : int(participant['summoner1Casts']),
                    "summoner1id" : int(participant['summoner1Id']),
                    "summoner2casts" : int(participant['summoner2Casts']),
                    "summoner2id" : int(participant['summoner2Id']),
                    "summonerlevel" : int(participant['summonerLevel']),
                    "summonername" : "{summonerName}".format(summonerName=participant['summonerName']),
                    "teamearlysurrendered" : participant['teamEarlySurrendered'],
                    "teamid" : int(participant['teamId']),
                    "teamposition" : "{teamPosition}".format(teamPosition=participant['teamPosition']),
                    "timeccingothers" : int(participant['timeCCingOthers']),
                    "timeplayed" : int(participant['timePlayed']),
                    "totaldamagedealt" : int(participant['totalDamageDealt']),
                    "totaldamagedealttochampions" : int(participant['totalDamageDealtToChampions']),
                    "totaldamageshieldedonteammates" : int(participant['totalDamageShieldedOnTeammates']),
                    "totaldamagetaken" : int(participant['totalDamageTaken']),
                    "totalheal" : int(participant['totalHeal']),
                    "totalhealsonteammates" : int(participant['totalHealsOnTeammates']),
                    "totalminionskilled" : int(participant['totalMinionsKilled']),
                    "totaltimeccdealt" : int(participant['totalTimeCCDealt']),
                    "totaltimespentdead" : int(participant['totalTimeSpentDead']),
                    "totalunitshealed" : int(participant['totalUnitsHealed']),
                    "triplekills" : int(participant['tripleKills']),
                    "truedamagedealt" : int(participant['trueDamageDealt']),
                    "truedamagedealttochampions" : int(participant['trueDamageDealtToChampions']),
                    "truedamagetaken" : int(participant['trueDamageTaken']),
                    "turretkills" : int(participant['turretKills']),
                    "turrettakedowns" : int(participant['turretTakedowns']),
                    "turretslost" : int(participant['turretsLost']),
                    "unrealkills" : int(participant['unrealKills']),
                    "visionscore" : int(participant['visionScore']),
                    "visionwardsboughtingame" : int(participant['visionWardsBoughtInGame']),
                    "wardskilled" : int(participant['wardsKilled']),
                    "wardsplaced" : int(participant['wardsPlaced']),
                    "win" : participant['win']
                }))


    else :
        match_data = response.json()    

    # for participant in participants :
    #     summoner = get_summoner(participant)