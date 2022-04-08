import requests
import consts as Consts

key = 'RGAPI-dea1d3b6-48d0-47d0-b41c-b74acb5a8113'

class RiotApi(object) :
    def __init__(self, api_key, region) :
        self.api_key = api_key
        self.region=region

    def request(self, api_url, params={}) :
        args = {'api_key' : self.api_key}
        for key, value in params.items() :
            if key not in args :
                args[key] = value
        response = requests.get(
            Consts.URL['base'].format(
                region=self.region,
                url=api_url
            ), 
            params = args
        )
        #print (response.url)
        return response.json()
    
    # Look up summoner information using their summoner name.
    def get_summoner_by_name(self, name) :
        api_url = 'summoner/v4/summoners/by-name/{name}'.format(
            name=name
        )
        return self.request(api_url)
    
    # Look up summoner information using their summoner name.
    def get_summoner_by_puuid(self, puuid) :
        api_url = 'summoner/v4/summoners/by-puuid/{puuid}'.format(
            puuid=puuid
        )
        return self.request(api_url)

    # Look up account information using puuid.
    def get_account_by_puuid(self, puuid) :
        api_url = Consts.URL['account_by_puuid'].format(
            version = Consts.API_VERSIONS['account'],
            puuid = puuid
        )
        return self.request(api_url)

    # Look up league information using encrypted summoner id.
    def get_league_by_summoner_id(self, summonerid) :
        api_url = Consts.URL['league_by_summoner_id'].format(
            version = Consts.API_VERSIONS['league'],
            summonerID = summonerid
        )
        return self.request(api_url)

    # Look up champion mastery information using encrypted summoner id.
    def get_champ_mastery_by_summoner_id(self, summonerid) :
        api_url = Consts.URL['champion_mastery_by_summoner_id'].format(
            version = Consts.API_VERSIONS['champion-mastery'],
            summonerID = summonerid
        )
        return self.request(api_url)

    # Look up live match information using encrypted summoner id.
    def get_live_match_by_summoner_id(self, summonerid) :
        api_url = Consts.URL['live_match_by_id'].format(
            version = Consts.API_VERSIONS['spectator'],
            summonerID = summonerid
        )
        return self.request(api_url)
    
    # Look up matches based on puuid and start and end indices.
    def get_match_list_by_summoner_id(self, puuid, start, count) :
        api_url = Consts.URL['matches'].format(
            version = Consts.API_VERSIONS['match'],
            puuid = puuid,
            start = start,
            count = count
        )
        return self.request(api_url)
    
    # Look up match based on matchid.
    def get_match_by_match_id(self, matchid) :
        api_url = Consts.URL['match'].format(
            version = Consts.API_VERSIONS['match'],
            matchID = matchid
        )
        return self.request(api_url)