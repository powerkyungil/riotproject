from unittest import result
from django.shortcuts import render

import urllib.parse
import requests

api_key = "RGAPI-752ec192-ec55-44a8-a900-0d89cef06352"
gameName = '세웠습니다'
gameName = urllib.parse.quote(gameName)
tagLine = 'KR1'
base_url = "https://{region}.api.riotgames.com"

api_url = {
    "getPuuid": "/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}",
    "getSummoner": "/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}",
    "getMatchId": "/lol/match/v5/matches/by-puuid/{puuid}/ids",
    "getSummonerInfo": "/lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
}
# Create your views here.
def getData(request_url):
    result = {}
    header = {"X-Riot-Token" : api_key}

    response = requests.get(request_url, headers=header, timeout=10)

    # HTTP 상태 코드 확인
    if response.status_code == 200:
        result = response.json()
    else:
        result['code'] = response.status_code
        result = apiError("API 호출 ERROR")

    return result

def apiError(message):
    result = {}
    result['result'] = 'ERROR'
    result['message'] = message
    return result

def record_search(request):
    if request.method == 'GET':
        data = request.GET
    else:
        data = {}

    if not data.get('type'):
        return render(request, 'record_list.html', {"data": None})

    if data.get('type') == 'getRecord':
            result = get_record(data)

    return render(request, 'record_list.html', {"data": result})

def get_record(data):
    result = {}
    api_region = 'asia'
    url_template = base_url+api_url['getPuuid']
    requestUrl = url_template.format(region=api_region, gameName=data['gameName'], tagLine=data['tagLine'])

    # return [type dict]
    # {
    #     "puuid": "6kkHOCXtI6hDfwYSxkWqw7MOHn_JC_C0uYncg5f_mihCOytmup-sM1x0Gcz_kG7zJazqam4EK_LjVg",
    #     "gameName": "세웠습니다",
    #     "tagLine": "KR1"
    # }
    get_puuid = getData(requestUrl)

    if not get_puuid:
        return apiError("PUUID를 찾을 수 없습니다.")

    api_region = 'kr'
    url_template = base_url+api_url['getSummoner']
    requestUrl = url_template.format(region=api_region, encryptedPUUID=get_puuid['puuid'])
    # return [type dict]
    # {
    #     "id": "EVuw4hf2hhlCws9etNtiERtSJF4H--RjjsdvYDi-pR5u6jg",
    #     "accountId": "uXCk-9RnmkLTlATtgwfOrg8HWbojc6WLNE76Yz2pzHZ8uQo",
    #     "puuid": "6kkHOCXtI6hDfwYSxkWqw7MOHn_JC_C0uYncg5f_mihCOytmup-sM1x0Gcz_kG7zJazqam4EK_LjVg",
    #     "profileIconId": 4419,
    #     "revisionDate": 1719145640000,
    #     "summonerLevel": 481
    # }
    get_summoner = getData(requestUrl)

    if not get_summoner:
        return apiError("소환자 정보를 찾을 수 없습니다.")

    api_region = 'kr'
    url_template = base_url+api_url['getSummonerInfo']
    requestUrl = url_template.format(region=api_region, encryptedSummonerId=get_summoner['id'])
    # return [type dict]
    # [
    #     {
    #         "leagueId": "3fe30b56-69b0-4995-b954-d0823e1e4280",
    #         "queueType": "RANKED_SOLO_5x5",
    #         "tier": "GOLD",
    #         "rank": "III",
    #         "summonerId": "cCZpLBcAwY9nmhYTP1t8XMOw_JiJACDv0jNszIX4Hr6sqVk",
    #         "leaguePoints": 21,
    #         "wins": 40,
    #         "losses": 43,
    #         "veteran": false,
    #         "inactive": false,
    #         "freshBlood": false,
    #         "hotStreak": false
    #     }
    # ]
    get_summoner_info = getData(requestUrl)

    if not get_summoner_info:
        result = apiError("소환사 정보가 존재하지 않습니다. 언랭일 경우 처리필요")
    else:
        result['summoner_info'] = get_summoner_info

    # url_template = api_url['getMatchIds']
    # requestUrl = url_template.format(puuid=get_puuid['puuid'])
    # # TODO index, count 페이징 처리 추가필요 - 기본 20개 가져옴
    # # return [type dict]
    # # [
    # #     "KR_7121536938",
    # #     "KR_7121501949"
    # # ]
    # get_match_ids = getData(requestUrl)

    # if not get_match_ids:
    #     return apiError("게임 정보를 찾을 수 없습니다.")

    return result