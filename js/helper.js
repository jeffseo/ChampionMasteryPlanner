var apiKey = "?api_key=174ef72a-54df-4458-ae37-fa609507cbda";
var riotApiAddress = "https://na.api.pvp.net/";
function getSummonerInfo() 
{   
    var form = document.getElementById("searchForm");
    var summonerName = form.elements.summonerName.value;
    var platformId = form.elements.platform.value;
    var summonerId = getSummonerId(summonerName,platformId);
    var championMasteryInfo = getChampionMastery(summonerId,platformId);

}

    // "playerId": 29484755,
    // "championId": 236,
    // "championLevel": 5,
    // "championPoints": 23458,
    // "lastPlayTime": 1462056233000,
    // "championPointsSinceLastLevel": 1858,
    // "championPointsUntilNextLevel": 0,
    // "chestGranted": false,
    // "highestGrade": "S-"
function getChampionMastery(summonerId, platformId)
{
    platformId = platformId.concat('1'); //TODO: make function maybe to convert region to platform id
    console.log(platformId);
    var requestString = riotApiAddress.concat('/championmastery/location/{platformId}/player/{playerId}/topchampions'.replace("{platformId}",platformId).replace('{playerId}',summonerId).concat(apiKey));
    var ritoPls = riotApiRequest(requestString);
    if (ritoPls.status == 200) 
    {
        var response = JSON.parse(ritoPls.responseText);
        console.log(response);
        for (var i = 0; i < response.length; i++) {
            var obj = response[i];
            console.log(obj.championId);
            console.log(obj.championLevel);
            console.log(obj.championPointsUntilNextLevel);
        }
        //var summonerId = summonerInfoJSON.eval(summonerName).id;
    }       
}

function getSummonerId(summonerName, region) 
{
    var summonerInfo = "/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}".replace("{region}",region).replace("{summonerNames}",summonerName);
    var ritoPls = riotApiRequest(riotApiAddress.concat(summonerInfo).concat(apiKey));
    //ritoPls.open("get", riotApiAddress.concat(summonerInfo).concat(apiKey), false);
    //ritoPls.send();
    if (ritoPls.status == 200) 
    {
        //alert(ritoPls.responseText);    
        JSON.parse(ritoPls.responseText, function(k, v)
            {
                //console.log(k);
                if (k === "id")
                {
                    summonerId = v;
                }
            });
        //var summonerId = summonerInfoJSON.eval(summonerName).id;
        //console.log(summonerId);
        return summonerId;
    }
}

function riotApiRequest(requestString)
{
    var request = new XMLHttpRequest();
    request.open("get", requestString, false);
    request.send();
    return request;
}