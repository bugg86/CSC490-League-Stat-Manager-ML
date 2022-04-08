from api import RiotApi
import json
import consts as Consts
import requests
from riotapiutilities import api as rau
from lsmrestapiutilities import api as lsm

riot_key = 'RGAPI-61fe34b1-5fca-44f2-9ee7-6b9acff0ea3b'

rest_key = 'Token a7cb48f9a0645e2eb18ea44795907fb7be41dc58'

na1_api = rau.RiotApi(riot_key, Consts.REGIONS['north_america'])
americas_api = rau.RiotApi(riot_key, Consts.REGIONS['americas'])

summoner_name = input('Enter summoner name: ')

