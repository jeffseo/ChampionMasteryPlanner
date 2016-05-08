API_KEY = "174ef72a-54df-4458-ae37-fa609507cbda"

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
    'league_version' : "api/lol/static-data/{region}/v{version}/versions"
}

API_VERSIONS = {
    'summoner': '1.4',
    'static-data': '1.2'
}

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
