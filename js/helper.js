/*
To reach 
Tier    CP Required     Cumulative CP Required  Cumulative CP %
1       0               0                       0
2       1800            1800                    8
3       4200            6000                    28
4       6600            12600                   58
5       9000            21600                   100
6       11400           33000                   -
7       13800           46800                   -
*/

var apiKey = "?api_key=174ef72a-54df-4458-ae37-fa609507cbda";
var riotApiAddress = "https://na.api.pvp.net/";
var riotApiAddressGlobal = "https://global.api.pvp.net/";

//http://stackoverflow.com/questions/2177548/load-json-into-variable
var championData = (function () {
    var json = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': 'static-champion-data.json',
        'dataType': "json",
        'success': function (data) {
            json = data;
        }
    });
    return json;
})(); 

function championInfo()
{
    this.championImage;
    this.championName;
    this.championLevel;
    this.championPoints;
    this.pointsUntilNextLevel;
    this.pointsSinceLastLevel;
    this.championIcon;
}

function createTop10Page()
{
    championMasteryList = getSummonerInfo();
    if (championMasteryList === undefined)
    {
        return;
    }
    removeForm();
    //console.log(championMasteryList);
    document.getElementById("champion-data").innerHTML = createMasteryTable(championMasteryList);
}

function createMasteryTable(championMasteryList)
{
    var myTable= "<table class='table' style='border: 1px white;'><tr>"
    myTable += "<th style='text-align: center; background-color:#000000;\'></th>";
    myTable += "<th style='width: 100px; text-align: center; background-color:#000000;'>Champion</th>";
    myTable += "<th style='width: 100px; text-align: center; background-color:#000000;'>Mastery Level</th>";
    myTable += "<th style='width: 100px; red; text-align: center; background-color:#000000;'>Mastery Points</th>";
    myTable += "<th style='width: 100px; red; text-align: center; background-color:#000000;'>Points for level</th>";
    myTable += "<th style='width: 100px; red; text-align: center; background-color:#000000;'>Games needed</th></tr>"

  for (var i=0; i<10; i++) {
    myTable+="<tr><td style='width: 100px;text-align:center; background-color:#000033;\'><img src=\"" + championMasteryList[i].championIcon + '" width="40" height="40"></td>'
    myTable+="<td style='width: 100px; text-align:center; background-color:#000033;'>"  + championMasteryList[i].championName + "</td>";
    myTable+="<td style='width: 100px; background-color:#000033; text-align: center;'>" + championMasteryList[i].championLevel + "</td>";
    myTable+="<td style='width: 100px; background-color:#000033; text-align: center;'>" + championMasteryList[i].championPoints + "</td>";
    myTable+="<td style='width: 100px; background-color:#000033; text-align: center;'>" + championMasteryList[i].pointsUntilNextLevel + "</td>";
    myTable+="<td style='width: 100px; background-color:#000033; text-align: center;'>" + "temp" + "</td></tr>";
  }  
   myTable+="</table><bg-helper></bg-helper>";
   return myTable;
}

