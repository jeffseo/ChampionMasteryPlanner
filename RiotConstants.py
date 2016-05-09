import os
if os.environ.get('RIOT_API_KEY'):
    API_KEY = os.environ['RIOT_API_KEY']
elif os.path.isfile("RIOT_API_KEY") and os.path.getsize("RIOT_API_KEY") > 0:
        with open("RIOT_API_KEY", 'r') as key:
            API_KEY = key.readline()
else:
    raise Exception("API KEY NOT FOUND")

# To reach 
# Tier    CP Required     Cumulative CP Required  Cumulative CP %
# 1       0               0                       0
# 2       1800            1800                    8
# 3       4200            6000                    28
# 4       6600            12600                   58
# 5       9000            21600                   100
# 6       11400           33000                   -
# 7       13800           46800                   -
MASTERY_POINTS = {
    1 : 0,
    2 : 1800,
    3 : 6000,
    4 : 12600,
    5 : 21600,
    6 : 33000,
    7 : 46800
}

URL = {
    'base': 'https://{proxy}.api.pvp.net/{url}',
    'summoner_by_name': 'api/lol/{region}/v{version}/summoner/by-name/{names}',
    'champion_by_id' : 'api/lol/static-data/{region}/v{version}/champion/{id}',
    'top_champion_mastery': 'championmastery/location/{platformId}/player/{playerId}/topchampions?count={count}',
    'all_champion_mastery': "championmastery/location/{platformId}/player/{playerId}/champions",
    'single_champion_mastery': 'championmastery/location/{platformId}/player/{playerId}/champion/{championId}',
    'champion_list_by_id': "api/lol/static-data/{region}/v{version}/champion?dataById=true",
    'champion_list_by_name': "api/lol/static-data/{region}/v{version}/champion",
    'league_version' : "api/lol/static-data/{region}/v{version}/versions",
    'recent_game': "/api/lol/{region}/v{version}/game/by-summoner/{summonerId}/recent"

}

API_VERSIONS = {
    'summoner': '1.4',
    'static-data': '1.2',
    'game': '1.3'
}

# Used to filter out only game modes that award champion mastery points
# (i.e. no ARAM, no Bot games, etc).
VALID_GAME_MODES = ['NORMAL', 'RANKED_SOLO_5x5', 'RANKED_PREMADE_5x5',
                    'RANKED_TEAM_5x5', 'CAP_5x5', 'ONEFORALL_5x5', 'SR_6x6', 
                    'URF', 'ASCENSION', 'HEXAKILL', 'KING_PORO']

#https://developer.riotgames.com/docs/regional-endpoints
ENDPOINTS = {
    'BR' : {
        'region': 'br',
        'platform': 'BR1',
    },

    'EUNE' : {
        'region': 'eune',
        'platform': 'EUN1',
    },

    'EUW' : {
        'region': 'euw',
        'platform': 'EUW1',
    },

    'JP' : {
        'region': 'jp',
        'platform': 'JP1',
    },

    'KR' : {
        'region': 'kr',
        'platform': 'KR'
    },

    'LAN' : {
        'region': "lan",
        'platform': "LA1",
    },

    'LAS' : {
        'region': "las",
        'platform': "LA2",
    },

    'NA' : {
        'region': "na",
        'platform': "NA1",
    },

    'OCE' : {
        'region': "oce",
        'platform': "OC1",
    },

    'TR' : {
        'region': "tr",
        'platform': "TR1",
    },

    'RU' : {
        'region': "ru",
        'platform': "RU",
    },

    'PBE' : {
        'region': "pbe",
        'platform': "PBE1",
    },

    'Global' : {
        'region': 'global'
    }
}
