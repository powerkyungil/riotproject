from django.shortcuts import render

import urllib.parse
import requests

api_key = "RGAPI-2e46369b-952b-4804-8821-1965f3e6c625"
gameName = '세웠습니다'
gameName = urllib.parse.quote(gameName)
tagLine = 'KR1'
region = "asia"

api_url = {
    "getPuuid": "/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
}
# Create your views here.
def getData(url):
    result = {}
    header = {"X-Riot-Token" : api_key}

    request_url = "http://"+region+".api.riotgames.com"+url
    print(request_url)
    response = requests.get(request_url, headers=header, timeout=10)
    
    result = response.json()

    return result

def getPuuid():
    requestUrl = api_url['getPuuid'].replace("{gameName}", gameName).replace("{tagLine}", tagLine)

    result = getData(requestUrl)

    return result

def record_search(request):

    get_puuid = getPuuid()
    
    return render(request, 'record_list.html')