function getSummonerInfo(summonerName, region) 
{   
    if (!summonerName && !region)
    {
        // var form = document.getElementById("searchForm");
        // var summonerName = form.elements.summonerName.value;
        // var region = form.elements.platform.value;   
        var summonerName = getParameterByName('summonerName');
        var region = getParameterByName('region');
    }
    console.log(summonerName, region);
    if (summonerName === null || region === null)
    {
        return;
    }
    var summonerId = getSummonerId(summonerName,region);
    var championMasteryList = getChampionMasteryList(summonerId,region);
    return championMasteryList;

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
function getChampionMasteryList(summonerId, region)
{
    var championMasteryList = [];
    var platformId = region.concat('1'); //TODO: make function maybe to convert region to platform id
    var requestString = riotApiAddress.concat('/championmastery/location/{platformId}/player/{playerId}/champions'.replace("{platformId}",platformId).replace('{playerId}',summonerId).concat(apiKey));
    var ritoPls = riotApiRequest(requestString);
    var version = getLatestVersion(region);
    if (ritoPls.status == 200) 
    {
        var response = JSON.parse(ritoPls.responseText);

        for (var i = 0; i < response.length; i++) {
            var obj = response[i];
            var currentChampionInfo = new championInfo();  
            currentChampionInfo.championName = getChampionName(obj.championId);
            currentChampionInfo.championLevel = obj.championLevel;
            currentChampionInfo.championPoints = obj.championPoints;
            currentChampionInfo.pointsUntilNextLevel = obj.championPointsUntilNextLevel;
            currentChampionInfo.pointsSinceLastLevel = obj.championPointsSinceLastLevel;
            currentChampionInfo.championIcon = getChampionImageSource(getChampionKey(obj.championId),version); //This can take long?
            championMasteryList.push(currentChampionInfo);
        }
        return championMasteryList;
    }       
}

function getChampionMastery(region, playerId, championId)
{
    var platformId = region.concat('1'); //some platformId doesn't attach 1, make function to convert region to platformid
    ///championmastery/location/{platformId}/player/{playerId}/champion/{championId}
    var requestString = riotApiAddress.concat('/championmastery/location/{platformId}/player/{playerId}/champion/{championId}'.replace("{platformId}",platformId).replace("{playerId}",playerId).replace("{championId}",championId).concat(apiKey));
    var ritoPls = riotApiRequest(requestString);
    if (ritoPls.status == 200)
    {
        return JSON.parse(ritoPls.responseText);
    }
}

function getChampionName(championId, region)
{
    if (region)
    {
        var requestString = riotApiAddressGlobal.concat('/api/lol/static-data/{region}/v1.2/champion/{id}'.replace('{region}',region.toLowerCase()).replace('{id}',championId).concat(apiKey));
        var ritoPls = riotApiRequest(requestString);
        if (ritoPls.status = 200)
        {
            var championInfo = JSON.parse(ritoPls.responseText);
            return championInfo.name;
        }       
    }
    else
    {
        return championData.data[championId].name;           
    }
}

function getChampionKey(championId)
{
    //TODO: write section to get it from online
    return championData.data[championId].key;           
}

function getSummonerId(summonerName, region) 
{
    var summonerInfo = "/api/lol/{region}/v1.4/summoner/by-name/{summonerNames}".replace("{region}",region).replace("{summonerNames}",summonerName);
    var ritoPls = riotApiRequest(riotApiAddress.concat(summonerInfo).concat(apiKey));
    if (ritoPls.status == 200) 
    {  
        JSON.parse(ritoPls.responseText, function(k, v)
            {
                if (k === "id")
                {
                    summonerId = v;
                }
            });
        return summonerId;
    }
}

function getChampionImageSource(championKey,version)
{
    return requestString = "http://ddragon.leagueoflegends.com/cdn/" + version + "/img/champion/" + championKey +".png";
}

function getLatestVersion(region)
{
    var requestString = "/api/lol/static-data/{region}/v1.2/versions".replace("{region}",region.toLowerCase());
    var ritoPls = riotApiRequest(riotApiAddressGlobal + requestString + apiKey);
    if (ritoPls.status == 200)
    {
        versions = JSON.parse(ritoPls.responseText);
        return versions[0];
    }
}

function riotApiRequest(requestString)
{
    var request = new XMLHttpRequest();
    request.open("get", requestString, false);
    request.send();
    return request;
}

//http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function removeForm()
{
    var theFormItself = document.getElementById('search summoner');
    theFormItself.style.display = 'none';
    //document.getElementById('cover-info').style.display = 'none';
    document.getElementById('champion info').style.display = 'block';
    // var theSuccessMessage = 
    //     document.getElementById('successMessage');  
    // theSuccessMessage.style.display = 'block';          
}

function createSingleChampionPage()
{
    document.getElementById('top10 row').style.display = 'none';
    document.getElementById('single-champion').style.display = 'block';
    var summonerName = getParameterByName('summonerName');
    var region = getParameterByName('region');

    var championName = document.getElementById("champion-form").elements.championName.value;
    if (isChampionValid(championName))
    {
        var championId = getChampionId(championName);
        if (championId === undefined)
        {
            return;
        }
        else
        {
            var championMastery = getChampionMastery(region,getSummonerId(summonerName,region),championId);
            console.log(championMastery);
        }
    }
    else
    {
        alert("invalid Champion Name");
    }
  
}

function getChampionId(championName)
{
    var championName = championName.toLowerCase();
    championList = championData.data;
    for (var key in championList) {
      if (championList.hasOwnProperty(key)) {
        if (championName == championList[key].name.toLowerCase())
        {
            return championList[key].id;
        }
      }
    } 
}

// http://stackoverflow.com/questions/684672/loop-through-javascript-object
function isChampionValid(championName)
{
    var championName = championName.toLowerCase();
    championList = championData.data;
    for (var key in championList) {
      if (championList.hasOwnProperty(key)) {
        if (championName == championList[key].name.toLowerCase())
        {
            return true;
        }
      }
    }
    return false;
}


