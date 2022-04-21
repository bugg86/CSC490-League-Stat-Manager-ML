from api import RiotApi
import json
import consts as Consts
import requests
from riotapiutilities import api as rau
from lsmrestapiutilities import api as lsm
import time

riot_key = 'RGAPI-ef3247df-953a-4361-80f7-f3f2c255b5d0'

rest_key = 'Token a7cb48f9a0645e2eb18ea44795907fb7be41dc58'

na1_api = rau.RiotApi(riot_key, Consts.REGIONS['north_america'])
americas_api = rau.RiotApi(riot_key, Consts.REGIONS['americas'])
lsm_api = lsm.RESTAPI(rest_key)

summoner_name = input('Enter summoner name: ')

summonerObj = lsm_api.get_summoner_by_name(summoner_name)

if summonerObj == [] :
    print('Summoner not found')
    lsm_api.post_summoner(na1_api.get_summoner_by_name(summoner_name))
    print(lsm_api.get_summoner_by_name(summoner_name))
    summonerObj = lsm_api.get_summoner_by_name(summoner_name)[0]
    exit()
else :
    print('Summoner found')
    summonerObj = summonerObj[0]

matches = americas_api.get_match_list_by_summoner_id(summonerObj['puuid'], start=0, count=100)
for match in matches :
    print(match)
    matchObj = lsm_api.get_match_by_id(match)
    if matchObj == [] : 
        print('Match not found')
        lsm_api.post_all_match_data (americas_api.get_match_by_match_id(match))
        time.sleep(10)
    else :
        print('Match found')

matches = americas_api.get_match_list_by_summoner_id(summonerObj['puuid'], start=100, count=100)
for match in matches :
    print(match)
    matchObj = lsm_api.get_match_by_id(match)
    if matchObj == [] : 
        print('Match not found')
        lsm_api.post_all_match_data (americas_api.get_match_by_match_id(match))
        time.sleep(10)
    else :
        print('Match found')

matches = americas_api.get_match_list_by_summoner_id(summonerObj['puuid'], start=200, count=100)
for match in matches :
    print(match)
    matchObj = lsm_api.get_match_by_id(match)
    if matchObj == [] : 
        print('Match not found')
        lsm_api.post_all_match_data (americas_api.get_match_by_match_id(match))
        time.sleep(10)
    else :
        print('Match found')

# participants = requests.get(url='https://csc490-lsm-rest-api.net/api/matchparticipants/', headers={'Authorization' : rest_key}).json()
# for participant in participants :
#     summonerid = participant['summonerid']
#     puuid = participant['puuid']
#     league = lsm_api.get_league_by_summonerid(summonerid)
#     championid = participant['championid']
#     championmastery = lsm_api.get_championmastery_by_championid_and_summonerid(championid, summonerid)
#     if league == [] :
#         print('league not found')
#         lsm_api.post_league(na1_api.get_league_by_summoner_id(summonerid))
#         time.sleep(.5)
#     if championmastery == [] :
#         print('championmastery not found')
#         lsm_api.post_championMastery(na1_api.get_champ_mastery_by_summoner_id_and_champ_id(summonerid, championid))
#         time.sleep(.5)
#     print('league and champmastery generated for ', summonerid, ' and ', championid)