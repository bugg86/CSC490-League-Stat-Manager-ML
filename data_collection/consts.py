API_VERSIONS = {
    'summoner' : '4',
    'match' : '5',
    'league' : '4',
    'champion-mastery' : '4',
    'spectator' : '4',
    'account' : '1'
}

REGIONS = {
    'north_america' : 'na1',
    'americas' : 'americas'
}

URL = {
    'base' : 'https://{region}.api.riotgames.com/lol/{url}',
    'summoner_by_name' : 'summoner/v{version}/summoners/by-name/{name}',
    'matches' : 'match/v{version}/matches/by-puuid/{puuid}/ids?start={start}&count={count}',
    'match' : 'match/v{version}/matches/{matchID}',
    'summoner_by_puuid' : 'summoner/v{version}/summoners/by-puuid/{puuid}',
    'league_by_summoner_id' : 'league/v{version}/entries/by-summoner/{summonerID}',
    'champion_mastery_by_summoner_id' : 'champion-mastery/v{version}/champion-masteries/by-summoner/{summonerID}',
    'live_match_by_id' : 'spectator/v{version}/active-games/by-summoner/{summonerID}',
    'summoner_by_id' : 'summoner/v{version}/summoners/{summonerID}',
    'account_by_puuid' : 'account/v{version}/accounts/by-puuid/{puuid}'
}